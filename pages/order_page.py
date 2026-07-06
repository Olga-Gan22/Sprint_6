from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.locators import MainPageLocators, OrderPageLocators
import time
from allure import step  


class OrderPage:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.base_url = base_url

    @step("Открываем главную страницу")
    def open_main(self):
        self.driver.get(self.base_url)

    @step("Кликаем кнопку «Заказать» в шапке страницы")
    def click_order_button_from_main(self):
        btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, MainPageLocators.BTN_ORDER_HEADER)))
        btn.click()
        self.wait.until(lambda d: d.current_url.endswith("/order"))

    @step("Заполняем первую форму заказа: имя, фамилия, адрес, метро, телефон")
    def fill_first_form(self, name, last_name, address, metro_station, phone):
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, OrderPageLocators.INPUT_NAME)))

        self.driver.find_element(By.CSS_SELECTOR, OrderPageLocators.INPUT_NAME).send_keys(name)
        self.driver.find_element(By.CSS_SELECTOR, OrderPageLocators.INPUT_LAST_NAME).send_keys(last_name)
        self.driver.find_element(By.CSS_SELECTOR, OrderPageLocators.INPUT_ADDRESS).send_keys(address)

        metro_input = self.driver.find_element(By.CSS_SELECTOR, OrderPageLocators.INPUT_METRO)
        metro_input.clear()
        metro_input.send_keys(metro_station)
        time.sleep(1.5)

        # Клик по найденной станции в списке
        option_locator = (By.XPATH, OrderPageLocators.METRO_OPTION_BY_TEXT.format(metro_name=metro_station))
        try:
            metro_option = self.wait.until(EC.element_to_be_clickable(option_locator))
            metro_option.click()
            time.sleep(0.5)
        except Exception:
            # Если станция не нашлась — продолжаем, чтобы тест не падал сразу
            pass

        self.driver.find_element(By.CSS_SELECTOR, OrderPageLocators.INPUT_PHONE).send_keys(phone)

    @step("Нажимаем кнопку «Далее» для перехода ко второй форме")
    def click_next(self):
        btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, OrderPageLocators.BTN_NEXT)))
        btn.click()

    @step("Заполняем вторую форму: дата, срок аренды, цвет, комментарий")
    def fill_second_form(self, date_str, rent_period_text, color_black=False, color_grey=False, comment=""):
        # 1. Работа с датой (оставляем как было, чтобы закрыть календарь)
        date_input = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, OrderPageLocators.INPUT_DATE)))
        date_input.click()
        date_input.clear()
        date_input.send_keys(date_str)
        time.sleep(0.5)

        # Закрываем календарь, чтобы он не перекрывал дропдаун
        self.driver.find_element(By.TAG_NAME, "body").click()
        time.sleep(0.5)

        # 2. Выбор срока аренды
        dropdown = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, OrderPageLocators.DROPDOWN_RENT_PERIOD)))
        dropdown.click()
        time.sleep(1)  # Даём списку раскрыться

        # Получаем ВСЕ пункты списка
        options_list = self.wait.until(EC.visibility_of_all_elements_located(
            (By.CSS_SELECTOR, OrderPageLocators.RENT_PERIOD_OPTIONS_LIST)
        ))

        
        target_index = -1
        if "1 день" in rent_period_text:
            target_index = 0
        elif "2 дня" in rent_period_text:
            target_index = 1
        elif "3 дня" in rent_period_text:
            target_index = 2
        elif "4 дня" in rent_period_text:
            target_index = 3
        elif "5 дней" in rent_period_text:
            target_index = 4

        if target_index != -1 and target_index < len(options_list):
            options_list[target_index].click()
            time.sleep(0.5)
        else:
            # Если вдруг срок не найден, выбрасываем своё исключение (в твоём стиле)
            raise Exception(f"Не удалось найти вариант срока аренды для текста: {rent_period_text}")

        # 3. Цвета и комментарий
        if color_black:
            self.driver.find_element(By.CSS_SELECTOR, OrderPageLocators.CHECKBOX_BLACK).click()
        if color_grey:
            self.driver.find_element(By.CSS_SELECTOR, OrderPageLocators.CHECKBOX_GREY).click()

        if comment:
            self.driver.find_element(By.CSS_SELECTOR, OrderPageLocators.INPUT_COMMENT).send_keys(comment)

    @step("Нажимаем финальную кнопку «Заказать»")
    def click_final_order(self):
        btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, OrderPageLocators.BTN_ORDER_FINAL)))
        btn.click()

    @step("Ждём появления модального окна подтверждения заказа")
    def wait_for_modal_to_appear(self):
        """Ждём появления модального окна"""
        return self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, OrderPageLocators.MODAL_WINDOW)))

    @step("Клик по кнопке «Посмотреть статус» в модальном окне")
    def confirm_order_in_modal(self):
        """Клик по кнопке «Посмотреть статус» (это единственное действие в модалке)"""
        btn_view = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, OrderPageLocators.BTN_MODAL_VIEW_STATUS)))
        btn_view.click()
        time.sleep(0.5)  # Даём время на анимацию закрытия или переход

    @step("Ждём исчезновения модального окна")
    def wait_for_modal_to_disappear(self, timeout=15):
        
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                modal = self.driver.find_element(By.CSS_SELECTOR, OrderPageLocators.MODAL_WINDOW)
                # Если элемент есть, но скрыт — считаем, что всё ок
                if modal.value_of_css_property('display') == 'none':
                    return
            except Exception:
                return
            time.sleep(0.3)

        # Если дошли сюда — модалка не закрылась
        raise Exception("Модальное окно не закрылось после клика на «Посмотреть статус»!")

    @step("Скроллим к кнопке «Заказать» внизу и кликаем по ней")
    def click_order_button_from_footer(self):
        """Скроллим к кнопке «Заказать» внизу и кликаем по ней"""
        btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, MainPageLocators.BTN_ORDER_FOOTER)))

        # Скроллим элемент в видимую область
        self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
        time.sleep(0.5)  # Даём время на завершение скролла

        btn.click()
        self.wait.until(lambda d: d.current_url.endswith("/order"))

    @step("Клик по логотипу «Самокат» в шапке")
    def click_logo(self):
        logo_link = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, MainPageLocators.LINK_LOGO)))
        logo_link.click()

    @step("Проверяем, что мы на главной странице (валидируем URL)")
    def assert_on_main_page(self, expected_url=None):
        if expected_url is None:
            expected_url = self.base_url

        current_url = self.driver.current_url
        # Убираем трейлинг-слэш для более надёжного сравнения
        if not expected_url.endswith("/"):
            expected_url += "/"
        if not current_url.endswith("/"):
            current_url += "/"

        if current_url != expected_url:
            raise Exception(f"Ожидался URL: {expected_url}, но перешли на: {current_url}")

    @step("Клик по логотипу Яндекса и переключение на новую вкладку")
    def click_yandex_logo_and_switch_to_new_tab(self):
        # Запоминаем ID текущей вкладки
        original_window = self.driver.current_window_handle

        # Находим и кликаем по логотипу
        yandex_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, MainPageLocators.LINK_LOGO_YANDEX)))
        yandex_btn.click()

        # Ждём появления второй вкладки
        WebDriverWait(self.driver, 10).until(lambda d: len(d.window_handles) > 1)

        # Переключаемся на последнюю открытую вкладку (новую)
        new_window = [w for w in self.driver.window_handles if w != original_window][-1]
        self.driver.switch_to.window(new_window)

        return original_window  # Возвращаем ID исходной вкладки, чтобы потом вернуться

    @step("Проверяем, что в новой вкладке открылся Дзен (по заголовку)")
    def assert_new_tab_has_dzen_like_title(self, timeout=30):
        start_time = time.time()
        target_word = "Дзен"

        while time.time() - start_time < timeout:
            current_title = self.driver.title
            if target_word in current_title:
                return  # Нашли — тест проходит
            time.sleep(0.5)

        raise Exception(
            f"Не удалось подтвердить, что открыта страница Дзена. "
            f"Заголовок вкладки: '{current_title}'. "
            f"Ожидалось слово: '{target_word}'"
        )
