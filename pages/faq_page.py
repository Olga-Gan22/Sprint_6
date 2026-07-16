from allure_commons._allure import step
from locators.locators import ScooterLocators
from .base_page import BasePage


class FaqPage(BasePage):

    @step("Открываем вопрос FAQ с индексом: {index}")
    def open_question(self, index: int):
        btn_locator = ScooterLocators.question_button(index)
        self.scroll_into_view(btn_locator)
        self.click_element(
            btn_locator,
            message=f"Кнопка вопроса №{index} не стала кликабельной"
        )

        answer_panel_locator = ScooterLocators.answer_panel(index)
        self.wait_for_visible(
            answer_panel_locator,
            message=f"Ответ на вопрос №{index} не появился после клика — возможно, баг тренажёра или неверный локатор"
        )

    @step("Проверяем, раскрыт ли вопрос с индексом: {index} (возвращаем bool)")
    def is_question_expanded(self, index: int) -> bool:
        locator = ScooterLocators.answer_panel(index)
        panel = self.find_element(locator)
        has_hidden_attr = panel.get_attribute("hidden") is not None
        return not has_hidden_attr

    @step("Получаем состояние аккордеона: (текущий_раскрыт, предыдущий_закрыт)")
    def get_accordion_state(self, curr_index: int, prev_index: int) -> tuple[bool, bool]:
        curr_is_expanded = self.is_question_expanded(curr_index)
        prev_is_closed = not self.is_question_expanded(prev_index)
        return curr_is_expanded, prev_is_closed

    @step("Получаем текст ответа для вопроса с индексом: {index}")
    def get_answer_text(self, index: int) -> str:
        locator = ScooterLocators.answer_panel(index)
        panel = self.wait_for_visible(
            locator,
            message=f"Панель ответа №{index} не видна"
        )
        return panel.text.strip()
