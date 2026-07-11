import pytest
import allure
from data.config import BASE_URL, ORDER_DATA_SET_1, ORDER_DATA_SET_2
from pages.order_page import OrderPage
from locators.locators import OrderPageLocators
from selenium.webdriver.support.ui import WebDriverWait

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
    def test_full_order_process(self, data):

        self.page.perform_full_order_flow(data)
        self.page.click_logo()
        self.page.assert_on_main_page()

    @allure.title("Проверка перехода на форму заказа через кнопку внизу страницы")
    def test_transition_via_footer_button_only(self):
        self.page.click_order_button_from_footer()
        input_name = self.page.wait_for_visible(OrderPageLocators.INPUT_NAME)
        assert input_name.is_displayed(), "Поле ввода имени не отобразилось после перехода к форме заказа"



@allure.feature("Навигация по сайту")
@allure.story("Проверка элементов шапки")
class TestHeaderNavigation:

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.page = OrderPage(driver, BASE_URL)

    @allure.title("Клик по логотипу Яндекса открывает страницу Дзена (dzen.ru) в новой вкладке")
    def test_yandex_logo_opens_yandex_in_new_tab(self):
        self.page.click_yandex_logo_and_switch_to_new_tab()
