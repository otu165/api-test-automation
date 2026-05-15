"""
경로 : shop-backend/tests/api/test_auth.py
파일명 : test_auth.py

회원가입 및 로그인 API 테스트를 담당하는 파일

이 파일의 역할:
- 회원가입 성공 응답 검증
- 로그인 성공 응답 검증
- JWT Access Token 발급 여부 검증

"""


from fastapi.testclient import TestClient

from app.main import app
from tests.clients import auth_client
from app.constants import error_codes

client = TestClient(app)


def test_signup_success():
    """회원가입 성공 응답 검증"""

    response = auth_client.signup(
        client = client,
        email = "signup@example.com",
        password = "1234",
        name = "테스트유저"
    )

    # 상태코드 검증
    assert response.status_code == 201

    body = response.json()

    # 공통 응답 구조(success_response) 검증
    assert body["success"] is True
    assert body["message"] == "회원가입 성공"
    assert body["error"] is None

    # data 구조 검증
    assert "data" in body
    assert isinstance(body["data"], dict)

    # data > user_id 검증
    assert "user_id" in body["data"]
    assert isinstance(body["data"]["user_id"], str)
    assert 0 < len(body["data"]["user_id"])



def test_signin_success():
    """로그인 성공 및 JWT 발급 검증"""

    # 회원가입
    auth_client.signup(
        client = client,
        email = "signin@example.com",
        password = "1234",
        name = "로그인유저"
    )

    # 로그인
    response = auth_client.signin(
        client = client,
        email = "signin@example.com",
        password = "1234"
    )

    # 상태코드 검증
    assert response.status_code == 200

    body = response.json()

    # 공통 응답 구조(success_response) 검증
    assert body["success"] is True
    assert body["message"] == "로그인 성공"
    assert body["error"] is None

    # data 구조 검증
    assert "data" in body
    assert isinstance(body["data"], dict)

    # data > access_token 검증
    assert "access_token" in body["data"]
    assert isinstance(body["data"]["access_token"], str)
    assert 0 < len(body["data"]["access_token"])

    # data > token_type 검증
    assert "token_type" in body["data"]
    assert body["data"]["token_type"] == "bearer"


def test_signup_duplicate_email():
    """중복 이메일 회원가입 실패 응답 검증"""

    auth_client.signup(
        client = client,
        email = "duplicate@example.com",
        password = "1234",
        name = "첫번째유저"
    )

    response = auth_client.signup(
        client = client,
        email = "duplicate@example.com",
        password = "4321",
        name = "두번째유저"
    )

    # 상태코드 검증
    assert response.status_code == 400

    body = response.json()

    # 공통 응답 구조(error_response) 검증
    assert body["success"] is False
    assert body["message"] == "회원가입 실패"
    assert body["data"] is None

    # error 구조 검증
    assert "error" in body
    assert isinstance(body["error"], dict)

    # error > code 검증
    assert "code" in body["error"]
    assert body["error"]["code"] == error_codes.DUPLICATED_EMAIL


def test_signin_wrong_password():
    """잘못된 비밀번호 로그인 실패 응답 검증"""

    auth_client.signup(
        client = client,
        email = "wrong-password@example.com",
        password = "1234",
        name = "비밀번호테스트유저"
    )

    response = auth_client.signin(
        client = client,
        email="wrong-password@example.com",
        password="wrong-password"
    )

    # 상태코드 검증
    assert response.status_code == 400

    body = response.json()

    # 공통 응답 구조(error_response) 검증
    assert body["success"] is False
    assert body["message"] == "로그인 실패"
    assert body["data"] is None

    # error 구조 검증
    assert "error" in body
    assert isinstance(body["error"], dict)

    # error > code 검증
    assert "code" in body["error"]
    assert body["error"]["code"] == error_codes.INVALID_CREDENTIALS


def test_signin_not_registered_email():
    """존재하지 않는 이메일 로그인 실패 응답 검증"""

    response = auth_client.signin(
        client = client,
        email = "not-found@example.com",
        password = "1234"
    )

    # 상태코드 검증
    assert response.status_code == 400

    body = response.json()

    # 공통 응답 구조(error_response) 검증
    assert body["success"] is False
    assert body["message"] == "로그인 실패"
    assert body["data"] is None

    # error 구조 검증
    assert "error" in body
    assert isinstance(body["error"], dict)

    # error > code 검증
    assert "code" in body["error"]
    assert body["error"]["code"] == error_codes.INVALID_CREDENTIALS


def test_signup_invalid_email_format():
    """
    잘못된 이메일 형식 회원가입 실패 응답 검증
    models > EmailStr 타입이 자동 검증하는 부분 (공통 에러 응답 사용 X)
    """

    response = auth_client.signup(
        client = client,
        email = "invalid-email",
        password = "1234",
        name = "이메일형식테스트유저"
    )

    # 상태코드 검증
    assert response.status_code == 422



