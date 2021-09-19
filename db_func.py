import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from settings import pswd
def db_connect():
    try:
        # Подключение к существующей базе данных
        con = psycopg2.connect(user="postgres",
                                database="postgres",
                                password=pswd,
                                host="127.0.0.1",
                                port="5432")
        cur = con.cursor()
        return con, cur
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)


def table_create():
    con, cur = db_connect()
    cur.execute('''CREATE TABLE REMINDERS  
        (TELEGRAM_ID INT NOT NULL,
        REM_ID INT NOT NULL,
        REM_TYPE TEXT NOT NULL,
        REM_STATUS BOOLEAN NOT NULL,
        COIN_ID TEXT NOT NULL,
        REM_VALUE FLOAT NOT NULL,
        VALUE_TIME TIME NOT NULL,
        LAST_VALUE FLOAT NOT NULL);''')

    con.commit() 
    print("Table created successfully") 
    con.close()

def add_reminder(TELEGRAM_ID,REM_ID,REM_TYPE,REM_STATUS,COIN_ID,REM_VALUE,VALUE_TIME,LAST_VALUE):
    con, cur = db_connect()
    cur.execute(
        """INSERT INTO REMINDERS 
        (TELEGRAM_ID,REM_ID,REM_TYPE,REM_STATUS,COIN_ID,REM_VALUE,VALUE_TIME,LAST_VALUE) 
        VALUES ({},{},{},{},{},{},{},{})""".format(TELEGRAM_ID,REM_ID,REM_TYPE,REM_STATUS,COIN_ID,REM_VALUE,VALUE_TIME,LAST_VALUE)
    )
    con.commit()  
    print("Record inserted successfully")
    con.close()

def simple_reminder_get_data(REM_VALUE):
    con, cur = db_connect()
    cur.execute("SELECT TELEGRAM_ID, COIN_ID from REMINDERS where REM_TYPE='simple_type' and REM_STATUS=True and REM_VALUE = {}".format(REM_VALUE,))  
    rows = cur.fetchall()  
    for row in rows: 
        print(row)
    con.commit()  
    con.close()

def value_reminder_get_data(REM_VALUE):
    con, cur = db_connect()
    cur.execute("SELECT TELEGRAM_ID, COIN_ID from REMINDERS where REM_TYPE='value_type' and REM_STATUS=True and REM_VALUE = {}".format(REM_VALUE,))  
    rows = cur.fetchall()  
    for row in rows: 
        print(row)
    con.commit()  
    con.close()

def delete_reminder(REM_ID):
    con, cur = db_connect()
    cur.execute("DELETE from REMINDERS  where REM_ID={}".format(REM_ID,))
    con.commit()  
    con.close()

def freeze_reminder(REM_STATUS, REM_ID):
    con, cur = db_connect()
    cur.execute("UPDATE REMINDERS set REM_STATUS = {} where REM_ID = {}".format(REM_STATUS, REM_ID)) 
    con.commit()  
    con.close()

def check_status(REM_ID):
    con, cur = db_connect()
    cur.execute("SELECT REM_STATUS from REMINDERS where REM_ID={}".format(REM_ID,)) 
    status = cur.fetchone() 
    con.commit()  
    con.close()
    print(status)
    return status

def edit_reminder(REM_VALUE, REM_ID):
    con, cur = db_connect()
    cur.execute("UPDATE REMINDERS set REM_VALUE = {} where REM_ID = {}".format(REM_VALUE, REM_ID)) 
    con.commit()  
    con.close()

def show_all_reminders(TELEGRAM_ID):
    con, cur = db_connect()
    cur.execute("SELECT REM_ID, REM_TYPE, REM_STATUS, COIN_ID, REM_VALUE, VALUE_TIME, LAST_VALUE from REMINDERS where TELEGRAM_ID={}".format(TELEGRAM_ID,))  
    rows = cur.fetchall()  
    for row in rows: 
        print(row)
    con.commit()  
    con.close()
    return rows

def get_min_data():
    con, cur = db_connect()
    cur.execute("SELECT TELEGRAM_ID, REM_ID, COIN_ID, REM_VALUE, VALUE_TIME, LAST_VALUE from REMINDERS where REM_TYPE='value_type' and REM_STATUS=True ORDER BY TELEGRAM_ID")  
    rows = cur.fetchall()  
    con.commit()  
    con.close()
    return rows

def update_value_reminder(REM_ID, LAST_VALUE, VALUE_TIME):
    con, cur = db_connect()
    cur.execute("UPDATE REMINDERS set LAST_VALUE= {}, VALUE_TIME = {} where REM_ID = {}".format(LAST_VALUE, VALUE_TIME, REM_ID)) 
    con.commit()  
    con.close()

def get_new_id(TELEGRAM_ID):
    con, cur = db_connect()
    cur.execute("SELECT REM_ID from REMINDERS where TELEGRAM_ID={}".format(TELEGRAM_ID,))  
    rows = cur.fetchall()

    if len(rows) == 0:
        return int(str(TELEGRAM_ID) + "001")
    ids = [str(rows[0])[-3:] for row in rows]

    new_count = int(sorted(ids)[-1])+1
    new_id = str(TELEGRAM_ID) + "000{}".format(str(new_count))[-3:]

    con.commit()  
    con.close()
    return new_id
