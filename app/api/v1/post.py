from fastapi import APIRouter
from app.models import PostCreate, PostUpdate, PostResponse
from app.services import PostServiceDep

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/", response_model=PostResponse, status_code=201)
def create_post(payload: PostCreate, service: PostServiceDep) -> PostResponse:
    """"""
    return service.create_post(payload)


@router.get("/{post_id}", response_model=PostResponse, status_code=200)
def get_post(post_id: int, service: PostServiceDep) -> PostResponse:
    """"""
    return service.read_one_post(post_id)


@router.get("/", response_model=list[PostResponse], status_code=200)
def get_all_posts(
    service: PostServiceDep,
    offset: int = 0,
    limit: int = 100
    ) -> list[PostResponse]:
    """"""
    return service.read_all_posts(offset, limit)


@router.put("/{post_id}", response_model=PostResponse, status_code=200)
def update_post(
    post_id: int,
    payload: PostUpdate,
    service: PostServiceDep
) -> PostResponse:
    """"""
    return service.update_post(post_id, payload)


@router.delete("/{post_id}", status_code=204)
def delete_post(post_id: int, service: PostServiceDep) -> None:
    """"""
    service.delete_post(post_id)
