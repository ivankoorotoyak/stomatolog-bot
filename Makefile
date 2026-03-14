.PHONY: run-main run-clean run-joke run-all

run-main:
	source venv/bin/activate && source /root/tokens.env && python bots/main_bot.py

run-clean:
	source venv/bin/activate && source /root/tokens.env && python bots/clean_bot.py

run-joke:
	source venv/bin/activate && source /root/tokens.env && python bots/joke_bot.py

run-all:
	@echo "Запуск всех ботов в фоне..."
	@nohup make run-main > /dev/null 2>&1 &
	@nohup make run-clean > /dev/null 2>&1 &
	@nohup make run-joke > /dev/null 2>&1 &
	@echo "Боты запущены"
