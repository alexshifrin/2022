from typing import Optional
from fastapi import FastAPI, Response, status
from pydantic import BaseModel

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

@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = max([post["id"] for post in my_posts]) + 1
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = _find_post(id)
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"post with id {id} not found"}
    return {"data": post}
