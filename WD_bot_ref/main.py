from datetime import timedelta
from logging import getLogger, Logger

import config
from buttons import get_Keyboard_DeliveryOrder, get_Keyboard_Finish_order, get_Keyboard_Sent_Order_to_reply, \
    get_Keyboard_SendNameProf, get_Keyboard_ZapProfCommands, get_Keyboard_Button_Edit, \
    get_Keyboard_ZapProf, get_Keyboard_orders, get_Keyboard_TypeFace, get_Keyboard_City, \
    get_Keyboard_order, get_Keyboard_temp_order, get_Keyboard_temp_order2, get_Keyboard_temp_order3
from config import TG_API_URL, TG_TOKEN, CHAT_ID_BUGS, CHAT_ID_COMPANY, CHAT_ID_LOGS, HashTagFindLogsINFO, \
    HashTagFindLogsWARN, HashTagFindORDER
from telegram import Bot, ReplyKeyboardRemove, Update
from telegram.ext import CommandHandler, ConversationHandler, Filters, MessageHandler, Updater
from telegram.utils.request import Request
from validators import *
from validators import validate_count, validate_date

logger: Logger = getLogger(__name__)

flag = None


# Функция отправки в лог чат
def logTOchat(bot: Bot, update: Update, text: str):
    bot.send_message(
        chat_id=CHAT_ID_LOGS,
        text=text,
    )


# Декоратор для лога
def debug_requests(f):
    # Декоратор для обработки событий от телеграма
    #
    def inner(*args, **kwargs):
        try:
            logger.info("Обращение в функцию {}".format(f.__name__))
            bot = args[0]
            bot.send_message(
                chat_id=CHAT_ID_LOGS,
                text=f"{HashTagFindLogsINFO}" +
                     "\n==============================================\n" \
                     "Обращение в функцию {}\n\n".format(f.__name__),
            )
            return f(*args, **kwargs)
        except Exception:
            update = args[1]
            bot = args[0]
            bot.send_message(
                chat_id=CHAT_ID_BUGS,
                text=f"{HashTagFindLogsWARN}" + "Ошибка в обработчике {1} Exception = {1}".format(f.__name__,Exception),
            )
            logger.exception("Ошибка в обработчике {}".format(f.__name__))
            raise

    return inner


TYPE_FACE, NAME, \
COMPANY, ADDRESS, \
ADDRESS_CITY, MOB_PHONE, \
MENU, NEW_ORDER, \
EDIT_PROFILE, ORDERS, \
TEMPORARY_ENTER_QUANTITY, TEMPORARY_ENTER_QUANTITY2, \
CHECKOUT, CHECKOUT2, \
FINISH_ORDER = range(15)


@debug_requests
def do_start(bot: Bot, update: Update):
    upTextL = update.message.text.lower()
    chat_id = update.message.chat_id
    name = update.message.from_user.first_name.lower()
    # Логирование
    # logger.info("do_start START - text =" + upTextL + "; chat_id=" + str(
    #     update.message.chat_id) + "; name= " + name)
    logTOchat(bot=bot, update=update,
              text=f"{HashTagFindLogsINFO} - do_start START - text =" + upTextL + "; chat_id=" + str(
                  update.message.chat_id) + "; name= " + name)
    # Основная логика
    bot.send_message(
        chat_id=chat_id,
        text="Здраствуйте! Вас приветствует ассистент заказа воды \"Просто вода\". Для начала работы, пожайлуста "
             "нажмите \'Заполнить профиль\'",
        reply_markup=get_Keyboard_ZapProf(),
    )


@debug_requests
def do_Help(bot: Bot, update: Update):
    upTextL = update.message.text.lower()
    chat_id = update.message.chat_id
    name = update.message.from_user.first_name.lower()
    # Логирование
        # logger.info("do_Help START - text =" + upTextL + "; chat_id=" + str(
        #     update.message.chat_id) + "; name= " + name)
    logTOchat(bot=bot, update=update,
              text=f"{HashTagFindLogsINFO} - do_Help START - text =" + upTextL + "; chat_id=" + str(
                  update.message.chat_id) + "; name= " + name)
    # Основная логика
    bot.send_message(
        chat_id=chat_id,
        text="Здраствуйте! Вас приветствует ассистент заказа воды \"Просто вода\". Для начала работы, пожайлуста " +
             "введите команду /start",
        reply_markup=get_Keyboard_ZapProf(),
    )


@debug_requests
def start_reg(bot: Bot, update: Update):
    upTextL = update.message.text.lower()
    chat_id = update.message.chat_id
    name = update.message.from_user.first_name.lower()
    # Логирование
        # logger.info("hand_checkout2 - text =" + upTextL + "; chat_id=" + str(
        #     update.message.chat_id) + "; name= " + name)
    logTOchat(bot=bot, update=update,
              text=f"{HashTagFindLogsINFO} - hand_checkout2 - text =" + upTextL + "; chat_id=" + str(
                  update.message.chat_id) + "; name= " + name)
    # Основная логика
    if upTextL == 'заполнить профиль':
        bot.send_message(
            chat_id=chat_id,
            text="Выберите, вы кто:",
            reply_markup=get_Keyboard_TypeFace(),
        )
        return TYPE_FACE
    else:
        return MENU


@debug_requests
def hend_type_face(bot: Bot, update: Update, user_data: dict):
    upTextL = update.message.text.lower()
    chat_id = update.message.chat_id
    name = update.message.from_user.first_name.lower()
    # Логирование
    logger.info("hend_type_face - text =" + upTextL + "; chat_id=" + str(
        update.message.chat_id) + "; name= " + name)
    logTOchat(bot=bot, update=update,
              text=f"{HashTagFindLogsINFO} - hend_type_face - text =" + upTextL + "; chat_id=" + str(
                  update.message.chat_id) + "; name= " + name)
    # Проверка старта
    if upTextL == 'заполнить профиль':
        bot.send_message(
            chat_id=chat_id,
            text="Выберите, вы кто:",
            reply_markup=get_Keyboard_TypeFace(),
        )
        return TYPE_FACE
    # Основная логика
    # Проверка
    if upTextL != 'юр.лицо' and upTextL != 'физ.лицо':
        bot.send_message(
            chat_id=chat_id,
            text="Выберите, вы кто:",
            reply_markup=get_Keyboard_TypeFace(),
        )
        return TYPE_FACE
    else:
        # Получить тип лица (Физ и Юр)
        user_data[TYPE_FACE] = upTextL

        # Разветвление Спрашиваем юзера
        if upTextL == 'юр.лицо':
            bot.send_message(
                chat_id=chat_id,
                text="Напишите название компании, пожалуйста",
                reply_markup=ReplyKeyboardRemove(),
            )
            return COMPANY
        elif upTextL == 'физ.лицо':
            bot.send_message(
                chat_id=chat_id,
                text="Напишите как к вам обращаться или нажмите на кнопку \"Отправить имя профиля\"",
                reply_markup=get_Keyboard_SendNameProf(),
            )
            return NAME
        else:
            return TYPE_FACE


@debug_requests
def hend_name(bot: Bot, update: Update, user_data: dict):
    upTextL = update.message.text.lower()
    name = update.effective_chat.first_name.lower()
    chat_id = update.message.chat_id
    chat_id = update.message.chat_id
    name = update.message.from_user.first_name.lower()
    # Логирование
        # logger.info("hend_name - text =" + upTextL + "; chat_id=" + str(
        #     update.message.chat_id) + "; name= " + name)
    logTOchat(bot=bot, update=update,
              text=f"{HashTagFindLogsINFO} - hend_name - text =" + upTextL + "; chat_id=" + str(
                  update.message.chat_id) + "; name= " + name)
    # Проверка старта
    if upTextL == 'заполнить профиль':
        bot.send_message(
            chat_id=chat_id,
            text="Выберите, вы кто:",
            reply_markup=get_Keyboard_TypeFace(),
        )
        return TYPE_FACE
    # Основная логика
    # Проверка
    if upTextL == 'отправить имя профиля':
        upTextL = update.effective_chat.first_name.lower()

    # Получить имя
    user_data[NAME] = upTextL

    # Спрашиваем юзера
    bot.send_message(
        chat_id=chat_id,
        text="Выберите ваш город:",
        reply_markup=get_Keyboard_City(),
    )
    return ADDRESS_CITY


@debug_requests
def hend_company(bot: Bot, update: Update, user_data: dict):
    upTextL = update.message.text.lower()
    chat_id = update.message.chat_id
    name = update.message.from_user.first_name.lower()
    # Логирование
    logger.info("hend_company - text =" + upTextL + "; chat_id=" + str(
        update.message.chat_id) + "; name= " + name)
    logTOchat(bot=bot, update=update,
              text=f"{HashTagFindLogsINFO} - hend_company - text =" + upTextL + "; chat_id=" + str(
                  update.message.chat_id) + "; name= " + name)
    # Проверка старта
    if upTextL == 'заполнить профиль':
        bot.send_message(
            chat_id=chat_id,
            text="Выберите, вы кто:",
            reply_markup=get_Keyboard_TypeFace(),
        )
        return TYPE_FACE
    upTextL = update.message.text.lower()
    chat_id = update.message.chat_id
    name = update.message.from_user.first_name.lower()
    # Логирование
    # Получение сообщения
    # Получить тип лица (Физ и Юр)
    user_data[COMPANY] = update.message.text
    # Спрашиваем юзера
    bot.send_message(
        chat_id=chat_id,
        text="Напишите как к вам обращаться или нажмите на кнопку \"Отправить имя профиля\"",
        reply_markup=get_Keyboard_SendNameProf(),
    )
    return NAME


@debug_requests
def hend_address(bot: Bot, update: Update, user_data: dict):
    upTextL = update.message.text.lower()
    chat_id = update.message.chat_id
    name = update.message.from_user.first_name.lower()
    # Логирование
    logger.info("hend_address - text =" + upTextL + "; chat_id=" + str(
        update.message.chat_id) + "; name= " + name)
    logTOchat(bot=bot, update=update,
              text=f"{HashTagFindLogsINFO} - hend_address - text =" + upTextL + "; chat_id=" + str(
                  update.message.chat_id) + "; name= " + name)
    # Проверка старта

    if upTextL == 'заполнить профиль':
        bot.send_message(
            chat_id=chat_id,
            text="Выберите, вы кто:",
            reply_markup=get_Keyboard_TypeFace(),
        )
        return TYPE_FACE
    # Основная логика
    # Получить город
    user_data[ADDRESS] = upTextL
    # Спрашиваем юзера
    bot.send_message(
        chat_id=chat_id,
        text="Введите ваш номер телефона:",
        reply_markup=ReplyKeyboardRemove(),
    )
    return MOB_PHONE


@debug_requests
def hend_address_city(bot: Bot, update: Update, user_data: dict):
    global flag
    upTextL = update.message.text.lower()
    chat_id = update.message.chat_id
    name = update.message.from_user.first_name.lower()
    # Логирование
        # logger.info("hend_address_city - text =" + upTextL + "; chat_id=" + str(
        #     update.message.chat_id) + "; name= " + name)
    logTOchat(bot=bot, update=update,
              text=f"{HashTagFindLogsINFO} - hend_address_city - text =" + upTextL + "; chat_id=" + str(
                  update.message.chat_id) + "; name= " + name)
    # Проверка старта
    if upTextL == 'заполнить профиль':
        bot.send_message(
            chat_id=chat_id,
            text="Выберите, вы кто:",
            reply_markup=get_Keyboard_TypeFace(),
        )
        return TYPE_FACE
    # Основная логика
    # Проверка
    city = [
        'москва',
        'калуга',
        'серпухов',
        'орехово-зуево'
    ]
    for citi in city:
        if citi == upTextL:
            flag = True
            break
    if not flag:
        bot.send_message(
            chat_id=chat_id,
            text="Выберите ваш город:",
            reply_markup=get_Keyboard_City(),
        )
        return ADDRESS_CITY
    # Получить город
    user_data[ADDRESS_CITY] = upTextL
    # Спрашиваем юзера
    bot.send_message(
        chat_id=chat_id,
        text="Введите адрес для доставки. Укажите улицу, номер и корпус дома, номер квартиры:",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ADDRESS


@debug_requests
def hend_mob_phone(bot: Bot, update: Update, user_data: dict):
    upTextL = update.message.text.lower()
    chat_id = update.message.chat_id
    name = update.message.from_user.first_name.lower()
    # Логирование
    # logger.info("hend_mob_phone - text =" + upTextL + "; chat_id=" + str(
    #     update.message.chat_id) + "; name= " + name)
    logTOchat(bot=bot, update=update,
              text=f"{HashTagFindLogsINFO} - hend_mob_phone - text =" + upTextL + "; chat_id=" + str(
                  update.message.chat_id) + "; name= " + name)
    # Проверка старта
    if upTextL == 'заполнить профиль':
        bot.send_message(
            chat_id=chat_id,
            text="Выберите, вы кто:",
            reply_markup=get_Keyboard_TypeFace(),
        )
        return TYPE_FACE
    # Основная логика
    # Получить адрес
    user_data[MOB_PHONE] = upTextL
    # Создание листа заказа
    user_data[ORDERS] = list()
    user_data[ORDERS].insert(0, 0)
    user_data[ORDERS].insert(1, 0)
    user_data[ORDERS].insert(2, 0)
    user_data[ORDERS].insert(3, 0)
    # Спрашиваем юзера
    bot.send_message(
        chat_id=chat_id,
        text=f"Спасибо! Теперь Вы можете приступить к покупкам. Не забудьте посетить наш сайт {config.url_site}.",
        reply_markup=get_Keyboard_ZapProfCommands('1'),
    )
    if user_data[TYPE_FACE] == 'физ.лицо':
        user_data[COMPANY] = None
    logger.info('user_data: %s', user_data)
    logTOchat(bot=bot, update=update, text=f'{HashTagFindLogsINFO} - user_data: {user_data}')
    return MENU


@debug_requests
def cancel_handler(bot: Bot, update: Update, user_data: dict):
    """ Отменить весь процесс диалога. Данные будут утеряны
    """
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Отмена. Для начала с нуля нажмите /start',
    )
    return ConversationHandler.END


@debug_requests
def hand_select_menu(bot: Bot, update: Update, user_data: dict):
    upTextL = update.message.text.lower()
    chat_id = update.message.chat_id
    name = update.message.from_user.first_name.lower()
    # Логирование
        # logger.info("hand_select_menu - text =" + upTextL + "; chat_id=" + str(
        #     update.message.chat_id) + "; name= " + name)
    logTOchat(bot=bot, update=update,
              text=" #infoWaterDelivery - hand_select_menu - text =" + upTextL + "; chat_id=" + str(
                  update.message.chat_id) + "; name= " + name)
    # Проверка старта
    if upTextL == 'заполнить профиль':
        bot.send_message(
            chat_id=chat_id,
            text="Выберите, вы кто:",
            reply_markup=get_Keyboard_TypeFace(),
        )
        return TYPE_FACE
    # Основная логика
    # получение текста
    if upTextL == 'новый заказ':
        bot.send_message(
            chat_id=chat_id,
            text=f'Наш магазин предлагает Вам широкий ассортимент питьевой бутилированной воды. Хотите больше товаров? '
                 f'Посетите наш сайт {config.url_site}',
            reply_markup=get_Keyboard_orders()
        )
        return NEW_ORDER
    elif upTextL == 'повторить прошлый заказ':
        # Проверка на наличие заказов
        flag = None
        if (user_data[ORDERS][0] == 0 or user_data[ORDERS][0] < 2) \
                and (user_data[ORDERS][1] == 0 or user_data[ORDERS][1] < 6) \
                and (user_data[ORDERS][2] == 0 or user_data[ORDERS][2] < 1):
            flag = False
        else:
            flag = True
        # Или ругаем юзера
        # Или выводим сообщ с данными
        if not flag:
            # Выводим сообщение о том что юзер не делал заказы
            bot.send_message(
                chat_id=chat_id,
                text="Вы ранее не заказывали у нас доставку воды. Сделайте новый заказ и далее вы сможете повторять новый заказ",
                reply_markup=get_Keyboard_ZapProfCommands('1'),
            )
            return MENU
        else:
            # Выводим сообщение о том что юзер делал заказы и бот повторил заказ
            order_text = 'Ваш заказ содержит:\n\n'
            if user_data[ORDERS][0] > 1:
                order_text = order_text + f'\n  - 19 литровая бутыль ({user_data[ORDERS][0]} шт.)'
            if user_data[ORDERS][1] > 5:
                order_text = order_text + f'\n  - 6 литровая бутыль ({user_data[ORDERS][1]} шт.)'
            if user_data[ORDERS][2] > 0:
                order_text = order_text + f'\n  - Механическая помпа ({user_data[ORDERS][2]} шт.)'
            sum = user_data[ORDERS][0] * 270 + user_data[ORDERS][1] * 100 + user_data[ORDERS][2] * 799
            order_text = order_text + f'\n\nОбщая стоимость заказа: {user_data[ORDERS][3]} руб.'
            bot.send_message(
                chat_id=chat_id,
                text=order_text,
                reply_markup=get_Keyboard_Sent_Order_to_reply(),
            )
            return CHECKOUT
    elif upTextL == 'изменить профиль':
        if user_data[TYPE_FACE] == 'юр.лицо':
            bot.send_message(
                chat_id=chat_id,
                text=f'       Ваш профиль:\n\n' +
                     f'- Имя: {str(user_data[NAME])}\n' +
                     f'- Компания: {str(user_data[COMPANY])}\n' +
                     f'- Город: {str(user_data[ADDRESS_CITY])}\n' +
                     f'- Адрес: {str(user_data[ADDRESS])}\n' +
                     f'- Номер телефона: {str(user_data[MOB_PHONE])}',
                reply_markup=get_Keyboard_Button_Edit()
            )
        else:
            bot.send_message(
                chat_id=chat_id,
                text=f'       Ваш профиль:\n\n' +
                     f'- Имя: {str(user_data[NAME])}\n' +
                     f'- Город: {str(user_data[ADDRESS_CITY])}\n' +
                     f'- Адрес: {str(user_data[ADDRESS])}\n' +
                     f'- Номер телефона: {str(user_data[MOB_PHONE])}',
                reply_markup=get_Keyboard_Button_Edit()
            )
        return EDIT_PROFILE


def order_text(cost: int, count: int):
    return f"\n\nСтоимость: {cost} за штуку \n\n  - Артезианская\n  - Без накипи \n\n\n Минимальное кол-во для заказа {count} шт."


@debug_requests
def hand_new_order(bot: Bot, update: Update, user_data: dict):
    upTextL = update.message.text.lower()
    chat_id = update.message.chat_id
    name = update.message.from_user.first_name.lower()
    # Логирование
        # logger.info("hand_new_order - text =" + upTextL + "; chat_id=" + str(
        #     update.message.chat_id) + "; name= " + name)
    logTOchat(bot=bot, update=update,
              text=f"{HashTagFindLogsINFO} - hand_new_order - text =" + upTextL + "; chat_id=" + str(
                  update.message.chat_id) + "; name= " + name)
    # Проверка старта
    if upTextL == 'заполнить профиль':
        bot.send_message(
            chat_id=chat_id,
            text="Выберите, вы кто:",
            reply_markup=get_Keyboard_TypeFace(),
        )
        return TYPE_FACE
    # Основная логика
    if upTextL == "вернуться назад":
        bot.send_message(
            chat_id=chat_id,
            text=f'Наш магазин предлагает Вам широкий ассортимент питьевой бутилированной воды. Хотите больше товаров? '
                 f'Посетите наш сайт {config.url_site}',
            reply_markup=get_Keyboard_ZapProfCommands('1')
        )
        return MENU
    elif upTextL == "19 литровая бутыль воды":
        bot.send_message(
            chat_id=chat_id,
            text='19 литровая бутыль c водой' + order_text(270, 2),
            reply_markup=get_Keyboard_order()
        )
        user_data[ORDERS].pop(0)
        user_data[ORDERS].insert(0, -1)
        return TEMPORARY_ENTER_QUANTITY
    elif upTextL == "6 литровая бутыль воды":
        bot.send_message(
            chat_id=chat_id,
            text='6 литровая бутыль c водой' + order_text(100, 6),
            reply_markup=get_Keyboard_order()
        )
        user_data[ORDERS].pop(1)
        user_data[ORDERS].insert(1, -1)
        return TEMPORARY_ENTER_QUANTITY
    elif upTextL == "ручная помпа":
        bot.send_message(
            chat_id=chat_id,
            text='Помпа для воды механическая "АЕЛ"(AEL)\nПредназначена для 19 литровой бутыли с водой\n\n\nСтоимость: 799 рублей',
            reply_markup=get_Keyboard_order()
        )
        user_data[ORDERS].pop(2)
        user_data[ORDERS].insert(2, -1)
        return TEMPORARY_ENTER_QUANTITY
    elif upTextL == 'cделать ещё заказ':
        bot.send_message(
            chat_id=chat_id,
            text=f'Наш магазин предлагает Вам широкий ассортимент питьевой бутилированной воды. Хотите больше товаров? '
                 f'Посетите наш сайт {config.url_site}',
            reply_markup=get_Keyboard_orders()
        )
        return NEW_ORDER


@debug_requests
def hand_edit_profile(bot: Bot, update: Update, user_data: dict):
    upTextL = update.message.text.lower()
    chat_id = update.message.chat_id
    name = update.message.from_user.first_name.lower()
    # Логирование
        # logger.info("hend_type_face - text =" + upTextL + "; chat_id=" + str(
        #     update.message.chat_id) + "; name= " + name)
    logTOchat(bot=bot, update=update,
              text=f"{HashTagFindLogsINFO} - hend_type_face - text =" + upTextL + "; chat_id=" + str(
                  update.message.chat_id) + "; name= " + name)
    # Проверка старта
    if upTextL == 'заполнить профиль':
        bot.send_message(
            chat_id=chat_id,
            text="Выберите, вы кто:",
            reply_markup=get_Keyboard_TypeFace(),
        )
        return TYPE_FACE
    # Основная логика
    if upTextL == 'изменить':
        bot.send_message(
            chat_id=chat_id,
            text="Выберите, вы кто:",
            reply_markup=get_Keyboard_TypeFace(),
        )
        return TYPE_FACE
    elif upTextL == 'вернуться обратно':
        bot.send_message(
            chat_id=chat_id,
            text='Сделайте ваш заказ:',
            reply_markup=get_Keyboard_ZapProfCommands('1')
        )
        return MENU
    else:
        bot.send_message(
            chat_id=chat_id,
            text='Нажмите на кнопки снизу:',
            reply_markup=get_Keyboard_Button_Edit()
        )
        return NEW_ORDER


@debug_requests
def hand_temorary_enter_quanity(bot: Bot, update: Update, user_data: dict):
    upTextL = update.message.text.lower()
    chat_id = update.message.chat_id
    name = update.message.from_user.first_name.lower()
    # Логирование
    # logger.info("hand_temorary_enter_quanity - text =" + upTextL)
    logTOchat(bot=bot, update=update,
              text=f"{HashTagFindLogsINFO} - hand_temorary_enter_quanity - text =" + upTextL)
    # Проверка старта
    if upTextL == 'заполнить профиль':
        bot.send_message(
            chat_id=chat_id,
            text="Выберите, вы кто:",
            reply_markup=get_Keyboard_TypeFace(),
        )
        return TYPE_FACE
    # Основная логика
    if upTextL == 'отменить':
        bot.send_message(
            chat_id=chat_id,
            text=f'Наш магазин предлагает Вам широкий ассортимент питьевой бутилированной воды. Хотите больше товаров? '
                 f'Посетите наш сайт {config.url_site}',
            reply_markup=get_Keyboard_orders()
        )
        return NEW_ORDER
    elif upTextL == 'ввести кол-во':
        if user_data[ORDERS][0] == -1:
            min = 2
        elif user_data[ORDERS][1] == -1:
            min = 6
        elif user_data[ORDERS][2] == -1:
            min = 1
        bot.send_message(
            chat_id=chat_id,
            text=f'Введите кол-во товаров числом,\nМинимальное кол-во {min} шт.',
            reply_markup=ReplyKeyboardRemove()
        )
        return TEMPORARY_ENTER_QUANTITY2
    elif upTextL == 'оформить заказ':
        order_text = 'Ваш заказ содержит:\n\n'
        if user_data[ORDERS][0] > 1:
            order_text = order_text + f'\n  - 19 литровая бутыль ({user_data[ORDERS][0]} шт.)'
        if user_data[ORDERS][1] > 5:
            order_text = order_text + f'\n  - 6 литровая бутыль ({user_data[ORDERS][1]} шт.)'
        if user_data[ORDERS][2] > 0:
            order_text = order_text + f'\n  - Механическая помпа ({user_data[ORDERS][2]} шт.)'
        sum = user_data[ORDERS][0] * 270 + user_data[ORDERS][1] * 100 + user_data[ORDERS][2] * 799
        user_data[ORDERS].pop(3)
        user_data[ORDERS].insert(3, sum)
        order_text = order_text + f'\n\nОбщая стоимость заказа: {user_data[ORDERS][3]} руб.'
        bot.send_message(
            chat_id=chat_id,
            text=order_text,
            reply_markup=get_Keyboard_temp_order3()
        )
        return CHECKOUT
    elif upTextL == 'добавить ещё товар':
        bot.send_message(
            chat_id=chat_id,
            text=f'Наш магазин предлагает Вам широкий ассортимент питьевой бутилированной воды. Хотите больше товаров? '
                 f'Посетите наш сайт {config.url_site}',
            reply_markup=get_Keyboard_orders()
        )
        return NEW_ORDER


@debug_requests
def hand_enter_quanity2(bot: Bot, update: Update, user_data: dict):
    upTextL = update.message.text.lower()
    chat_id = update.message.chat_id
    name = update.message.from_user.first_name.lower()
    # Логирование
        # logger.info("hand_enter_quanity2 - text =" + upTextL + "; chat_id=" + str(
        #     update.message.chat_id) + "; name= " + name)
    logTOchat(bot=bot, update=update,
              text=f"{HashTagFindLogsINFO} - hand_enter_quanity2 - text =" + upTextL + "; chat_id=" + str(
                  update.message.chat_id) + "; name= " + name)
    # Основная логика
    if user_data[ORDERS][0] == -1:
        min = 2
    elif user_data[ORDERS][1] == -1:
        min = 6
    elif user_data[ORDERS][2] == -1:
        min = 1
    count = validate_count(text=upTextL, min=min)
    if count is None:
        bot.send_message(
            chat_id=chat_id,
            text='Введите кол-во товаров числом',
            reply_markup=ReplyKeyboardRemove()
        )
        return TEMPORARY_ENTER_QUANTITY2
    elif count < min:
        bot.send_message(
            chat_id=chat_id,
            text=f'Вы ввели {count} штук. Минимальное кол-во {min} шт. для этого товара. Введите повторно, пожалуйста кол-во товара или нажмите отменить',
            reply_markup=get_Keyboard_temp_order()
        )
        return TEMPORARY_ENTER_QUANTITY2
    else:
        if user_data[ORDERS][0] == -1:
            user_data[ORDERS][0] = count
        elif user_data[ORDERS][1] == -1:
            user_data[ORDERS][1] = count
        elif user_data[ORDERS][2] == -1:
            user_data[ORDERS][2] = count
        bot.send_message(
            chat_id=chat_id,
            text=f'Вы выбрали {count} товар(ов).',
            reply_markup=get_Keyboard_temp_order2()
        )
        return TEMPORARY_ENTER_QUANTITY


@debug_requests
def hand_checkout(bot: Bot, update: Update, user_data: dict):
    upTextL = update.message.text.lower()
    chat_id = update.message.chat_id
    name = update.message.from_user.first_name.lower()
    # Логирование
    # logger.info("hand_checkout - text =" + upTextL)
    logTOchat(bot=bot, update=update,
              text=f"{HashTagFindLogsINFO} - hand_checkout - text =" + upTextL)
    # Основная логика
    after_tomorrow = datetime.now() + timedelta(1)
    after_the_day_after_tomorrow = datetime.now() + timedelta(2)
    if upTextL == 'подтвердить заказ':
        bot.send_message(
            chat_id=chat_id,
            text=f'Пожайлуста, выберите, когда вам доставить заказ',
            reply_markup=get_Keyboard_DeliveryOrder(
                data1="{}.{}.{}".format(after_tomorrow.day, after_tomorrow.month, after_tomorrow.year),
                data2="{}.{}.{}".format(after_the_day_after_tomorrow.day, after_the_day_after_tomorrow.month,
                                        after_the_day_after_tomorrow.year),
            )
        )
        return CHECKOUT2


@debug_requests
def hand_checkout2(bot: Bot, update: Update, user_data: dict):
    upTextL = update.message.text.lower()
    chat_id = update.message.chat_id
    name = update.message.from_user.first_name.lower()
    # Логирование
        #     logger.info("hand_checkout2 - text =" + upTextL + "; chat_id=" + str(
        #         update.message.chat_id) + "; name= " + name)
    logTOchat(bot=bot, update=update,
              text=f"{HashTagFindLogsINFO} - hand_checkout2 - text =" + upTextL + "; chat_id=" + str(
                  update.message.chat_id) + "; name= " + name)
    # Основная логика
    vdata = validate_date(upTextL)
    if upTextL == 'вернуться в меню':
        return NEW_ORDER
    elif upTextL == 'завтра':
        now = datetime.now()
        user_data[ORDERS].insert(4, "{}.{}.{}".format(now.day, now.month, now.year))
        order_text = 'Ваш заказ оформлен:\n\n'
        if user_data[ORDERS][0] > 1:
            order_text = order_text + f'\n  - 19 литровая бутыль ({user_data[ORDERS][0]} шт.)'
        if user_data[ORDERS][1] > 5:
            order_text = order_text + f'\n  - 6 литровая бутыль ({user_data[ORDERS][1]} шт.)'
        if user_data[ORDERS][2] > 0:
            order_text = order_text + f'\n  - Механическая помпа ({user_data[ORDERS][2]} шт.)'
        order_text = order_text + f'\n\nОбщая стоимость заказа:  {user_data[ORDERS][3]} руб.' + \
                     f'Заказ будет доставлен {user_data[ORDERS][4]}' + \
                     '\n\nОплата наличными курьеру'
        bot.send_message(
            chat_id=chat_id,
            text=order_text,
            reply_markup=get_Keyboard_Finish_order(),
        )
        # Отправка данных в компанию
        order_text = "\n\n----------------------------------------------------------------------------"
        order_text: str = order_text + "\n         Заказ состоит из: "
        if user_data[ORDERS][0] > 1:
            order_text = order_text + f'\n  - 19 литровая бутыль ({user_data[ORDERS][0]} шт.)'
        if user_data[ORDERS][1] > 5:
            order_text = order_text + f'\n  - 6 литровая бутыль ({user_data[ORDERS][1]} шт.)'
        if user_data[ORDERS][2] > 0:
            order_text = order_text + f'\n  - Механическая помпа ({user_data[ORDERS][2]} шт.)'
        order_text = order_text + "\n\n----------------------------------------------------------------------------"
        order_text = order_text + f"\n   Заказ должен быть доставлен: {user_data[ORDERS][4]}"
        order_text = order_text + "\n\n----------------------------------------------------------------------------"

        order_text = order_text + f'\nСумма: {user_data[ORDERS][3]} руб.'
        bot.send_message(
            chat_id=CHAT_ID_COMPANY,
            text=f'{HashTagFindORDER}\n\n  Поступил заказ:\n' \
                 f'\nТип лица: {user_data[TYPE_FACE]}' \
                 f'\nКомпания: {user_data[COMPANY]}'
                 f'\nИмя: {user_data[NAME]}' \
                 f'\nГород: {user_data[ADDRESS_CITY]}' \
                 f'\nАдрес: {user_data[ADDRESS]}' \
                 f'\nНомер мобильного телефона: {user_data[MOB_PHONE]}' + order_text,
        )

        return FINISH_ORDER
    elif vdata is not None:
        user_data[ORDERS].insert(4, upTextL)
        order_text = 'Ваш заказ оформлен:\n\n'
        if user_data[ORDERS][0] > 1:
            order_text = order_text + f'\n  - 19 литровая бутыль ({user_data[ORDERS][0]} шт.)'
        if user_data[ORDERS][1] > 5:
            order_text = order_text + f'\n  - 6 литровая бутыль ({user_data[ORDERS][1]} шт.)'
        if user_data[ORDERS][2] > 0:
            order_text = order_text + f'\n  - Механическая помпа ({user_data[ORDERS][2]} шт.)'
        order_text = order_text + f'\n\nОбщая стоимость заказа:  {user_data[ORDERS][3]} руб.' + \
                     f'Заказ будет доставлен {user_data[ORDERS][4]}' + \
                     '\n\nОплата наличными курьеру'
        bot.send_message(
            chat_id=chat_id,
            text=order_text,
            reply_markup=get_Keyboard_Finish_order(),
        )
        # Отправка данных в компанию
        order_text = "\n\n----------------------------------------------------------------------------"
        order_text: str = order_text + "\n         Заказ состоит из: "
        if user_data[ORDERS][0] > 1:
            order_text = order_text + f'\n  - 19 литровая бутыль ({user_data[ORDERS][0]} шт.)'
        if user_data[ORDERS][1] > 5:
            order_text = order_text + f'\n  - 6 литровая бутыль ({user_data[ORDERS][1]} шт.)'
        if user_data[ORDERS][2] > 0:
            order_text = order_text + f'\n  - Механическая помпа ({user_data[ORDERS][2]} шт.)'
        order_text = order_text + "\n\n----------------------------------------------------------------------------"
        order_text = order_text + f"\n   Заказ должен быть доставлен: {user_data[ORDERS][4]}"
        order_text = order_text + "\n\n----------------------------------------------------------------------------"

        order_text = order_text + f'\nСумма: {user_data[ORDERS][3]} руб.'
        bot.send_message(
            chat_id=CHAT_ID_COMPANY,
            text=f'{HashTagFindORDER}\n\n  Поступил заказ:\n' \
                 f'\nТип лица: {user_data[TYPE_FACE]}' \
                 f'\nКомпания: {user_data[COMPANY]}'
                 f'\nИмя: {user_data[NAME]}' \
                 f'\nГород: {user_data[ADDRESS_CITY]}' \
                 f'\nАдрес: {user_data[ADDRESS]}' \
                 f'\nНомер мобильного телефона: {user_data[MOB_PHONE]}' + order_text,
        )

        return FINISH_ORDER
    else:
        after_tomorrow = datetime.now() + timedelta(1)
        after_the_day_after_tomorrow = datetime.now() + timedelta(2)
        if upTextL == 'подтвердить заказ':
            bot.send_message(
                chat_id=chat_id,
                text=f'Пожайлуста, выберите корректное время, когда вам доставить заказ',
                reply_markup=get_Keyboard_DeliveryOrder(
                    data1="{}.{}.{}".format(after_tomorrow.day, after_tomorrow.month, after_tomorrow.year),
                    data2="{}.{}.{}".format(after_the_day_after_tomorrow.day, after_the_day_after_tomorrow.month,
                                            after_the_day_after_tomorrow.year),
                )
            )
            return CHECKOUT2


@debug_requests
def hand_finish_order(bot: Bot, update: Update, user_data: dict):
    upTextL = update.message.text.lower()
    chat_id = update.message.chat_id
    name = update.message.from_user.first_name.lower()
    # Логирование
        # logger.info("hand_checkout2 - text =" + upTextL + "; chat_id=" + str(
        #     update.message.chat_id) + "; name= " + name)
    logTOchat(bot=bot, update=update,
              text=f"{HashTagFindLogsINFO} - hand_checkout2 - text =" + upTextL + "; chat_id=" + str(
                  update.message.chat_id) + "; name= " + name)
    # Основная логика
    if upTextL == 'вернуться в меню' and update.message.chat_id != config.CHAT_ID_COMPANY and update.message.chat_id != config.CHAT_ID_BUGS:
        bot.send_message(
            chat_id=chat_id,
            text='Сделайте ваш заказ:',
            reply_markup=get_Keyboard_ZapProfCommands('1')
        )
        return MENU
    else:
        bot.send_message(
            chat_id=chat_id,
            text=f'Наш магазин предлагает Вам широкий ассортимент питьевой бутилированной воды. Хотите больше товаров? '
                 f'Посетите наш сайт {config.url_site}',
            reply_markup=get_Keyboard_orders()
        )
        return NEW_ORDER


def main():
    logger.info("Запускаем бота...")

    req = Request(
        connect_timeout=5.0,
        read_timeout=4.0,
    )

    bot = Bot(
        token=TG_TOKEN,
        request=req,
        base_url=TG_API_URL,
    )
    updater = Updater(
        bot=bot,
    )

    bot.send_message(
        chat_id=CHAT_ID_LOGS,
        text="\n\n\n\nЗапуск бота\n\n\n\n",
    )
    bot.send_message(
        chat_id=CHAT_ID_COMPANY,
        text="\n\n\n\nЗапуск бота\n\n\n\n",
    )
    bot.send_message(
        chat_id=CHAT_ID_BUGS,
        text="\n\n\n\nЗапуск бота\n\n\n\n",
    )

    # Проверить что бот корректно подключился к Telegram API
    info = bot.get_me()
    logger.info(f'Bot info: {info}')

    bot.send_message(
        chat_id=CHAT_ID_LOGS,
        text=f"\n\n\n\n{info}\n\n\n\n",
    )
    # Навесить обработчики команд
    Main_handler = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.all, start_reg),
        ],
        states={
            TYPE_FACE: [
                MessageHandler(Filters.all, hend_type_face, pass_user_data=True),
            ],
            NAME: [
                MessageHandler(Filters.all, hend_name, pass_user_data=True),
            ],
            COMPANY: [
                MessageHandler(Filters.all, hend_company, pass_user_data=True),
            ],
            ADDRESS: [
                MessageHandler(Filters.all, hend_address, pass_user_data=True),
            ],
            ADDRESS_CITY: [
                MessageHandler(Filters.all, hend_address_city, pass_user_data=True),
            ],
            MOB_PHONE: [
                MessageHandler(Filters.all, hend_mob_phone, pass_user_data=True),
            ],
            MENU: [
                MessageHandler(Filters.all, hand_select_menu, pass_user_data=True),
            ],
            NEW_ORDER: [
                MessageHandler(Filters.all, hand_new_order, pass_user_data=True),
            ],
            EDIT_PROFILE: [
                MessageHandler(Filters.all, hand_edit_profile, pass_user_data=True),
            ],
            ORDERS: [
                MessageHandler(Filters.all, hand_edit_profile, pass_user_data=True),
            ],
            TEMPORARY_ENTER_QUANTITY: [
                MessageHandler(Filters.all, hand_temorary_enter_quanity, pass_user_data=True),
            ],
            TEMPORARY_ENTER_QUANTITY2: [
                MessageHandler(Filters.all, hand_enter_quanity2, pass_user_data=True),
            ],
            CHECKOUT: [
                MessageHandler(Filters.all, hand_checkout, pass_user_data=True),
            ],
            CHECKOUT2: [
                MessageHandler(Filters.all, hand_checkout2, pass_user_data=True),
            ],
            FINISH_ORDER: [
                MessageHandler(Filters.all, hand_finish_order, pass_user_data=True),

            ],
        },
        fallbacks=[
            CommandHandler('cancel', cancel_handler),
        ],
    )

    start_handler = CommandHandler("start", do_start)
    help_handler = CommandHandler("help", do_start)
    # message_handler = MessageHandler(Filters.all, do_echo)
    updater.dispatcher.add_handler(help_handler)
    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(Main_handler)
    # updater.dispatcher.add_handler(message_handler)

    # Начать бесконечную обработку входящих сообщений
    updater.start_polling()
    updater.idle()

    bot.send_message(
        chat_id=CHAT_ID_LOGS,
        text="\n\n\n\nБот выключается\n\n\n\n",
    )

    bot.send_message(
        chat_id=CHAT_ID_COMPANY,
        text="\n\n\n\nБот выключается\n\n\n\n",
    )
    bot.send_message(
        chat_id=CHAT_ID_BUGS,
        text="\n\n\n\nБот выключается\n\n\n\n",
    )
    logger.info("Закончили...")


if __name__ == '__main__':
    main()
