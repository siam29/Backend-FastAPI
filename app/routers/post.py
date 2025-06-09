from .. import schemas, models, utils,oauth2
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from ..database import engine,SessionLocal, get_db
from fastapi import FastAPI,Response,status,HTTPException,Depends
from sqlalchemy.orm import Session
from typing import Union,Optional,List

router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/",response_model=List[schemas.Post])
def get_posts(db:Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user),limit:int=10,skip:int =0, search:Optional[str] = ""):
    posts=db.query(models.Post).filter(models.Post.content.contains(search)).limit(limit).offset(skip).all()
    print(posts)
    return posts
    

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db:Session=Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    print(current_user.email)
    print("User ID:", current_user.id)
    new_post=models.Post(owner_id=current_user.id,**post.dict())
    print("new_post",new_post)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model=schemas.Post)
def get_post(id:int,db:Session=Depends(get_db),current_user:int = Depends(oauth2.get_current_user),limit: int  = 10):

    post = db.query(models.Post).limit(limit).all()
    print("post",post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} was not found")
    return post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int, updated_post:schemas.PostCreate, db:Session=Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()

