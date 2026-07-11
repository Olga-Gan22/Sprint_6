from selenium.webdriver.common.by import By

class ScooterLocators:
    @staticmethod
    def question_button(index: int):
        return By.CSS_SELECTOR, f".accordion__item:nth-child({index + 1}) .accordion__button"

    @staticmethod
    def answer_panel(index: int):
        return By.CSS_SELECTOR, f".accordion__item:nth-child({index + 1}) .accordion__panel"

class MainPageLocators:
    BTN_ORDER_HEADER = (By.CSS_SELECTOR, ".Header_Nav__AGCXC button.Button_Button__ra12g")
    BTN_ORDER_FOOTER = (By.CSS_SELECTOR, ".Home_FinishButton__1_cWm button.Button_Button__ra12g")
    LINK_LOGO = (By.CSS_SELECTOR, "a.Header_LogoScooter__3lsAR")
    LINK_LOGO_YANDEX = (By.CSS_SELECTOR, "a.Header_LogoYandex__3TSOI")


class OrderPageLocators:
    # Поля формы
    INPUT_NAME = (By.CSS_SELECTOR, "input[placeholder='* Имя']")
    INPUT_LAST_NAME = (By.CSS_SELECTOR, "input[placeholder='* Фамилия']")
    INPUT_ADDRESS = (By.CSS_SELECTOR, "input[placeholder='* Адрес: куда привезти заказ']")
    INPUT_METRO = (By.CSS_SELECTOR, "input.select-search__input")
    METRO_OPTION_BY_TEXT = "//*[contains(text(), '{metro_name}')]"
    INPUT_PHONE = (By.CSS_SELECTOR, "input[placeholder='* Телефон: на него позвонит курьер']")
    BTN_NEXT = (By.CSS_SELECTOR, ".Order_NextButton__1_rCA button.Button_Button__ra12g")


    # --- Вторая форма ---
    INPUT_DATE = (By.CSS_SELECTOR, "input[placeholder*='Когда привезти самокат']")
    DROPDOWN_RENT_PERIOD = (By.CSS_SELECTOR, ".Dropdown-control")
    RENT_PERIOD_OPTIONS_LIST = (By.CSS_SELECTOR, ".Dropdown-option[role='option']")

    CHECKBOX_BLACK = (By.CSS_SELECTOR, "[name='colorBlack']")
    CHECKBOX_GREY = (By.CSS_SELECTOR, "[name='colorGrey']")
    INPUT_COMMENT = (By.CSS_SELECTOR, "textarea[placeholder*='Комментарий']")
    BTN_ORDER_FINAL = (By.CSS_SELECTOR, ".Order_Buttons__1xGrp button:not(.Button_Inverted__3IF-i)")
    CALENDAR_POPPER = (By.CSS_SELECTOR, ".react-datepicker__popper")

    
    # Модальные окна
    BTN_MODAL_VIEW_STATUS = (By.CSS_SELECTOR, ".Order_Modal__YZ-d3 button.Button_Button__ra12g")
    MODAL_WINDOW = (By.CSS_SELECTOR, ".Order_Modal__YZ-d3")
    BTN_MODAL_YES = (By.CSS_SELECTOR, ".Order_Modal__YZ-d3 button:not(.Button_Inverted__3IF-i)")
    BTN_MODAL_NO = (By.CSS_SELECTOR, ".Order_Modal__YZ-d3 button.Button_Inverted__3IF-i")

    

    