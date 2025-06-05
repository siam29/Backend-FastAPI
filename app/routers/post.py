from .. import schemas, models, utils
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from ..database import engine,SessionLocal, get_db
from fastapi import FastAPI,Response,status,HTTPException,Depends
from sqlalchemy.orm import Session
from typing import Union,Optional,List

router=APIRouter(
    prefix="/posts"
)

@router.get("/",response_model=List[schemas.Post])
def get_posts(db:Session = Depends(get_db)):
    posts=db.query(models.Post).all()
    print(posts)
    return posts
    

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db:Session=Depends(get_db)):
    new_post=models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model=schemas.Post)
def get_post(id:int,db:Session=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print("post",post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} was not found")
    return post

@router.get("/latest")
def get_latest_post():
    post=my_post[len(my_post)-1]
    return{"detail":post}

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int, updated_post:schemas.PostCreate, db:Session=Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()

