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


if __name__ == "__main__":
    id_zoom = '790 6801 4518'
    zoom_pass = 'N3jgQd'
    names = [
        # "Nguyễn Minh Tuấn",
        # "Lê Thị Lan",
        # "Trần Quang Hieu",
        "Phạm Thanh Mai",
        "Vũ Hoàng Nam",
        # "Bùi Thị Hoa",
        # "Đặng Minh Tâm",
        # "Hồ Quang Anh",
        "Phan Thị Kim",
        "Cao Hữu Tín"
    ]

    for name in names:
        driver = setup_driver()
        url = "https://app.zoom.us/wc/join"
        driver.get(url)

        id_input = driver.find_element(
            By.XPATH, ".//input[@class='join-meetingId']"
        )

        id_input.send_keys(id_zoom)

        join_button = driver.find_element(
            By.XPATH, ".//button[contains(@class, 'btn-join')]"
        )

        join_button.click()

        driver.switch_to.frame(driver.find_element(By.ID, "webclient"))
        html_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, ".//html[@lang='en-US']"))
        )

        continue_w = WebDriverWait(html_element, 30).until(
            EC.presence_of_element_located((By.XPATH, ".//div[contains(@class, 'without')]"
        )))

        continue_w.click()
        continue_w.click()

        password_input = html_element.find_element(
            By.XPATH, ".//input[@id='input-for-pwd']"
        )
        password_input.send_keys(zoom_pass)

        name_input = html_element.find_element(
            By.XPATH, ".//input[@id='input-for-name']"
        )
        name_input.send_keys(name)

        join_button = html_element.find_element(
            By.XPATH, ".//button[contains(@class, 'join-button')]"
        )
        join_button.click()
        time.sleep(40)

    while True:
        q = input("Enter q to stop: ")
        if q == 'q':
            break

    exit(0)

