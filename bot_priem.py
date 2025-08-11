import time
import telebot
import sqlite3
from datetime import datetime


def cikl():
    bot = telebot.TeleBot('8287431291:AAH-0y4YeXucOP5gkpQrC732m-Jo70PS49M')
    try:
        @bot.message_handler()
        def start(message):
                if message.text == '/start' or message.text == '/help':
                    bot.send_message(chat_id=message.chat.id, text='Привет! Я бот-напоминалка. ' +
                                                                   'Любое отправленное мне сообщение будет запомнено и возвращено Вам через полтора часа. ' +
                                                                   'Если необходимо напомнить через другое время, то надо ответить на мое сообщение,' +
                                                                   ' в котором содержится ссылка на запомненную информацию, числом (можно использовать дробное число, например 0,5)' +
                                                                   ' и указать время в часах, начиная от текущего момента. После срабатывания напоминания, оно перейдет в режим ожидания на следующие полтора часа, время снова можно изменить, ответив на мое сообщение. Также можно запоминать пересланные из других чатов сообщения, тогда я напомню вам в каком чате требуется ваш ответ. Чтобы удалить напоминание, ответьте мне любым символом, кроме числа. Для вызова справки используйте команду /start или /help.')
                else:
                    if datetime.now().second == 0:
                        time.sleep(1)
                    conn = sqlite3.connect('bd_bot.db')
                    cursor = conn.cursor()
                    id = message.message_id
                    user_id = message.chat.id
                    username = message.chat.username
                    if message.forward_from != None:
                        if message.forward_from.username != None:
                            user_id_2 = message.forward_from.username
                        else:
                            user_id_2 = message.forward_from.id
                    else:
                        user_id_2 = message.from_user.username
                    join_date = message.date
                    message_id_to_id = message.text
                    if (message.reply_to_message != None):
                        proverka = message.text.replace(",", ".")
                        id_from_text = message.reply_to_message.text.split()
                        try:
                            join_date = int(message.date - 5400 + float(proverka) * 3600)
                            now = datetime.fromtimestamp(join_date + 5400)
                            week = int(now.strftime("%w"))
                            if week >= 6:
                                day = "суббота"
                            elif week >= 5:
                                day = 'пятница'
                            elif week >= 4:
                                day = 'четверг'
                            elif week >= 3:
                                day = 'среда'
                            elif week >= 2:
                                day = 'вторник'
                            elif week == 1:
                                day = 'понедельник'
                            else:
                                day = 'воскресенье'
                            cursor.execute("UPDATE users SET join_date=(?) WHERE id=(?)", (join_date, id_from_text[0]))
                            bot.send_message(chat_id=message.chat.id, text=str(id_from_text[0]) + ' Напоминание было перенесено на ' + str(now.strftime("%d.%m ")) + str(day) + str(now.strftime(" %H:%M")))
                        except ValueError:
                            cursor.execute("DELETE from users where id = (?)", (id_from_text[0], ))
                            bot.reply_to(message, text=str(id_from_text[0]) + ' Напоминание было удалено')
                    else:
                        cursor.execute("INSERT INTO users values (?, ?, ?, ?, ?, ?)", (id, user_id, user_id_2, join_date, message_id_to_id,username, ))
                        bot.reply_to(message, str(id) + ' Ответ цифрой задает время напоминания (в часах), другим символом отменяет его')
                    conn.commit()
                    conn.close()
        bot.polling()
    except Exception as e:
        bot.infinity_polling()
        time.sleep(1)
        cikl()
cikl()

