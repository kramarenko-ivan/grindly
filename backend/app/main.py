from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return { "message": "Hello, Grindly!" }

@app.post("/register")
def register(user: dict):
    return { "status": "registered", "user": user}