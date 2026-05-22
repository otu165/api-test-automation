"""
경로 : shop-backend/tests/api/test_auth_signup.py
파일명 : test_auth_signup.py

회원가입 API 테스트를 담당하는 파일

이 파일의 역할:
- 회원가입 성공 응답 검증
- 회원가입 실패 응답 검증
- JWT Access Token 발급 여부 검증

"""


from tests.clients.auth_client import AuthClient
from app.constants import error_codes
from app.repositories import user_repository


def test_signup_success(client):
    """회원가입 성공 응답 검증"""

    auth_client = AuthClient(client)

    response = auth_client.signup(
        email = "signup-success@example.com",
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


def test_signup_email_too_long(client):
    """이메일 길이(254) 초과 회원가입 실패 검증"""

    auth_client = AuthClient(client)

    too_long_email = f"{"a" * 249}@a.com"

    response = auth_client.signup(
        email = too_long_email,
        password = "1234",
        name = "too-long-email"
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


def test_signup_password_is_hashed(client):
    """회원가입 시 비밀번호 해시 저장 검증"""

    email = "hased-password@example.com"
    password = "1234"

    auth_client = AuthClient(client)

    response = auth_client.signup(
        email = email,
        password = password,
        name = "hashed-pwd-user"
    )

    # 상태코드 검증
    assert response.status_code == 201

    # body 검증
    body = response.json()

    assert body["success"] is True
    assert body["message"] == "회원가입 성공"
    assert body["error"] is None

    # DB에서 email 과 일치하는 유저 직접 조회
    user = user_repository.select_user_by_email(email)

    assert user is not None
    assert user["password"] != password
    assert user["password"].startswith("$2b$")  # bcrytp 로 hashing 됨 검증


def test_signup_password_too_short(client):
    """비밀번호 길이 부족(min_length = 4) 회원가입 실패"""
    auth_client = AuthClient(client)

    response = auth_client.signup(
        email="too-short-password@example.com",
        password="aaa",
        name="too-short-password"
    )

    # 상태코드 검증
    assert response.status_code == 422

    # 공통 응답 구조(error_response) 검증
    body = response.json()

    assert body["success"] is False
    assert body["message"] == "부적절한 데이터 입력"
    assert body["data"] is None

    assert body["error"]["code"] == error_codes.VALIDATION_ERROR
    assert "4 characters" in body["error"]["detail"]



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

    # 공통 응답 구조(error_response) 검증
    body = response.json()

    assert body["success"] is False
    assert body["message"] == "부적절한 데이터 입력"
    assert body["data"] is None

    assert body["error"]["code"] == error_codes.VALIDATION_ERROR
    assert "72 characters" in body["error"]["detail"]



def test_signup_duplicate_email(client):
    """중복 이메일 회원가입 실패 응답 검증"""

    auth_client = AuthClient(client)

    auth_client.signup(
        email = "duplicate@example.com",
        password = "1234",
        name = "첫번째유저"
    )

    response = auth_client.signup(
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


def test_signup_invalid_email_format(client):
    """
    잘못된 이메일 형식 회원가입 실패 응답 검증
    models > EmailStr 타입이 자동 검증하는 부분 (공통 에러 응답 사용 X)
    """

    auth_client = AuthClient(client)

    response = auth_client.signup(
        email = "invalid-email",
        password = "1234",
        name = "이메일형식테스트유저"
    )

    # 상태코드 검증
    assert response.status_code == 422

    body = response.json()

    # 공통 응답 구조(error_response) 검증
    assert body["success"] is False
    assert body["message"] == "부적절한 데이터 입력"
    assert body["data"] is None

    # error 구조 검증
    assert "error" in body
    assert isinstance(body["error"], dict)

    # error > code 검증
    assert "code" in body["error"]
    assert body["error"]["code"] == error_codes.VALIDATION_ERROR


