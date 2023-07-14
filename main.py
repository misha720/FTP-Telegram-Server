"""
    FTPServer v1.0
    Powered by S-Ch
"""

# Import
import asyncio
import random
import os

# AIOGRAM
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ParseMode


class Main:
    def __init__(self):
        self.token = "5905474933:AAHwSlNgnKF6XweS4vNkWmGDecDnCT0oWpg"
        self.bot = Bot(token=self.token)
        self.dp = Dispatcher(self.bot)

    async def loop(self):
        # При запуске бота
        @self.dp.message_handler(commands=["start"])
        async def start_command(message: Message):
            await self.bot.send_message(message.from_user.id,
                                        "Добро пожаловать в FTP-Client")

        # Если пользователь просит список команд
        @self.dp.message_handler(commands=["help"])
        async def start_command(message: Message):
            content = """
            _Привет Друг!_
            
Этот бот позволит тебе *быстро сохранять свои файлы на сервере* - это удобно!
По этому давай я расскажу тебе о его функционале)
            
`/ls` - команда *выведет* все твои сохранёные файлы.
`/get` - после этой команды введи название файла и *бот тебе его пришлёт*.
*А если хочешь вывести все файлы*, то напиши `/get #all`.
            
Что бы не переписывать название файла в ручнуюю *просто нажми на его название(оно сохраниться в буфер)*.
            
Ну и на конец, *что бы загрузить в бота фото, видео или файл - просто отправь его!*
            """
            await self.bot.send_message(message.from_user.id,
                                        text=content,
                                        parse_mode=ParseMode.MARKDOWN)

        # Вывести все файлы
        @self.dp.message_handler(commands=["ls"])
        async def start_command(message: Message):
            if self.check_user(message.from_user.id):
                user_files = self.get_user_files(message.from_user.id)

                content = "Список файлов:\n"
                for item_user_files in user_files:
                    content += '`' + item_user_files +'`\n'

                await self.bot.send_message(message.from_user.id,
                                            text=content, parse_mode=ParseMode.MARKDOWN)
            else:
                await self.bot.send_message(message.from_user.id,
                                            "Вы здесь впервые, но мы создали для вас хранилище. Вы уже можете им воспользоваться!")

        # Загрузка звука на сервер
        @self.dp.message_handler(content_types=["audio"])
        async def process_photo(message: types.Message):
            if self.check_user(message.from_user.id):
                await self.bot.send_message(message.from_user.id,
                                            "Хорошо, это может занять некоторое время.")
            else:
                await self.bot.send_message(message.from_user.id,
                                            "Вы здесь впервые, но мы создали для вас хранилище. Не волнуйтесь, я загружу ваш первый файл!")

            file_name = "./data/" + str(message.from_user.id) + "/" + message.audio.file_name

            await message.audio.download(file_name)

            await self.bot.send_message(message.from_user.id,
                                        "Готово!")

        # Загрузка фото на сервер
        @self.dp.message_handler(content_types=["photo"])
        async def process_photo(message: types.Message):
            if self.check_user(message.from_user.id):
                await self.bot.send_message(message.from_user.id,
                                            "Хорошо, это может занять некоторое время.")
            else:
                await self.bot.send_message(message.from_user.id,
                                            "Вы здесь впервые, но мы создали для вас хранилище. Не волнуйтесь, я загружу ваш первый файл!")

            file_name = "./data/" + str(message.from_user.id) + "/" + str(
                random.randint(1000000000, 9999999999)) + ".jpg"

            await message.photo[-1].download(file_name)

            await self.bot.send_message(message.from_user.id,
                                        "Готово!")

        # Загрузка видео на сервер
        @self.dp.message_handler(content_types=["video"])
        async def download_video(message: types.Message):

            if self.check_user(message.from_user.id):
                await self.bot.send_message(message.from_user.id,
                                            "Хорошо, это может занять некоторое время.")
            else:
                await self.bot.send_message(message.from_user.id,
                                            "Вы здесь впервые, но мы создали для вас хранилище. Не волнуйтесь, я загружу ваш первый файл!")

            file_id = message.video.file_id
            user_id = message.from_user.id
            file_name = "./data/" + str(user_id) + "/" + str(random.randint(1000000000, 9999999999)) + ".mp4"

            file = await self.bot.get_file(file_id)

            await self.bot.download_file(file.file_path, file_name)

            await self.bot.send_message(user_id,
                                        "Готово!")

        # Загрузка файла на сервер
        @self.dp.message_handler(content_types=["document"])
        async def add_file(file: Message):

            if self.check_user(file.chat.id):
                await self.bot.send_message(file.chat.id,
                                            "Хорошо, это может занять некоторое время.")
            else:
                await self.bot.send_message(file.chat.id,
                                            "Вы здесь впервые, но мы создали для вас хранилище. Не волнуйтесь, я загружу ваш первый файл!")

            print("downloading document - " + str(file.document.file_name))

            user_id = file.chat.id
            file_name = "./data/" + str(file.chat.id) + "/" + file.document.file_name
            file_id = file.document.file_id

            file = await self.bot.get_file(file_id)

            await self.bot.download_file(file.file_path, file_name)

            await self.bot.send_message(user_id,
                                        "Готово!")

        # Сторонние команды для сервера
        @self.dp.message_handler(content_types="text")
        async def text_types(message: Message):

            if self.check_user(message.from_user.id):
                # Получаем и обрабатываем запрос
                input_text = str(message.text).lower()
                input_text = input_text.split()

                if input_text[0] == "get":
                    """
                        Получить файл
                    """
                    search_file = input_text[1]
                    user_path = "./data/" + str(message.from_user.id) + "/"

                    if search_file == "#all":
                        # Если пользователь запросил все файлы
                        list_files = self.get_user_files(message.from_user.id)

                        for file_name in list_files:
                            await message.reply_document(open(user_path + file_name, 'rb'))

                    if os.path.isfile(user_path + search_file):
                        # Если пользователь запросил определённый файл
                        await message.reply_document(open(user_path + search_file, 'rb'))
                    else:
                        await self.bot.send_message(message.from_user.id,
                                                    "Такого файла не существует!")

            else:
                await self.bot.send_message(message.from_user.id,
                                            "Вы здесь впервые, но мы создали для вас хранилище. Вы уже можете им воспользоваться!")

        # RUN BOT
        await self.dp.start_polling(self.bot)

    @staticmethod
    def create_new_user(url):
        """
            Создаёт папку с id пользователя
        """
        os.mkdir("./data/" + str(url) + "/")

    def check_user(self, url):
        """
            Проверяет на существование юзера
        """
        if os.path.isdir("./data/" + str(url) + "/"):
            return True
        else:
            self.create_new_user(url)
            return False

    @staticmethod
    def get_user_files(url):
        """
            Возвращает список файлов юзера
        """
        return os.listdir("./data/" + str(url) + "/")


# RUN
if __name__ == '__main__':
    engine = Main()
    asyncio.run(engine.loop())
