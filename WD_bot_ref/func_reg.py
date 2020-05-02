from logging import getLogger

import telegram
from telegram import Bot
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram import Update
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater

import config
import buttons
from config import TG_API_URL
from config import TG_TOKEN

import  user
from user import user_from_bot

from buttons import BUTTON_2_1_YurFace
from buttons import BUTTON_2_2_FizFace

from buttons import BUTTON_3_1_City
from buttons import BUTTON_3_2_City
from buttons import BUTTON_3_3_City
from buttons import BUTTON_3_4_City

from buttons import BUTTON_4_1_SendNameProf

from buttons import BUTTON_5_1_EditProf
from buttons import BUTTON_5_2_NewOrder
from buttons import BUTTON_5_3_ReplyOldOrder

from buttons import get_Keyboard_TypeFace

import user
from user import user_from_bot


logger = getLogger(__name__)


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


# ==========================================================================#
# Program functions Start

@debug_requests
def get_type_face(bot: Bot, update: Update, user: user_from_bot):
    type_face = user.get_type_face()
    if type_face != 'Юр.лицо' or type_face != 'Физ.лицо':
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Выберите, вы кто:",
            reply_markup=get_Keyboard_TypeFace(),
        )

        text = update.message.text
        if text == 'Юр.лицо' or text == 'Физ.лицо':
            return text
        else:
            get_type_face(bot=bot, update=update)
        pass

@debug_requests
def get_name(bot: Bot, update: Update, user: user_from_bot):
    pass

@debug_requests
def get_company(bot: Bot, update: Update, user: user_from_bot):
    pass

@debug_requests
def get_address(bot: Bot, update: Update, user: user_from_bot):
    pass

@debug_requests
def get_address_city(bot: Bot, update: Update, user: user_from_bot):
    pass

@debug_requests
def get_mob_phone(bot: Bot, update: Update, user: user_from_bot):
    pass
