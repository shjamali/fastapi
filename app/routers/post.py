from typing import List, Optional
from fastapi import Depends, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models, oauth2
from ..database import get_db
from sqlalchemy import func

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=List[schemas.PostOut])
async def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 100,
    skip: int = 0,
    search: Optional[str] = "",
):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    posts = (
        db.query(models.Post, func.count(models.Votes.user_id).label("votes"))
        .join(models.Votes, models.Post.id == models.Votes.post_id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    posts = [{"post": post, "votes": votes} for post, votes in posts]
    return posts


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
async def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute(
    #     "INSERT INTO posts (title, content,published) VALUES (%s, %s, %s) returning *",
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()
    print(current_user)

    new_post = models.Post(**post.model_dump())
    new_post.owner_id = current_user.id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{post_id}", response_model=schemas.PostOut)
async def get_post(
    post_id: int,
    response: Response,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    
    # db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    db_post = (
        db.query(models.Post, func.count(models.Votes.user_id).label("votes"))
        .join(models.Votes, models.Post.id == models.Votes.post_id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == post_id).first()
    )
    print(db_post)
    if db_post:
        db_post = {"post": db_post[0], "votes": db_post[1]}
        return db_post
    else:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {post_id} not found",
    )
    # cursor.execute("SELECT * FROM posts WHERE id=%s", (str(post_id),))
    # post = cursor.fetchone()
    # if post:
    #     return {"data": post}
    # else:
    #     response.status_code = status.HTTP_404_NOT_FOUND
    #     return {"data": f"post with id: {post_id} not found"}


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute("DELETE FROM posts WHERE id=%s returning *", (str(post_id),))
    # delete_post = cursor.fetchone()
    # if delete_post:
    #     conn.commit()
    #     return Response(status_code=status.HTTP_204_NO_CONTENT)
    # else:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"post with id: {post_id} not found",
    #     )
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post:
        if db_post.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"you are not authorized to delete this post",
            )
        db.delete(db_post)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {post_id} not found",
        )


@router.put("/{post_id}", response_model=schemas.PostResponse)
async def update_post(
    post_id: int,
    update_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute(
    #     "UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s returning *",
    #     (update_post.title, update_post.content, update_post.published, str(post_id)),
    # )
    # update_post = cursor.fetchone()
    # if update_post:
    #     conn.commit()
    #     return {"data": update_post}
    # else:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"post with id: {post_id} not found",
    #     )
    db_post_qry = db.query(models.Post).filter(models.Post.id == post_id)
    db_post = db_post_qry.first()
    if db_post:
        if db_post.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"you are not authorized to update this post",
            )
        db_post_qry.update(update_post.model_dump(), synchronize_session=False)
        db.commit()
        db.refresh(db_post)
        return db_post
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {post_id} not found",
        )
