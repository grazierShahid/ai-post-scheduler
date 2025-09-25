from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Request
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import ValidationError
import json

from app.dependencies import get_db
from app.schemas.post import (
    PostSubmitRequest, PostSubmitResponse, PostListResponse,
    PostDetailResponse, AISuggestionsRequest, AISuggestionsResponse, get_post_submit_form,
    AIBestTimeRequest, AIBestTimeResponse
)
from app.utils.logger import get_logger
from app.services.post import PostService
from app.utils.image_storage import save_upload_file_as_jpg

logger = get_logger(__name__)

router = APIRouter()

@router.post("/submit-post", response_model=PostSubmitResponse)
async def submit_post(
    req: Request,
    form_data: PostSubmitRequest = Depends(get_post_submit_form),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    try:
        logger.info(f"receive api request")

        image_path: Optional[str] = None

        if image is not None:
            image_path = await save_upload_file_as_jpg(image, subdir=str(form_data.user_id))

        service = PostService(db)
        return service.submit(form_data.dict(), image_file_path=image_path)
    except ValidationError as e:
        print(f"Validation error: {e}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/posts", response_model=PostListResponse)
def list_posts(req: Request, limit: int = 20, offset: int = 0, db: Session = Depends(get_db)):
    service = PostService(db)
    return service.list(limit=limit, offset=offset)

@router.get("/post/{post_id}", response_model=PostDetailResponse)
def get_post(req: Request, post_id: int, db: Session = Depends(get_db)):
    service = PostService(db)
    detail = service.detail(post_id)
    if not detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return detail

@router.post("/suggest-hashtag", response_model=AISuggestionsResponse)
async def suggest_hashtag(req: Request, payload: AISuggestionsRequest, db: Session = Depends(get_db)):
    service = PostService(db)
    return await service.suggest_hashtags(payload.user_id, payload)

@router.post("/suggest-best-time", response_model=AIBestTimeResponse)
async def suggest_best_time(req: Request, payload: AIBestTimeRequest, db: Session = Depends(get_db)):
    service = PostService(db)
    return await service.suggest_best_posting_time(payload)