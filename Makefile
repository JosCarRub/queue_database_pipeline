.PHONY: run

run:
	python manage.py runserver
up:
	docker compose up -d

migration:
	python manage.py makemigrations

migrate:
	python manage.py migrate
