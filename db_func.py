import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from settings import pswd
def db_connect():
    try:
        con = psycopg2.connect(user="postgres",
                                database="postgres",
                                password=pswd,
                                host="127.0.0.1",
                                port="5432")
        cur = con.cursor()
        return con, cur
    except (Exception, Error) as error:
        print("Error at working with PostgreSQL", error)


def table_create():
    con, cur = db_connect()
    cur.execute('''CREATE TABLE REMINDERS  
        (TELEGRAM_ID BIGINT NOT NULL,
        REM_ID BIGINT NOT NULL,
        REM_TYPE TEXT NOT NULL,
        REM_STATUS BOOLEAN NOT NULL,
        COIN_ID TEXT NOT NULL,
        REM_VALUE FLOAT NOT NULL,   
        VALUE_TIME TEXT,
        LAST_VALUE FLOAT );''')

    con.commit() 
    print("Table created successfully") 
    con.close()

def delete_table():
    con, cur = db_connect()
    cur.execute('DROP TABLE IF EXISTS REMINDERS')
    con.commit() 
    print("Table delete successfully") 
    con.close()

def add_reminder(TELEGRAM_ID,REM_ID,REM_TYP,REM_STATUS,COIN_ID,REM_VALUE,VALUE_TIME,LAST_VALUE):
    con, cur = db_connect()
    cur.execute(
        """INSERT INTO REMINDERS 
        (TELEGRAM_ID,REM_ID,REM_TYPE,REM_STATUS,COIN_ID,REM_VALUE,VALUE_TIME,LAST_VALUE) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",(TELEGRAM_ID,REM_ID,str(REM_TYP),REM_STATUS,COIN_ID,REM_VALUE,VALUE_TIME,LAST_VALUE)
    )
    con.commit()  
    print("Record inserted successfully")
    con.close()

def simple_reminder_get_data(REM_VALUE):
    con, cur = db_connect()
    cur.execute("SELECT TELEGRAM_ID, COIN_ID from REMINDERS where REM_TYPE='simple_typ' and REM_STATUS=True and REM_VALUE = %s;",(REM_VALUE,))  
    rows = cur.fetchall()  
    for row in rows: 
        print(row)
    con.commit()  
    con.close()

def value_reminder_get_data(REM_VALUE):
    con, cur = db_connect()
    cur.execute("SELECT TELEGRAM_ID, COIN_ID from REMINDERS where REM_TYPE='value_typ' and REM_STATUS=True and REM_VALUE = %s;",(REM_VALUE,))  
    rows = cur.fetchall()  
    for row in rows: 
        print(row)
    con.commit()  
    con.close()

def delete_reminder(REM_ID):
    con, cur = db_connect()
    cur.execute("DELETE from REMINDERS  where REM_ID=%s;",(REM_ID,))
    con.commit()  
    con.close()

def freeze_reminder(REM_STATUS, REM_ID):
    con, cur = db_connect()
    cur.execute("UPDATE REMINDERS set REM_STATUS = %s where REM_ID = %s;",(REM_STATUS, REM_ID)) 
    con.commit()  
    con.close()

def check_status(REM_ID):
    con, cur = db_connect()
    cur.execute("SELECT REM_STATUS from REMINDERS where REM_ID=%s;",(REM_ID,)) 
    status = cur.fetchone()[0]
    con.commit()  
    con.close()
    return status

def edit_reminder(REM_ID, REM_VALUE):
    con, cur = db_connect()
    cur.execute("UPDATE REMINDERS set REM_VALUE = %s where REM_ID = %s;",(REM_VALUE, REM_ID)) 
    con.commit()  
    con.close()
    print("done")

def show_all_reminders(TELEGRAM_ID):
    con, cur = db_connect()
    cur.execute("SELECT REM_ID, REM_TYPE, REM_STATUS, COIN_ID, REM_VALUE, VALUE_TIME, LAST_VALUE from REMINDERS where TELEGRAM_ID=%s;",(TELEGRAM_ID,))  
    rows = cur.fetchall()  
    con.commit()  
    con.close()
    simple_text = "SIMPLE TYPE\n" + "{:^16} | {:^12} | {:^9} | {}\n".format("Reminder ID","Coin","Time step","Status",)
    value_text = "\nVALUE TYPE\n" + "{:^16} | {:^12} | {:^10} | {} | {:^12}\n".format("Reminder ID","Coin","Price step","Status","Last price")
    for row in rows: 
        if row[1]=='simple_typ':
            simple_text += "{:^16} | {:^12} | {:^9} | {:^6}\n".format("/"+str(row[0]), row[3], str(row[4]) + "hour(s)", row[2])
        else:
            value_text += "{:^16} | {:^12} | {:^10} | {:^6} | {:^12} , {}\n".format("/"+str(row[0]), row[3], str(row[4])+"$", row[2], str(row[6])+"$ ", row[5])
    text = simple_text + value_text
    return text

def get_min_data():
    con, cur = db_connect()
    cur.execute("SELECT TELEGRAM_ID, REM_ID, COIN_ID, REM_VALUE, VALUE_TIME, LAST_VALUE from REMINDERS where REM_TYPE='value_typ' and REM_STATUS=True ORDER BY TELEGRAM_ID")  
    rows = cur.fetchall()  
    con.commit()  
    con.close()
    return rows

def update_value_reminder(REM_ID, LAST_VALUE, VALUE_TIME):
    con, cur = db_connect()
    cur.execute("UPDATE REMINDERS set LAST_VALUE= %s, VALUE_TIME = %s where REM_ID = %s;",(LAST_VALUE, VALUE_TIME, REM_ID)) 
    con.commit()  
    con.close()

def get_new_id(TELEGRAM_ID):
    con, cur = db_connect()
    cur.execute("SELECT REM_ID from REMINDERS where TELEGRAM_ID=%s;",(TELEGRAM_ID,))  
    rows = cur.fetchall()
    if len(rows) == 0:
        return int(str(TELEGRAM_ID) + "001")
    ids = [str(row[0])[-3:] for row in rows]
    new_count = int(sorted(ids)[-1])+1
    new_id = str(TELEGRAM_ID) + "000{}".format(str(new_count))[-3:]
    con.commit()  
    con.close()
    return new_id

def reminder_id_list(TELEGRAM_ID):
    con, cur = db_connect()
    cur.execute("SELECT REM_ID from REMINDERS where TELEGRAM_ID=%s;",(TELEGRAM_ID,)) 
    rows = cur.fetchall() 
    con.commit()  
    con.close()
    id_list = [int(row[0]) for row in rows]
    return id_list


def check_reminder_type(REM_ID):
    con, cur = db_connect()
    cur.execute("SELECT REM_TYPE from REMINDERS where REM_ID=%s;",(REM_ID,)) 
    rem_type = cur.fetchone()[0] 
    con.commit()  
    con.close()
    return rem_type

def get_all_data():
    con, cur = db_connect()
    cur.execute("SELECT * from REMINDERS ")  
    rows = cur.fetchall()  
    con.commit()  
    con.close()
    for row in rows:
        print(row)
