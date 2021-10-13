from api import get_coin_list

def check_coin_id(coin_id):
    if coin_id[1:] in get_coin_list():
        return True
    else:
        return False

def check_price_value(value):
    try:
        value = float(value)
    except:
        return False
    return True


