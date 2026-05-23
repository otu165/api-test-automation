"""
경로 : shop-backend/tests/api/point/test_point_query.py
파일명 : test_point_query.py

포인트 조회 API 테스트를 담당하는 파일

이 파일의 역할:
- 인증된 사용자의 포인트 조회 성공 검증
- 잘못된 토큰 요청 실패 검증

"""


from fastapi.testclient import TestClient

from tests.clients.point_client import PointClient
from tests.helpers.assertions import (
    assert_success_response,
    assert_unauthorized_response
)


def test_get_point_success(
        client: TestClient,
        access_token: str
):
    """포인트 조회 성공 응답 검증"""

    point_client = PointClient(client, access_token)

    response = point_client.get_point()

    # 상태코드 검증
    assert response.status_code == 200

    # success_response 검증
    body = response.json()

    assert_success_response(
        body = body,
        message = "포인트 조회 성공"
    )

    # data > point 검증
    assert "point" in body["data"]
    assert isinstance(body["data"]["point"], int)
    assert 0 <= body["data"]["point"]


def test_get_point_with_invalid_token(
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


def test_get_point_without_auth_header(
        client: TestClient
):
    """Authorization Header 없이 포인트 조회 실패 응답 검증"""

    response = client.get("/points") # header 넘기지 않았음

    # 상태코드 검증
    assert response.status_code == 401

    # 사용자 인증 실패 응답 검증
    assert_unauthorized_response(response.json())


def test_get_point_with_invalid_auth_header(
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
