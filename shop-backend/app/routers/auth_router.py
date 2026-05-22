"""
경로 : shop-backend/app/routers/auth_router.py
파일명 : auth_router.py

회원가입 및 로그인 API 라우터를 관리하는 파일

이 파일의 역할:
- 회원가입 API endpoint 정의
- 로그인 API endpoint 정의

"""


from fastapi import APIRouter

from app.shcemas.models import SignUpRequest, SignInRequest
from app.services import auth_service


router = APIRouter(prefix = "/auth", tags = ["Auth"])


@router.post(
    path = "/signup",
    status_code = 201,
    summary = "회원가입",
    description = "이메일, 비밀번호, 이름을 입력해 사용자를 생성한다."
)
def signup(request: SignUpRequest):
    """회원가입 API"""

    return auth_service.insert_user(
        email = str(request.email),
        password = request.password,
        name = request.name
    )


@router.post(
    path = "/signin",
    summary = "로그인",
    description = "이메일과 비밀번호를 검증하고 access_token 을 발급한다."
)
def signin(request: SignInRequest):
    """로그인 API"""

    return auth_service.select_user_by_email(
        email = str(request.email),
        password = request.password
    )