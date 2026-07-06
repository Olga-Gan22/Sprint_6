from selenium.webdriver.common.by import By

class ScooterLocators:
    @staticmethod
    def question_button(index: int):
        return (By.ID, f"accordion__heading-{index}")

    @staticmethod
    def answer_panel(index: int):
        return (By.ID, f"accordion__panel-{index}")


class MainPageLocators:
    BTN_ORDER_HEADER = ".Header_Nav__AGCXC button.Button_Button__ra12g"

     # Кнопка «Заказать» внизу страницы (после скролла)
    BTN_ORDER_FOOTER = ".Home_FinishButton__1_cWm button.Button_Button__ra12g"

    # Логотип «Самокат» в шапке (ссылка)
    LINK_LOGO = "a.Header_LogoScooter__3lsAR"

    # Логотип Яндекса (target="_blank", ведёт наружу)
    LINK_LOGO_YANDEX = "a.Header_LogoYandex__3TSOI"


class OrderPageLocators:
    # --- Первая форма ---
    INPUT_NAME = "input[placeholder='* Имя']"
    INPUT_LAST_NAME = "input[placeholder='* Фамилия']"
    INPUT_ADDRESS = "input[placeholder='* Адрес: куда привезти заказ']"
    INPUT_METRO = ".select-search__input"
    METRO_OPTION_BY_TEXT = "//*[contains(text(), '{metro_name}')]"
    INPUT_PHONE = "input[placeholder='* Телефон: на него позвонит курьер']"
    BTN_NEXT = ".Order_NextButton__1_rCA button.Button_Button__ra12g"

    # --- Вторая форма ---
    INPUT_DATE = ".react-datepicker__input-container input"
    DROPDOWN_RENT_PERIOD = ".Dropdown-control"
    
    # ВАЖНО: Ищем все видимые элементы внутри дропдауна (обычно это li или div)
    RENT_PERIOD_OPTIONS_LIST = ".Dropdown-menu .Dropdown-option" 

    CHECKBOX_BLACK = "#black"
    CHECKBOX_GREY = "#grey"
    INPUT_COMMENT = "input[placeholder='Комментарий для курьера']"
    BTN_ORDER_FINAL = ".Order_Buttons__1xGrp button:not(.Button_Inverted__3IF-i)"


    # Кнопка в модальном окне «Посмотреть статус»
    BTN_MODAL_VIEW_STATUS = ".Order_Modal__YZ-d3 button.Button_Button__ra12g"
    MODAL_WINDOW = ".Order_Modal__YZ-d3"

    # --- Модальное окно ---
    MODAL_WINDOW = ".Order_Modal__YZ-d3"
    BTN_MODAL_YES = ".Order_Modal__YZ-d3 button:not(.Button_Inverted__3IF-i)"
    BTN_MODAL_NO = ".Order_Modal__YZ-d3 button.Button_Inverted__3IF-i"