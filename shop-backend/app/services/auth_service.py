"""
경로 : shop-backend/app/services/auth_service.py
파일명 : auth_service.py

회원가입 및 로그인 비즈니스 로직을 담당하는 파일

이 파일의 역할:
- 회원가입 요청 처리
- 로그인 요청 처리

"""

import uuid

from fastapi import status

from app.constants import error_codes
from app.exceptions.api_exception import ApiException
from app.repositories import user_repository
from app.utils.response import success_response
from app.utils.auth import create_access_token


def insert_user(
        email: str,
        password: str,
        name: str
) -> dict:
    """신규 회원가입 처리"""

    # 이메일 입력 검증
    if not email:
        raise ApiException(
            status_code = status.HTTP_400_BAD_REQUEST,
            message = "회원가입 실패",
            code = error_codes.INVALID_EMAIL,
            detail = "올바른 이메일을 입력하세요."
        )

    # 비밀번호 입력 검증
    if not password:
        raise ApiException(
            status_code = status.HTTP_400_BAD_REQUEST,
            message = "회원가입 실패",
            code = error_codes.INVALID_PASSWORD,
            detail = "올바른 비밀번호를 입력하세요."
        )

    # 이름 검증
    if not name:
        raise ApiException(
            status_code = status.HTTP_400_BAD_REQUEST,
            message = "회원가입 실패",
            code = error_codes.INVALID_NAME,
            detail = "올바른 이름을 입력하세요."
        )

    # 이메일 중복 검증
    user = user_repository.select_user_by_email(email)

    if user:
        raise ApiException(
            status_code = status.HTTP_400_BAD_REQUEST,
            message = "회원가입 실패",
            code = error_codes.DUPLICATED_EMAIL,
            detail = "입력된 이메일로 가입된 계정이 있습니다."
        )

    user_id = str(uuid.uuid4())
    user_repository.insert_user(user_id, email, password, name)

    return success_response(
        message = "회원가입 성공",
        data = {
            "user_id" : user_id
        }
    )


def select_user_by_email_and_password(
        email: str,
        password: str
) -> dict:
    """로그인 처리"""

    # 1. 이메일 입력 검증
    if not email:
        raise ApiException(
            status_code = status.HTTP_400_BAD_REQUEST,
            message = "로그인 실패",
            code = error_codes.INVALID_EMAIL,
            detail = "올바른 이메일을 입력하세요."
        )

    # 2. 비밀번호 입력 검증
    if not password:
        raise ApiException(
            status_code = status.HTTP_400_BAD_REQUEST,
            message = "로그인 실패",
            code = error_codes.INVALID_PASSWORD,
            detail = "올바른 비밀번호를 입력하세요."
        )

    user = user_repository.select_user_by_email_and_password(email, password)

    if user is None:
        raise ApiException(
            status_code = status.HTTP_400_BAD_REQUEST,
            message = "로그인 실패",
            code = error_codes.INVALID_CREDENTIALS,
            detail = "아이디 또는 비밀번호가 다릅니다."
        )

    # JWT 토큰 생성
    access_token = create_access_token(user["user_id"])

    # 토큰 반환
    return success_response(
        message = "로그인 성공",
        data = {
            "access_token" : access_token,
            "token_type" : "bearer"
        }
    )