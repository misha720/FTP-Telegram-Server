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
	def __init__(self):
		super(Main,self).__init__()
		
		self.token = "5820991971:AAHbItnxvAieTrGyRmQMbuov9DEz4WebtKY"
		self.bot = Bot(token=self.token)
		self.dp = Dispatcher(self.bot)

		self.root_path = "./safe/"
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

			elif input_text[0] == "download":
				search_file = input_text[1]

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

				crop_dir = os.listdir(path=self.path)

				if os.path.isdir(self.path+input_text[1]):
					self.path += input_text[1] + "/"
				else:
					await self.bot.send_message(message.from_user.id,
						"Такой папки не существует!")


		# RUN BOT
		await self.dp.start_polling(self.bot)


#	Run
if __name__ == '__main__':
	engine = Main()
	asyncio.run(engine.loop())