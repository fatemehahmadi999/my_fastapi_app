# my_fastapi_app

Small FastAPI app that serves HTML on the root URL `/`.

## Repository layout

- **`app/asgi.py`** — FastAPI app and `if __name__ == "__main__"` entrypoint (runs Uvicorn).
- **`app_mnist/`** — Empty placeholder for a future MNIST-related piece.

## Branches

- **`main`** and **`lecture`** exist locally and on `origin`. Use the branch your instructor or team specifies.

## Setup

There is no `requirements.txt` or `pyproject.toml` yet. Use a virtual environment and install:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install fastapi uvicorn
```

## Run the app

From the repository root:

```bash
python app/asgi.py
```

This binds **host `0.0.0.0`** and **port `8000`**.

Alternatively:

```bash
uvicorn app.asgi:app --host 0.0.0.0 --port 8000
```

Run these from the project root so Python can resolve the `app` package.

## Try the endpoints

- **GET** `http://localhost:8000/` — browser or `curl http://localhost:8000/`
- **POST** `http://localhost:8000/` — e.g. `curl -X POST http://localhost:8000/`

## Code note

Both route handlers are named `read_root`. FastAPI still registers GET and POST because each decorator runs at import time. Renaming (e.g. `read_root_get` / `read_root_post`) is optional but clearer for readers.

## Follow-ups for the team

- Add **`requirements.txt`** or **`pyproject.toml`** so installs are reproducible.
- Decide what goes in **`app_mnist/`** and update imports or docs when you add code.
