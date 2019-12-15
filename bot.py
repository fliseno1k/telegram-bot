import telebot 
import apiai, json

from telebot.types import Message


TOKEN = "1001205469:AAF8ZGi1hC5OacAiVyfa0byU9BaAfefFtCw"
bot = telebot.TeleBot(TOKEN)


'''@bot.message_handler(func=lambda message: True)
def upper(message: Message):
    bot.reply_to(message, message.text.upper())'''


#AI mode
@bot.message_handler(func=lambda message: True)
def upper(message: Message):
    request = apiai.ApiAI('053380e328a047f79dc16bc3c739af1d').text_request() 
    request.lang = 'ru' 
    request.session_id = 'Pretty' 
    request.query = update.message.text
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech']
    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Я Вас не совсем понял!')

      
if __name__=="__main__":
    bot.polling()