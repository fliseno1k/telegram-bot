import telebot 
from telebot.types import Message



TOKEN = "1001205469:AAF8ZGi1hC5OacAiVyfa0byU9BaAfefFtCw"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def upper(message: Message):
    bot.reply_to(message, message.text.upper())

if __name__=="__main__":
    bot.polling()