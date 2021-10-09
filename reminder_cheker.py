from api import time_now
import json
from api import get_price, time_now, get_price_all
from db_func import check_status, get_min_data, update_value_reminder
from reminder_sender import send_value_reminder, send_simple_reminder
from misc import dp, bot
import asyncio

def check_simple_reminders():
    data_rows = get_min_data()  #TELEGRAM_ID, REM_ID, COIN_ID, REM_VALUE, VALUE_TIME, LAST_VALUE
    actual_coin_price_data = get_price_all()
    data_for_sending = {}
    print(data_rows)
    for i in range(len(data_rows)):
        print(i)
        print(len(data_rows))
        actual_coin_price = actual_coin_price_data[data_rows[i][2]]['usd']
        last_coin_price = data_rows[i][5]
        reminder_value = data_rows[i][3]
        current_time = time_now()
        coin_change = last_coin_price - actual_coin_price

        if len(data_for_sending) == 0:
            print("пустой")
            data_for_sending['tel_id'] = data_rows[i][0]
        elif data_for_sending['tel_id'] != data_rows[i][0]:
            print("новый")
            asyncio.run(send_value_reminder(data_for_sending))
            data_for_sending.clear()
            data_for_sending['tel_id'] = data_rows[i][0]
        elif data_for_sending['tel_id'] == data_rows[i][0]:
            print("уже есть")
            pass

        if coin_change/reminder_value >= 1 or coin_change/reminder_value <= -1:
            print("запись на отправку")
            data_for_sending[data_rows[i][2]] = {'actual_coin_price': actual_coin_price, 
                        'actual_coin_price_time': current_time, 
                        'last_coin_price': last_coin_price,
                        'last_coin_price_time':data_rows[i][4],
                        'coin_change': coin_change}
            update_value_reminder(data_rows[i][1],actual_coin_price, current_time)
            
        if i == int(len(data_rows)-1):
            print("конец и отправляем")
            asyncio.run(send_value_reminder(data_for_sending)) 
            data_for_sending.clear()







def check_db_reminders():
    pass