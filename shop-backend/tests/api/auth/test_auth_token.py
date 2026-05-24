"""
경로 : shop-backend/tests/api/auth/test_auth_token.py
파일명 : test_auth_token.py

JWT 인증 실패 케이스를 검증하는 파일
ㄴ 보호 API 중 "/points" 를 대표 API 로 사용하여
ㄴ Authorization Header 및 JWT 토큰 검증 흐름을 테스트한다.

이 파일의 역할:
- Authorization Header 없음 검증
- Bearer 형식이 아닌 Header 검증
- 잘못된 JWT 형식 검증
- 위조/만료/user_id 없는 JWT 검증

"""


from jose import jwt
from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient

from app.utils.auth import SECRET_KEY, ALGORITHM
from tests.clients.point_client import PointClient
from tests.helpers.assertions import assert_unauthorized_response

import pytest

pytestmark = pytest.mark.auth


def test_protected_api_with_invalid_token(
        client: TestClient
):
    """잘못된 토큰 포인트 조회 실패 응답 검증"""

    point_client = PointClient(
        client,
        access_token = "invalid-token"
    )

    response = point_client.get_point()

    # 상태코드 검증
    assert response.status_code == 401

    # 사용자 인증 실패 응답 검증
    assert_unauthorized_response(response.json())


def test_protected_api_with_forged_jwt_token(
        client: TestClient
):
    """위조된 JWT 토큰 포인트 조회 실패 응답 검증"""

    payload = {
        "user_id": "fake-user-id"
        # SECRET_KEY 불일치가 우선 검증되므로, exp 가 없어도 상관 없다.
    }

    forged_token = jwt.encode(
        payload,
        "wrong-secret-key",
        algorithm = ALGORITHM
    )

    # 위조된 토큰으로 포인트 조회 API 요청
    response = client.get(
        "/points",
        headers = {
            "Authorization" : f"Bearer {forged_token}"
        }
    )

    # 상태코드 검증
    assert response.status_code == 401

    # 사용자 인증 실패 응답 검증
    assert_unauthorized_response(response.json())


def test_protected_api_with_expired_jwt_token(
        client: TestClient
):
    """만료된 JWT 토큰 포인트 조회 실패 응답 검증"""

    payload = {
        "user_id": "expired-user-id",
        "exp": datetime.now(UTC) - timedelta(minutes=1)  # 1분 전에 만료된 시간으로 세팅
    }

    expired_token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm = ALGORITHM
    )

    # 만료된 토큰으로 포인트 조회 API 요청
    response = client.get(
        "/points",
        headers = {
            "Authorization" : f"Bearer {expired_token}"
        }
    )

    # 상태코드 검증
    assert response.status_code == 401

    # 사용자 인증 실패 응답 검증
    assert_unauthorized_response(response.json())


def test_protected_api_with_missing_user_id_jwt_token(
        client: TestClient
):
    """user_id 가 없는 JWT 토큰 포인트 조회 실패 응답 검증"""

    payload = {
        "exp" : datetime.now(UTC) + timedelta(minutes=10)
    }

    token_without_user_id = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    # user_id 가 없는 토큰으로 포인트 조회 API 요청
    response = client.get(
        "/points",
        headers = {
            "Authorization" : f"Bearer {token_without_user_id}"
        }
    )

    # 상태코드 검증
    assert response.status_code == 401

    # 사용자 인증 실패 응답 검증
    assert_unauthorized_response(response.json())


def test_protected_api_without_auth_header(
        client: TestClient
):
    """Authorization Header 없이 포인트 조회 실패 응답 검증"""

    response = client.get("/points") # header 넘기지 않았음

    # 상태코드 검증
    assert response.status_code == 401

    # 사용자 인증 실패 응답 검증
    assert_unauthorized_response(response.json())


def test_protected_api_with_invalid_auth_header(
        client: TestClient
):
    """Bearer 형식이 아닌 Auth Header 포인트 조회 실패 응답 검증"""

    response = client.get(
        "/points",
        headers = {
            "Authorization" : "Token invalid-token"
        }
    )

    # 상태코드 검증
    assert response.status_code == 401

    # 사용자 인증 실패 응답 검증
    assert_unauthorized_response(response.json())