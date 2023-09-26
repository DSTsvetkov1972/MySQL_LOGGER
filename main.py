import functions
import os
import csv
from datetime import datetime

datetime_now = str(datetime.now())
# получаем параметры базы и таблицы которую нужно отслеживать
params = functions.Params_from_sqlite()
print(params)
# получаем датафрейм с текущими данными
try:    
    df_to_check = functions.Df_from_mysql(params)
    # получаем датафрейм с последними сохраненными данными
    df_last_table = functions.Df_from_sqlite(params) 
    # если что-то поменялось, записываем новые данные в базу данных
    result = functions.Checker(datetime_now,df_to_check,df_last_table)
    if result == 'Что-то поменялось!':
        functions.Mailer(params['email_recipient'], 'Changes fixed at %s for %s!'%(datetime_now,params['table'])) 
except:
    result = 'Не удалось провести проверку'
    functions.Mailer(params['email_recipient'],'Check mySQL connection parameters')

#print(list(os.walk('.'))[0][2])
if 'logger.csv' in list(os.walk('.'))[0][2]:
    with open('logger.csv', 'a', newline='',encoding='UTF-8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        spamwriter.writerow([datetime_now, result])
else:
    with open('logger.csv', 'w', newline='',encoding='UTF-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['Chect_datetime','Result'])
        writer.writeheader()
        spamwriter = csv.writer(csvfile, delimiter=',')
        spamwriter.writerow([datetime_now, result])

    
        



    
