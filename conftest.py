#фикстуры

import pytest
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from data.config import BASE_URL
from pages.faq_page import FaqPage
from locators.locators import ScooterLocators
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from pages.order_page import OrderPage
from selenium.webdriver.firefox.service import Service


@pytest.fixture(scope="function")
def driver():
    options = Options()
    service = Service(executable_path=GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)

    driver.maximize_window()
    driver.get(BASE_URL)
    yield driver
    driver.quit()

@pytest.fixture
def faq_page(driver):
    page = FaqPage(driver, BASE_URL)
    page.wait.until(
        EC.presence_of_element_located(ScooterLocators.question_button(0)),
        message="Первый вопрос FAQ не появился на странице после загрузки"
    )
    return page


@pytest.fixture
def order_page(driver):
    page = OrderPage(driver, BASE_URL)
    return page