import telebot
from telebot.types import Message
from telebot import types
import os
import logging

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.
token = '1192087203:AAFS_q5p-gj04n4c0vtuB7vCPLY9sonTiIE'

url_site = ''
company = ''
name = ''
mob_phone = ''
number = ''
type_face = ''
address = ''

def set_final_settings():
    if mob_phone == '':
        return False
    else:
        return True

final_settings = set_final_settings()

# token = os.getenv("TOKEN")
bot = telebot.TeleBot(token)


# Команда Заполнить профиль(start_reg(message))
def start_reg(message):
    keyboard1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2) #наша клавиатура №1
    keyboard1.add(types.KeyboardButton('Юр.лицо'),
                  types.KeyboardButton('Физ.лицо'))  #кнопка «Юр.лицо» и кнопка «Физ.лицо». добавляем кнопку в клавиатуру
    keyboard2 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2) #наша клавиатура №2
    keyboard2.add(types.KeyboardButton('Заполнить профиль')) #кнопка «Отправить имя профиля». добавляем кнопку в клавиатуру
    if message.text.lower() == 'заполнить профиль':
        bot.send_message(message.from_user.id,
                         "Выберите, кто вы:",
                         reply_markup=keyboard1)
        get_type_face(message)
        bot.register_next_step_handler(message, get_type_face) #следующий шаг – функция get_type_face
    else:
        bot.send_message(message.from_user, 'Напиши или нажми \"Заполнить профиль\"',reply_markup=keyboard2)
        start_reg(message)
        bot.register_next_step_handler(message, start_reg) #следующий шаг – функция start_reg

# функция изменения типа(get_type_face(message))
def get_type_face(message: Message):
    global type_face
    keyboard1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2) #наша клавиатура №1
    keyboard1.add(types.KeyboardButton('Отправить имя профиля'))  #кнопка «Отправить имя профиля». добавляем кнопку в клавиатуру
    keyboard2 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2) #наша клавиатура №2
    keyboard2.add(types.KeyboardButton('Юр.лицо'),
                  types.KeyboardButton('Физ.лицо'))  #кнопка «Юр.лицо». добавляем кнопку в клавиатуру
    if message.text == 'Юр.лицо':
        type_face = 'Юр.лицо'
        bot.send_message(message.from_user, "Напишите название компании, пожалуйста")
        get_company(message)
        bot.register_next_step_handler(message, get_company) #следующий шаг – get_company
    elif message.text == 'Физ.лицо':
        type_face = 'Физ.лицо'
        bot.send_message(message.from_user,
                         "Напишите как к вам обращаться или нажмите на кнопку \"Отправить имя профиля\"",
                         reply_markup=keyboard1)
        get_name(message)
        bot.register_next_step_handler(message, get_name) #следующий шаг – функция get_name
    else:
        get_type_face(message)
        bot.send_message(message.from_user,
                         'Нажмите на кнопку \"Юр.лицо\"  или \"Физ.лицо\"',
                         reply_markup=keyboard2)
        bot.register_next_step_handler(message, get_type_face) #следующий шаг – функция get_type_face

# функция получения имени(get_name(message))
def get_name(message: Message):
    global name
    if message.text == 'Отправить имя профиля':
        name = message.from_first_name
    else:
        name = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2) #наша клавиатура №1
    keyboard.add(types.KeyboardButton('Москва'),
                 types.KeyboardButton('Калуга'),
                 types.KeyboardButton('Серпухов'),
                 types.KeyboardButton('Орехово-Зуево'))              #кнопка «Москва». добавляем кнопку в клавиатуру
        
    bot.send_message(message.from_user, 'Выберите ваш город:',reply_markup=keyboard)
    get_address_city(message)
    bot.register_next_step_handler(message, get_address_city)

# функция получения названия компании(get_company(message))
def get_company(message: Message):
    global company
    company = message.text
    keyboard1 = types.ReplyKeyboardMarkup() #наша клавиатура №1
    keyboard1.add(types.KeyboardButton('Отправить имя профиля'))  #кнопка «Отправить имя профиля». добавляем кнопку в клавиатуру
    bot.send_message(message.from_user, 
                     "Напишите как к вам обращаться или нажмите на кнопку \"Отправить имя профиля\"",
                     reply_markup=keyboard1)
    get_name(message)
    bot.register_next_step_handler(message, get_name) #следующий шаг – функция get_name

# функция получения названия города(get_address(message))
def get_address_city(message: Message):
    global address
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2) #наша клавиатура №1
    keyboard.add(types.KeyboardButton('Москва'),
                 types.KeyboardButton('Калуга'),
                 types.KeyboardButton('Серпухов'),
                 types.KeyboardButton('Орехово-Зуево'))              #кнопка «Москва». добавляем кнопку в клавиатуру
    if message.text == 'Москва':
        address = 'г.' + message.text 
        bot.send_message(message.from_user,
                         'Введите адрес для доставки. Укажите улицу, номер и корпус дома, номер квартиры:')
        get_address(message)
        bot.register_next_step_handler(message, get_address)
    elif message.text == 'Орехово-Зуево':
        address ='г.' + message.text
        bot.send_message(message.from_user, 
                        'Введите адрес для доставки. Укажите улицу, номер и корпус дома, номер квартиры:')
        get_address(message)
        bot.register_next_step_handler(message, get_address)
    elif message.text == 'Серпухов':
        address = 'г.' +message.text
        bot.send_message(message.from_user, 
                        'Введите адрес для доставки. Укажите улицу, номер и корпус дома, номер квартиры:')
        get_address(message)
        bot.register_next_step_handler(message, get_address)        
    elif message.text == 'Калуга':
        address = 'г.' +message.text
        bot.send_message(message.from_user, 
                        'Введите адрес для доставки. Укажите улицу, номер и корпус дома, номер квартиры:')
        get_address(message)
        bot.register_next_step_handler(message, get_address)
    else:
        bot.send_message(message.from_user, 
                        'Выберите ваш город:',
                        reply_markup=keyboard)
        get_address_city(message)
        bot.register_next_step_handler(message, get_address_city)

# функция получения остальных данных адреса(get_address(message))
def get_address(message: Message):
    global address
    address = address + message.text
    bot.send_message(message.from_user, 
                    'Введите ваш номер телефона:')
    get_mob_phone(message)
    bot.register_next_step_handler(message, get_mob_phone)

# функция получения номера моб телефона(get_mob_phone(message))
def get_mob_phone(message: Message):
    global mob_phone
    global final_settings
    mob_phone = message.text
    bot.send_message(message.from_user, 
                    'Спасибо! Теперь Вы можете приступить к покупкам. Не забудьте посетить наш сайт '+url_site+'.')
    final_settings = True

# Метод для получения текстовых сообщений
@bot.message_handler(commands=['start','reg','help'])
def send_welcome(message: Message):
    print(str(message.text) + ' - send_welcome')
    logging.info(message.text )
    # В этом участке кода мы объявили слушателя для текстовых сообщений и метод их обработки. 
    # Поле content_types может принимать разные значения, и не только одно
    # @bot.message_handler(content_types=['text', 'document', 'audio'])
    keyboard1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2) #наша клавиатура №1
    keyboard1.add(types.KeyboardButton('Заполнить профиль'))  #кнопка «Отправить имя профиля». добавляем кнопку в клавиатуру
    keyboard2 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2) #наша клавиатура №2
    keyboard2.add(types.KeyboardButton('Заполнить профиль'))  #кнопка «Отправить имя профиля». добавляем кнопку в клавиатуру
    keyboard4 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2) #наша клавиатура №4
    keyboard4.add(types.KeyboardButton('Новый заказ'),types.KeyboardButton('Повторить прошлый заказ'))  #кнопка «Юр.лицо» и кнопка «Физ.лицо». добавляем кнопку в клавиатуру
    keyboard4.add(types.KeyboardButton('Изменить профиль'))  #кнопка «Юр.лицо» и кнопка «Физ.лицо». добавляем кнопку в клавиатуру
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Здраствуйте! вас приветствует ассистент заказа воды \"Просто вода\". Для начала работы, пожайлуста заполните профиль",reply_markup=keyboard1)
    elif message.text == "/help":
        if final_settings == True:
            bot.send_message(message.from_user.id, "Сейчас доступны данные команды:",reply_markup=keyboard4)
        elif final_settings == False:
            bot.send_message(message.from_user.id, "Сейчас доступны данные команды:",reply_markup=keyboard2)
    elif message.text == "/reg": 
        get_message(message)    
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

@bot.message_handler(content_types=['text'])
def get_message(message: Message):
    print(str(message.text) + ' - get_message')
    logging.info(message.text)
    keyboard3 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2) #наша клавиатура №3
    keyboard3.add(types.KeyboardButton('Юр.лицо'),types.KeyboardButton('Физ.лицо'))  #кнопка «Юр.лицо» и кнопка «Физ.лицо». добавляем кнопку в клавиатуру
    
    if message.text == "Заполнить профиль":
        start_reg(message)
        # user.start_reg()
        bot.register_next_step_handler(message, start_reg) #следующий шаг – функция start_reg        
    
bot.polling(none_stop=True, interval=0)
