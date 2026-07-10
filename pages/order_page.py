from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.locators import MainPageLocators, OrderPageLocators
from selenium.webdriver.common.keys import Keys
from .base_page import BasePage
import time
from allure import step
from time import sleep

class OrderPage(BasePage):  # <-- наследование от BasePage
    def __init__(self, driver, base_url):
        super().__init__(driver=driver, base_url=base_url, timeout=15)
        
    @step("Открываем главную страницу")
    def open_main(self):
        self.driver.get(self.base_url)

    @step("Кликаем кнопку «Заказать» в шапке страницы")
    def click_order_button_from_main(self):
        btn = self.wait.until(EC.element_to_be_clickable(MainPageLocators.BTN_ORDER_HEADER))
        btn.click()
        self.wait.until(lambda d: d.current_url.endswith("/order"))

    @step("Заполняем первую форму заказа: имя, фамилия, адрес, метро, телефон")
    def fill_first_form(self, name, last_name, address, metro_station, phone):
        # --- Имя ---
        el = self.wait.until(EC.visibility_of_element_located(OrderPageLocators.INPUT_NAME))
        el.clear()
        el.send_keys(name)

        # --- Фамилия ---
        el = self.wait.until(EC.visibility_of_element_located(OrderPageLocators.INPUT_LAST_NAME))
        el.clear()
        el.send_keys(last_name)

        # --- Адрес ---
        el = self.wait.until(EC.visibility_of_element_located(OrderPageLocators.INPUT_ADDRESS))
        el.clear()
        el.send_keys(address)

        # --- МЕТРО (ВОЗВРАЩАЕМ ТВОЙ РАБОЧИЙ ВАРИАНТ) ---
        # 1. Находим поле ввода метро и кликаем в него
        metro_input = self.wait.until(EC.element_to_be_clickable(OrderPageLocators.INPUT_METRO))
        metro_input.clear()
        metro_input.send_keys(metro_station)
        
        # 2. ВАЖНО: Даём 1.5 секунды на появление выпадающего списка
        time.sleep(1.5)

        # 3. Формируем локатор для поиска станции по тексту
        option_locator = (By.XPATH, OrderPageLocators.METRO_OPTION_BY_TEXT.format(metro_name=metro_station))

        try:
            metro_option = self.wait.until(EC.element_to_be_clickable(option_locator))
            metro_option.click()
            time.sleep(0.5)  # Даём интерфейсу зафиксировать выбор
        except Exception as e:
            raise Exception(f"Не удалось выбрать станцию метро '{metro_station}'. "
                            f"Список не раскрылся или текст станции не совпадает. Ошибка: {e}")

        # --- Телефон ---
        el = self.wait.until(EC.visibility_of_element_located(OrderPageLocators.INPUT_PHONE))
        el.clear()
        el.send_keys(phone)

    @step("Нажимаем кнопку «Далее» для перехода ко второй форме")
    def click_next(self):
        btn = self.wait.until(EC.element_to_be_clickable(OrderPageLocators.BTN_NEXT))
        btn.click()

    @step("Заполняем вторую форму: дата, срок аренды, цвет, комментарий")
    def fill_second_form(self, date_str, rent_period_text, color_black=False, color_grey=False, comment=""):
        date_input = self.wait_for_clickable(OrderPageLocators.INPUT_DATE)
        date_input.click()
        date_input.clear()
        
        if date_str:
            date_input.send_keys(date_str)
            time.sleep(0.5)  
            
            self.driver.find_element(By.TAG_NAME, "body").click()
            time.sleep(0.5)  # Ждём, пока анимация закрытия календаря доиграет

        dropdown = self.wait_for_clickable(OrderPageLocators.DROPDOWN_RENT_PERIOD)
        dropdown.click()

        self.wait.until(
            lambda d: len(d.find_elements(*OrderPageLocators.RENT_PERIOD_OPTIONS_LIST)) > 0,
            message="Список сроков аренды не раскрылся"
        )

        options_list = self.driver.find_elements(*OrderPageLocators.RENT_PERIOD_OPTIONS_LIST)

        if not options_list:
            raise Exception("Список сроков аренды пуст!")

        target_text = rent_period_text.strip().lower()
        found = False

        for option in options_list:
            option_text = option.text.strip().lower()
            if option_text == target_text:
                option.click()
                found = True
                break

        if not found:
            available_options = [o.text.strip() for o in options_list]
            raise Exception(
                f"Не удалось выбрать срок аренды '{rent_period_text}'. "
                f"В списке найдены: {available_options}"
            )

        time.sleep(0.5)
        
        # 3. Цвета и комментарий (оставляем как было)
        if color_black:
            cb_black = self.wait_for_clickable(OrderPageLocators.CHECKBOX_BLACK)
            if not cb_black.is_selected():
                cb_black.click()

        if color_grey:
            cb_grey = self.wait_for_clickable(OrderPageLocators.CHECKBOX_GREY)
            if not cb_grey.is_selected():
                cb_grey.click()

        comment_input = self.wait_for_visible(OrderPageLocators.INPUT_COMMENT)
        comment_input.clear()
        if comment:
            comment_input.send_keys(comment)

    @step("Нажимаем финальную кнопку «Заказать»")
    def click_final_order(self):
        btn = self.wait.until(EC.element_to_be_clickable(OrderPageLocators.BTN_ORDER_FINAL))
        btn.click()

    @step("Ждём появления модального окна подтверждения заказа")
    def wait_for_modal_to_appear(self):
        return self.wait.until(EC.visibility_of_element_located(OrderPageLocators.MODAL_WINDOW))

    @step("Клик по кнопке «Посмотреть статус» в модальном окне")
    def confirm_order_in_modal(self):
        btn_view = self.wait.until(EC.element_to_be_clickable(OrderPageLocators.BTN_MODAL_VIEW_STATUS))
        btn_view.click()
        time.sleep(0.5)

    @step("Ждём исчезновения модального окна")
    def wait_for_modal_to_disappear(self, timeout=15):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                modal = self.driver.find_element(*OrderPageLocators.MODAL_WINDOW)
                if modal.value_of_css_property('display') == 'none':
                    return
            except Exception:
                return
            time.sleep(0.3)
        raise Exception("Модальное окно не закрылось после клика на «Посмотреть статус»!")

    @step("Скроллим к кнопке «Заказать» внизу и кликаем по ней")
    def click_order_button_from_footer(self):
        btn = self.wait.until(EC.element_to_be_clickable(MainPageLocators.BTN_ORDER_FOOTER))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
        time.sleep(0.5)
        btn.click()
        self.wait.until(lambda d: d.current_url.endswith("/order"))

    @step("Клик по логотипу «Самокат» в шапке")
    def click_logo(self):
        logo_link = self.wait.until(EC.element_to_be_clickable(MainPageLocators.LINK_LOGO))
        logo_link.click()

    @step("Проверяем, что мы на главной странице (валидируем URL)")
    def assert_on_main_page(self, expected_url=None):
        if expected_url is None:
            expected_url = self.base_url
        current_url = self.driver.current_url
        if not expected_url.endswith("/"):
            expected_url += "/"
        if not current_url.endswith("/"):
            current_url += "/"
        if current_url != expected_url:
            raise Exception(f"Ожидался URL: {expected_url}, но перешли на: {current_url}")

    @step("Клик по логотипу Яндекса и переключение на новую вкладку")
    def click_yandex_logo_and_switch_to_new_tab(self):
        original_window = self.driver.current_window_handle
        yandex_btn = self.wait.until(EC.element_to_be_clickable(MainPageLocators.LINK_LOGO_YANDEX))
        yandex_btn.click()
        WebDriverWait(self.driver, 10).until(lambda d: len(d.window_handles) > 1)
        new_window = [w for w in self.driver.window_handles if w != original_window][-1]
        self.driver.switch_to.window(new_window)
        return original_window

    @step("Проверяем, что в новой вкладке открылся Дзен (по заголовку)")
    def assert_new_tab_has_dzen_like_title(self, timeout=30):
        start_time = time.time()
        target_word = "Дзен"
        while time.time() - start_time < timeout:
            current_title = self.driver.title
            if target_word in current_title:
                return
            time.sleep(0.5)
        raise Exception(
            f"Не удалось подтвердить, что открыта страница Дзена. "
            f"Заголовок вкладки: '{current_title}'. "
            f"Ожидалось слово: '{target_word}'"
        )

    @step("Выполняем полный поток заказа")
    def perform_full_order_flow(self, data):
    # 1.открываем форму заказа
        self.click_order_button_from_main()
    
    # Пауза, чтобы форма успела отрисоваться
        time.sleep(1)

    # 2. Теперь заполняем формы 
        self.fill_first_form(
            name=data["name"],
            last_name=data["last_name"],
            address=data["address"],
            metro_station=data["metro"],
            phone=data["phone"]
    )
    # 3. Нажимаем "Далее"
        self.click_next()

    # 4. Заполняем вторую форму
        self.fill_second_form(
            date_str=data.get("date", ""),
            rent_period_text=data.get("rent_period", "сутки"),  # <-- это спасёт от KeyError
            color_black=data.get("color_black", False),
            color_grey=data.get("color_grey", False),
            comment=data.get("comment", "")
        )

    # 5. Финальный клик и проверка модалки
        self.click_final_order()
        self.wait_for_modal_to_appear()
        self.confirm_order_in_modal()
        self.wait_for_modal_to_disappear()
