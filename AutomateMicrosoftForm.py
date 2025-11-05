from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from config import get_answers
from utils import setup_driver
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,

)


def index_increment(index):
    global index  # Declare the global index variable
    index += 1


def continue_click():
    continue_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((
        By.XPATH, '//button[@aria-label="Next"]'
    )))
    continue_button.click()


def question_click(sub=0):
    global index

    step = 0

    list_questions = driver.find_elements(
        By.XPATH,
        './/div[@role="region"]' +
        '//div[contains(@data-automation-id, "questionItem") or contains(@data-automation-id, "likerSubQuestion")]'
    )
    for i, question in enumerate(list_questions):

        if isinstance(LIST_OF_VALUES[index], str):
            try:
                # String Only
                question_input = question.find_element(
                    By.XPATH,
                    f'.//span[contains(@data-automation-value, "{LIST_OF_VALUES[index]}")]/input'
                )

                time.sleep(random.uniform(0.1, 0.6))
                question_input.click()
                index_increment(index)

            except NoSuchElementException:
                try:
                    # Text area
                    text = question.find_element(
                        By.XPATH,
                        './/textarea[@aria-label="Văn bản Nhiều Dòng"]'
                    )
                    text.send_keys(LIST_OF_VALUES[index])
                    index_increment(index)
                except NoSuchElementException:
                    continue

        elif isinstance(LIST_OF_VALUES[index], list):
            # List of Values
            for value in LIST_OF_VALUES[index]:
                question_input = driver.find_element(
                    By.XPATH,
                    f'.//span[contains(@data-automation-value, "{value}")]/input'
                )
                time.sleep(random.uniform(0.1, 0.6))
                question_input.click()
            index_increment(index)

        else:
            try:

                question_input = question.find_element(
                    By.XPATH,
                    f'.//input[@aria-label="{LIST_OF_VALUES[index]}" and contains(@aria-checked, "f")]'
                )
                if sub > 0 and step == 0:
                    step = 5
                    sub -= 1
                    continue
                step -= 1
                question_input.click()
                index_increment(index)

            except (TimeoutException, NoSuchElementException):
                try:
                    # Numbers Only
                    question_input = question.find_element(
                        By.XPATH,
                        f'.//div[@aria-label="{LIST_OF_VALUES[index]}"]'
                    )
                    question_input.click()
                    index_increment(index)
                except (TimeoutException, NoSuchElementException):
                    continue

    try:
        continue_click()
    except TimeoutException:
        send_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((
            By.XPATH, '//button[contains(@data-automation-id, "submit")]'
        )))
        send_button.click()
    time.sleep(random.uniform(0.1, 0.6))


if __name__ == "__main__":
    for _ in range(1):
        driver = setup_driver()

        form_url = "https://docs.google.com/forms/d/e/1FAIpQLSfaSj7Eqtt36QmzL6UDdQUhoNBeLcACPoRpsKJt6_Ow-gccsw/viewform?usp=publish-editor"
        driver.get(form_url)

        index = 0
        n = random.choices([1, 4], weights=[0.3, 0.7], k=1)[0]
        LIST_OF_VALUES = get_answers(n)
        print(LIST_OF_VALUES)

        # start_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((
        #     By.XPATH, '//*[@id="form-main-content1"]/div/div[3]/div[3]/button'
        # )))

        # start_button.click()
        # continue_click()

        # #  Part 1 - Question: 1-4
        # question_click()

        # # Part 2
        # continue_click()

        # # Question 5
        # question_click()
        # if n == 4:

        #     # Question 6-10
        #     question_click()

        #     # Part 3 - Question: 11-13
        #     question_click(1)

        #     # Part 4 - Question 14
        #     question_click()
        #     #
        #     # Question 15 - 16 (YES)
        #     question_click()
        #     #
        #     # # Question 17
        #     question_click()

        # else:
        #     question_click()
        #     question_click()

        # time.sleep(random.uniform(180, 200))

        # question_click()

        driver.quit()

