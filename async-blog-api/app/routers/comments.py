from fastapi import APIRouter

router = APIRouter(prefix="/posts/{post_id}/comments", tags=["Comments"])