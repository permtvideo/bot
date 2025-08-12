import time
import telebot
import sqlite3
from datetime import datetime

def cikl():

    bot = telebot.TeleBot('8287431291:AAH-0y4YeXucOP5gkpQrC732m-Jo70PS49M')
    try:
        while True:
                if (datetime.now().second == 0 and (datetime.now().hour >= 8 or datetime.now().hour <= 1)):
                    conn = sqlite3.connect('bd_bot.db')
                    cursor = conn.cursor()
                    cursor.execute("SELECT id, user_id, user_id_2, join_date, message, username FROM users")
                    testarray = cursor.fetchall()
                    for i in range(testarray.__len__()):
                        if (int(datetime.now().timestamp()) - testarray[i][3]) >= 5400:
                            join_date = int(datetime.now().timestamp())
                            id = testarray[i][0]
                            cursor.execute("UPDATE users SET join_date=(?) WHERE id=(?)", (join_date, id))
                            if testarray[i][5] == testarray[i][2]:
                                bot.send_message(chat_id=testarray[i][1],
                                                text=str(testarray[i][0]) + ' ' + str(testarray[i][4]),
                                                reply_to_message_id=testarray[i][0])
                            else:
                                bot.send_message(chat_id=testarray[i][1], text=str(testarray[i][0]) + ' ' + 'https://t.me/' + str(testarray[i][2]) , reply_to_message_id=testarray[i][0])
                            conn.commit()
                    conn.close()
                    time.sleep(10)
    except Exception as e:
        #bot.send_message(chat_id=testarray[i][1], text='Все сломалось! Обратитесь к специалистам!')
        if " blocked " in str(e):
            cursor.execute("DELETE from users where id = (?)", (testarray[i][0], ))
            conn.commit()
            bot.send_message(chat_id=306095025, text=str(testarray[i][0]) + ' ' + str(testarray[i][2]) + '  удалено из-за блока юзером')
        else:
            if " message to be replied not found " in str(e):
            cursor.execute("UPDATE users SET join_date=(?) WHERE id=(?)", (join_date, id))
            conn.commit()
            bot.send_message(chat_id=testarray[i][1], text=str(testarray[i][0]) + ' ' + str(testarray[i][4]))
            else:
                bot.send_message(chat_id=306095025, text=str(testarray[i][0]) + ' ' + str(testarray[i][2]) + '  ' + str(e))
        conn.close()
        time.sleep(1)
        print(e)
        cikl()
cikl()


