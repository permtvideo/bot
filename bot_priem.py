import time
import telebot
import sqlite3
from datetime import datetime

bot = telebot.TeleBot('5195821377:AAF8WyEzmyl40dSTcqQp0WVYnvyJjEyUo2o')

users = {}

@bot.message_handler()
def start(message):
    if datetime.now().second == 0:
        time.sleep(1)
    conn = sqlite3.connect('bd_bot.db')
    cursor = conn.cursor()
    id = message.message_id
    user_id = message.chat.id
    username = message.chat.username
    if message.forward_from != None:
        user_id_2 = message.forward_from.username
    else:
        user_id_2 = message.from_user.username
    join_date = message.date
    message_id_to_id = message.text
    if (message.reply_to_message != None):
        id_from_text = message.reply_to_message.text.split()
        cursor.execute("DELETE from users where id = (?)", (id_from_text[1], ))
    else:
        cursor.execute("INSERT INTO users values (?, ?, ?, ?, ?, ?)", (id, user_id, user_id_2, join_date, message_id_to_id,username, ))
        bot.reply_to(message, 'запомнил')
    conn.commit()
    conn.close()
bot.polling()
