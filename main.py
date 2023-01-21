

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
	def __init__(self, config, list_user):
		super(Main,self).__init__()
		
		self.token = config['token_bot']
		self.bot = Bot(token=self.token)
		self.dp = Dispatcher(self.bot)

		self.root_users = config['root_users']
		self.root_path = config['root_path']
		self.path = self.root_path
		self.users = list_user
		self.second_user = {}

	async def loop(self):

		# OnStarted
		@self.dp.message_handler(commands=["start"])
		async def start_command(message: Message):

			self.check_user(message.from_user.id)

			await self.bot.send_message(message.from_user.id,
				"Добро пожаловать в FTP-Client")

		# FTP COMMAND
		@self.dp.message_handler(content_types="text")
		async def text_types(message: Message):

			input_text = str(message.text).lower()
			input_text = input_text.split()

			if input_text[0] == "ls":
				self.check_user(message.from_user.id)

				crop_dir = os.listdir(path=self.path)

				output_to_bot = "В папке - '" + self.path + "' найдено:\n"
				for file_name in crop_dir:
					output_to_bot += file_name + "\n"

				await self.bot.send_message(message.from_user.id,
				output_to_bot)

			elif input_text[0] == "get":
				self.check_user(message.from_user.id)

				search_file = input_text[1]

				if search_file == "#all":

					crop_dir = os.listdir(path=self.second_user['path'])
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
				self.check_user(message.from_user.id)
				await self.bot.send_message(message.from_user.id,
				self.path)

			elif input_text[0] == "cd":
				self.check_user(message.from_user.id)
				if input_text[1] == '~':
					self.path = self.root_path
					self.cd_path(message.from_user.id,self.path)

				else:
					crop_dir = os.listdir(path=self.path)

					if os.path.isdir(self.path+input_text[1]):
						self.path += input_text[1] + "/"
						self.cd_path(message.from_user.id,self.path)
					else:
						await self.bot.send_message(message.from_user.id,
							"Такой папки не существует!")

		@self.dp.message_handler(content_types=["document"])
		async def add_file(file: Message):
			self.check_user(file.chat.id)

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

	def save_users(self):
		with open("users.json",'w') as file_users:
			json.dump(self.users, file_users)

	def check_user(self, user_id):
		if len( self.users ) != 0:
			for user in self.users:
				if user['user_id'] == user_id:
					self.path = user['path']
					return
			self.add_user(user_id)
		else:
			self.users.append({
				"user_id":user_id,
				"path":self.root_path
				})
			self.save_users()

	def add_user(self, user_id):
		new_lot = {
			"user_id" : user_id,
			"path" : self.root_path
		}
		self.users.append(new_lot)
		self.save_users()

	def cd_path(self, user_id, path):
		for user_item in range(len(self.users)):
			if user_id == self.users[user_item]['user_id']:
				self.users[user_item]['path'] = str(path)
				self.save_users()

		

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

	# Users
	if os.path.isfile('users.json'):
		with open("users.json",'r') as file_users:
			list_user = json.load(file_users)
	else:
		list_user = []
		with open("users.json",'w') as file_users:
			json.dump(list_user, file_users)


	# RUN
	engine = Main(config, list_user)
	asyncio.run(engine.loop())