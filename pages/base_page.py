#Базовый 

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import allure


class BasePage:
    def __init__(self, driver, base_url, timeout=15):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, timeout)

    @allure.step("Открываем страницу по базовому URL")
    def open(self):
        self.driver.get(self.base_url)

    @allure.step("Находим элемент по локатору: {locator}")
    def find_element(self, locator):
        return self.wait.until(
            EC.presence_of_element_located(locator),
            message=f"Элемент не найден по локатору: {locator}"
        )

    @allure.step("Ждём, пока элемент станет кликабельным: {locator}")
    def wait_for_clickable(self, locator, message=None):
        custom_msg = message or f"Элемент не стал кликабельным по локатору: {locator}"
        return self.wait.until(
            EC.element_to_be_clickable(locator),
            message=custom_msg
        )

    @allure.step("Ждём, пока элемент станет видимым: {locator}")
    def wait_for_visible(self, locator, message=None):
        custom_msg = message or f"Элемент не стал видимым по локатору: {locator}"
        return self.wait.until(
            EC.visibility_of_element_located(locator),
            message=custom_msg
        )

    @allure.step("Кликаем по элементу: {locator}")
    def click_element(self, locator, message=None):
        element = self.wait_for_clickable(locator, message=message)
        element.click()

    @allure.step("Вводим текст '{text}' в поле: {locator}")
    def send_keys(self, locator, text, clear_first=True):
        element = self.wait_for_visible(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)

    @allure.step("Получаем значение атрибута value у элемента: {locator}")
    def get_element_value(self, locator):
        element = self.wait_for_visible(locator)
        return element.get_attribute("value")

    @allure.step("Прокручиваем страницу, чтобы элемент по локатору {locator} стал видимым")
    def scroll_into_view(self, locator):
        element = self.find_element(locator)
        self.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

    @allure.step("Получаем handle текущего окна браузера")
    def get_current_window_handle(self):
        return self.driver.current_window_handle

    @allure.step("Получаем список handles всех открытых окон браузера")
    def get_window_handles(self):
        return self.driver.window_handles

    @allure.step("Переключаемся на окно браузера по handle: {handle}")
    def switch_to_window(self, handle):
        self.driver.switch_to.window(handle)

    @allure.step("Переключаемся на новую вкладку (не текущую: {original_window})")
    def switch_to_new_window(self, original_window):
        wait = WebDriverWait(self.driver, 10)
        wait.until(lambda d: len(d.window_handles) > 1)

        new_window = None
        for h in self.get_window_handles():
            if h != original_window:
                new_window = h
                break

        if new_window is None:
            raise TimeoutException("Не найдена новая вкладка после клика")

        self.switch_to_window(new_window)
        return new_window

    @allure.step("Проверяем, что URL заканчивается на: {path}")
    def assert_url_ends_with(self, path):
        try:
            self.wait.until(lambda d: d.current_url.endswith(path))
        except TimeoutException:
            raise TimeoutException(
                f"Ожидался URL, заканчивающийся на '{path}', но текущий URL: '{self.driver.current_url}'"
            )

    @allure.step("Ждём видимости всех элементов по локатору: {locator} (таймаут: {custom_timeout})")
    def wait_for_elements_visible(self, locator, custom_timeout=None):
        timeout = custom_timeout if custom_timeout is not None else self.wait._timeout
        local_wait = WebDriverWait(self.driver, timeout)
        return local_wait.until(
            EC.visibility_of_all_elements_located(locator),
            message=f"Не найдены элементы по локатору {locator}"
        )

    @allure.step("Выполняем JS-скрипт: {script}")
    def execute_script(self, script, *args):
        return self.driver.execute_script(script, *args)

    @allure.step("Ищем все элементы по локатору (By, value)")
    def find_elements(self, by, value=None):
        if value is None:
            return self.driver.find_elements(*by)
        return self.driver.find_elements(by, value)

    @allure.step("Получаем текущий URL страницы")
    def get_current_url(self):
        return self.driver.current_url
