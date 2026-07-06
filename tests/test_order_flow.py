import pytest
import allure
from data.config import BASE_URL, ORDER_DATA_SET_1, ORDER_DATA_SET_2
from pages.order_page import OrderPage

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
    @allure.title("Оформление заказа: {data[name]} {data[last_name]} + возврат на главную через логотип")
    def test_full_order_process(self, data, driver):
        # 1. Старт с главной + клик по кнопке «Заказать»
        self.page.open_main()
        self.page.click_order_button_from_main()

        # 2. Заполнение первой формы
        self.page.fill_first_form(
            name=data["name"],
            last_name=data["last_name"],
            address=data["address"],
            metro_station=data["metro"],
            phone=data["phone"]
        )

        # 3. Переход ко второй форме
        self.page.click_next()

        # 4. Заполнение второй формы
        self.page.fill_second_form(
            date_str=data["date"],
            rent_period_text=data["rent_period_text"],
            color_black=data["color_black"],
            color_grey=data["color_grey"],
            comment=data["comment"]
        )

        # 5. Кнопка «Заказать» -> Модалка
        self.page.click_final_order()
        self.page.wait_for_modal_to_appear()

        # Клик по «Посмотреть статус»
        self.page.confirm_order_in_modal()

        # Проверка, что окно ушло
        self.page.wait_for_modal_to_disappear()

        # --- НОВАЯ ПРОВЕРКА: клик по логотипу и возврат на главную ---
        self.page.click_logo()
        self.page.assert_on_main_page()


    @allure.title("Оформление заказа через кнопку внизу страницы")
    def test_order_via_footer_button(self, driver):
        # 1. Открываем главную
        self.page.open_main()
        
        # 2. Скроллим и кликаем кнопку «Заказать» внизу
        self.page.click_order_button_from_footer()
        
        # Дальше логика заполнения форм такая же, как в основном тесте
        self.page.fill_first_form(
            name=ORDER_DATA_SET_1["name"],
            last_name=ORDER_DATA_SET_1["last_name"],
            address=ORDER_DATA_SET_1["address"],
            metro_station=ORDER_DATA_SET_1["metro"],
            phone=ORDER_DATA_SET_1["phone"]
        )
        
        self.page.click_next()
        
        self.page.fill_second_form(
            date_str=ORDER_DATA_SET_1["date"],
            rent_period_text=ORDER_DATA_SET_1["rent_period_text"],
            color_black=ORDER_DATA_SET_1["color_black"],
            color_grey=ORDER_DATA_SET_1["color_grey"],
            comment=ORDER_DATA_SET_1["comment"]
        )
        
        self.page.click_final_order()
        self.page.wait_for_modal_to_appear()
        self.page.confirm_order_in_modal()
        self.page.wait_for_modal_to_disappear()

    @allure.title("Клик по логотипу Яндекса открывает Дзен в новой вкладке") 
    def test_yandex_logo_opens_dzen_in_new_tab(self, driver):
        # 1. Сначала оформляем заказ, чтобы оказаться на главной после закрытия модалки
        self.page.open_main()
        self.page.click_order_button_from_main()

        self.page.fill_first_form(
            name=ORDER_DATA_SET_1["name"],
            last_name=ORDER_DATA_SET_1["last_name"],
            address=ORDER_DATA_SET_1["address"],
            metro_station=ORDER_DATA_SET_1["metro"],
            phone=ORDER_DATA_SET_1["phone"]
        )

        self.page.click_next()

        self.page.fill_second_form(
            date_str=ORDER_DATA_SET_1["date"],
            rent_period_text=ORDER_DATA_SET_1["rent_period_text"],
            color_black=ORDER_DATA_SET_1["color_black"],
            color_grey=ORDER_DATA_SET_1["color_grey"],
            comment=ORDER_DATA_SET_1["comment"]
        )

        self.page.click_final_order()
        self.page.wait_for_modal_to_appear()
        self.page.confirm_order_in_modal()
        self.page.wait_for_modal_to_disappear()

        # 2. Теперь мы на странице с шапкой, где есть логотип Яндекса
        # Клик по Яндексу и переключение на новую вкладку
        original_window = self.page.click_yandex_logo_and_switch_to_new_tab()

        # 3. Проверяем, что новая вкладка — это Дзен (по заголовку)
        self.page.assert_new_tab_has_dzen_like_title()

       