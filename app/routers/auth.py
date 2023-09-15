from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils, oauth2
from fastapi.security import OAuth2PasswordRequestForm

router=APIRouter(prefix="/auth",tags=["auth"])

@router.post("/login",status_code=status.HTTP_200_OK,response_model=schemas.Token)
def login(user: OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    print("I am here")
    db_user=db.query(models.User).filter(models.User.email==user.username).first()
    if db_user:
        if utils.verify(user.password,db_user.password):
            access_token=oauth2.create_access_token(data={"user_id":db_user.id})
            return {'access_token':access_token,'token_type':'bearer'}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid credentials")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid credentials")