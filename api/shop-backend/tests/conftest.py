"""
경로 : shop-backend/tests/conftest.py
파일명 : conftest.py

pytest 공통 fixture 를 관리하는 파일

이 파일의 역할:
- 테스트용 FastAPI Client 생성
- 테스트용 회원가입/로그인 데이터 생성
- 인증 API 테스트에서 사용할 access_token 생성

"""


import pytest
from fastapi.testclient import TestClient

from app.main import app
from tests.clients import auth_client


@pytest.fixture
def client():
    """테스트용 FastAPI Client 생성"""

    return TestClient(app)


@pytest.fixture
def signed_up_user(client: TestClient):
    """테스트용 회원가입 유저 생성"""

    user_data = {
        "email" : "fixture-user@example.com",
        "password" : "1234",
        "name" : "fixture-user"
    }

    response = auth_client.signup(
        client = client,
        email = user_data["email"],
        password = user_data["password"],
        name = user_data["name"]
    )

    # 상태코드 검증
    assert response.status_code == 201

    # 회원가입에 사용한 유저 데이터 반환
    # (다른 테스트에서 email, password 사용하기 위함)
    return user_data


@pytest.fixture
def access_token(
        client: TestClient,
        signed_up_user: dict
):
    """테스트용 access_token 생성"""

    response = auth_client.signin(
        client = client,
        email = signed_up_user["email"],
        password = signed_up_user["password"]
    )

    # 상태코드 검증
    assert response.status_code == 200

    body = response.json()

    # access_token 검증
    assert "access_token" in body["data"]
    assert isinstance(body["data"]["access_token"], str)
    assert 0 < len(body["data"]["access_token"])

    # JWT token 반환
    return body["data"]["access_token"]

