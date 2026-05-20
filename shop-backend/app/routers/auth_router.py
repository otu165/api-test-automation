"""
경로 : shop-backend/app/routers/auth_router.py
파일명 : auth_router.py

회원가입 및 로그인 API 라우터를 관리하는 파일

이 파일의 역할:
- 회원가입 API endpoint 정의
- 로그인 API endpoint 정의

"""


from fastapi import APIRouter

from app.models import SignUpRequest, SignInRequest
from app.services import auth_service


router = APIRouter(prefix = "/auth", tags = ["Auth"])


@router.post("/signup", status_code = 201)
def signup(request: SignUpRequest):
    """회원가입 API"""

    return auth_service.insert_user(
        email = str(request.email),
        password = request.password,
        name = request.name
    )


@router.post("/signin")
def signin(request: SignInRequest):
    """로그인 API"""

    return auth_service.select_user_by_email_and_password(
        email = str(request.email),
        password = request.password
    )