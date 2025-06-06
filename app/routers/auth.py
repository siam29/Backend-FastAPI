from fastapi import APIRouter,Depends,status,HTTPException,Response
from sqlalchemy.orm import Session
from ..database import engine,SessionLocal, get_db
from .. import schemas, models, utils,oauth2
from fastapi.security import OAuth2PasswordRequestForm
router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credential: OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db)):

    # username password
    user = db.query(models.User).filter(models.User.email == user_credential.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_NOT_FOUND, detail=f"Invalid Credentails")
    
    if not utils.verify(user_credential.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_NOT_FOUND, detail=f"Invalid Credentails")

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    # create a token
    # return token
    return {"access_token":access_token, "token_type":"bearer"}
