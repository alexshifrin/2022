from dataclasses import dataclass

from fastapi import FastAPI

app = FastAPI()

@dataclass
class Message:
    msg: str
    val: int

msg = Message("Hello, World!", 100)

@app.get("/")
async def root():
    return msg

@app.get("/item/{item_id}")
async def show_item(item_id: int):
    return {"item_id": item_id}

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: int):
    return {"user_id": user_id}