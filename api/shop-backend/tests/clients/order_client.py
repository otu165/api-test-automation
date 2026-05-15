"""
경로 : shop-backend/tests/clients/order_client.py
파일명 : order_client.py

주문 API 테스트 요청을 담당하는 파일

이 파일의 역할:
- 주문 생성 API 요청을 보냄
- Authorization 헤더 포함 요청을 보냄
- 테스트 코드의 API 호출 중복을 줄임

"""


from fastapi.testclient import TestClient


def create_order(
        client: TestClient,
        product_id: str,
        quantity: int,
        access_token: str | None = None
):
    """주문 생성 API 요청"""

    headers = {}

    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"

    return client.post(
        "/orders",
        headers = headers,
        json = {
            "product_id" : product_id,
            "quantity" : quantity
        }
    )