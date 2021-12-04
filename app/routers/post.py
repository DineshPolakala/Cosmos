from app import oauth2
from fastapi.param_functions import Depends
from .. import models, schemas, oauth2
from typing import  List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. database import engine, get_db
from sqlalchemy.orm import Session
from sqlalchemy import func


router = APIRouter(prefix="/posts", tags=['Posts'])



# @router.get("/", response_model=List[schemas.PostResponse])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), get_current_user : int = Depends(oauth2.get_current_user), limit:int = 10, skip:int = 0
                ,search :Optional[str] = ""):
    # cur.execute("""select * from posts ;""")
    # posts = cur.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit=limit).offset(skip).all()
    # return posts
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.get("/users/{id}", response_model=List[schemas.PostResponse])
def get_posts_uploaded_by_user(id:int,db: Session = Depends(get_db), user_id : int = Depends(oauth2.get_current_user)):
    # cur.execute(f"""select * from posts WHERE id = %s ;""",(str(id),))
    # post = cur.fetchone()
    post = db.query(models.Post).filter(models.Post.user_id == int(id)).all()
    return post
    

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post : schemas.CreatePost,db: Session = Depends(get_db), current_user_id : int = Depends(oauth2.get_current_user)):
    # cur.execute("""INSERT INTO Posts (title, published, content) VALUES (%s,%s,%s) returning * """,(new_post.title, new_post.published,new_post.content))
    # new_post = cur.fetchone()
    # conn.commit()
    # print(current_user_id.id)
    new_post = models.Post(user_id =current_user_id.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post




@router.get("/latest")
def get_latest_posts():
    # return my_posts
    pass

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id : int,db: Session = Depends(get_db), user_id : int = Depends(oauth2.get_current_user)):
    # cur.execute(f"""select * from posts WHERE id = %s ;""",(str(id),))
    # post = cur.fetchone()
    
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"post with {id} was not found")
    # return post
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    return post



@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int,db: Session = Depends(get_db), current_user_id : int = Depends(oauth2.get_current_user)):
    
    # cur.execute(""" DELETE FROM posts where id = %s returning *;""" ,(str(id),) )
    # deleted_post = cur.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"post with {id} was not found")
    if post.user_id != int(current_user_id.id) :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail = f"Not Authorized to perform requested action")

    post_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id:int, post:schemas.UpdatePost,db: Session = Depends(get_db),  user_id: int = Depends(oauth2.get_current_user)):
    # cur.execute(""" UPDATE posts set title = %s , content = %s, published = %s where id = %s returning *;""" ,(post.title,post.content,post.published,str(id),) )
    # updated_post = cur.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"post with {id} was not found")
    if post_query.first().user_id != int(user_id.id) :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail = f"Not Authorized to perform requested action")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()

