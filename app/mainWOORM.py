from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='deojjked',cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print('connected to database')
        break
    except Exception as e:
        print("connection failed")
        print("Error:", e)
        time.sleep(5)
        

my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "title of post 2", "content": "content of post 2", "id": 2},
]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    cursor.execute("INSERT INTO posts (title, content,published) VALUES (%s, %s, %s) returning *", (post.title, post.content,post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{post_id}")
async def get_post(post_id: int, response: Response):
    cursor.execute("SELECT * FROM posts WHERE id=%s", (str(post_id),))
    post = cursor.fetchone()
    if post:
        return {"data": post}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"data": f"post with id: {post_id} not found"}
    


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int):
    cursor.execute("DELETE FROM posts WHERE id=%s returning *", (str(post_id),))
    delete_post = cursor.fetchone()
    if delete_post:
        conn.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {post_id} not found",
        )


@app.put("/posts/{post_id}")
async def update_post(post_id: int, update_post: Post):
    cursor.execute("UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s returning *", (update_post.title, update_post.content,update_post.published, str(post_id)))
    update_post = cursor.fetchone()
    if update_post:
        conn.commit()
        return {"data": update_post}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {post_id} not found",
        )
