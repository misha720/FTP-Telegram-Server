# FTP Telegram Server

#### Данный инструмент позволяет быстро разворачивать свои "Папки общего доступа" ( тут они называются ftp-server )
### Настройка:
В первый запуск main.py Вам понадобиться настроить Бота.
1. Первым параметом идёт токен бота
2. Далее укажите папку общего доступа. Рекомендую использовать папку в той же дириктории что и файл main.py, то есть создайте папку и уже туда перекидывайте свои файлы.
С терминалом всё!
### Настройка Рут прав
Данный бот даёт Вам возможность не только скачивать файлы, но и загружать их. Но в целях безопасности - может это делать только пользователи которым можно доверять.
Что бы установить кого то в роли root-пользователя, нужно открыть файл config.json и вписать свой ID аккаунта под ключом root-users.
*** Что бы загрузить данные на сервер: ***
- Перейдите в нужную папку
- Отправьте любой тип как файл(то есть даже картинку или видео нужно отправлять как файл)

### Список команд:
|Команда|Доп. параметр|Описание|Пример|
|--|--|--|--|
|**ls**|Нет|*Выводит содержание папки*|***ls***|
|**pwd**|Нет|*Выводит папку в который Вы находитесь*|***pwd***|
|**cd**|Имя папки|*Переходит в указанную папку*|***cd dir2***|
|**download**|Имя файла|*Присылает указанный файл*|***download file.txt***|
