from typing import List, Optional
from fastapi import Depends, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models, oauth2
from ..database import get_db

router = APIRouter(prefix="/vote", tags=["vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post= db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {vote.post_id} not found",
        )
    current_vote = (
        db.query(models.Votes)
        .filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)
        .first()
    )
    if vote.dir == 1:
        if current_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="already upvoted"
            )
        else:
            new_vote = models.Votes(post_id=vote.post_id, user_id=current_user.id)
            new_vote.user_id = current_user.id
            db.add(new_vote)
            db.commit()
            db.refresh(new_vote)
            return {"detail": "voted"}
    else:
        if not current_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"You havent liked the Post with id {vote.post_id}",
            )
        else:
            delete_vote = (
                db.query(models.Votes)
                .filter(
                    models.Votes.post_id == vote.post_id,
                    models.Votes.user_id == current_user.id,
                )
                .first()
            )
            db.delete(delete_vote)
            db.commit()
            return {"detail": "vote deleted"}

    
