import pytest
import allure
from data.config import BASE_URL
from data.faq_questions import FAQ_QUESTIONS
from pages.faq_page import FaqPage

@allure.feature("FAQ")
@allure.story("Вопросы о важном")
class TestFaqQuestions:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.page = FaqPage(driver, BASE_URL)
        self.page.open()
        self.page.scroll_to_faq()

    @pytest.mark.parametrize("index, question_text", FAQ_QUESTIONS)
    @allure.title("Открытие вопроса FAQ: {question_text}")
    def test_open_single_question(self, index, question_text, driver):
        """Отдельный тест на открытие каждого вопроса (всего 8 тестов)"""
        self.page.open_question(index)
        assert self.page.is_question_expanded(index), f"Не раскрылся вопрос: {question_text}"

    @pytest.mark.parametrize(
        "prev_index, curr_index",
        [(i, i + 1) for i in range(len(FAQ_QUESTIONS) - 1)],
     )
    
    @allure.title("Проверка переключения вопросов FAQ: при открытии №{curr_index} предыдущий №{prev_index} закрывается")
    def test_accordion_closes_previous_when_opening_next(self, prev_index, curr_index, driver):
        
        self.page.open_question(prev_index)
        assert self.page.is_question_expanded(prev_index), "Предыдущий вопрос не раскрылся перед проверкой"

        self.page.open_question(curr_index)
        self.page.verify_accordion_behavior(curr_index, prev_index)
