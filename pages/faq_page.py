# логика работы с FAQ

from pages.base_page import BasePage
from locators.locators import ScooterLocators
from allure import step  


class FaqPage(BasePage):

    @step("Скроллим в самый низ страницы к блоку FAQ")
    def scroll_to_faq(self):
        # Скроллим в самый низ страницы, где находится блок FAQ
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    @step("Открываем вопрос FAQ по индексу: {index}")
    def open_question(self, index: int):
        locator = ScooterLocators.question_button(index)
        self.click_element(locator)

    @step("Проверяем, раскрыт ли вопрос FAQ с индексом: {index}")
    def is_question_expanded(self, index: int) -> bool:
        locator = ScooterLocators.question_button(index)
        element = self.find_element(locator)
        return element.get_attribute("aria-expanded") == "true"

    @step("Проверяем, что нужный вопрос раскрылся, а предыдущий закрылся")
    def verify_accordion_behavior(self, current_index: int, previous_index: int | None = None):
        assert self.is_question_expanded(current_index), f"Вопрос {current_index} не раскрылся"
        if previous_index is not None:
            assert not self.is_question_expanded(previous_index), f"Предыдущий вопрос {previous_index} не закрылся"
