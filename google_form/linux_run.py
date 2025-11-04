from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import gc 
from config import get_all_answers
from utils import setup_driver_linux
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
)

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
    
    print(f"Total questions found: {len(list_questions)}")

    for question in list_questions:
        if index >= len(LIST_OF_VALUES):
            break

        value = LIST_OF_VALUES[index]
        
        if value is None:
            return 
        
        print("Processing question index:", index, "with value:", value)
        try:
            if isinstance(value, str):
                # 1) chọn option theo data-automation-value trong phạm vi câu hỏi
                try:
                    safe_click_in(question, f".//div[@data-value='{value}' and @aria-checked='false']")
                    index += 1
                    print("Clicked option with value:", value)
                    continue
                except Exception:
                    print("Option not found for value:", value)
                    
                # 2) nhập text vào ô input trong phạm vi câu hỏi
                try:
                    safe_input_field(question, value)
                    index += 1
                    print("Input text value:", value)
                    continue
                except Exception:
                    print("Input field not found for value", value)

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

def main():
    global index
    for _ in range(1):
        index = 0
        form_url = "https://docs.google.com/forms/d/e/1FAIpQLSfaSj7Eqtt36QmzL6UDdQUhoNBeLcACPoRpsKJt6_Ow-gccsw/viewform?usp=publish-editor"
        try:
            driver = setup_driver_linux()
            driver.get(form_url)
            
            LIST_OF_VALUES = get_all_answers()
            print(LIST_OF_VALUES)
            while True:
                question_click(driver, LIST_OF_VALUES)
                
                if index >= len(LIST_OF_VALUES):
                    print("All questions processed.")
                    break
                
            submit_click(driver)  
            
        except Exception as e:
            print(f"Error accessing the form: {e}")
        try:
            driver.quit()
        except Exception:
            print("Error quitting the driver.")
        finally:
            del driver
            gc.collect()
        
         

if __name__ == "__main__": 
    main()