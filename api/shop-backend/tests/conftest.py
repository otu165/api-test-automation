"""
경로 : shop-backend/tests/conftest.py
파일명 : conftest.py

pytest 공통 fixture 를 관리하는 파일

이 파일의 역할:
- 테스트용 FastAPI Client 생성
- 테스트용 회원가입/로그인 데이터 생성
- 인증 API 테스트에서 사용할 access_token 생성

"""


import os
import uuid

# app.main 을 import 하면 내부에서 init_db() 가 실행되기 때문에
# from app.main import app 보다 위에 위치해야 함
#
# 현재 실행중인 Python 프로세스 메모리 안에서만 환경변수 생성
# ㄴ 즉, pytest 프로세스 안에서만 유효하므로 pytest 종료 시 환경변수가 사라진다
os.environ["DATABASE_NAME"] = "test_shop.db"


import pytest
from fastapi.testclient import TestClient

from app.main import app
from tests.clients.auth_client import AuthClient
from app.database import get_connection
from app import sql_queries


@pytest.fixture
def client():
    """테스트용 FastAPI Client 생성"""

    return TestClient(app)


# autouse = True : 모든 테스트 전에 자동 실행
# 즉, 테스트 함수에 reset_test_database 를 적지 않아도 자동으로 항상 실행한다.
@pytest.fixture(autouse = True)
def reset_test_database():
    """테스트 실행 전 테스트 DB 초기화"""

    with get_connection() as connection:
        cursor = connection.cursor()

        # users 테이블 데이터 삭제
        cursor.execute("DELETE FROM tb_user")

        # products 테이블 데이터 삭제
        cursor.execute("DELETE FROM tb_product")

        # orders 테이블 데이터 삭제
        cursor.execute("DELETE FROM tb_order")

        # 테스트용 기본 상품 데이터 재생성
        products = [
            ("KB1001", "키보드", 500, 10),
            ("MS1001", "마우스", 300, 10)
        ]

        cursor.executemany(sql_queries.INSERT_PRODUCT, products)

        connection.commit()


@pytest.fixture
def signed_up_user(client: TestClient):
    """테스트용 회원가입 유저 생성"""

    user_data = {
        "email" : f"fixture-user-{uuid.uuid4()}@example.com",
        "password" : "1234",
        "name" : "fixture-user"
    }

    auth_client = AuthClient(client)

    response = auth_client.signup(
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

    auth_client = AuthClient(client)

    response = auth_client.signin(
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

