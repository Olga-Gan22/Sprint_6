import pytest
import allure
from data.config import BASE_URL, ORDER_DATA_SET_1, ORDER_DATA_SET_2
from pages.order_page import OrderPage


@allure.feature("Заказ самоката")
@allure.story("Позитивный сценарий оформления заказа")
class TestOrderFlow:

    @pytest.mark.parametrize(
        "data",
        [ORDER_DATA_SET_1, ORDER_DATA_SET_2],
        ids=["DataSet_1_Black", "DataSet_2_Grey"]
    )
    @allure.title("Оформление заказа: {data[name]} {data[last_name]} + возврат на главную")
    def test_full_order_process(self, order_page, data):
        order_page.perform_full_order_flow(data)
        order_page.click_logo()
        current_url = order_page.get_current_url()
        assert BASE_URL in current_url, f"Ожидался URL с {BASE_URL}, но получен: {current_url}"

    @allure.title("Проверка перехода на форму заказа через кнопку внизу страницы")
    def test_transition_via_footer_button_only(self, order_page):
        order_page.click_order_button_from_footer()
        is_visible = order_page.verify_name_input_is_visible()
        assert is_visible, "Поле ввода имени не отображается после перехода через кнопку в футере"


@allure.feature("Навигация по сайту")
@allure.story("Проверка элементов шапки")
class TestHeaderNavigation:

    @allure.title("Клик по логотипу Яндекса открывает страницу Дзена (dzen.ru) в новой вкладке")
    def test_yandex_logo_opens_yandex_in_new_tab(self, order_page):
        original_window = order_page.click_yandex_logo_and_switch_to_new_tab()
        current_url = order_page.get_current_url()
        assert "dzen.ru" in current_url, f"Ожидался dzen.ru, но открыт: {current_url}"
        order_page.switch_to_window(original_window)


