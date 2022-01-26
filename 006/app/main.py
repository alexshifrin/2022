import time
from os import stat
from typing import Optional

import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from starlette.responses import Response
from fastapi import FastAPI, HTTPException, status

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="shifty",
            password="",
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connection was succesful!")
        break
    except Exception as error:
        print("Connection to database failed!")
        print("Error: ", error)
        time.sleep(2)


my_posts = [
    {"title": "post 1 title", "content": "post 1 content", "id": 1},
    {"title": "post 2 title", "content": "post 2 content", "id": 2}
]

def _find_post(id):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return (index, post)
    else:
        return (None, None)

# GET root
@app.get("/")
def root():
    return {"message": "root"}

# GET /posts
@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts;""")
    posts = cursor.fetchall()
    return {"data": posts}

# POST /posts
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
        (post.title, post.content, post.published)
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

# GET /posts/{id}
@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found",
        )

    return {"data": post}

# DELETE /posts/{id}
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index, deleted_post = _find_post(id)
    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found or deleted",
        )
    global my_posts
    my_posts.pop(index)
    # my_posts = [post for post in my_posts if post["id"] != id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# PUT /posts/{id}
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index, updated_post = _find_post(id)
    if not update_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} not found to update",
        )
    post_dict = post.dict()
    post_dict["id"] = id
    global my_posts
    my_posts[index] = post_dict
    return {"message": "updated post!", "post": post}

