# pytest web_test_prog.py 

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
import time

@pytest.fixture
def driver():
    chromedriver_path = '/home/iliya/Downloads/chromedriver-linux64/chromedriver'
    service = ChromeService(executable_path=chromedriver_path)

    driver = webdriver.Chrome(service=service)
    yield driver
    driver.quit()
    
def auth(driver):
    driver.get("http://localhost:8181/")
    time.sleep(4)
    # wait = WebDriverWait(driver, 5)

    username_input = driver.find_element(By.NAME, "user")
    password_input = driver.find_element(By.NAME, "password")
    username_input.send_keys("user")
    password_input.send_keys("password")  

    password_input.send_keys(Keys.RETURN) 


def test_login(driver):

        auth(driver)

        wait = WebDriverWait(driver, 10)    
        os_version_element = wait.until(EC.presence_of_element_located((By.XPATH, "//td[text()='OS version']/following-sibling::td/span")))
        os_version = os_version_element.text
        print("Текущая версия OS:", os_version)

        # Проверка значения "OS version"
        expected_version = "X.Y.Z"

        if os_version == expected_version:
            print("Юнит-кейс пройден: версия OS соответствует ожидаемому значению.")
        else:
            print("Юнит-кейс не пройден: версия OS не соответствует ожидаемому значению.")
        assert os_version == expected_version, f"Неправильная версия OS. Ожидаемая версия: {expected_version}, текущая версия: {os_version}"


    # print (dropdown_button)
    # print (dropdown_values)
        # print("Значение выпадающего списка:", value_element.get_attribute("value"))




