from typing import Union,Optional,List
from fastapi.params import Body
from fastapi import FastAPI,Response,status,HTTPException,Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models,schemas
from sqlalchemy.orm import Session
from .database import engine,SessionLocal, get_db

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

@app.get("/")
def read_root():
    return {"Hello": "World welcome to FastAPI!!!"}



@app.get("/posts",response_model=List[schemas.Post])
def get_posts(db:Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts= cursor.fetchall()
    # print(posts)
    posts=db.query(models.Post).all()
    print(posts)
    return posts
    

@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db:Session=Depends(get_db)):
    #print(new_post)
    #print(new_post.dict())
    # new_post= new_post.dict()
    # new_post['id']=randrange(0,1000)
    # my_post.append(new_post)
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                (new_post.title, new_post.content, new_post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post=models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/{id}",response_model=schemas.Post)
def get_post(id:int,db:Session=Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id)))
    # test_post= cursor.fetchone()
    # print("test_post",test_post)
    # post=find_post(id)

    post = db.query(models.Post).filter(models.Post.id == id).first()
    print("post",post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{'message':f"post with id: {id} was not found"}
    return post

@app.get("/posts/latest")
def get_latest_post():
    post=my_post[len(my_post)-1]
    return{"detail":post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db)):

    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""",(str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    post.delete(synchronize_session=False)
    db.commit()


    # index=find_index_post(id)

    # if deleted_post == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} was not found")
        # return {"message": f"post with id: {id} was not found"}
    #my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# @app.put("/posts/{id}")
# def update_post(id:int,post:Post):

#     cursor.execute("""UPDATE post SET title = %s, content = %s, published =%s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,id))
#     updatd_post = cursor.fetchone()
#     conn.commit()
#     # index= find_index_post(id)
#     if updatd_post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} was not found")
#         # return {"message": f"post with id: {id} was not found"}

#     print(post)
#     return{'message':updatd_post}

@app.put("/posts/{id}",response_model=schemas.Post)
def update_post(id: int, updated_post:schemas.PostCreate, db:Session=Depends(get_db)):
    # cursor.execute("""
    #     UPDATE posts SET title = %s, content = %s, published = %s 
    #     WHERE id = %s RETURNING *;
    # """, (post.title, post.content, post.published, id))
    
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()


@app.post("/users",response_model=schemas.UserOut,status_code=status.HTTP_201_CREATED)
def create_user(user:schemas.UserCreate,db:Session = Depends(get_db)):
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
