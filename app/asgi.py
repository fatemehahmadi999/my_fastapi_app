import fastapi
import uvicorn
from fastapi.responses import HTMLResponse
from fastapi import Form

app = fastapi.FastAPI()

@app.post("/")
def read_root():
    return HTMLResponse("<h1> Post Method: Hello Miss Fatemah!</h1>")

@app.get("/")
def read_root():
    return HTMLResponse("<h1> Get Method: Hello Miss Fatemah!</h1>")

@app.post("/profile")
def create_profile(name: str = Form(...), age: int = Form(...)):
    return HTMLResponse(f"<h1> Profile Created: {name} is {age} years old!</h1>")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)