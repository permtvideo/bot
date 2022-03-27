import time
import telebot
import sqlite3
from datetime import datetime

bot = telebot.TeleBot('5195821377:AAF8WyEzmyl40dSTcqQp0WVYnvyJjEyUo2o')

while True:
        if (datetime.now().second == 0) & ((datetime.now().hour >=8) or (datetime.now().hour <=1)):
            conn = sqlite3.connect('bd_bot.db')
            cursor = conn.cursor()
            cursor.execute("SELECT id, user_id, user_id_2, join_date, message, username FROM users")
            testarray = cursor.fetchall()
            for i in range(testarray.__len__()):
                if (int(datetime.now().timestamp()) - testarray[i][3]) >= 60:
                    join_date = int(datetime.now().timestamp())
                    id = testarray[i][0]
                    cursor.execute("UPDATE users SET join_date=(?) WHERE id=(?)", (join_date, id))
                    if testarray[i][5] == testarray[i][2]:
                        bot.send_message(chat_id=testarray[i][1],
                                         text='Напоминалка' + ' ' + str(testarray[i][0]),
                                         reply_to_message_id=testarray[i][0])
                    else:
                        bot.send_message(chat_id=testarray[i][1], text='https://t.me/' + testarray[i][2] + ' ' + str(testarray[i][0]), reply_to_message_id=testarray[i][0])
                    conn.commit()
            conn.close()
