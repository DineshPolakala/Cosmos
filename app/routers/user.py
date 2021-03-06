from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. database import engine, get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users",
                    tags=['Users'])

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def Create_User(user : schemas.UserCreate, db: Session = Depends(get_db)):

    #  hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    post_query = db.query(models.Post).filter(models.User.email == user.email)

    if post_query.first() != None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"post with {user.email} was not found")
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
@router.get("/{id}", response_model=schemas.UserResponse)
def getUser(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"User with {id} not found")
    return user