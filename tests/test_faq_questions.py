import pytest
import allure
from data.faq_questions import FAQ_QUESTIONS
from locators.locators import ScooterLocators

@allure.feature("FAQ")
@allure.story("Вопросы о важном")
class TestFaqQuestions:

    @pytest.mark.parametrize("index, question_text, expected_answer", FAQ_QUESTIONS)
    @allure.title("Открытие вопроса FAQ: {question_text}")
    def test_open_single_question(self, index, question_text, expected_answer, faq_page):
        faq_page.open_question(index)
        actual_answer = faq_page.get_answer_text(index)

        assert actual_answer == expected_answer, (
            f"Для вопроса '{question_text}' ожидался ответ: '{expected_answer}', "
            f"а получен: '{actual_answer}'"
        )

    @pytest.mark.parametrize(
        "prev_index, curr_index",
        [(i, i + 1) for i in range(len(FAQ_QUESTIONS) - 1)],
    )
    @allure.title(
        "Проверка переключения вопросов FAQ: при открытии №{curr_index} предыдущий №{prev_index} закрывается"
    )
    def test_accordion_closes_previous_when_opening_next(self, prev_index, curr_index, faq_page):
        # 1. Открываем предыдущий
        faq_page.open_question(prev_index)
        assert faq_page.is_question_expanded(prev_index), "Предыдущий вопрос не раскрылся перед проверкой"

        # 2. Открываем текущий
        faq_page.open_question(curr_index)

        # 3. Получаем состояние от страницы 
        curr_is_expanded, prev_is_closed = faq_page.get_accordion_state(curr_index, prev_index)

        # 4. Все проверки — только здесь, в тесте
        assert curr_is_expanded, f"Вопрос №{curr_index} не раскрылся"
        assert prev_is_closed, f"Предыдущий вопрос №{prev_index} НЕ закрылся!"
