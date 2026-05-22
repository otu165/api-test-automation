"""
경로 : shop-backend/tests/api/auth/test_auth_signin.py
파일명 : test_auth_signin.py

로그인 API 테스트를 담당하는 파일

이 파일의 역할:
- 로그인 성공 응답 검증
- 로그인 실패 응답 검증

"""


from tests.clients.auth_client import AuthClient
from app.constants import error_codes


def test_signin_success(client):
    """로그인 성공 및 JWT 발급 검증"""

    email = "signin-success@example.com"

    auth_client = AuthClient(client)

    # 회원가입
    auth_client.signup(
        email = email,
        password = "1234",
        name = "로그인유저"
    )

    # 로그인
    response = auth_client.signin(
        email = email,
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



def test_signin_wrong_password(client):
    """잘못된 비밀번호 로그인 실패 응답 검증"""

    auth_client = AuthClient(client)

    auth_client.signup(
        email = "wrong-password@example.com",
        password = "1234",
        name = "비밀번호테스트유저"
    )

    response = auth_client.signin(
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


def test_signin_not_registered_email(client):
    """존재하지 않는 이메일 로그인 실패 응답 검증"""

    auth_client = AuthClient(client)

    response = auth_client.signin(
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



def test_signin_email_too_long(client):
    """이메일 길이 초과 로그인 실패"""

    auth_client = AuthClient(client)

    too_long_email = f"{"a" * 249}@a.com"

    response = auth_client.signin(
        email = too_long_email,
        password = "1234"
    )

    # 상태코드 검증
    assert response.status_code == 422

    body = response.json()

    # 공통 응답 구조(error_response) 검증
    assert body["success"] is False
    assert body["message"] == "부적절한 데이터 입력"
    assert body["data"] is None

    # error 검증
    assert "error" in body
    assert isinstance(body["error"], dict)

    # error > code 검증
    assert "code" in body["error"]
    assert body["error"]["code"] == error_codes.VALIDATION_ERROR

    # error > detail 검증
    assert "detail" in body["error"]
    assert "too long" in body["error"]["detail"]


