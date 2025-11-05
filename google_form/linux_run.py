from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse
import csv
import random
import re
import time
from datetime import datetime, timedelta
from collections import defaultdict
import gc 
from config import get_all_answers
from utils import setup_driver_linux, setup_driver
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
)

from tqdm import tqdm

def submit_click(driver, timeout=5):
    buttons = WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((By.XPATH, "//span[@class='NPEfkd RveJvd snByac']"))
    )
    
    if len(buttons) > 1:
        buttons[1].click()

def continue_click(driver):
    continue_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((
            By.XPATH, "//span[contains(text(), 'Tiếp') or contains(text(), 'Next')]"
        ))
    )
    continue_button.click()
    print("Clicked Continue/Next button.")

    
def safe_input_field(question, value, timeout=5):
    input_field = WebDriverWait(question, timeout).until(
        EC.element_to_be_clickable((By.XPATH, ".//input[@type='text']"))
    )
    input_field.send_keys(value)


def safe_click_in(question, xpath, timeout=5):
    el = WebDriverWait(question, timeout).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    el.click()

def question_click(driver, LIST_OF_VALUES, sub=0):
    global index
    skip_remaining = sub  # số lần cần bỏ qua trước khi click

    value = LIST_OF_VALUES[index]
        
    if value is None:
        return 

    list_questions = driver.find_elements(
        By.XPATH,
        "//div[@class='RH5hzf RLS9Fe']//div[@jsmodel='CP1oW']"
    )
    print("Found:", len(list_questions), "questions on the page.")
    
    for question in list_questions:
        if index >= len(LIST_OF_VALUES):
            break

        value = LIST_OF_VALUES[index]
        
        if value is None:
            return 
        
        try:
            if isinstance(value, str):
                # 1) chọn option theo data-automation-value trong phạm vi câu hỏi
                try:
                    safe_click_in(question, f".//div[@data-value='{value}' and @aria-checked='false']")
                    index += 1
                    continue
                except Exception:
                    pass                        
                # 2) nhập text vào ô input trong phạm vi câu hỏi
                try:
                    safe_input_field(question, value)
                    index += 1
                    continue
                except Exception:
                    pass
        except Exception:
            # không làm gì nếu câu hỏi này không phù hợp
            continue
        
    # next hoặc submit
    try:
        continue_click(driver)
    except TimeoutException:
        send_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(@data-automation-id, "submit")]'))
        )
        send_button.click()

index = 0

def args_parser():
    import argparse

    parser = argparse.ArgumentParser(description="Google Form Auto Filler")
    parser.add_argument("--source", type=str, default="resouces/05_11.txt")
    return parser.parse_args()


# ---------- Parse TimeSlot helpers ----------

_TS_PATTERN = re.compile(r"\s*(\d{1,2})h\s*(\d{0,2})?\s*-\s*(\d{1,2})h\s*(\d{0,2})?\s*", re.IGNORECASE)

def _hhmm_to_minutes(h_str: str, m_str: str | None) -> int:
    h = int(h_str)
    m = int(m_str) if (m_str and m_str.isdigit()) else 0
    return h * 60 + m

def parse_timeslot_to_minutes(ts: str) -> tuple[int, int]:
    """
    '14h00-14h30' or '18h-19h' -> (start_min, end_min) minutes from 00:00.
    """
    m = _TS_PATTERN.fullmatch(ts.replace(" ", ""))
    if not m:
        # try with spaces tolerant
        m = _TS_PATTERN.match(ts)
    if not m:
        raise ValueError(f"Invalid TimeSlot format: {ts!r}")
    h1, m1, h2, m2 = m.group(1), m.group(2), m.group(3), m.group(4)
    s = _hhmm_to_minutes(h1, m1)
    e = _hhmm_to_minutes(h2, m2)
    if e <= s:
        # guard: ensure end after start (if equal or before, push to +30 min)
        e = s + 30
    return s, e

def minutes_now_local() -> int:
    now = datetime.now()
    return now.hour * 60 + now.minute

def sleep_until_minutes(target_min: int):
    """
    Sleep until today's target minute-of-day.
    If already past, return immediately.
    """
    now = datetime.now()
    today_target = now.replace(hour=target_min // 60, minute=target_min % 60, second=0, microsecond=0)
    delta = (today_target - now).total_seconds()
    if delta > 0:
        time.sleep(delta)

# ---------- Schedule helpers ----------

def generate_staggered_times(start_min: int, end_min: int, k: int, min_gap: int = 30) -> list[int]:
    """
    Create k timestamps in [start_min, end_min] with at least min_gap minutes between
    consecutive attempts. If not enough room, we cap k to the maximum that fits.
    Times are randomized but guaranteed non-decreasing and within the slot.
    """
    if k <= 0:
        return []
    slot_len = end_min - start_min
    max_fit = 1 + (slot_len // min_gap)
    if max_fit <= 0:
        return []
    if k > max_fit:
        print(f"[WARN] Not enough room for {k} attempts in this slot; capping to {max_fit}.")
        k = max_fit

    if k == 1:
        # any minute inside the slot
        return [start_min + random.randint(0, max(0, slot_len))]

    base_times = [start_min + i * min_gap for i in range(k)]
    slack = slot_len - min_gap * (k - 1)
    # distribute slack randomly, non-decreasing via cumulative jitters
    cuts = sorted([random.randint(0, slack) for _ in range(k - 1)])
    # prepend 0 and append slack to make k segments
    cuts = [0] + cuts + [slack]
    segs = [cuts[i + 1] - cuts[i] for i in range(len(cuts) - 1)]
    # cumulative jitter
    jitters = []
    acc = 0
    for s in segs:
        acc += s
        jitters.append(acc)
    # assign jitter to each base time
    return [base_times[i] + jitters[i] for i in range(k)]

# ---------- CSV reading ----------

def _detect_columns(header: list[str]) -> list[str]:
    """
    Build the 42-question column list in order:
    Q1..Q40: N1..N40 but allow N2 to be named 'Experience' in output.
    Q41: Company
    Q42: Position
    """
    cols = []
    # N1
    cols.append("N1" if "N1" in header else "N01")
    # N2 may be 'N2' or 'Experience'
    if "N2" in header:
        cols.append("N2")
    elif "Experience" in header:
        cols.append("Experience")
    else:
        raise ValueError("Cannot find N2 or Experience column.")
    # N3..N40
    for i in range(3, 41):
        cname = f"N{i}"
        if cname not in header:
            raise ValueError(f"Missing expected column: {cname}")
        cols.append(cname)
    # Company, Position
    if "Company" not in header or "Position" not in header:
        raise ValueError("Missing Company and/or Position columns.")
    cols.append("Company")
    cols.append("Position")
    return cols  # len == 42

def get_all_questions(src) -> list[list]:
    """
    Read the per-day CSV and return a list of length M:
      - Each item is a list of 42 values (Q1..Q42 in order).
    TimeSlot is stored separately in a parallel list (attached to function attribute).
    The attempts are sorted by TimeSlot (ascending by start time).
    """
    questions: list[list] = []
    timeslots: list[str] = []

    with open(src, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames or []
        if "TimeSlot" not in header:
            raise ValueError("CSV must contain a 'TimeSlot' column.")
        qcols = _detect_columns(header)

        # load rows into buffer to sort by TimeSlot start
        buffer = []
        for row in reader:
            ts = row["TimeSlot"].strip()
            s_min, e_min = parse_timeslot_to_minutes(ts)
            values = [row.get(c, None) for c in qcols]
            buffer.append((s_min, e_min, ts, values))

        # sort by start minute then end minute
        buffer.sort(key=lambda x: (x[0], x[1]))

        for s_min, e_min, ts, values in buffer:
            questions.append(values)
            timeslots.append(ts)

    # attach timeslots parallel to returned list
    get_all_questions.timeslots = timeslots  # type: ignore[attr-defined]
    return questions

# ---------- Your form execution placeholder ----------

def perform_attempt(form_url: str, values: list):
    """
    TODO: Nhét logic điền form của bạn ở đây.
    'values' là list 42 phần tử theo thứ tự Q1..Q42.
    """
    index = 0
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSfaSj7Eqtt36QmzL6UDdQUhoNBeLcACPoRpsKJt6_Ow-gccsw/viewform?usp=publish-editor"
    try:
        driver = setup_driver()
        driver.get(form_url)
        
        while index < len(values):
            question_click(driver, values)
            
        submit_click(driver)  
        
    except Exception as e:
        print(f"Error accessing the form: {e}")
        print(index, values[index-1])
    try:
        driver.quit()
    except Exception:
        print("Error quitting the driver.")
    finally:
        del driver
        gc.collect()    


# ---------- Args & Main ----------

def args_parser():
    p = argparse.ArgumentParser()
    p.add_argument("--source", type=str, required=True, help="Path to per-day CSV output.")
    p.add_argument("--form-url", type=str, required=True, help="Google Form URL.")
    p.add_argument("--min-gap", type=int, default=30, help="Minimum gap between attempts in minutes.")
    p.add_argument("--dry-run", action="store_true", help="Print schedule only, do not execute.")
    return p.parse_args()

def main():
    # global index  # nếu bạn cần dùng ở chỗ khác
    args = args_parser()

    LIST_OF_QUESTIONS = get_all_questions(args.source)
    TIME_SLOTS = getattr(get_all_questions, "timeslots", [])
    if len(LIST_OF_QUESTIONS) != len(TIME_SLOTS):
        raise RuntimeError("Questions and TimeSlot list out of sync.")

    # Gom theo TimeSlot
    slot_to_indices: defaultdict[str, list[int]] = defaultdict(list)
    for i, ts in enumerate(TIME_SLOTS):
        slot_to_indices[ts].append(i)

    # Duyệt theo TimeSlot đã sort sẵn (nhờ get_all_questions)
    unique_slots_in_order = []
    seen = set()
    for ts in TIME_SLOTS:
        if ts not in seen:
            unique_slots_in_order.append(ts)
            seen.add(ts)

    total_planned = 0
    plan_per_slot: dict[str, list[tuple[int, int]]] = {}  # ts -> list of (index, planned_minute)

    # Lên lịch thời điểm thực hiện cho từng slot
    for ts in unique_slots_in_order:
        indices = slot_to_indices[ts]
        s_min, e_min = parse_timeslot_to_minutes(ts)
        k = len(indices)

        planned_minutes = generate_staggered_times(s_min, e_min, k, min_gap=args.min_gap)
        # Có thể bị cắt bớt nếu không đủ khoảng trống
        usable = min(len(indices), len(planned_minutes))
        plan = [(indices[i], planned_minutes[i]) for i in range(usable)]
        plan_per_slot[ts] = plan
        total_planned += usable

    print(f"[INFO] Total attempts planned: {total_planned}")

    # Thực thi theo lịch
    for ts in unique_slots_in_order:
        s_min, e_min = parse_timeslot_to_minutes(ts)
        plan = plan_per_slot.get(ts, [])
        if not plan:
            print(f"[SKIP] {ts}: no planned attempts.")
            continue

        print(f"[SLOT] {ts}: {len(plan)} attempt(s).")
        for idx, when_min in plan:
            # nếu chưa đến giờ slot bắt đầu, chờ đến when_min
            now_min = minutes_now_local()
            if now_min < when_min:
                print(f"  - Waiting until {when_min//60:02d}:{when_min%60:02d} for attempt #{idx}")
                if not args.dry_run:
                    sleep_until_minutes(when_min)

            # check lại thời gian hiện tại
            now_min = minutes_now_local()
            if not (s_min <= now_min <= e_min):
                print(f"  - Skipped attempt #{idx}: now {now_min//60:02d}:{now_min%60:02d} outside slot {ts}")
                continue

            LIST_OF_VALUES = LIST_OF_QUESTIONS[idx]
            # index = 0  # nếu quy trình điền form của bạn cần reset chỉ số
            if args.dry_run:
                print(f"  - DRY RUN execute #{idx} at {now_min//60:02d}:{now_min%60:02d}")
            else:
                perform_attempt(args.form_url, LIST_OF_VALUES)

        # đảm bảo không chạy ngoài khung slot
        if not args.dry_run and minutes_now_local() < e_min:
            # optional: ngủ đến hết slot (không bắt buộc)
            pass

if __name__ == "__main__":
    main()


# def main():
    
    
#     LIST_OF_QUESTIONS = get_all_questions(args.source)
    
#     for i in range(tqdm(len(LIST_OF_QUESTIONS), desc="Filling forms")):
#         index = 0
#         form_url = "https://docs.google.com/forms/d/e/1FAIpQLSfaSj7Eqtt36QmzL6UDdQUhoNBeLcACPoRpsKJt6_Ow-gccsw/viewform?usp=publish-editor"
#         LIST_OF_VALUES = LIST_OF_QUESTIONS[i]
#         try:
#             driver = setup_driver_linux()
#             driver.get(form_url)
            
#             LIST_OF_VALUES = get_all_answers()
#             print(LIST_OF_VALUES)
#             while index < len(LIST_OF_VALUES):
#                 question_click(driver, LIST_OF_VALUES)
                
#             submit_click(driver)  
            
#         except Exception as e:
#             print(f"Error accessing the form: {e}")
#         try:
#             driver.quit()
#         except Exception:
#             print("Error quitting the driver.")
#         finally:
#             del driver
#             gc.collect()
        
         

if __name__ == "__main__": 
    main()