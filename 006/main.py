from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
def root():
    return {"message": "root"}

@app.get("/posts")
def get_posts():
    return {"data": "Here are your posts"}

@app.post("/createposts")
def create_posts(post: Post):
    print(post)
    return {"new_post": f"title: {post.title} content:{post.content}"}
