import datetime 
import random 
import wishes
import DBController
from bot import bot

def send_wishes():
    connection = DBController.connect_to_db()
    cursor = connection.cursor()

    hour = datetime.datetime.now().hour  

    cursor.execute(f"""SELECT chat_id FROM users WHERE morning_time={hour}""")
    for userid in cursor:
        if userid:
            try:
                bot.send_message(userid[0] , wishes.good_morning_wishes[random.randint(0, len(wishes.good_morning_wishes)-1)])
            except Exception:
                DBController.delete_user_data(userid[0])
    cursor.execute(f"""SELECT chat_id FROM users WHERE day_time={hour}""")        
    for userid in cursor:
        if userid:
            try:
                bot.send_message(userid[0] , wishes.motivated_quotes[random.randint(0, len(wishes.motivated_quotes)-1)])
            except:
                DBController.delete_user_data(userid[0])
    cursor.execute(f"""SELECT chat_id FROM users WHERE night_time={hour}""")
    for userid in cursor:
        if userid:
            try:
                bot.send_message(userid[0] , wishes.good_night_wishes[random.randint(0, len(wishes.good_night_wishes)-1)]) 
            except:
                DBController.delete_user_data(userid[0]) 
    
    cursor.close() 
    connection.commit()  

if __name__=="__main__":
    send_wishes()