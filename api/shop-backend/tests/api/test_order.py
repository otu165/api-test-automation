"""
경로 : shop-backend/tests/api/test_order.py
파일명 : test_order.py

주문 API 테스트를 담당하는 파일

이 파일의 역할:
- 인증된 사용자의 주문 생성 성공 검증
- 잘못된 토큰 요청 실패 검증

"""


from fastapi.testclient import TestClient

from tests.clients import order_client


def test_create_order_success(
        client: TestClient,
        access_token: str
):
    """주문 생성 성공 응답 검증"""

    product_id = "KB1001"
    quantity = 1

    response = order_client.create_order(
        client = client,
        access_token = access_token,
        product_id = product_id,
        quantity = quantity
    )

    # 상태코드 검증
    assert response.status_code == 201

    body = response.json()

    # 공통 응답 구조(success_response) 검증
    assert body["success"] is True
    assert body["message"] == "주문 성공"
    assert body["error"] is None

    # data 구조 검증
    assert "data" in body
    assert isinstance(body["data"], dict)

    # data > product_id 검증
    assert "product_id" in body["data"]
    assert isinstance(body["data"]["product_id"], str)
    assert body["data"]["product_id"] == product_id

    # data > quantity 검증
    assert "quantity" in body["data"]
    assert isinstance(body["data"]["quantity"], int)
    assert body["data"]["quantity"] == quantity


def test_create_order_with_invalid_token(
        client: TestClient
):
    """잘못된 토큰 주문 생성 실패 응답 검증"""

    response = order_client.create_order(
        client = client,
        access_token = "invalid-token",
        product_id = "KB1001",
        quantity = 1
    )

    # 상태코드 검증
    assert response.status_code == 401
