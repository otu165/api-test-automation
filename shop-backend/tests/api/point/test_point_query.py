"""
경로 : shop-backend/tests/api/point/test_point_query.py
파일명 : test_point_query.py

포인트 조회 API 테스트를 담당하는 파일

이 파일의 역할:
- 인증된 사용자의 포인트 조회 성공 검증
- 잘못된 토큰 요청 실패 검증

"""


from fastapi.testclient import TestClient

from app.constants import error_codes
from tests.clients.point_client import PointClient


def test_get_point_success(
        client: TestClient,
        access_token: str
):
    """포인트 조회 성공 응답 검증"""

    point_client = PointClient(client, access_token)

    response = point_client.get_point()

    # 상태코드 검증
    assert response.status_code == 200

    body = response.json()

    # 공통 응답 구조(success_response) 검증
    assert body["success"] is True
    assert body["message"] == "포인트 조회 성공"
    assert body["error"] is None

    # data 구조 검증
    assert "data" in body
    assert isinstance(body["data"], dict)

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

    body = response.json()

    # 공통 응답 구조(error_response) 검증
    assert body["success"] is False
    assert body["message"] == "사용자 인증 실패"
    assert body["data"] is None

    # error 검증
    assert "error" in body
    assert isinstance(body["error"], dict)

    # error > code 검증
    assert "code" in body["error"]
    assert body["error"]["code"] == error_codes.UNAUTHORIZED