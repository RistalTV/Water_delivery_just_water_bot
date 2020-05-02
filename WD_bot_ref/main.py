from logging import getLogger, Logger
from datetime import timedelta, datetime
import config
from telegram import Bot, ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup, Update, ParseMode
from telegram.ext import CommandHandler, ConversationHandler, Filters, CallbackQueryHandler
from telegram.ext import MessageHandler, Updater
from telegram.utils.request import Request
from config import TG_API_URL, TG_TOKEN, url_site
from buttons import get_Keyboard_ZapProf, get_Keyboard_orders, get_Keyboard_TypeFace, get_Keyboard_City
from buttons import get_Keyboard_SendNameProf, get_Keyboard_ZapProfCommands, get_Keyboard_Button_Edit
from buttons import get_Keyboard_order, get_Keyboard_temp_order, get_Keyboard_temp_order2, get_Keyboard_temp_order3
from buttons import get_Keyboard_DeliveryOrder, get_Keyboard_Finish_order, get_Keyboard_Sent_Order_to_reply
from validators import validate_count, validate_date
from buttons import *
from validators import *

from db import add_info_of_user
from db import add_order_of_user
from db import exits_user

logger: Logger = getLogger(__name__)

flag = None


# Декоратор для лога
def debug_requests(f):
    # Декоратор для обработки событий от телеграма
    #
    def inner(*args, **kwargs):
        try:
            logger.info("Обращение в функцию {}".format(f.__name__))
            return f(*args, **kwargs)
        except Exception:
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
    logger.info("do_start START - text =" + str(update.message.text) + "; chat_id=" + str(
        update.message.chat_id) + "; name= " + str(update.message.from_user.first_name))
    user = exits_user(user_id=update.message.chat_id)
    # logger.info(user['id'])
    if user is None:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Здраствуйте! Вас приветствует ассистент заказа воды \"Просто вода\". Для начала работы, пожайлуста "
                 "нажмите \'Заполнить профиль\'",
            reply_markup=get_Keyboard_ZapProf(),
        )
    elif user[0]:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Здраствуйте, {0}! Вас приветствует ассистент заказа воды \"Просто вода\".Вы можете приступить к покупкам. Не забудьте посетить наш сайт {1}.".format(
                user[0][2], config.url_site),
            reply_markup=get_Keyboard_ZapProfCommands('1'),
        )


@debug_requests
def start_reg(bot: Bot, update: Update):
    if update.message.text.lower() == 'заполнить профиль':
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Выберите, вы кто:",
            reply_markup=get_Keyboard_TypeFace(),
        )
        return TYPE_FACE
    else:
        return MENU


@debug_requests
def hend_type_face(bot: Bot, update: Update, user_data: dict):
    # Логирование
    logger.info("hend_type_face - text =" + update.message.text.lower())
    # Проверка
    text = update.message.text.lower()
    if text != 'юр.лицо' and text != 'физ.лицо':
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Выберите, вы кто:",
            reply_markup=get_Keyboard_TypeFace(),
        )
        return TYPE_FACE
    else:
        # Получить тип лица (Физ и Юр)
        user_data[TYPE_FACE] = text

        # Разветвление Спрашиваем юзера
        if text == 'юр.лицо':
            bot.send_message(
                chat_id=update.message.chat_id,
                text="Напишите название компании, пожалуйста",
                reply_markup=ReplyKeyboardRemove(),
            )
            return COMPANY
        elif text == 'физ.лицо':
            bot.send_message(
                chat_id=update.message.chat_id,
                text="Напишите как к вам обращаться или нажмите на кнопку \"Отправить имя профиля\"",
                reply_markup=get_Keyboard_SendNameProf(),
            )
            return NAME
        else:
            return TYPE_FACE


@debug_requests
def hend_name(bot: Bot, update: Update, user_data: dict):
    # Логирование
    logger.info("hend_name - text =" + update.message.text.lower())
    # Проверка
    text = update.message.text.lower()
    if text == 'отправить имя профиля':
        text = update.effective_chat.first_name

    # Получить имя
    user_data[NAME] = text

    # Спрашиваем юзера
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Выберите ваш город:",
        reply_markup=get_Keyboard_City(),
    )
    return ADDRESS_CITY


@debug_requests
def hend_company(bot: Bot, update: Update, user_data: dict):
    # Логирование
    logger.info("hend_company - text =" + update.message.text.lower())
    # Получение сообщения
    # Получить тип лица (Физ и Юр)
    user_data[COMPANY] = update.message.text

    # Спрашиваем юзера
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Напишите как к вам обращаться или нажмите на кнопку \"Отправить имя профиля\"",
        reply_markup=get_Keyboard_SendNameProf(),
    )
    return NAME


@debug_requests
def hend_address(bot: Bot, update: Update, user_data: dict):
    # Логирование
    logger.info("hend_address - text =" + update.message.text.lower())
    # Получение адреса
    text = update.message.text.lower()
    # Получить город
    user_data[ADDRESS] = text

    # Спрашиваем юзера
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Введите ваш номер телефона:",
        reply_markup=ReplyKeyboardRemove(),
    )
    return MOB_PHONE


@debug_requests
def hend_address_city(bot: Bot, update: Update, user_data: dict):
    # Логирование
    global flag
    logger.info("hend_address_city - text =" + update.message.text.lower())
    # Проверка
    city = [
        'москва',
        'калуга',
        'серпухов',
        'орехово-зуево'
    ]
    text = update.message.text.lower()
    for citi in city:
        if citi == text:
            flag = True
            break
    if not flag:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Выберите ваш город:",
            reply_markup=get_Keyboard_City(),
        )
        return ADDRESS_CITY
    # Получить город
    user_data[ADDRESS_CITY] = text

    # Спрашиваем юзера
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Введите адрес для доставки. Укажите улицу, номер и корпус дома, номер квартиры:",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ADDRESS


@debug_requests
def hend_mob_phone(bot: Bot, update: Update, user_data: dict):
    # Логирование
    logger.info("hend_mob_phone - text =" + update.message.text.lower())
    # Получение номера
    text = update.message.text.lower()
    # Получить адрес
    user_data[MOB_PHONE] = text

    # Спрашиваем юзера
    bot.send_message(
        chat_id=update.message.chat_id,
        text=f"Спасибо! Теперь Вы можете приступить к покупкам. Не забудьте посетить наш сайт {config.url_site}.",
        reply_markup=get_Keyboard_ZapProfCommands('1'),
    )
    if user_data[TYPE_FACE] == 'физ.лицо':
        user_data[COMPANY] = None
    # add_info_of_user(
    #     user_id=update.message.chat_id,
    #     username=user_data[NAME],
    #     company=user_data[COMPANY],
    #     address=user_data[ADDRESS],
    #     address_city=user_data[ADDRESS_CITY],
    #     mob_phone=user_data[MOB_PHONE]
    # )
    logger.info('user_data: %s', user_data)
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
    # Логирование
    logger.info("hand_select_menu - text =" + update.message.text.lower())
    # Создание листа заказа
    user_data[ORDERS] = list()
    user_data[ORDERS].insert(0, 0)
    user_data[ORDERS].insert(1, 0)
    user_data[ORDERS].insert(2, 0)
    user_data[ORDERS].insert(3, 0)
    # получение текста
    text = update.message.text.lower()
    if text == 'новый заказ':
        bot.send_message(
            chat_id=update.message.chat_id,
            text=f'Наш магазин предлагает Вам широкий ассортимент питьевой бутилированной воды. Хотите больше товаров? '
                 f'Посетите наш сайт {config.url_site}',
            reply_markup=get_Keyboard_orders()
        )
        return NEW_ORDER
    elif text == 'повторить прошлый заказ':
        # Проверка на наличие заказов
        flag = None
        if user_data[ORDERS][0] == 0 or user_data[ORDERS][0] < 2:
            flag = False
        elif user_data[ORDERS][1] == 0 or user_data[ORDERS][1] < 6:
            flag = False
        elif user_data[ORDERS][2] == 0 or user_data[ORDERS][2] < 1:
            flag = False
        else:
            flag = True
        # Или ругаем юзера
        # Или выводим сообщ с данными
        if not flag:
            # Выводим сообщение о том что юзер не делал заказы
            bot.send_message(
                chat_id=update.message.chat_id,
                text="Вы ранее не заказывали у нас доставку воды. Сделайте новый заказ и далее вы сможете повторять новый заказ",
                reply_markup=get_Keyboard_ZapProfCommands('1'),
            )
            return MENU
        else:
            # Выводим сообщение о том что юзер делал заказы и бот повторил заказ
            order_text = 'Ваш заказ содержит:\n\n'
            if user_data[ORDERS][0] != 0 and user_data[ORDERS][0] > 2:
                order_text = order_text + f'\n  - 19 литровая бутыль ({user_data[ORDERS][0]} шт.)'
            elif user_data[ORDERS][1] != 0 and user_data[ORDERS][1] > 6:
                order_text = order_text + f'\n  - 6 литровая бутыль ({user_data[ORDERS][1]} шт.)'
            elif user_data[ORDERS][2] != 0 and user_data[ORDERS][2] > 1:
                order_text = order_text + f'\n  - Механическая помпа ({user_data[ORDERS][2]} шт.)'
            sum = user_data[ORDERS][0] * 270 + user_data[ORDERS][1] * 100 + user_data[ORDERS][2] * 799
            order_text = order_text + f'\n\nОбщая стоимость заказа: {user_data[ORDERS][3]} руб.'
            bot.send_message(
                chat_id=update.message.chat_id,
                text=order_text,
                reply_markup=get_Keyboard_Sent_Order_to_reply(),
            )
            return CHECKOUT
    elif text == 'изменить профиль':
        # text1 = '<h1><b>Ваш профиль:</b></h1>\n<h4>' + \
        #         f'<ol><li>Имя: <b>{user_data[NAME]}</b></li></ol>\n' + \
        #         f'<ol><li>Компания: <b>{user_data[COMPANY]}</b></li></ol>\n' + \
        #         f'<ol><li>Город: <b>{user_data[ADDRESS_CITY]}</b></li></ol>\n' + \
        #         f'<ol><li>Адрес: <b>{user_data[ADDRESS]}</b></li></ol>\n' + \
        #         f'<ol><li>Номер телефона: <b>{user_data[MOB_PHONE]}</b></li></ol></h4>'
        if user_data[TYPE_FACE] == 'юр.лицо':
            bot.send_message(
                chat_id=update.message.chat_id,
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
                chat_id=update.message.chat_id,
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
    # Логирование
    logger.info("hand_new_order - text =" + update.message.text.lower())
    text = update.message.text.lower()
    if text == "вернуться назад":
        bot.send_message(
            chat_id=update.message.chat_id,
            text=f'Наш магазин предлагает Вам широкий ассортимент питьевой бутилированной воды. Хотите больше товаров? '
                 f'Посетите наш сайт {config.url_site}',
            reply_markup=get_Keyboard_ZapProfCommands('1')
        )
        return MENU
    elif text == "19 литровая бутыль воды":
        bot.send_message(
            chat_id=update.message.chat_id,
            text='19 литровая бутыль c водой' + order_text(270, 2),
            reply_markup=get_Keyboard_order()
        )
        user_data[ORDERS].pop(0)
        user_data[ORDERS].insert(0, -1)
        return TEMPORARY_ENTER_QUANTITY
    elif text == "6 литровая бутыль воды":
        bot.send_message(
            chat_id=update.message.chat_id,
            text='6 литровая бутыль c водой' + order_text(100, 6),
            reply_markup=get_Keyboard_order()
        )
        user_data[ORDERS].pop(1)
        user_data[ORDERS].insert(1, -1)
        return TEMPORARY_ENTER_QUANTITY
    elif text == "ручная помпа":
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Помпа для воды механическая "АЕЛ"(AEL)\nПредназначена для 19 литровой бутыли с водой\n\n\nСтоимость: 799 рублей',
            reply_markup=get_Keyboard_order()
        )
        user_data[ORDERS].pop(2)
        user_data[ORDERS].insert(2, -1)
        return TEMPORARY_ENTER_QUANTITY
    elif text == 'cделать ещё заказ':
        bot.send_message(
            chat_id=update.message.chat_id,
            text=f'Наш магазин предлагает Вам широкий ассортимент питьевой бутилированной воды. Хотите больше товаров? '
                 f'Посетите наш сайт {config.url_site}',
            reply_markup=get_Keyboard_orders()
        )
        return NEW_ORDER

@debug_requests
def hand_edit_profile(bot: Bot, update: Update, user_data: dict):
    # Логирование
    logger.info("hend_type_face - text =" + update.message.text.lower())
    if update.message.text.lower() == 'изменить':
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Выберите, вы кто:",
            reply_markup=get_Keyboard_TypeFace(),
        )
        return TYPE_FACE
    elif update.message.text.lower() == 'вернуться обратно':
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Сделайте ваш заказ:',
            reply_markup=get_Keyboard_ZapProfCommands('1')
        )
        return MENU
    else:
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Нажмите на кнопки снизу:',
            reply_markup=get_Keyboard_Button_Edit()
        )
        return EDIT_PROFILE


@debug_requests
def hand_temorary_enter_quanity(bot: Bot, update: Update, user_data: dict):
    # Логирование
    logger.info("hand_temorary_enter_quanity - text =" + update.message.text.lower())
    text = update.message.text.lower()
    if text == 'отменить':
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Нажмите на кнопки снизу:',
            reply_markup=get_Keyboard_Button_Edit()
        )
        return NEW_ORDER
    elif text == 'ввести кол-во':
        if user_data[ORDERS][0] == -1:
            min = 2
        elif user_data[ORDERS][1] == -1:
            min = 6
        elif user_data[ORDERS][2] == -1:
            min = 1
        bot.send_message(
            chat_id=update.message.chat_id,
            text=f'Введите кол-во товаров числом,\nМинимальное кол-во {min} шт.',
            reply_markup=ReplyKeyboardRemove()
        )
        return TEMPORARY_ENTER_QUANTITY2
    elif text == 'оформить заказ':
        # user_data[ORDERS][0] != 0 \
        # and user_data[ORDERS][1] != 0 \
        # and user_data[ORDERS][2] != 0 \
        # and
        order_text = 'Ваш заказ содержит:\n\n'
        if user_data[ORDERS][0] != 0 and user_data[ORDERS][0] > 2:
            order_text = order_text + f'\n  - 19 литровая бутыль ({user_data[ORDERS][0]} шт.)'
        elif user_data[ORDERS][1] != 0 and user_data[ORDERS][1] > 6:
            order_text = order_text + f'\n  - 6 литровая бутыль ({user_data[ORDERS][1]} шт.)'
        elif user_data[ORDERS][2] != 0 and user_data[ORDERS][2] > 1:
            order_text = order_text + f'\n  - Механическая помпа ({user_data[ORDERS][2]} шт.)'
        sum = user_data[ORDERS][0] * 270 + user_data[ORDERS][1] * 100 + user_data[ORDERS][2] * 799
        user_data[ORDERS].pop(3)
        user_data[ORDERS].insert(3, sum)
        order_text = order_text + f'\n\nОбщая стоимость заказа: {user_data[ORDERS][3]} руб.'
        bot.send_message(
            chat_id=update.message.chat_id,
            text=order_text,
            reply_markup=get_Keyboard_temp_order3()
        )
        return CHECKOUT
    elif text == 'добавить ещё товар':
        bot.send_message(
            chat_id=update.message.chat_id,
            text=f'Наш магазин предлагает Вам широкий ассортимент питьевой бутилированной воды. Хотите больше товаров? '
                 f'Посетите наш сайт {config.url_site}',
            reply_markup=get_Keyboard_orders()
        )
        return NEW_ORDER


@debug_requests
def hand_enter_quanity2(bot: Bot, update: Update, user_data: dict):
    # Логирование
    logger.info("hand_enter_quanity2 - text =" + update.message.text.lower())
    # Основная логика функции
    if user_data[ORDERS][0] == -1:
        min = 2
    elif user_data[ORDERS][1] == -1:
        min = 6
    elif user_data[ORDERS][2] == -1:
        min = 1
    count = validate_count(text=update.message.text.lower(), min=min)
    if count is None:
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Введите кол-во товаров числом',
            reply_markup=ReplyKeyboardRemove()
        )
        return TEMPORARY_ENTER_QUANTITY2
    elif count < min:
        bot.send_message(
            chat_id=update.message.chat_id,
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
            chat_id=update.message.chat_id,
            text=f'Вы выбрали {count} товар(ов).',
            reply_markup=get_Keyboard_temp_order2()
        )
        return TEMPORARY_ENTER_QUANTITY


@debug_requests
def hand_checkout(bot: Bot, update: Update, user_data: dict):
    # Логирование
    logger.info("hand_checkout - text =" + update.message.text.lower())
    # Основная логика функции
    text = update.message.text.lower()
    after_tomorrow = datetime.now() + timedelta(1)
    after_the_day_after_tomorrow = datetime.now() + timedelta(2)
    if text == 'подтвердить заказ':
        bot.send_message(
            chat_id=update.message.chat_id,
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
    # Логирование
    logger.info("hand_checkout2 - text =" + update.message.text.lower())
    # Основная логика функции
    text = update.message.text.lower()
    vdata = validate_date(text)
    if text == 'вернуться в меню':
        return NEW_ORDER
    elif text == 'завтра':
        now = datetime.now()
        user_data[ORDERS].pop(4)
        user_data[ORDERS].insert(4, "{}.{}.{}".format(now.day, now.month, now.year))
        order_text = 'Ваш заказ оформлен:\n\n'
        if user_data[ORDERS][0] != 0 and user_data[ORDERS][0] > 2:
            order_text = order_text + f'\n  - 19 литровая бутыль ({user_data[ORDERS][0]} шт.)'
        elif user_data[ORDERS][1] != 0 and user_data[ORDERS][1] > 6:
            order_text = order_text + f'\n  - 6 литровая бутыль ({user_data[ORDERS][1]} шт.)'
        elif user_data[ORDERS][2] != 0 and user_data[ORDERS][2] > 1:
            order_text = order_text + f'\n  - Механическая помпа ({user_data[ORDERS][2]} шт.)'
        order_text = order_text + f'\n\nОбщая стоимость заказа:  {user_data[ORDERS][3]} руб.' + \
                     f'Заказ будет доставлен {user_data[ORDERS][4]}' + \
                     '\n\nОплата наличными курьеру'
        bot.send_message(
            chat_id=update.message.chat_id,
            text=order_text,
            reply_markup=get_Keyboard_Finish_order(),
        )
        return FINISH_ORDER
    elif vdata is not None:
        user_data[ORDERS].insert(4, text)
        order_text = 'Ваш заказ оформлен:\n\n'
        if user_data[ORDERS][0] != 0 and user_data[ORDERS][0] > 2:
            order_text = order_text + f'\n  - 19 литровая бутыль ({user_data[ORDERS][0]} шт.)'
        elif user_data[ORDERS][1] != 0 and user_data[ORDERS][1] > 6:
            order_text = order_text + f'\n  - 6 литровая бутыль ({user_data[ORDERS][1]} шт.)'
        elif user_data[ORDERS][2] != 0 and user_data[ORDERS][2] > 1:
            order_text = order_text + f'\n  - Механическая помпа ({user_data[ORDERS][2]} шт.)'
        order_text = order_text + f'\n\nОбщая стоимость заказа:  {user_data[ORDERS][3]} руб.' + \
                     f'Заказ будет доставлен {user_data[ORDERS][4]}' + \
                     '\n\nОплата наличными курьеру'
        bot.send_message(
            chat_id=update.message.chat_id,
            text=order_text,
            reply_markup=get_Keyboard_Finish_order(),
        )
        return FINISH_ORDER
    else:
        after_tomorrow = datetime.now() + timedelta(1)
        after_the_day_after_tomorrow = datetime.now() + timedelta(2)
        if text == 'подтвердить заказ':
            bot.send_message(
                chat_id=update.message.chat_id,
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
    # Логирование
    logger.info("hand_checkout2 - text =" + update.message.text.lower())
    # Основная логика функции
    text = update.message.text.lower()
    if text == 'вернуться в меню':
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Сделайте ваш заказ:',
            reply_markup=get_Keyboard_ZapProfCommands('1')
        )
        return MENU
    else:
        bot.send_message(
            chat_id=update.message.chat_id,
            text=f'Наш магазин предлагает Вам широкий ассортимент питьевой бутилированной воды. Хотите больше товаров? '
                 f'Посетите наш сайт {config.url_site}',
            reply_markup=get_Keyboard_orders()
        )
        return NEW_ORDER


def main():

    logger.info("Запускаем бота...")

    req = Request(
        connect_timeout=3.0,
        read_timeout=2.0,
    )
    bot = Bot(
        token=TG_TOKEN,
        request=req,
        base_url=TG_API_URL,
    )

    updater = Updater(
        bot=bot,
    )
    # Проверить что бот корректно подключился к Telegram API
    info = bot.get_me()
    logger.info(f'Bot info: {info}')

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
    # message_handler = MessageHandler(Filters.all, do_echo)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(Main_handler)
    # updater.dispatcher.add_handler(message_handler)

    # Начать бесконечную обработку входящих сообщений
    updater.start_polling()
    updater.idle()

    logger.info("Закончили...")


if __name__ == '__main__':
    main()
