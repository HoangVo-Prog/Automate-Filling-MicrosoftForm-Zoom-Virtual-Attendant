import argparse
import os
import random
import re
from pathlib import Path
from typing import List, Optional

import pandas as pd


# -----------------------------
# User-provided distributions
# -----------------------------
def get_items(n: int) -> List[str]:
    # Part 1
    if n == 1:
        return ["Có", "Không"]
    elif n == 2:
        return ["Dưới 1 năm", "Từ 1 năm đến 5 năm", "Từ 6 năm đến 10 năm", "Trên 10 năm"]

    # Part 2
    elif 3 <= n <= 38:
        return ["1", "2", "3", "4", "5"]

    # Part 3
    elif n == 39:
        return ["Nam", "Nữ"]
    elif n == 40:
        return [
            "Dưới 21 tuổi",
            "Từ 21 tuổi đến 30 tuổi",
            "Từ 31 tuổi đến 40 tuổi",
            "Từ 41 tuổi đến 50 tuổi",
            "Trên 50 tuổi",
        ]
    elif n == 41:
        return ["Bosch"]
    elif n == 42:
        return ["Logistics Inbond"]

    raise ValueError(f"Unsupported n={n}")


def get_weights(n: int) -> List[float]:
    if n == 1:
        return [1.0, 0.0]
    elif n == 2:
        return [0.0, 0.3, 0.3, 0.4]
    elif 3 <= n <= 38:
        return [0.1, 0.1, 0.1, 0.2, 0.5]
    elif n == 39:
        return [0.7, 0.3]
    elif n == 40:
        return [0.2, 0.4, 0.2, 0.1, 0.1]
    elif n == 41:
        return [1]
    elif n == 42:
        return [1]
    raise ValueError(f"Unsupported n={n}")


def get_answers(n: int) -> str:
    items = get_items(n)
    weights = get_weights(n)
    return random.choices(items, weights=weights, k=1)[0]


def get_all_answers(num_questions: int = 42) -> List[Optional[str]]:
    answers: List[Optional[str]] = []
    for i in range(1, num_questions + 1):
        answers.append(get_answers(i))

    # dependency rules
    # n=1 at index 0, n=2 at index 1, n=3 at index 2
    if answers[0] == "Không":
        answers[1] = None
    if answers[1] == "Dưới 1 năm":
        answers[2] = None
    return answers


# -----------------------------
# Helpers
# -----------------------------
def sanitize_filename(text: str) -> str:
    text = str(text).strip()
    text = re.sub(r"[^\w\-.]+", "_", text)
    return text.strip("_")


def equal_weight_companies(company_field: str, k: int) -> List[str]:
    """
    Split `company_field` by "/" and draw k samples with equal weights.
    Example: "A / B / C" -> choose each of A,B,C with probability 1/3 for each form.
    """
    if not isinstance(company_field, str) or not company_field.strip():
        return [str(company_field)] * k
    names = [c.strip() for c in company_field.split("/") if c.strip()]
    if not names:
        names = [""]
    return [random.choice(names) for _ in range(k)]


def normalize_experience(value: Optional[str]) -> Optional[str]:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    v = str(value).strip().lower()
    mapping = {
        "dưới 1 năm": "Dưới 1 năm",
        "1-5 năm": "Từ 1 năm đến 5 năm",
        "từ 1 năm đến 5 năm": "Từ 1 năm đến 5 năm",
        "6-10 năm": "Từ 6 năm đến 10 năm",
        "từ 6 năm đến 10 năm": "Từ 6 năm đến 10 năm",
        "trên 10 năm": "Trên 10 năm",
        ">10 năm": "Trên 10 năm",
    }
    for key, cat in mapping.items():
        if v == key:
            return cat
    allowed = set(get_items(2))
    if str(value) in allowed:
        return str(value)
    return None


# -----------------------------
# Core generation
# -----------------------------
def generate_for_schedule(
    schedule_csv: Path,
    out_dir: Path,
    seed: Optional[int] = None,
    include_day_column: bool = False,
) -> None:
    if seed is not None:
        random.seed(seed)

    df = pd.read_csv(schedule_csv)

    required = {"Company", "Position", "Day", "TimeSlot", "FormCount"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Schedule is missing columns: {missing}")

    # define 42 columns: N1..N40, Company(n=41), Position(n=42)
    qcols = [f"N{i}" for i in range(1, 41)] + ["Company", "Position"]

    out_dir.mkdir(parents=True, exist_ok=True)

    for day, g in df.groupby("Day", sort=False):
        records = []
        for _, row in g.iterrows():
            company_field = row["Company"]
            position = row["Position"]
            forms = int(row["FormCount"])
            timeslot = row["TimeSlot"]
            exp_override = normalize_experience(row["Experience"]) if "Experience" in row else None

            # choose company for each form with equal weights
            companies = equal_weight_companies(company_field, forms)

            for cval in companies:
                answers = get_all_answers(42)
                # override n=41 and n=42
                answers[40] = cval           # Company at index 40
                answers[41] = position       # Position at index 41

                # optional override for n=2
                if exp_override is not None:
                    answers[1] = exp_override

                # re-apply dependency logic after overrides
                if answers[0] == "Không":
                    answers[1] = None
                if answers[1] == "Dưới 1 năm":
                    answers[2] = None

                rec = {col: val for col, val in zip(qcols, answers)}
                rec["TimeSlot"] = timeslot
                if include_day_column:
                    rec["Day"] = day
                records.append(rec)

        columns = qcols + ["TimeSlot"]
        if include_day_column:
            columns = qcols + ["TimeSlot", "Day"]

        day_df = pd.DataFrame.from_records(records, columns=columns)
        # rename N2 to Experience for readability
        day_df = day_df.rename(columns={"N2": "Experience"})

        # sort for easier review
        sort_keys = ["Company", "Position", "TimeSlot"]
        if include_day_column:
            sort_keys = ["Day"] + sort_keys
        day_df = day_df.sort_values(by=sort_keys).reset_index(drop=True)

        # save
        fname = sanitize_filename(str(day)) + ".csv"
        out_path = out_dir / fname
        day_df.to_csv(out_path, index=False, encoding="utf-8-sig")

    print(f"Done. Files are in: {str(out_dir.resolve())}")


# -----------------------------
# CLI
# -----------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Generate per-day interview CSVs with 42-question schema plus TimeSlot."
    )
    parser.add_argument(
        "--schedule",
        type=str,
        default="logistics_interview_schedule_expanded.csv",
        help="Path to schedule CSV.",
    )
    parser.add_argument(
        "--outdir",
        type=str,
        default="out_csv_by_day",
        help="Output directory for per-day CSVs.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=20251104,
        help="Random seed for reproducibility.",
    )
    parser.add_argument(
        "--include-day",
        action="store_true",
        help="If set, include a Day column in each output CSV.",
    )
    args = parser.parse_args()

    generate_for_schedule(
        schedule_csv=Path(args.schedule),
        out_dir=Path(args.outdir),
        seed=args.seed,
        include_day_column=args.include_day,
    )


if __name__ == "__main__":
    main()