import datetime 
import random 
import wishes
import DBController
import apscheduler

from bot import bot
from apscheduler.schedulers.blocking import BlockingScheduler


sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=60)
def send_wishes():
    connection = DBController.connect_to_db()
    cursor = connection.cursor()

    hour = datetime.datetime.now().hour  

    cursor.execute(f"""SELECT userid FROM users WHERE morning_time={hour}""")
    for userid in cursor:
        if userid:
            bot.send_message(userid[0] , wishes.good_morning_wishes[random.randint(0, len(wishes.good_morning_wishes)-1)])
    cursor.execute(f"""SELECT userid FROM users WHERE day_time={hour}""")        
    for userid in cursor:
        if userid:
            bot.send_message(userid[0] , wishes.motivated_quotes[random.randint(0, len(wishes.motivated_quotes)-1)])
    cursor.execute(f"""SELECT userid FROM users WHERE night_time={hour}""")
    for userid in cursor:
        if userid:
            bot.send_message(userid[0] , wishes.good_night_wishes[random.randint(0, len(wishes.good_night_wishes)-1)]) 
                
    cursor.close() 
    connection.commit()  

if __name__=="__main__":
    sched.start()