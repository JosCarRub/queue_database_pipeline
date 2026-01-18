.PHONY: run

run:
	python manage.py runserver
up:
	docker compose up -d

down:
	docker compose down -v

migration:
	python manage.py makemigrations

migrate:
	python manage.py migrate

worker:
	python worker.py
