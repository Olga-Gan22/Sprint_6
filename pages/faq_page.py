from allure_commons._allure import step
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.locators import ScooterLocators
from .base_page import BasePage

class FaqPage(BasePage):
    @step("Открываем вопрос FAQ с индексом: {index}")
    def open_question(self, index: int):
        locator = ScooterLocators.question_button(index)
        self.scroll_into_view(locator)
        self.click_element(locator)

    @step("Проверяем, раскрыт ли вопрос с индексом: {index}")
    def is_question_expanded(self, index: int) -> bool:
        locator = ScooterLocators.answer_panel(index)
        panel = self.driver.find_element(*locator)

        has_hidden_attr = panel.get_attribute("hidden") is not None
        return not has_hidden_attr

    @step("Проверяем поведение аккордеона: текущий открыт, предыдущий закрыт")
    def verify_accordion_behavior(self, curr_index: int, prev_index: int):
        assert self.is_question_expanded(curr_index), f"Вопрос №{curr_index} не раскрылся"
        assert not self.is_question_expanded(prev_index), f"Предыдущий вопрос №{prev_index} НЕ закрылся!"

    @step("Получаем текст ответа для вопроса с индексом: {index}")
    def get_answer_text(self, index: int) -> str:
        locator = ScooterLocators.answer_panel(index)
        panel = self.wait_for_visible(locator)
        return panel.text.strip()
