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
