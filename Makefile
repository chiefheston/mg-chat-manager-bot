DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
BOT_CONTAINER = mg_telegram_chat_manager_bot
BOT_FILE = docker-compose.yaml
ENV = --env-file .env

.PHONY: bot
bot:
	${DC} -f ${BOT_FILE} ${ENV} up --build -d

.PHONY: bot-down
bot-down:
	${DC} -f ${BOT_FILE} ${ENV} down

.PHONY: bot-logs
logs:
	${LOGS} ${BOT_CONTAINER} -f

.PHONY: bot-shell
shell:
	${EXEC} ${BOT_CONTAINER} bash
