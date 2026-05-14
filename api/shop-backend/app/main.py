"""
경로 : shop-backend/app/main.py
파일명 : main.py

FastAPI 애플리케이션 실행을 담당하는 파일

이 파일의 역할:
- FastAPI 앱 생성
- 서버 상태 확인 API 제공

"""

from fastapi import FastAPI

from app.database import init_db


# FastAPI 앱 생성
app = FastAPI()

# 서버 시작 시 DB 테이블 생성
init_db()


@app.get("/")
def home():
    """서버 동작 확인 API"""
    return {
        "message" : "Shop Backend Server is running"
    }
