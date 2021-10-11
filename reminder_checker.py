from api import time_now
from api import get_price, time_now, get_price_all
from db_func import check_status, get_min_data, update_value_reminder
import requests
from settings import URL, TOKEN


def float_round(num, normal_num):
    if "." in normal_num:
        round_count = len(normal_num.split(".")[1].rstrip("0"))
    else:
        round_count = 0
    return round(num, round_count)

def check_simple_reminders():
    data_rows = get_min_data()  #TELEGRAM_ID, REM_ID, COIN_ID, REM_VALUE, VALUE_TIME, LAST_VALUE
    actual_coin_price_data = get_price_all()
    data_for_sending = {}
    for i in range(len(data_rows)):
        actual_coin_price, last_coin_price, reminder_value, current_time = actual_coin_price_data[data_rows[i][2]]['usd'], data_rows[i][5], data_rows[i][3], time_now()
        coin_change = actual_coin_price - last_coin_price
        if len(data_for_sending) == 0:
            data_for_sending['tel_id'] = data_rows[i][0]
        elif data_for_sending['tel_id'] != data_rows[i][0]:
            if len(data_for_sending) < 2:
                pass
            else:
                send_message_value(data_for_sending)
            data_for_sending.clear()
            data_for_sending['tel_id'] = data_rows[i][0]
        elif data_for_sending['tel_id'] == data_rows[i][0]:
            pass

        if coin_change/reminder_value >= 1 or coin_change/reminder_value <= -1:
            data_for_sending[data_rows[i][2]] = {'actual_coin_price': actual_coin_price, 
                        'actual_coin_price_time': current_time, 
                        'last_coin_price': last_coin_price,
                        'last_coin_price_time':data_rows[i][4],
                        'coin_change': coin_change}
            update_value_reminder(data_rows[i][1],actual_coin_price, current_time)
            
        if i == int(len(data_rows)-1):
            if len(data_for_sending) < 2:
                pass
            else:
                send_message_value(data_for_sending)
            data_for_sending.clear()


def send_message_value(data):
    message_text = ""
    for key, value in data.items():
        if key == 'tel_id':
            chat_id = value
        else:
            if value['coin_change'] > 0:
                emodji = "📈"
            else:
                emodji = "📉"
            message_text += "🔔<code>{} price change {} <strong>{} USD</strong></code>\n".format(
                                key.upper(), 
                                emodji,
                                float_round(value['coin_change'],str(value['last_coin_price'])))
            message_text += "{:^16}➡️{:^16}\n".format(
                                str(value['last_coin_price']) + " USD",
                                str(value['actual_coin_price']) + " USD")
            message_text += "{}➡️{}\n\n".format(
                                value['last_coin_price_time'],
                                value['actual_coin_price_time'])
    message_data = {
        'chat_id': chat_id,
        'text': message_text,
        'parse_mode': 'HTML' 
    }
    try:
        request = requests.post(f'{URL}{TOKEN}/sendMessage', data=message_data)
    except:
        print('Send message error')
        return False





def check_db_reminders():
    pass