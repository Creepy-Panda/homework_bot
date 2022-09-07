# Bot-Assistent

### Технологии:
![Python-telegram-bot](https://img.shields.io/badge/python-python--telegram--bot-red?style=for-the-badge&logo=appveyor)

## Описание проекта

***Функционал***

  - *обращается к API сервиса Практикум.Домашка: проверяет каждые 30 минут взято ли задание на проверку. если взято, то присылает уведомление зачтено или нет*
  - *логирует свою работу и присылает уведомление в случае ошибки.*

  - *присылает сообщения о статусе выполнения workflow, подключенного стороннего проекта*

## Запуск бота:
1. Клонируйте репозиторий:
```
    git clone https://github.com/Creepy-Panda/homework_bot.git
```
 
2. Создайте виртуальное окружение - должен быть флажок (venv)в начале строки:
```
    python -m venv venv
```
 
3. Установите зависимости:
```
    pip install -r requirements.txt
```

4. Создайте аккаунт бота в мессенджере Telegram:
    
5. Полученные токкены запишите за место PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID или запишите их в .env файле для безопасности
