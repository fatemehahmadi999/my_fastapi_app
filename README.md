# my_fastapi_app

Welcome. This repository is a **small FastAPI service** that returns HTML so you can see requests and responses without building a front end first. Treat it as a sandbox: run it, hit the URLs, then open `**app/asgi.py`**—the file includes short comments in the voice of a walkthrough so you can connect the code to what you see in the browser or in `curl`.

## What lives where

- `**app/asgi.py**` — This is the heart of the lesson for now: the `FastAPI()` app, the route functions, and the `if __name__ == "__main__"` block that starts Uvicorn when you run the file as a script.
- `**app_mnist/**` — Reserved for a later exercise (for example MNIST-related code). It is intentionally empty until we wire something in.

## Before you run anything: install dependencies

Install the two packages we rely on directly. Run these in the environment you use for class (virtualenv, conda, or your system Python—whatever your instructor prefers):

```bash
pip install fastapi
pip install uvicorn
pip install python-multipart
```

**Pydantic** (used for `BaseModel` in the JSON profile route) is installed automatically as a dependency of FastAPI, so you do not need a separate `pip install pydantic` for this project to run.

## Starting the server

From the **repository root** (the folder that contains `app/`), run:

```bash
python app/asgi.py
```

That starts Uvicorn with **host `0.0.0.0`** and **port `8000`**. I use `0.0.0.0` so you can reach the server from another device on the same network when we demo from a phone or a classmate’s laptop.

If you prefer the command-line style you will see in deployment tutorials, this is equivalent:

```bash
uvicorn app.asgi:app --host 0.0.0.0 --port 8000
```

**Important:** run these commands from the project root. If your current working directory is wrong, Python may not resolve `app.asgi` the way we expect.

## Routes you should know (checklist)

Use this table as a checklist while you read `app/asgi.py` line by line.


| Method | Path            | What I want you to notice                                                             |
| ------ | --------------- | ------------------------------------------------------------------------------------- |
| GET    | `/`             | Same path as POST, different verb—HTTP method matters.                                |
| POST   | `/`             | Compare the response string to the GET handler.                                       |
| POST   | `/profile/form` | Data arrives as **form** fields `name` and `age` (think HTML forms or `curl -d`).     |
| POST   | `/profile/json` | Same logical fields, but the body must be **JSON** and must match the Pydantic model. |


## A teaching moment about names

Both handlers on `/` are named `read_root` in Python. In a typical script that would be confusing, but **FastAPI registered each route when its decorator ran**, so both endpoints still work. For your own projects I encourage clearer names (`read_root_get`, `read_root_post`); here I left the duplication so we can talk about it in class.

