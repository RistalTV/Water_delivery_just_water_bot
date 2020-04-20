import telebot;
import os;
from telebot import types

token = os.getenv("TOKEN");
bot = telebot.TeleBot(token);

url_site = '';
company = '';
name = '';
email = '';
mob_phone = '';
number = '';
type_face = '';
address = '';

final_settings = ''; 

# # Метод-обработчик
# @bot.callback_query_handler(func=lambda call: True)
# def callback_worker(call):
#     if call.data == "Заполнить профиль": #call.data это callback_data, которую мы указали при объявлении кнопки
                
#     elif call.data == "/help":
#         bot.send_message(call.message.chat.id, "Сейчас доступны данные команды:",reply_markup=keyboard2)

#     elif call.data == "Юр.лицо":
    
#     elif call.data == "Юр.лицо":

#     elif call.data == "Юр.лицо":

#     elif call.data == "Юр.лицо":

#     elif call.data == "Юр.лицо":

#     elif call.data == "Юр.лицо":
                

# Метод для получения текстовых сообщений
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    # В этом участке кода мы объявили слушателя для текстовых сообщений и метод их обработки. 
    # Поле content_types может принимать разные значения, и не только одно
    # @bot.message_handler(content_types=['text', 'document', 'audio'])
    keyboard1 = types.InlineKeyboardMarkup(); #наша клавиатура №1
    keyboard1.add(types.InlineKeyboardButton(text='Заполнить профиль', callback_data='Заполнить профиль'));  #кнопка «Отправить имя профиля». добавляем кнопку в клавиатуру
    keyboard2 = types.InlineKeyboardMarkup(); #наша клавиатура №2
    keyboard2.add(types.InlineKeyboardButton(text='Заполнить профиль', callback_data='Заполнить профиль'));  #кнопка «Отправить имя профиля». добавляем кнопку в клавиатуру
    
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Здраствуйте! вас приветствует ассистент заказа воды \"Просто вода\". Для начала работы, пожайлуста заполните профиль",reply_markup=keyboard1)
    elif message.text == "Заполнить профиль":
        bot.send_message(message.from_user.id, "Заполнить профиль")
        bot.register_next_step_handler(message, start_reg); #следующий шаг – функция start_reg        
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Сейчас доступны данные команды:",reply_markup=keyboard2)
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
bot.polling(none_stop=True, interval=0)

# Команда Заполнить профиль(start_reg(message))
def start_reg(message):       
    keyboard1 = types.InlineKeyboardMarkup(); #наша клавиатура №1
    keyboard1.add(types.InlineKeyboardButton(text='Юр.лицо', callback_data='Юр.лицо'));  #кнопка «Юр.лицо». добавляем кнопку в клавиатуру
    keyboard1.add(types.InlineKeyboardButton(text='Физ.лицо', callback_data='Физ.лицо'));#кнопка «Физ.лицо». добавляем кнопку в клавиатуру
    keyboard2 = types.InlineKeyboardMarkup(); #наша клавиатура №2
    keyboard2.add(types.InlineKeyboardButton(text='Заполнить профиль', callback_data='Заполнить профиль'));  #кнопка «Отправить имя профиля». добавляем кнопку в клавиатуру
                                      
    if message.text == 'Заполнить профиль':
        bot.send_message(message.from_user.id, "Выберите, кто вы:",reply_markup=keyboard1);
        bot.register_next_step_handler(message, get_type_face); #следующий шаг – функция get_type_face
    else:
        bot.send_message(message.from_user.id, 'Напиши или нажми Заполнить профиль',reply_markup=keyboard2);
        bot.register_next_step_handler(message, start_reg); #следующий шаг – функция start_reg

# функция изменения типа(get_type_face(message))
def get_type_face(message):                                     

    keyboard1 = types.InlineKeyboardMarkup(); #наша клавиатура №1
    keyboard1.add(types.InlineKeyboardButton(text='Отправить имя профиля', callback_data='Отправить имя профиля'));  #кнопка «Отправить имя профиля». добавляем кнопку в клавиатуру
    keyboard2 = types.InlineKeyboardMarkup(); #наша клавиатура №2
    keyboard2.add(types.InlineKeyboardButton(text='Юр.лицо', callback_data='Юр.лицо'));  #кнопка «Юр.лицо». добавляем кнопку в клавиатуру
    keyboard2.add(types.InlineKeyboardButton(text='Физ.лицо', callback_data='Физ.лицо'));#кнопка «Физ.лицо». добавляем кнопку в клавиатуру
      
    global type_face;
    if message.text == 'Юр.лицо':
        type_face = 'Юр.лицо';
        bot.send_message(message.from_user.id, "Напишите название компании, пожалуйста");
        bot.register_next_step_handler(message, get_company); #следующий шаг – get_company
    elif message.text == 'Физ.лицо':
        type_face = 'Физ.лицо';
        bot.send_message(message.from_user.id, "Напишите как к вам обращаться или нажмите на кнопку \"Отправить имя профиля\"",reply_markup=keyboard1);
        bot.register_next_step_handler(message, get_name); #следующий шаг – функция get_name
    else:
        bot.send_message(message.from_user.id, 'Нажмите на кнопку \"Юр.лицо\"  или \"Физ.лицо\"',reply_markup=keyboard2);
        bot.register_next_step_handler(message, get_type_face); #следующий шаг – функция get_type_face

# функция получения имени(get_name(message))
def get_name(message):                                             
    global name;
    
    if message.text == 'Отправить имя профиля':
        name = message.from_user.first_name;
    else:
        name = message.text;
    keyboard = types.InlineKeyboardMarkup(); #наша клавиатура №1
    keyboard.add(types.InlineKeyboardButton(text='Москва', callback_data='Москва'));              #кнопка «Москва». добавляем кнопку в клавиатуру
    keyboard.add(types.InlineKeyboardButton(text='Орехово-Зуево', callback_data='Орехово-Зуево'));#кнопка «Орехово-Зуево». добавляем кнопку в клавиатуру
    keyboard.add(types.InlineKeyboardButton(text='Серпухов', callback_data='Серпухов'));          #кнопка «Серпухов». добавляем кнопку в клавиатуру
    keyboard.add(types.InlineKeyboardButton(text='Калуга', callback_data='Калуга'));              #кнопка «Калуга». добавляем кнопку в клавиатуру
    
    
    bot.send_message(message.from_user.id, 'Выберите ваш город:',reply_markup=keyboard);
    bot.register_next_step_handler(message, get_address_city);

# функция получения названия компании(get_company(message))
def get_company(message):                                           
    global company;
    company = message.text;
    keyboard1 = types.InlineKeyboardMarkup(); #наша клавиатура №1
    keyboard1.add(types.InlineKeyboardButton(text='Отправить имя профиля', callback_data='Отправить имя профиля'));  #кнопка «Отправить имя профиля». добавляем кнопку в клавиатуру
    bot.send_message(message.from_user.id, "Напишите как к вам обращаться или нажмите на кнопку \"Отправить имя профиля\"",reply_markup=keyboard1);
    bot.register_next_step_handler(message, get_name); #следующий шаг – функция get_name

# функция получения названия города(get_address(message))
def get_address_city(message):
    global address;
    keyboard = types.InlineKeyboardMarkup(); #наша клавиатура №1
    keyboard.add(types.InlineKeyboardButton(text='Москва', callback_data='Москва'));              #кнопка «Москва». добавляем кнопку в клавиатуру
    keyboard.add(types.InlineKeyboardButton(text='Орехово-Зуево', callback_data='Орехово-Зуево'));#кнопка «Орехово-Зуево». добавляем кнопку в клавиатуру
    keyboard.add(types.InlineKeyboardButton(text='Серпухов', callback_data='Серпухов'));          #кнопка «Серпухов». добавляем кнопку в клавиатуру
    keyboard.add(types.InlineKeyboardButton(text='Калуга', callback_data='Калуга'));              #кнопка «Калуга». добавляем кнопку в клавиатуру
    if message.text == 'Москва':
        address = message.text;
        bot.send_message(message.from_user.id, 'Введите адрес для доставки. Укажите улицу, номер и корпус дома, номер квартиры:');
        bot.register_next_step_handler(message, get_address);
    elif message.text == 'Орехово-Зуево':
        address = message.text;
        bot.send_message(message.from_user.id, 'Введите адрес для доставки. Укажите улицу, номер и корпус дома, номер квартиры:');
        bot.register_next_step_handler(message, get_address);
    elif message.text == 'Серпухов':
        address = message.text;
        bot.send_message(message.from_user.id, 'Введите адрес для доставки. Укажите улицу, номер и корпус дома, номер квартиры:');
        bot.register_next_step_handler(message, get_address);        
    elif message.text == 'Калуга':
        address = message.text;
        bot.send_message(message.from_user.id, 'Введите адрес для доставки. Укажите улицу, номер и корпус дома, номер квартиры:');
        bot.register_next_step_handler(message, get_address);
    else:
        bot.send_message(message.from_user.id, 'Выберите ваш город:',reply_markup=keyboard);
        bot.register_next_step_handler(message, get_address_city);

# функция получения остальных данных адреса(get_address(message))
def get_address(message):
    global address;
    address = address + message.text;
    bot.send_message(message.from_user.id, 'Введите ваш номер телефона:');
    bot.register_next_step_handler(message, get_mob_phone);



# функция получения номера моб телефона(get_mob_phone(message))
def get_mob_phone(message):
    global mob_phone;
    global final_settings;
    mob_phone = message.text;
    bot.send_message(message.from_user.id, 'Спасибо! Теперь Вы можете приступить к покупкам. Не забудьте посетить наш сайт '+url_site+'.');
    final_settings = True;
