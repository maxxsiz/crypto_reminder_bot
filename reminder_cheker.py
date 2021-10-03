from api import time_now
import json
from api import get_price, time_now, get_coin_list
from db_func import check_status, get_min_data, update_value_reminder
from reminder_sender import send_value_reminder, send_simple_reminder


def check_simple_reminders():
    data_rows = get_min_data()
    actual_coin_price_data = get_coin_list()
    data_for_sending = {}
    print("check_status")
    for i in range(len(data_rows)):
        actual_coin_price = actual_coin_price_data[data_rows[i][2]]['usd']
        last_coin_price = data_rows[i][5]
        reminder_value = data_rows[i][3]
        current_time = time_now()
        {'tel_id': 654654654, 'info': {'actual_coin_price', 'actual_coin_price_time', 'last_coin_price','last_coin_price_time','coin_change'}}
        coin_change = last_coin_price - actual_coin_price

        if len(data_for_sending) == 0:
            data_for_sending['tel_id'] = data_rows[i][0]
        elif data_for_sending['tel_id'] == data_rows[i][0]:
            pass
        elif data_for_sending['tel_id'] != data_rows[i][0]:
            send_value_reminder(data_for_sending)  
            data_for_sending.clear()
            data_for_sending['tel_id'] = data_rows[i][0]


        if coin_change/reminder_value >= 1:
            data_for_sending['info'] = {'actual_coin_price': actual_coin_price, 
                        'actual_coin_price_time': current_time, 
                        'last_coin_price': last_coin_price,
                        'last_coin_price_time':data_rows[i][4],
                        'coin_change': coin_change}
            update_value_reminder(data_rows[i][1],actual_coin_price, current_time)
            








def check_db_reminders():
    pass