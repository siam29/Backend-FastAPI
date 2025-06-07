from typing import Union,Optional,List
from fastapi.params import Body
from fastapi import FastAPI,Response,status,HTTPException,Depends
from pydantic import BaseModel
from random import randrange
from passlib.context import CryptContext
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models,schemas,utils
from sqlalchemy.orm import Session
from .database import engine,SessionLocal, get_db
from .routers import post,user,auth

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
models.Base.metadata.create_all(bind=engine)


app = FastAPI()


my_post=[{"title":"title 1","content":"content 1","id":1,"published":True},
          {"title":"title 2","content":"content 2","id":2,"published":True},
          {"title":"title 3","content":"content 3","id":3,"published":True}]

def find_post(id):
    for p in my_post:
        if p['id']==id:
            return id
        
def find_index_post(id):
    for i,p in enumerate(my_post):
        if p['id']==id:
            return i
    return None
    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} was not found")
    #connection to database

try:
    conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='1234',cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connection successful") 
except Exception as error: 
    print("Database connection failed") 
    print("Error:", error) 

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"Hello": "World welcome to FastAPI!!!"}