import time
from typing import Optional, List

import psycopg2
from psycopg2.extras import RealDictCursor

from pydantic import BaseModel
from starlette.responses import Response

from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session

from . import models, schemas, utils
from .database import engine, get_db

from .routers import post, user


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

app.include_router(post.router)
app.include_router(user.router)

# GET root
@app.get("/")
def root():
    return {"message": "root"}
