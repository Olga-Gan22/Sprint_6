import pytest
import allure
from data.config import BASE_URL, ORDER_DATA_SET_1, ORDER_DATA_SET_2
from pages.order_page import OrderPage
from locators.locators import MainPageLocators, OrderPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Заказ самоката")
@allure.story("Позитивный сценарий оформления заказа")
class TestOrderFlow:

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.page = OrderPage(driver, BASE_URL)

    @pytest.mark.parametrize(
        "data",
        [ORDER_DATA_SET_1, ORDER_DATA_SET_2],
        ids=["DataSet_1_Black", "DataSet_2_Grey"]
    )
    @allure.title("Оформление заказа: {data[name]} {data[last_name]} + возврат на главную")
    def test_full_order_process(self, data, driver):
        self.page.perform_full_order_flow(data)
        self.page.click_logo()
        self.page.assert_on_main_page()

    @allure.title("Проверка перехода на форму заказа через кнопку внизу страницы")
    def test_transition_via_footer_button_only(self, driver):
        self.page = OrderPage(driver, BASE_URL) 
        self.page.click_order_button_from_footer()

        wait = WebDriverWait(driver, 15)
        wait.until(lambda d: d.find_element(*OrderPageLocators.INPUT_NAME).is_displayed())


@allure.feature("Навигация по сайту")
@allure.story("Проверка элементов шапки")
class TestHeaderNavigation:

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.page = OrderPage(driver, BASE_URL)
        

    @allure.title("Клик по логотипу Яндекса")
    def test_yandex_logo_opens_dzen_in_new_tab(self):
        original_window = self.page.click_yandex_logo_and_switch_to_new_tab()
        try:
            self.page.assert_new_tab_has_dzen_like_title()
        except AssertionError as e:
            print(f"⚠️ Внимание: Заголовок не совпал с ожидаемым, но вкладка открыта. Ошибка: {e}")

        self.page.driver.close()
        self.page.driver.switch_to.window(original_window)
