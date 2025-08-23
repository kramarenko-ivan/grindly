# grindly
Grindly — a habit-tracking app with friendly competition, built with FastAPI, Vue.js, Supabase, and CI/CD for DevOps practice.

# Project README

This README currently contains instructions for setting up and running the backend. Additional documentation for other parts of the project will be added here later.

## Backend

### Prerequisites

Before using the Makefile commands, ensure that `make` is installed on your system:

- **Windows:** Install [Make for Windows](http://gnuwin32.sourceforge.net/packages/make.htm) or use `WSL`.
- **Linux / macOS:** `make` is usually preinstalled. If not, install via your package manager, e.g., `sudo apt install make` or `brew install make`.

Also, ensure Python and a virtual environment are available.

### Makefile Commands

The following commands are available in the `Makefile` inside the `backend` folder:

| Command   | Description |
|-----------|-------------|
| `install` | Install dependencies: `.venv\Scripts\activate && pip install -r requirements.txt` |
| `start`   | Start the backend server: `.venv\Scripts\activate && uvicorn app.main:app --reload` |
| `test`    | Run tests using pytest: `.venv\Scripts\activate && python -m pytest -s app/tests` |
| `save`    | Save current dependencies to `requirements.txt`: `pip freeze > requirements.txt` |

### How to Use

1. Install dependencies:

```md
make install
```

2. Start the backend server

```md
make start
```

3. Run tests

```md
make test
```