from telegram import KeyboardButton, ReplyKeyboardMarkup

BUTTON_1_1_ZapProf = "Заполнить профиль"

BUTTON_2_1_YurFace = "Юр.лицо"
BUTTON_2_2_FizFace = "Физ.лицо"

BUTTON_3_1_City = "Москва"
BUTTON_3_2_City = "Калуга"
BUTTON_3_3_City = "Серпухов"
BUTTON_3_4_City = "Орехово-Зуево"

BUTTON_4_1_SendNameProf = "Отправить имя профиля"

BUTTON_5_1_EditProf = "Изменить профиль"
BUTTON_5_2_NewOrder = "Новый заказ"
BUTTON_5_3_ReplyOldOrder = "Повторить прошлый заказ"

BUTTON_6_1_Edit = "Изменить"
BUTTON_6_2_Edit = "Вернуться обратно"

BUTTON_7_1_New_Order = "19 литровая бутыль воды"
BUTTON_7_2_New_Order = "6 литровая бутыль воды"
BUTTON_7_3_New_Order = "Ручная помпа"
BUTTON_7_4_New_Order = "Вернуться назад"

BUTTON_8_1_Order = "Ввести кол-во"
BUTTON_8_2_Order = "Отменить"

BUTTON_9_1_temp_order = "Отменить этот товар"

BUTTON_10_1_temp_order2 = "Добавить ещё товар"
BUTTON_10_2_temp_order2 = "Оформить заказ"

BUTTON_11_1_temp_order3 = "Подтвердить заказ"

BUTTON_12_1_DeliveryOrder = "Вернуться в меню"
BUTTON_12_2_DeliveryOrder = "Завтра"

BUTTON_12_1_Finish_order = "Вернуться в меню"
BUTTON_12_2_Finish_order = "Сделать ещё заказ"

BUTTON_13_1_Sent_Order_to_reply = "Подтвердить заказ"


def get_Keyboard_Sent_Order_to_reply():
    keyboard = [
        [
            KeyboardButton(BUTTON_13_1_Sent_Order_to_reply),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        one_time_keyboard=True,
        resize_keyboard=True,
        row_width=2,
    )


def get_Keyboard_Finish_order():
    keyboard = [
        [
            KeyboardButton(BUTTON_12_1_Finish_order),
        ],
        [
            KeyboardButton(BUTTON_12_2_Finish_order),
        ],

    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        one_time_keyboard=True,
        resize_keyboard=True,
        row_width=2,
    )


def get_Keyboard_DeliveryOrder(data1: str, data2: str):
    keyboard = [
        [
            KeyboardButton(BUTTON_12_1_DeliveryOrder),
        ],
        [
            KeyboardButton(BUTTON_12_2_DeliveryOrder),
        ],
        [
            KeyboardButton(data1),
        ],
        [
            KeyboardButton(data2),
        ],

    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        one_time_keyboard=True,
        resize_keyboard=True,
        row_width=2,
    )


def get_Keyboard_ZapProf():
    keyboard = [
        [
            KeyboardButton(BUTTON_1_1_ZapProf),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        one_time_keyboard=True,
        resize_keyboard=True,
        row_width=2,
    )


def get_Keyboard_orders():
    keyboard = [
        [
            KeyboardButton(BUTTON_7_1_New_Order),
        ],
        [
            KeyboardButton(BUTTON_7_2_New_Order),
        ],
        [
            KeyboardButton(BUTTON_7_3_New_Order),
        ],
        [
            KeyboardButton(BUTTON_7_4_New_Order),
        ],

    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        one_time_keyboard=True,
        resize_keyboard=True,
        row_width=2,
    )


def get_Keyboard_order():
    keyboard = [
        [
            KeyboardButton(BUTTON_8_1_Order),
        ],
        [
            KeyboardButton(BUTTON_8_2_Order),
        ]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        one_time_keyboard=True,
        resize_keyboard=True,
        row_width=2,
    )


def get_Keyboard_Button_Edit():
    keyboard = [
        [
            KeyboardButton(BUTTON_6_1_Edit),
            KeyboardButton(BUTTON_6_2_Edit),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        one_time_keyboard=True,
        resize_keyboard=True,
        row_width=2,
    )


def get_Keyboard_TypeFace():
    keyboard = [
        [
            KeyboardButton(BUTTON_2_1_YurFace),
            KeyboardButton(BUTTON_2_2_FizFace),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        one_time_keyboard=True,
        resize_keyboard=True,
        row_width=2,
    )


def get_Keyboard_City():
    keyboard = [
        [
            KeyboardButton(BUTTON_3_1_City),
            KeyboardButton(BUTTON_3_2_City),
        ],
        [
            KeyboardButton(BUTTON_3_3_City),
            KeyboardButton(BUTTON_3_4_City),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        one_time_keyboard=True,
        resize_keyboard=True,
        row_width=2,
    )


def get_Keyboard_SendNameProf():
    keyboard = [
        [
            KeyboardButton(BUTTON_4_1_SendNameProf),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        one_time_keyboard=True,
        resize_keyboard=True,
        row_width=2,
    )


def get_Keyboard_temp_order():
    keyboard = [
        [
            KeyboardButton(BUTTON_9_1_temp_order),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        one_time_keyboard=True,
        resize_keyboard=True,
        row_width=2,
    )


def get_Keyboard_temp_order2():
    keyboard = [
        [
            KeyboardButton(BUTTON_10_1_temp_order2),
        ],
        [
            KeyboardButton(BUTTON_10_2_temp_order2),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        one_time_keyboard=True,
        resize_keyboard=True,
        row_width=2,
    )


def get_Keyboard_temp_order3():
    keyboard = [
        [
            KeyboardButton(BUTTON_11_1_temp_order3),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        one_time_keyboard=True,
        resize_keyboard=True,
        row_width=2,
    )


def get_Keyboard_ZapProfCommands(flag):
    if flag == "1":
        keyboard = [
            [
                KeyboardButton(BUTTON_5_2_NewOrder),
                KeyboardButton(BUTTON_5_3_ReplyOldOrder),
            ],
            [
                KeyboardButton(BUTTON_5_1_EditProf),
            ],
        ]
    else:
        keyboard = [
            [
                KeyboardButton(BUTTON_1_1_ZapProf),
            ],
        ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        one_time_keyboard=True,
        resize_keyboard=True,
        row_width=2,
    )
