import datetime

#Time difference between server and user
def time_zone_difference(user_time):
    server_time = datetime.datetime.now().hour
    difference = 0

    if (server_time == 0):
        server_time = 24
    if (user_time == 0): 
        user_time = 24

    if (user_time > server_time and user_time - server_time != 12):
        if (user_time - server_time > 12): 
            difference = (server_time - user_time + 24) * (-1)
        else:
            difference = user_time - server_time

    elif (user_time < server_time and server_time - user_time != 12):
        if (server_time - user_time > 12):
            difference = (user_time + 24) - server_time
        else:
            difference = user_time - server_time

    elif (server_time == user_time):
        difference = 0
    else:
        difference = 12
    
    return difference


#Return array of times: morning_time, day_time, night_time
def calculate_times_message_send(difference):
    morning_time = 8 + (-1)*difference
    day_time = 12 + (-1)*difference
    night_time = 22 + (-1)*difference

    results = [morning_time, day_time, night_time]

    for i in range(3):
        if results[i] > 24:
            results[i] = 0 + results[i]%24
        elif results[i] < 0:
            results[i] = 24 + results[i]
    
    return results
            