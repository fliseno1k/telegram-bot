import psycopg2

def connect_to_db():
    connection = psycopg2.connect(user='uvddpqdceppasb',
                                password='4e130ef2da468e7125a52c52f064a0859473974a775ec5fe20f433b5b893d326',
                                host='ec2-46-137-187-23.eu-west-1.compute.amazonaws.com',
                                port = "5432",
                                database='d18kjd71r1b36b')

    '''cursor.execute("""CREATE TABLE users (id serial PRIMARY KEY,
                                        user_name VARCHAR(50) NOT NULL,
                                        chat_id INTEGER UNIQUE NOT NULL,
                                        morning_time INEGER,
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
