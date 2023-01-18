

#	Import
import asyncio
import random
import datetime
import time
import os
import json


#		AIOGRAM
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton


class Main():
	def __init__(self, config):
		super(Main,self).__init__()
		
		self.token = config['token_bot']
		self.bot = Bot(token=self.token)
		self.dp = Dispatcher(self.bot)

		self.root_users = config['root_users']
		self.root_path = config['root_path']
		self.path = self.root_path

	async def loop(self):

		# OnStarted
		@self.dp.message_handler(commands=["start"])
		async def start_command(message: Message):
			await self.bot.send_message(message.from_user.id,
				"Добро пожаловать в FTP-Client")

		# FTP COMMAND
		@self.dp.message_handler(content_types="text")
		async def text_types(message: Message):

			input_text = str(message.text)
			input_text = input_text.split()

			if input_text[0] == "ls":
				crop_dir = os.listdir(path=self.path)

				output_to_bot = "В папке - '" + self.path + "' найдено:\n"
				for file_name in crop_dir:
					output_to_bot += file_name + "\n"

				await self.bot.send_message(message.from_user.id,
				output_to_bot)

			elif input_text[0] == "get":
				search_file = input_text[1]

				if search_file == "#all":

					crop_dir = os.listdir(path=self.path)
					for file_name in crop_dir:
						await message.reply_document(open(self.path+file_name, 'rb'))
				
				else:
					if os.path.isfile(self.path+search_file):
						await self.bot.send_message(message.from_user.id,
							"Отправляю...")
						await message.reply_document(open(self.path+search_file, 'rb'))
					else:
						await self.bot.send_message(message.from_user.id,
							"Такого файла не существует!")

			elif input_text[0] == "pwd":
				await self.bot.send_message(message.from_user.id,
				self.path)

			elif input_text[0] == "cd":

				if input_text[1] == '~':
					self.path = self.root_path

				else:
					crop_dir = os.listdir(path=self.path)

					if os.path.isdir(self.path+input_text[1]):
						self.path += input_text[1] + "/"
					else:
						await self.bot.send_message(message.from_user.id,
							"Такой папки не существует!")

		@self.dp.message_handler(content_types=["document"])
		async def add_file(file: Message):
			if self.check_root(file.chat.id):
				random_path = self.path+"file_"+str(random.randint(1000, 9999))

				print("downloading document - "+str(file.document.file_id))

				file_id = file.document.file_id
				file = await self.bot.get_file(file_id)
				await self.bot.download_file(file.file_path, random_path)
			else:
				await self.bot.send_message(file.chat.id,"Отказано в доступе!")

		# RUN BOT
		await self.dp.start_polling(self.bot)


	# FUNCTION
	def check_root(self, user_id):
		# Проверяет, является ли пользователь рут пользователем
		for user in self.root_users:
			if user == str(user_id):
				return True
		return False
		

#	Run
if __name__ == '__main__':

	# Проверка CONFIG
	if os.path.isfile('config.json'):
		with open("config.json",'r') as file_config:
			config = json.load(file_config)
	else:
		# Get Value
		config = {}
		config['token_bot'] = input("Введите токен ftp-клиента: ")
		config['root_path'] = input('Введите путь до "Папки общего доступа": ')
		config['root_users'] = []

		with open("config.json",'w') as file_config:
			json.dump(config, file_config)

	# RUN
	engine = Main(config)
	asyncio.run(engine.loop())