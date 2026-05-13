# FastAPI exposes your Python functions as HTTP endpoints. Each decorator ties a URL
# and an HTTP method to a function. Run this file directly, or point Uvicorn at `app`.
import fastapi
import uvicorn
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi import Form

# One application object holds all routes, middleware, and dependency wiring.
app = fastapi.FastAPI()

# Same path (`/`) is fine here because the methods differ: browsers send GET;
# tools or forms often send POST. FastAPI dispatches by method first.
@app.post("/")
def read_root():
    return HTMLResponse("<h1> Post Method: Hello Miss Fatemah!</h1>")

@app.get("/")
def read_root():
    return HTMLResponse("<h1> Get Method: Hello Miss Fatemah!</h1>")

# For JSON bodies, we declare the shape once. Pydantic validates incoming JSON and
# gives you typed attributes—if `age` is not an integer, FastAPI returns 422 for you.
class ProfileIn(BaseModel):
    name: str
    age: int


# Form data is what HTML forms post (`application/x-www-form-urlencoded` or multipart).
# `Form(...)` means “required field”; omit it and the client gets a clear error response.
@app.post("/profile/form")
def create_profile(name: str = Form(...), age: int = Form(...)):
    return HTMLResponse(f"<h1> Profile Created: {name} is {age} years old!</h1>")


# JSON endpoints take a model (or dict) as the body parameter. Compare with the form
# route above: same fields, different content type—pick the style your client will send.
@app.post("/profile/json")
def create_profile_json(body: ProfileIn):
    return HTMLResponse(
        f"<h1> Profile Created: {body.name} is {body.age} years old!</h1>"
    )

# Handy for beginners: `python app/asgi.py` starts the server. In production you
# typically run `uvicorn app.asgi:app` instead; `0.0.0.0` makes the port reachable on your LAN.
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
