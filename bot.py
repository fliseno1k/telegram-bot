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
    request = apiai.ApiAI('81e85de2848f404bb9066c1f1b7ff5cf').text_request()
    request.lang = 'ru'
    request.session_id = 'Pretty'
    request.query = message.text
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech']
    if response:
        bot.send_message(message.chat.id, response) 


if __name__=="__main__":
    bot.polling()