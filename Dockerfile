# ==================================================
# CPU 기본 이미지 (Render / 일반 Linux 환경용)
# ==================================================
FROM python:3.11-slim

# 작업 디렉터리
WORKDIR /app/src

# ==================================================
# 시스템 패키지
# ==================================================
# - git: CLIP 또는 외부 repo 의존성 대비
# - build-essential: torch, 기타 패키지의 네이티브 빌드 대비
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# ==================================================
# Python 의존성 설치
# ==================================================
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# ==================================================
# 애플리케이션 소스 복사
# ==================================================
COPY src ./src

# ==================================================
# 런타임 설정
# ==================================================
# 로그가 즉시 출력되도록 설정 (Render 권장)
ENV PYTHONUNBUFFERED=1

# Render는 PORT 환경변수를 주입함
# 로컬 실행 시에는 기본값 8000 사용
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]