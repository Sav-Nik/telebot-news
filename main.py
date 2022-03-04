import config
import database

import telebot
import threading
from time import sleep

COUNT_NEWS = 0
BOOL_SEND = bool()

bot = telebot.TeleBot(config.token)
db = database.DataBase()

@bot.message_handler(commands=['start'])
def get_start(message):
	bot.send_message(message.chat.id, "Hello")
	db.add_user(int(message.chat.id))

@bot.message_handler(commands=['create_news'])
def create_news(message1):
	global BOOL_SEND

	bot.send_message(message1.chat.id, "Сreate new news")
	BOOL_SEND = True

	@bot.message_handler(content_types='text')
	def get_news(message2):
		global BOOL_SEND

		if BOOL_SEND:
			db.add_news([(int(message1.chat.id), message2.text)])
			BOOL_SEND = False

@bot.message_handler(commands=['end'])
def del_user(message):
	db.del_user(message.chat.id)

def check_base():
	global COUNT_NEWS

	while True:
		if COUNT_NEWS < db.return_number_news():
			list_news = db.return_news()[db.return_number_news()-COUNT_NEWS:]
			list_users = db.return_users()

			for item_news in list_news:
				for item_user in list_users:
					
					# if item_user[0] != item_news[0]:
					bot.send_message(item_user[0], item_news[1])
				COUNT_NEWS += 1
		sleep(2)

if __name__ == '__main__':
	threading.Thread(target = check_base).start()
	bot.infinity_polling()