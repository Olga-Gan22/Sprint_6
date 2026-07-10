#Базовый 

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class BasePage:
    def __init__(self, driver, base_url, timeout=15):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, timeout)

    def open(self):
        self.driver.get(self.base_url)

    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_for_clickable(self, locator, message=None):
        return self.wait.until(EC.element_to_be_clickable(locator), message=message)

    def wait_for_visible(self, locator, message=None):
        return self.wait.until(EC.visibility_of_element_located(locator), message=message)

    def click_element(self, locator, message=None):
        element = self.wait_for_clickable(locator, message=message)
        element.click()

    def send_keys(self, locator, text, clear_first=True):
        element = self.wait_for_visible(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)

    def get_element_value(self, locator):
        element = self.wait_for_visible(locator)
        return element.get_attribute("value")

    def scroll_into_view(self, locator):
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def switch_to_new_window(self, original_window):
        WebDriverWait(self.driver, 10).until(lambda d: len(d.window_handles) > 1)
        new_window = [w for w in self.driver.window_handles if w != original_window][-1]
        self.driver.switch_to.window(new_window)
        return new_window

    def assert_url_ends_with(self, path):
        try:
            self.wait.until(lambda d: d.current_url.endswith(path))
        except TimeoutException:
            raise Exception(f"Ожидался URL, заканчивающийся на '{path}', но текущий URL: {self.driver.current_url}")

    def is_element_visible(self, locator):
        try:
            return self.wait_for_visible(locator).is_displayed()
        except Exception:
            return False
        
    def wait_for_elements_visible(self, locator, custom_timeout=None):
        timeout = custom_timeout if custom_timeout else self.wait._timeout
        try:
            return self.wait.until(
                EC.visibility_of_all_elements_located(locator),
                message=f"Не найдены элементы по локатору {locator}"
            )
        except TimeoutException:
            raise

         # НОВЫЙ МЕТОД: прокрутка к элементу
    def scroll_to_element(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});",
            element
        )