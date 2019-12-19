import telebot 
import apiai, json

from telebot.types import Message


TOKEN = "1001205469:AAF8ZGi1hC5OacAiVyfa0byU9BaAfefFtCw"
AUTHOR_CHAT_ID = None
bot = telebot.TeleBot(TOKEN)


'''@bot.message_handler(func=lambda message: True)
def upper(message: Message):
    bot.reply_to(message, message.text.upper())'''

#Start command
@bot.message_handler(commands=['start'])
def command_hello(message):
    bot.send_message(message.chat.id, f"""Привет, {message.from_user.first_name}, рад тебя видеть!""") 

#Send chat id to user
@bot.message_handler(commands=['my_id'])
def command_my_id(message):
    bot.send_message(message.chat.id, message.from_user.id)

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
      
if __name__=="__main__":
    bot.polling()