[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
# Телеграм бот для взаимодейтсвия с сотрудниками MG в чатах компании. Быстрое удаление и добавление сотрудника. 

## Запуск проекта

1. **Клонируйте репозиторий и перейдите в папку проекта:**
    ```bash
    git clone https://github.com/chiefheston/mg-chat-manager-bot.git
    cd mg-chat-manager-bot
    ```
   
2. **Заполниете .env:**
    ```bash
    cp .env.example .env
    nano .env
    ```
   Нужно заполнить TOKEN: токен бота от @botfather

3. **Запустите бота:**
    ```bash
    make bot 
    ```

## Базовые команды
- `make bot`: создать контейнер с ботом
- `make bot-down`: положить контейнер с ботом
- `make shell`: открыть shell контейнера с ботом
- `make logs`: прочитать логи контейнера
