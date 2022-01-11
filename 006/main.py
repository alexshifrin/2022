from os import stat
from typing import Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from starlette.responses import Response

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [
    {"title": "post 1 title", "content": "post 1 content", "id": 1},
    {"title": "post 2 title", "content": "post 2 content", "id": 2}
]

def _find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post

@app.get("/")
def root():
    return {"message": "root"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = max([post["id"] for post in my_posts]) + 1
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id: int):
    post = _find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found",
        )
    return {"data": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    deleted_post = _find_post(id)
    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found or deleted",
        )
    global my_posts
    my_posts = [post for post in my_posts if post["id"] != id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    