from multiprocessing import synchronize
from nis import match
import time
from os import stat
from typing import Optional

import psycopg2
from psycopg2.extras import RealDictCursor

from pydantic import BaseModel
from starlette.responses import Response

from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session

from . import models
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)

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
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts ORDER BY id ASC;""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}

# POST /posts
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *;""",
    #     (post.title, post.content, post.published)
    # )
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}

# GET /posts/{id}
@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s;""", (id,))
    # post = cursor.fetchone()

    matched_post = db.query(models.Post).filter(models.Post.id == id).first()

    if not matched_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found",
        )
    return {"data": matched_post}

# DELETE /posts/{id}
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # index, deleted_post = _find_post(id)
    # if not deleted_post:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Post with id {id} not found or deleted",
    #     )
    # global my_posts
    # my_posts.pop(index)
    # # my_posts = [post for post in my_posts if post["id"] != id]
    # return Response(status_code=status.HTTP_204_NO_CONTENT)

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *;""", (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    delete_post_query = db.query(models.Post).filter(models.Post.id == id)
    if not delete_post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found or deleted",
        )
    delete_post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# PUT /posts/{id}
@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *;""",
    #     (post.title, post.content, post.published, id)
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()

    update_post_query = db.query(models.Post).filter(models.Post.id == id)

    updated_post = update_post_query.first()

    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found to update",
        )
    
    update_post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return {"message": "updated post!", "post": update_post_query.first()}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    # print(db.query(models.Post)) = "SELECT * FROM posts;"
    return {"data": posts}