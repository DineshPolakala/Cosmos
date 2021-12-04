from os import stat
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.param_functions import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import json
while True:

    try:
        print("trying to connect")
        conn = psycopg2.connect(host ="localhost", database = "fastapi", user = "postgres", password = "Change123", cursor_factory=RealDictCursor)
        cur = conn.cursor()
        print("Connection Successful")
       
        
       
        # for record in cur:
        #     print(record)
        break;
    except Exception as error  :
        print("can't able to connect")
        print("error found: ", error)
        time.sleep(2)

    




app = FastAPI()
my_posts = [{"title" : "title of the post",
                "content" : "content of the post1", "id" : 1},
            {"title" : "favourite foods",
                "content" : "I like pizza", "id" : 2}
            ]

class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    # rating: Optional[int] = None


@app.get("/")
async def root():
    return {"message":"Hello...! welcome to Cosmos"}


@app.get("/posts")
def get_posts():
    cur.execute("""select * from posts ;""")
    posts = cur.fetchall()
    
    return {"data"  :posts}
    

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create(new_post : Post):
    cur.execute("""INSERT INTO Posts (title, published, content) VALUES (%s,%s,%s) returning * """,(new_post.title, new_post.published,new_post.content))
    new_post = cur.fetchone()
    conn.commit()
    return {"data" : new_post}




@app.get("/posts/latest")
def get_latest_posts():
    return my_posts

@app.get("/posts/{id}")
def get_post(id : int, response : Response):
    cur.execute(f"""select * from posts WHERE id = %s ;""",(str(id),))
    post = cur.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"post with {id} was not found")
    return {"post details" : post}



@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    
    cur.execute(""" DELETE FROM posts where id = %s returning *;""" ,(str(id),) )
    deleted_post = cur.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"post with {id} was not found")
    print("deletion successful")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    cur.execute(""" UPDATE posts set title = %s , content = %s, published = %s where id = %s returning *;""" ,(post.title,post.content,post.published,str(id),) )
    updated_post = cur.fetchone()
    conn.commit()
    if updated_post == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"post with {id} was not found")
    return {"data" : updated_post}

