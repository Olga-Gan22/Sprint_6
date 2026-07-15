from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from locators.locators import MainPageLocators, OrderPageLocators
from .base_page import BasePage
from selenium.webdriver.support.wait import WebDriverWait
import allure


class OrderPage(BasePage):
    def __init__(self, driver, base_url, timeout=15):
        super().__init__(driver=driver, base_url=base_url, timeout=timeout)

    @allure.step("Открываем главную страницу")
    def open_main(self):
        self.open()

    @allure.step("Кликаем кнопку «Заказать» в шапке страницы")
    def click_order_button_from_main(self):
        btn = self.wait_for_clickable(MainPageLocators.BTN_ORDER_HEADER)
        btn.click()

    @allure.step("Заполняем первую форму заказа: имя, фамилия, адрес, метро, телефон")
    def fill_first_form(self, name, last_name, address, metro_station, phone):
        self.send_keys(OrderPageLocators.INPUT_NAME, name)
        self.send_keys(OrderPageLocators.INPUT_LAST_NAME, last_name)
        self.send_keys(OrderPageLocators.INPUT_ADDRESS, address)

        metro_input = self.wait_for_visible(OrderPageLocators.INPUT_METRO)
        metro_input.clear()
        metro_input.send_keys(metro_station)

        metro_option_locator = (By.XPATH, OrderPageLocators.METRO_OPTION_BY_TEXT.format(metro_name=metro_station))
        metro_option = self.wait_for_clickable(metro_option_locator)
        metro_option.click()

        self.send_keys(OrderPageLocators.INPUT_PHONE, phone)

    @allure.step("Нажимаем кнопку «Далее» для перехода ко второй форме")
    def click_next(self):
        btn = self.wait_for_clickable(OrderPageLocators.BTN_NEXT)
        btn.click()

    @allure.step("Заполняем вторую форму: дата, срок аренды, цвет, комментарий")
    def fill_second_form(self, date_str, rent_period_text, color_black=False, color_grey=False, comment=""):
        date_input = self.wait_for_clickable(OrderPageLocators.INPUT_DATE)
        date_input.click()
        date_input.clear()

        if date_str:
            date_input.send_keys(date_str)
            self.wait.until(
                lambda d: date_input.get_attribute("value") != "",
                message="Поле даты не приняло значение после ввода"
            )

        # Ждём закрытия календаря
        self.wait.until(
            lambda d: len(d.find_elements(By.CSS_SELECTOR, ".react-datepicker-popper")) == 0,
            message="БАГ ТРЕНАЖЁРА: Календарь не закрылся после клика вне поля."
        )

        dropdown = self.wait_for_clickable(OrderPageLocators.DROPDOWN_RENT_PERIOD)
        self.scroll_into_view(OrderPageLocators.DROPDOWN_RENT_PERIOD)
        self.execute_script("arguments[0].click();", dropdown)

        options_locator = OrderPageLocators.RENT_PERIOD_OPTIONS_LIST
        self.wait.until(
            lambda d: len(self.find_elements(*options_locator)) > 0,
            message="Список сроков аренды не раскрылся после клика (0 опций найдено)."
        )

        options_list = self.find_elements(*options_locator)

        target_text = rent_period_text.strip().lower()
        found = False
        for option in options_list:
            opt_text = option.text.strip().lower()
            if opt_text == target_text:
                self.execute_script("arguments[0].scrollIntoView({block:'center'});", option)
                option.click()
                found = True
                break

        if not found:
            available = [o.text.strip() for o in options_list]
            raise Exception(
                f"Не удалось выбрать срок аренды '{rent_period_text}'. В списке найдены: {available}"
            )

        if color_black:
            cb_black = self.wait_for_clickable(OrderPageLocators.CHECKBOX_BLACK)
            if not cb_black.is_selected():
                cb_black.click()

        if color_grey:
            cb_grey = self.wait_for_clickable(OrderPageLocators.CHECKBOX_GREY)
            if not cb_grey.is_selected():
                cb_grey.click()

        self.send_keys(OrderPageLocators.INPUT_COMMENT, comment, clear_first=True)

    @allure.step("Нажимаем финальную кнопку «Заказать»")
    def click_final_order(self):
        btn = self.wait_for_clickable(OrderPageLocators.BTN_ORDER_FINAL)
        btn.click()

    @allure.step("Ждём появления модального окна подтверждения заказа")
    def wait_for_modal_to_appear(self):
        return self.wait_for_visible(OrderPageLocators.MODAL_WINDOW)

    @allure.step("Клик по кнопке «Посмотреть статус» в модальном окне")
    def confirm_order_in_modal(self):
        btn_view = self.wait_for_clickable(OrderPageLocators.BTN_MODAL_VIEW_STATUS)
        btn_view.click()

    @allure.step("Ждём исчезновения модального окна")
    def wait_for_modal_to_disappear(self, timeout=15):
        self.wait.until(
            EC.invisibility_of_element_located(OrderPageLocators.MODAL_WINDOW),
            message="Модальное окно не закрылось после клика на «Посмотреть статус»"
        )

    @allure.step("Скроллим к кнопке «Заказать» внизу и кликаем по ней")
    def click_order_button_from_footer(self):
        locator = MainPageLocators.BTN_ORDER_FOOTER
        self.scroll_into_view(locator)
        btn = self.wait_for_clickable(locator)
        btn.click()

    @allure.step("Клик по логотипу «Самокат» в шапке (возврат на главную)")
    def click_logo(self):
        logo_link = self.wait_for_clickable(MainPageLocators.LINK_LOGO)
        logo_link.click()

    @allure.step("Клик по логотипу Яндекса (открытие в новой вкладке) и ожидание dzen.ru")
    def click_yandex_logo_and_switch_to_new_tab(self):
        original_window = self.get_current_window_handle()
        link = self.wait_for_clickable(MainPageLocators.LINK_LOGO_YANDEX)
        link.click()

        wait = WebDriverWait(self.driver, 15)
        wait.until(
            lambda d: len(d.window_handles) > 1,
            message="Не появилась новая вкладка после клика по логотипу Яндекса"
        )

        new_window = None
        for handle in self.get_window_handles():
            if handle != original_window:
                new_window = handle
                break

        assert new_window is not None, "Не найдена новая вкладка"
        self.switch_to_window(new_window)

        wait.until(
            lambda d: "dzen.ru" in self.get_current_url(),
            message=f"Ожидался URL с dzen.ru, но получен: {self.get_current_url()}"
        )
        return original_window

    @allure.step("Выполняем полный поток заказа")
    def perform_full_order_flow(self, data):
        self.click_order_button_from_main()
        self.fill_first_form(
            name=data["name"],
            last_name=data["last_name"],
            address=data["address"],
            metro_station=data["metro"],
            phone=data["phone"]
        )
        self.click_next()
        self.fill_second_form(
            date_str=data.get("date", ""),
            rent_period_text=data.get("rent_period", ""),
            color_black=data.get("color_black", False),
            color_grey=data.get("color_grey", False),
            comment=data.get("comment", "")
        )
        self.click_final_order()
        self.wait_for_modal_to_appear()
        self.confirm_order_in_modal()
        self.wait_for_modal_to_disappear()

    @allure.step("Проверяем, что поле ввода имени отображается на странице")
    def verify_name_input_is_visible(self):
        element = self.wait_for_visible(OrderPageLocators.INPUT_NAME)
        return element.is_displayed()
