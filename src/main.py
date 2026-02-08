# 정성우

from fastapi import FastAPI

from src.preview.PreviewController import router as preview_router
from src.verify.VerifyController import router as verify_router

# FastAPI 앱을 생성한다.
app = FastAPI(title="CLIP Challenge Image Verifier")

app.include_router(preview_router)
app.include_router(verify_router)

# 서버 배포 후, 서버가 살아있는지 확인하는 엔드포인트이다.
@app.get("/health")
def health():
    return {"ok": True}

# 로컬에서 서버를 실행하도록 해주는 코드로 실제 랜더 배포 시에는 사용되지 않는다.
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,   # 개발 중 자동 리로드
    )