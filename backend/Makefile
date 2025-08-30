.PHONY: clean up

test:
	.venv\Scripts\activate && python -m pytest -s app/tests
install:
	.venv\Scripts\activate && pip install -r requirements.txt
save:
	pip freeze > requirements.txt
start:
	.venv\Scripts\activate && uvicorn app.main:app --reload
migrate:
	.venv\Scripts\python -m alembic revision --autogenerate -m "init schema"
upgrade:
	.venv\Scripts\python -m alembic upgrade head
clean:
	docker-compose down --volumes
up: clean
	docker-compose up --build