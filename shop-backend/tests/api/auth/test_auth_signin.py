"""
경로 : shop-backend/tests/api/auth/test_auth_signin.py
파일명 : test_auth_signin.py

로그인 API 테스트를 담당하는 파일

이 파일의 역할:
- 로그인 성공 응답 검증
- 로그인 실패 응답 검증

"""


from fastapi.testclient import TestClient

from tests.clients.auth_client import AuthClient
from app.constants import error_codes
from tests.helpers.assertions import (
    assert_success_response,
    assert_error_response,
    assert_validation_error_response
)

import pytest

pytestmark = pytest.mark.auth


def test_signin_success(client):
    """로그인 성공 및 JWT 발급 검증"""

    email = "signin-success@example.com"

    auth_client = AuthClient(client)

    # 회원가입
    auth_client.signup(
        email = email,
        password = "test1234!",
        name = "로그인유저"
    )

    # 로그인
    response = auth_client.signin(
        email = email,
        password = "test1234!"
    )

    # 상태코드 검증
    assert response.status_code == 200

    body = response.json()

    # 공통 응답 구조(success_response) 검증
    assert_success_response(
        body = body,
        message = "로그인 성공"
    )

    # data > access_token 검증
    assert "access_token" in body["data"]
    assert isinstance(body["data"]["access_token"], str)
    assert 0 < len(body["data"]["access_token"])

    # data > token_type 검증
    assert "token_type" in body["data"]
    assert body["data"]["token_type"] == "bearer"



def test_signin_wrong_password(client):
    """잘못된 비밀번호 로그인 실패 응답 검증"""

    auth_client = AuthClient(client)

    auth_client.signup(
        email = "wrong-password@example.com",
        password = "test1234!",
        name = "비밀번호테스트유저"
    )

    response = auth_client.signin(
        email="wrong-password@example.com",
        password="wrong-password123@"
    )

    # 상태코드 검증
    assert response.status_code == 400

    body = response.json()

    # 공통 응답 구조(error_response) 검증
    assert_error_response(
        body = body,
        message = "로그인 실패",
        code = error_codes.INVALID_CREDENTIALS
    )


def test_signin_not_registered_email(client):
    """존재하지 않는 이메일 로그인 실패 응답 검증"""

    auth_client = AuthClient(client)

    response = auth_client.signin(
        email = "not-found@example.com",
        password = "test1234!"
    )

    # 상태코드 검증
    assert response.status_code == 400

    body = response.json()

    # 공통 응답 구조(error_response) 검증
    assert_error_response(
        body = body,
        message = "로그인 실패",
        code = error_codes.INVALID_CREDENTIALS
    )


def test_signin_password_too_short(
        client: TestClient,
        signed_up_user: dict
):
    """비밀번호 길이 부족(min_length = 8) 로그인 실패"""
    auth_client = AuthClient(client)

    response = auth_client.signin(
        email = signed_up_user["email"],
        password = signed_up_user["password"][:7],
    )

    # 상태코드 검증
    assert response.status_code == 422

    # 부적절한 데이터 입력 응답 검증
    body = response.json()

    assert_validation_error_response(body)
    assert "8 characters" in body["error"]["detail"]




def test_signin_email_too_long(client):
    """이메일 길이 초과 로그인 실패"""

    auth_client = AuthClient(client)

    too_long_email = f"{'a' * 249}@a.com"

    response = auth_client.signin(
        email = too_long_email,
        password = "test1234!"
    )

    # 상태코드 검증
    assert response.status_code == 422

    body = response.json()

    # 부적절한 데이터 입력 응답 검증
    assert_validation_error_response(body)

    # error > detail 검증
    assert "detail" in body["error"]
    assert "too long" in body["error"]["detail"]



def test_signin_password_without_letter(
        client: TestClient,
        signed_up_user: dict
):
    """영문 없는 비밀번호 로그인 실패"""

    auth_client = AuthClient(client)

    # 로그인 API 요청
    response = auth_client.signin(
        email = signed_up_user["email"],
        password = "123456!@#"
    )

    # 상태코드 검증
    assert response.status_code == 422

    body = response.json()

    # 부적절한 데이터 입력 응답 검증
    assert_validation_error_response(body)

    # error > detail 메시지 검증 (password_validator.py 에서 추가됨)
    assert "영문자" in body["error"]["detail"]


def test_signin_password_without_number(
        client: TestClient,
        signed_up_user: dict
):
    """숫자 없는 비밀번호 로그인 실패"""

    auth_client = AuthClient(client)

    # 로그인 API 요청
    response = auth_client.signin(
        email=signed_up_user["email"],
        password="asdf!@#$"
    )

    # 상태코드 검증
    assert response.status_code == 422

    body = response.json()

    # 부적절한 데이터 입력 응답 검증
    assert_validation_error_response(body)

    # error > detail 메시지 검증 (password_validator.py 에서 추가됨)
    assert "숫자" in body["error"]["detail"]


def test_signin_password_without_special_char(
        client: TestClient,
        signed_up_user: dict
):
    """특수문자 없는 비밀번호 로그인 실패"""

    auth_client = AuthClient(client)

    # 로그인 API 요청
    response = auth_client.signin(
        email=signed_up_user["email"],
        password="asdf123456",
    )

    # 상태코드 검증
    assert response.status_code == 422

    body = response.json()

    # 부적절한 데이터 입력 응답 검증
    assert_validation_error_response(body)

    # error > detail 메시지 검증 (password_validator.py 에서 추가됨)
    assert "특수문자" in body["error"]["detail"]
