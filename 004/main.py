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
async def show_item(item_id):
    return {"item_id": item_id}
    