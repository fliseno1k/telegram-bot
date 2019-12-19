import telebot 
import apiai, json
import datetime
import timeSettings
import DBController

from telebot.types import Message
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "1001205469:AAF8ZGi1hC5OacAiVyfa0byU9BaAfefFtCw"
AUTHOR_CHAT_ID = 457618671
bot = telebot.TeleBot(TOKEN)


'''@bot.message_handler(func=lambda message: True)
def upper(message: Message):
    bot.reply_to(message, message.text.upper())'''

#------------------
#------COMANDS-----
#------------------

#Start command
@bot.message_handler(commands=['start'])
def command_hello(message):
    bot.send_message(message.chat.id, f"""Привет, {message.from_user.first_name}, рад тебя видеть!""") 

#Send chat id to user
@bot.message_handler(commands=['my_id'])
def command_my_id(message):
    bot.send_message(message.chat.id, message.from_user.id)

@bot.message_handler(commands=['wishes'])
def command_wishes(message):
    keyboard = InlineKeyboardMarkup()
    button_yes = InlineKeyboardButton(text='Да', callback_data='Да') 
    button_no = InlineKeyboardButton(text='Нет', callback_data='Нет')   
    keyboard.add(button_yes, button_no) 

    bot.send_message(message.chat.id, 'Хотите получать пожелания от бота?', reply_markup=keyboard)

#AI mode
@bot.message_handler(func=lambda message: True)
def upper(message: Message):
    request = apiai.ApiAI('053380e328a047f79dc16bc3c739af1d').text_request() 
    request.lang = 'ru' 
    request.session_id = 'Pretty' 
    request.query = message.text
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech']
    if response:
        bot.send_message(chat_id=message.chat.id, text=response)
    else:
        bot.send_message(chat_id=message.chat.id, text='Я Вас не совсем понял!')

#Send chat id to user
@bot.message_handler(commands=['my_id'])
def command_my_id(message):
    bot.send_message(message.chat.id, message.from_user.id)


#-----------------------------
#------CALLBACK-BACKEND-------
#-----------------------------  

def aggre_to_recieve_wishes(callbackData):
    try: 
        #Calculate time difference
        time_difference = timeSettings.time_zone_difference(callbackData.data)

        #Calculate matrix of times on that server should send messages for current user
        times = timeSettings.calculate_times_message_send(time_difference)

        #Add user data into DB
        DBController.add_user_data(callbackData.message.from_user.first_name, callbackData.message.chat.id, times)

        bot.edit_message_text(chat_id=callbackData.message.chat.id, 
                              message_id=callbackData.message.message_id,
                              text='Спасибо! Операция выполнена успешно!')
    
        bot.send_message(callbackData.message.chat.id ,'Для отмены данной функции введите /wishes и в появившемся сообщении нажмите на кнопку \"Нет\".\nЕсли врем было введно неверно, или вы хотите его изменить, выполните команду /wishes заново и введите верные данные.')
    
    except Exception:
        bot.edit_message_text(chat_id=callbackData.message.chat.id, 
                              message_id=callbackData.message.message_id,
                              text='Что-то пошло не так!\nПожалуйста, повторите действие позже.')


def cancel_to_recieve_wishes(callbackData):
    try:
        DBController.delete_user_data(callbackData.message.chat.id)

        bot.edit_message_text(chat_id=callbackData.message.chat.id, 
                            message_id=callbackData.message.message_id,
                            text='Жаль, если вы передумаете, функция доступна по команде /wishes')
    except Exception:
        bot.edit_message_text(chat_id=callbackData.message.chat.id, 
                              message_id=callbackData.message.message_id,
                              text='Что-то пошло не так!\nПожалуйста, повторите действие позже.')

def create_time_zone_keyboard(callbackData):
    keyboard_time_zones = InlineKeyboardMarkup(row_width=6)
        
    keyboard_time_zones.add(InlineKeyboardButton(text='0',callback_data='0'),
                            InlineKeyboardButton(text='1',callback_data='1'),
                            InlineKeyboardButton(text='2',callback_data='2'),
                            InlineKeyboardButton(text='3',callback_data='3'),
                            InlineKeyboardButton(text='4',callback_data='4'),
                            InlineKeyboardButton(text='5',callback_data='5'))
    
    keyboard_time_zones.add(InlineKeyboardButton(text='6',callback_data='6'),
                            InlineKeyboardButton(text='7',callback_data='7'),
                            InlineKeyboardButton(text='8',callback_data='8'),
                            InlineKeyboardButton(text='9',callback_data='9'),
                            InlineKeyboardButton(text='10',callback_data='10'),
                            InlineKeyboardButton(text='11',callback_data='11'))

    keyboard_time_zones.add(InlineKeyboardButton(text='12',callback_data='12'),
                            InlineKeyboardButton(text='13',callback_data='13'),
                            InlineKeyboardButton(text='14',callback_data='14'),
                            InlineKeyboardButton(text='15',callback_data='15'),
                            InlineKeyboardButton(text='16',callback_data='16'),
                            InlineKeyboardButton(text='17',callback_data='17'))
    
    keyboard_time_zones.add(InlineKeyboardButton(text='18',callback_data='18'),
                            InlineKeyboardButton(text='19',callback_data='19'),
                            InlineKeyboardButton(text='20',callback_data='20'),
                            InlineKeyboardButton(text='21',callback_data='21'),
                            InlineKeyboardButton(text='22',callback_data='22'),
                            InlineKeyboardButton(text='23',callback_data='23'))
    
    bot.edit_message_text(chat_id=callbackData.message.chat.id,
                            message_id=callbackData.message.message_id,  
                            text='Для корректной работы бота укажите ваше время(час) в данный момент:',
                            reply_markup=keyboard_time_zones)

@bot.callback_query_handler(func=lambda clbk: clbk.data)
def callback_query(clbk):
    if clbk.data == 'Да':
        create_time_zone_keyboard(clbk)
    elif clbk.data in [str(x) for x in range(24)]:
        aggre_to_recieve_wishes(clbk)   
    elif clbk.data == 'Нет':
        cancel_to_recieve_wishes(clbk)


if __name__=="__main__":
    bot.polling()