# 정성우

from fastapi import APIRouter, Form
from pydantic import BaseModel

from src.preview.PreviewService import ChallengePreviewService

router = APIRouter(tags=["preview"])

preview_service = ChallengePreviewService()

class PreviewRequest(BaseModel):
    title: str

"""
챌린지 이름을 받아서 해당 챌린지 이름이 사진 검증을 받기 적합한지 알려주는 컨트롤러이다.
"""
@router.post("/preview")
def preview_challenge(req: PreviewRequest):
    return preview_service.preview(req.title)