import psycopg2
import data  

def connect_to_db():
    connection = psycopg2.connect(user=data.USER,
                                password=data.PASSWORD,
                                host=data.HOST,
                                port=data.PORT,
                                database=data.DATABASE)

    '''cursor.execute("""CREATE TABLE users (id serial PRIMARY KEY,
                                        user_name VARCHAR(50) NOT NULL,
                                        chat_id INTEGER UNIQUE NOT NULL,
                                        morning_time INTEGER,
                                        day_time INTEGER,
                                        night_time INTEGER);""")'''
    return connection                               


def add_user_data(user_name, chat_id, times_array):
    #times array [day_time, morning_time, niht_time]
    connection = connect_to_db()
    cursor = connection.cursor()

    cursor.execute(f"""INSERT INTO users (user_name, chat_id, morning_time, day_time, night_time)
                      VALUES ('{user_name}', {chat_id}, {times_array[0]}, {times_array[1]}, {times_array[2]})
                      ON CONFLICT ("chat_id") DO UPDATE
                      SET morning_time = excluded.morning_time,
                          day_time = excluded.day_time,
                          night_time = excluded.night_time""")
    
    connection.commit()
    cursor.close()


def delete_user_data(chat_id):
    connection = connect_to_db()
    cursor = connection.cursor()

    cursor.execute(f"""DELETE FROM users WHERE chat_id={chat_id}""")

    connection.commit() 
    cursor.close()
