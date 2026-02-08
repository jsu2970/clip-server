# 정성우

from io import BytesIO
from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from PIL import Image

# 전달 받은 이미지와 문자열의 유사도를 비교해주는 객체이다.
from app.verify.VerifyService import ClipVerifier

# 서버 시작 시 CLIP 검증기를 한 번만 로딩한다.
verifier = ClipVerifier(model_name="ViT-B/32")

router = APIRouter(tags=["verify"])

"""
이미지를 검증하기 위해 요청을 보내는 API이다.
title(챌린지 제목), image(인증 사진)을 multipart/form-data 형식으로 받는다.

ex) POST /verify
"""
@router.post("/verify")
async def verify(
    title: str = Form(...),
    image: UploadFile = File(...),
):
    # 업로드 된 이미지 파일이 진짜 이미지인지 1차 검증을 거친다.
    if image.content_type is None or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="image must be an image/* content type")

    data = await image.read()  # 업로드된 파일을 바이트로 읽는다.
    try:
        pil = Image.open(BytesIO(data)).convert("RGB")  # 이미지를 열어서 CLIP 입력 형식을 맞춘다. (여기선 RGB로 통일한다.)
    except Exception:
        raise HTTPException(status_code=400, detail="invalid image")  # 이미지가 깨져있다면 Bad Request를 반환한다.

    result = verifier.verify(title=title, image=pil)  # 이미지를 AI로 판별한다.
    return result  # 결과를 FastAPI가 자동으로 JSON으로 반환한다.