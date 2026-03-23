[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
# Телеграм бот для взаимодейтсвия с сотрудниками MG в чатах компании. Быстрое удаление и добавление сотрудника. 

## Цели и задачи проекта
- Повышение вовлечённости
- Оптимизация управления персоналом в чатах 
- Экономия времени

## Используемый стек и технологии

### Backend

- Python, Aiogram

##  Структура и назначение папок и файлов проекта
### src/
**папка с основным кодом**

## Запуск проекта

1. **Клонируйте репозиторий и перейдите в папку проекта:**

    ```bash
    git clone git@github.com:LevKorobeinikov/MG_BOT.git
    cd MG_BOT
    ```
2. **Заполниете .env:**
    ```bash
    cp .env.example .env
   nano .env
    ```
   Нужно заполнить TOKEN: токен бота от @botfather

5. **Запустите бота:**

    ```bash
    make bot 
    ```