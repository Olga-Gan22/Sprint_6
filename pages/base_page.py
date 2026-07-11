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
        """
        Возвращает элемент. Если не найден — падает с TimeoutException.
        Никаких try/except, чтобы баг был виден сразу.
        """
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
        # Сначала ждём, что элемент вообще есть в DOM, потом скроллим
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

    @allure.step("Переключаемся на новое окно (исходное окно: {original_window})")
    def switch_to_new_window(self, original_window):
        WebDriverWait(self.driver, 10).until(lambda d: len(d.window_handles) > 1)
        new_window = [w for w in self.driver.window_handles if w != original_window][-1]
        self.driver.switch_to.window(new_window)
        return new_window

    @allure.step("Проверяем, что URL заканчивается на: {path}")
    def assert_url_ends_with(self, path):
        try:
            self.wait.until(lambda d: d.current_url.endswith(path))
        except TimeoutException:
            # Честная ошибка: тест падает, и в отчёте Allure будет видно, какой URL был
            raise TimeoutException(
                f"Ожидался URL, заканчивающийся на '{path}', но текущий URL: '{self.driver.current_url}'"
            )

    # УДАЛЁН: is_element_visible с возвратом False. 
    # Если нужно проверить наличие элемента для логики — используй find_element.
    # Если элемент не нужен для сценария — не проверяй его.
    # Для тестов всегда лучше: "элемент должен быть" -> wait_for_visible, иначе падение.

    @allure.step("Ждём видимости всех элементов по локатору: {locator} (таймаут: {custom_timeout})")
    def wait_for_elements_visible(self, locator, custom_timeout=None):
        timeout = custom_timeout if custom_timeout else self.wait._timeout
        local_wait = WebDriverWait(self.driver, timeout)
        try:
            return local_wait.until(
                EC.visibility_of_all_elements_located(locator),
                message=f"Не найдены элементы по локатору {locator}"
            )
        except TimeoutException as e:
            raise e

    @allure.step("Плавно прокручиваем к элементу (center, smooth)")
    def scroll_to_element(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});",
            element
        )
