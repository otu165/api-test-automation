"""
경로 : shop-backend/tests/api/auth/test_auth_signup.py
파일명 : test_auth_signup.py

회원가입 API 테스트를 담당하는 파일

이 파일의 역할:
- 회원가입 성공 응답 검증
- 회원가입 실패 응답 검증
- JWT Access Token 발급 여부 검증

"""
from starlette.testclient import TestClient

from tests.clients.auth_client import AuthClient
from app.constants import error_codes
from app.repositories import user_repository
from tests.helpers.assertions import (
    assert_success_response,
    assert_error_response,
    assert_validation_error_response
)

import pytest

pytestmark = pytest.mark.auth


def test_signup_success(client):
    """회원가입 성공 응답 검증"""

    auth_client = AuthClient(client)

    response = auth_client.signup(
        email = "signup-success@example.com",
        password = "test1234!",
        name = "테스트유저"
    )

    # 상태코드 검증
    assert response.status_code == 201

    body = response.json()

    # 공통 응답 구조(success_response) 검증
    assert_success_response(
        body = body,
        message = "회원가입 성공"
    )

    # data > user_id 검증
    assert "user_id" in body["data"]
    assert isinstance(body["data"]["user_id"], str)
    assert 0 < len(body["data"]["user_id"])


def test_signup_email_too_long(client):
    """이메일 길이(254) 초과 회원가입 실패 검증"""

    auth_client = AuthClient(client)

    too_long_email = f"{'a' * 249}@a.com"

    response = auth_client.signup(
        email = too_long_email,
        password = "test1234!",
        name = "too-long-email"
    )

    # 상태코드 검증
    assert response.status_code == 422

    body = response.json()

    # 부적절한 데이터 입력 응답 검증
    assert_validation_error_response(body)

    # error > detail 검증
    assert "detail" in body["error"]
    assert "too long" in body["error"]["detail"]


def test_signup_password_is_hashed(client):
    """회원가입 시 비밀번호 해시 저장 검증"""

    email = "hased-password@example.com"
    password = "test1234!"

    auth_client = AuthClient(client)

    response = auth_client.signup(
        email = email,
        password = password,
        name = "hashed-pwd-user"
    )

    # 상태코드 검증
    assert response.status_code == 201

    # success_response 검증
    assert_success_response(
        body = response.json(),
        message = "회원가입 성공"
    )

    # DB에서 email 과 일치하는 유저 직접 조회
    user = user_repository.select_user_by_email(email)

    assert user is not None
    assert user["password"] != password
    assert user["password"].startswith("$2b$")  # bcrytp 로 hashing 됨 검증


def test_signup_password_too_short(client):
    """비밀번호 길이 부족(min_length = 8) 회원가입 실패"""
    auth_client = AuthClient(client)

    response = auth_client.signup(
        email="too-short-password@example.com",
        password="1234567",
        name="too-short-password"
    )

    # 상태코드 검증
    assert response.status_code == 422

    body = response.json()

    # 부적절한 데이터 입력 응답 검증
    assert_validation_error_response(body)

    assert "8 characters" in body["error"]["detail"]



def test_signup_password_too_long(client):
    """비밀번호 길이 초과(max_length = 72) 회원가입 실패"""

    auth_client = AuthClient(client)

    response = auth_client.signup(
        email = "too-long-password@example.com",
        password = f"{"a" * 73}",
        name = "too-long-password"
    )

    # 상태코드 검증
    assert response.status_code == 422

    body = response.json()

    # 부적절한 데이터 입력 응답 검증
    assert_validation_error_response(body)

    assert "72 characters" in body["error"]["detail"]



def test_signup_duplicate_email(client):
    """중복 이메일 회원가입 실패 응답 검증"""

    auth_client = AuthClient(client)

    auth_client.signup(
        email = "duplicate@example.com",
        password = "test1234!",
        name = "첫번째유저"
    )

    response = auth_client.signup(
        email = "duplicate@example.com",
        password = "4321test!",
        name = "두번째유저"
    )

    # 상태코드 검증
    assert response.status_code == 400

    body = response.json()

    # 공통 응답 구조(error_response) 검증
    assert_error_response(
        body = body,
        message = "회원가입 실패",
        code = error_codes.DUPLICATED_EMAIL
    )



def test_signup_invalid_email_format(client):
    """
    잘못된 이메일 형식 회원가입 실패 응답 검증
    models > EmailStr 타입이 자동 검증하는 부분 (공통 에러 응답 사용 X)
    """

    auth_client = AuthClient(client)

    response = auth_client.signup(
        email = "invalid-email",
        password = "test1234!",
        name = "이메일형식테스트유저"
    )

    # 상태코드 검증
    assert response.status_code == 422

    # 부적절한 데이터 입력 응답 검증
    assert_validation_error_response(response.json())


def test_signup_password_without_letter(
        client: TestClient
):
    """영문 없는 비밀번호 회원가입 실패"""

    auth_client = AuthClient(client)

    # 회원가입 API 요청
    response = auth_client.signup(
        email = "without-letter@example.com",
        password = "12345678!@#$%^&*",
        name = "pwd-without-letter-user"
    )

    # 상태코드 검증
    assert response.status_code == 422

    body = response.json()

    # 부적절한 데이터 입력 응답 검증
    assert_validation_error_response(body)

    # error > detail 메시지 검증 (password_validator.py 에서 추가됨)
    assert "영문자" in body["error"]["detail"]


def test_signup_password_without_number(
        client: TestClient
):
    """숫자 없는 비밀번호 회원가입 실패"""

    auth_client = AuthClient(client)

    # 회원가입 API 요청
    response = auth_client.signup(
        email="without-number@example.com",
        password="asdf!@#$%^&*",
        name="pwd-without-number-user"
    )

    # 상태코드 검증
    assert response.status_code == 422

    body = response.json()

    # 부적절한 데이터 입력 응답 검증
    assert_validation_error_response(body)

    # error > detail 메시지 검증 (password_validator.py 에서 추가됨)
    assert "숫자" in body["error"]["detail"]


def test_signup_password_without_special_char(
        client: TestClient
):
    """특수문자 없는 비밀번호 회원가입 실패"""

    auth_client = AuthClient(client)

    # 회원가입 API 요청
    response = auth_client.signup(
        email="without-special-char@example.com",
        password="asdf123456",
        name="pwd-without-special-char-user"
    )

    # 상태코드 검증
    assert response.status_code == 422

    body = response.json()

    # 부적절한 데이터 입력 응답 검증
    assert_validation_error_response(body)

    # error > detail 메시지 검증 (password_validator.py 에서 추가됨)
    assert "특수문자" in body["error"]["detail"]


def test_signup_empty_name(
        client: TestClient
):
    """빈 이름 회원가입 실패 응답 검증"""

    auth_client = AuthClient(client)

    response = auth_client.signup(
        email = "empty-name@example.com",
        password = "test1234!",
        name = ""
    )

    # 상태코드 검증
    assert response.status_code == 400

    # 회원가입 실패 응답 검증
    assert_error_response(
        body = response.json(),
        message = "회원가입 실패",
        code = error_codes.INVALID_NAME
    )