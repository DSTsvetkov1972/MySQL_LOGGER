import pandas as pd
import sqlite3
import pymysql


def Params_from_sqlite():
    con = sqlite3.connect("logger.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM sqlite_master where type='table'")
    if 'params' in [i[1] for i in cur.fetchall()]:
        cur.execute("SELECT * FROM params")
        params_tuple = cur.fetchone()
        params_dict = { 'host':params_tuple[0],
                        'user':params_tuple[1], 
                        'password':params_tuple[2], 
                        'database':params_tuple[3],
                        'table':params_tuple[4],
                        'email_recipient':params_tuple[5]}
    # если нет таблицы параметров, создаём таблицу с тестовым подключениме
    else:
        with con:
            cur.execute("""CREATE TABLE params (
                        host TEXT,
                        user TEXT,
                        password TEXT,
                        database TEXT,
                        `table` TEXT,
                        email_recipient TEXT);
                        """)
            cur.execute("""INSERT INTO params /*(host,user,password,database,`table`)*/
                        VALUES ('vh368.timeweb.ru'
                                ,'cm62750_logger'
                                ,'#$%^&*'
                                ,'cm62750_loggerrr'
                                ,'test'
                                ,'dstsvetkovpro@yandex.ru');
                        """)
            cur.execute("""SELECT * FROM params""")    
            params_dict = { 'host':'vh368.timeweb.ru',
                            'user':'cm62750_logger', 
                            'password':'#$%^&*', 
                            'database':'cm62750_loggerrr',
                            'table':'test',
                            'email_recipient':'dstsvetkovpro@yandex.ru'}

    return params_dict

Params_from_sqlite()

def Df_from_mysql(params):
    con = pymysql.connect(
                            host = params['host'],
                            user = params['user'], 
                            password = params['password'], 
                            database = params['database']
                            )
    with con:
        cur = con.cursor()        
        cur.execute("SELECT * FROM %s"%(params['table']))
        return pd.DataFrame(cur.fetchall())

def Df_from_sqlite(params):
    con = sqlite3.connect("logger.db")
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM sqlite_master where type='table'")
        tables_in_logger = [i[1] for i in cur.fetchall() if i[1] != 'params']
        if tables_in_logger:
            last_table_name = max(tables_in_logger)    
            cur.execute("SELECT * FROM '%s'"%(last_table_name))
            return pd.DataFrame(cur.fetchall())  

def Checker(datetime_now,df_to_check,df_last_table):
    print(df_to_check)
    print(df_last_table)
    if df_to_check.equals(df_last_table):
        return ('Ничего не поменялось!')
    else:
        con = sqlite3.connect("logger.db")
        with con:
            df_to_check.to_sql(datetime_now, con, index=False)
        return ('Что-то поменялось!')
    
def Mailer (mail_recipient, text):
    import smtplib as smtp

    server = smtp.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('mob89036177755@gmail.com', 'qfakqivdmvqvojfu')

    subject = 'Logger writes...'
    server.sendmail('mob89036177755@gmail.com', mail_recipient, f'Subject:{subject}\n{text}')  
