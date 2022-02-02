import time
from typing import Optional

import psycopg2
from psycopg2.extras import RealDictCursor

from pydantic import BaseModel
from starlette.responses import Response

from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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

# GET root
@app.get("/")
def root():
    return {"message": "root"}

# GET /posts
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

# POST /posts
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# GET /posts/{id}
@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    matched_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not matched_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found",
        )
    return matched_post

# DELETE /posts/{id}
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
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
@app.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    update_post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = update_post_query.first()
    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found to update",
        )
    update_post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return update_post_query.first()
