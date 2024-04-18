build:
	docker compose -f production.yml up --build -d --remove-orphans


up:
	docker compose -f production.yml up -d


down:
	docker compose -f production.yml down


show-logs:
	docker compose -f production.yml logs


show-logs-api:
	docker compose -f production.yml logs api


makemigrations:
	docker compose -f production.yml run --rm api python manage.py makemigrations


migrate:
	docker compose -f production.yml run --rm api python manage.py migrate


collectstatic:
	docker compose -f production.yml run --rm api python manage.py collectstatic --no-input --clear


superuser:
	docker compose -f production.yml run --rm api python manage.py createsuperuser


down-v:
	docker compose -f production.yml down -v


volume:
	docker volume inspect authors-haven_local_postgres_data


authors-db:
	docker compose -f production.yml exec postgres psql --username=root --dbname=authrors-live


flake8:
	docker compose -f production.yml exec api flake8 .


black-check:
	docker compose -f production.yml exec api black --check --exclude=migrations .


black-diff:
	docker compose -f production.yml exec api black --diff --exclude=migrations .


black:
	docker compose -f production.yml exec api black --exclude=migrations .


isort-check:
	docker compose -f production.yml exec api isort . --check-only --skip venv --skip migrations


isort-diff:
	docker compose -f production.yml exec api isort . --diff --skip venv --skip migrations


isort:
	docker compose -f production.yml exec api isort . --skip venv --skip migrations
