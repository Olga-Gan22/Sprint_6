#фикстуры

import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

@pytest.fixture(scope="function")
def driver():
    options = webdriver.FirefoxOptions()
    service = FirefoxService(executable_path=GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    driver.maximize_window()
    yield driver
    driver.quit()
