test:
	.venv\Scripts\activate && python -m pytest -s app/tests
install:
	.venv\Scripts\activate && pip install -r requirements.txt
save:
	pip freeze > requirements.txt
start:
	.venv\Scripts\activate && uvicorn app.main:app --reload