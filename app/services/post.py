from typing import Annotated
from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from datetime import datetime, timezone
from app.models import Post, PostCreate, PostUpdate, PostResponse
from app.database import SessionDep


class PostService:

    def __init__(self, session: Session) -> None:
        self._session: Session = session
    
    def post_to_response(self, post: Post) -> PostResponse:
        """"""
        return PostResponse(**post.model_dump())
    
    def create_post(self, payload: PostCreate) -> PostResponse:
        """"""
        post = Post(**payload.model_dump())
        self._session.add(post)
        self._session.commit()
        self._session.refresh(post)
        return self.post_to_response(post)
    
    def read_one_post(self, post_id: int) -> PostResponse:
        """"""
        post: Post | None = self._session.get(Post, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return self.post_to_response(post)
    
    def read_all_posts(self, offset: int = 0, limit: int = 100) -> list[PostResponse]:
        """"""
        statement = select(Post).offset(offset).limit(limit)
        posts = self._session.exec(statement).all()
        return [self.post_to_response(post) for post in posts]
    
    def update_post(self, post_id: int, payload: PostUpdate) -> PostResponse:
        """"""
        post: Post | None = self._session.get(Post, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        for key, value in payload.model_dump(exclude_none=True, exclude_unset=True).items():
            setattr(post, key, value)
        post.updated_at = datetime.now(timezone.utc)
        
        self._session.commit()
        self._session.refresh(post)

        return self.post_to_response(post)

    def delete_post(self, post_id: int) -> None:
        """"""
        post: Post | None = self._session.get(Post, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        self._session.delete(post)
        self._session.commit()


def get_post_service(session: SessionDep) -> PostService:
    """"""
    return PostService(session)


PostServiceDep = Annotated[PostService, Depends(get_post_service)]
