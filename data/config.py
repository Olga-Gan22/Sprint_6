#URL сайта

BASE_URL = "https://qa-scooter.praktikum-services.ru"

# --- Данные для теста заказа самоката ---
ORDER_DATA_SET_1 = {
    "name": "Ольга",
    "last_name": "Ганжова",
    "address": "Москва, ул. Ленина, д. 1",
    "metro": "Охотный Ряд",
    "phone": "89205537695",
    "date": "25.07.2026",
    "rent_period": "сутки",
    "color_black": True,      # заказываем чёрный
    "color_grey": False,       # серый НЕ заказываем
    "comment": "Оставьте у консьержа"
}

ORDER_DATA_SET_2 = {
    "name": "Иван",
    "last_name": "Петров",
    "address": "Санкт-Петербург, Невский пр., д. 10",
    "metro": "Спортивная",
    "phone": "89991234567",
    "date": "30.07.2026",
    "rent_period": "двое суток",
    "color_black": False,      # чёрный НЕ заказываем
    "color_grey": True,        # заказываем серый
    "comment": ""
}