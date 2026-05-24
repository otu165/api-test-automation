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
from tests.helpers.assertions import assert_success_response

import pytest

pytestmark = pytest.mark.point


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

