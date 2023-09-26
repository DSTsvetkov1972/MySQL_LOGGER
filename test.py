'''
import smtplib as smtp

server = smtp.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('mob89036177755@gmail.com', 'qfakqivdmvqvojfu')

subject = 'aaa'
text = 'bbb'
server.sendmail('mob89036177755@gmail.com', 'tsvetkovds@trcont.ru', f'Subject:{subject}\n{text}') 
'''

import smtplib as smtp

login = 'mob89036177755@gmail.com'
password = 'qwihwocfbxctxeip'

server = smtp.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(login, password)

subject = '123'
text = 'aaafgfdgfdg'

server.sendmail(login, 'tsvetkovds@trcont.ru', f'Subject:{subject}\n{text}')