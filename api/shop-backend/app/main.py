"""
경로 : shop-backend/app/main.py
파일명 : main.py

FastAPI 애플리케이션 실행을 담당하는 파일

이 파일의 역할:
- FastAPI 앱 생성
- 서버 상태 확인 API 제공

"""

from fastapi import FastAPI


# FastAPI 앱 생성
app = FastAPI()


@app.get("/")
def home():
    return {
        "message" : "Shop Backend Server is running"
    }
