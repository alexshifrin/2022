from dataclasses import dataclass
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

"""
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}
OR
{
    "name": "Foo",
    "price": 45.2
}
are valid JSON because of Optional type hint and None default
"""
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

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

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict