"""
경로 : shop-backend/app/main.py
파일명 : main.py

FastAPI 애플리케이션 실행을 담당하는 파일

이 파일의 역할:
- FastAPI 앱 생성
- 서버 상태 확인 API 제공

"""

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.core.database import init_db
from app.exceptions.api_exception import ApiException
from app.exceptions.exception_handlers import api_exception_handler, validation_exception_handler
from app.routers import auth_router, order_router, point_router


# FastAPI 앱 생성
app = FastAPI()

app.add_exception_handler(
    ApiException,           # 예외타입
    api_exception_handler   # 처리함수
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

# 서버 시작 시 DB 테이블 생성
init_db()

# API 라우터 등록
app.include_router(auth_router.router)
app.include_router(point_router.router)
app.include_router(order_router.router)


@app.get("/")
def home():
    """서버 동작 확인 API"""
    return {
        "message" : "Shop Backend Server is running"
    }
