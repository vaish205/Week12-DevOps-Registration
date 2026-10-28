
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

URL = "http://127.0.0.1:30080/"


@pytest.fixture
def driver():
    browser = webdriver.Chrome(
        service=Service(ChromeDriverManager().install())
    )
    yield browser
    browser.quit()


def submit_form(driver, username, password):
    driver.get(URL)
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "pwd").send_keys(password)
    driver.find_element(By.NAME, "sb").click()


@pytest.mark.parametrize("username,password,message", [
    ("", "Password123", "Username cannot be empty."),
    ("John Doe", "", "Password cannot be empty."),
    ("Jane", "abc1", "Password must be at least 6 characters long.")
])
def test_invalid_input(driver, username, password, message):
    submit_form(driver, username, password)
    alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
    assert alert.text == message
    alert.accept()


def test_valid_input(driver):
    submit_form(driver, "Alice", "abc123")

    WebDriverWait(driver, 10).until(
        EC.url_contains("/submit")
    )

    assert "Hello, Alice! Welcome to the website" in driver.find_element(
        By.TAG_NAME, "body"
    ).text
