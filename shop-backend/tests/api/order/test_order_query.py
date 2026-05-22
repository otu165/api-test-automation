"""
경로 : shop-backend/tests/api/order/test_order_query.py
파일명 : test_order_query.py

주문 조회 API 테스트를 담당하는 파일

이 파일의 역할:
- 내 주문 목록 조회 성공 검증
- 내 주문 상세 조회 성공 검증

"""


from tests.clients.order_client import OrderClient


def test_get_my_orders_success(
        order_client: OrderClient
):
    """내 주문 히스토리 조회 API 성공 검증"""

    # 키보드 주문 생성
    kb_order_res = order_client.create_order(
        product_id = "KB1001",
        quantity = 1
    )

    # 마우스 주문 생성
    ms_order_res = order_client.create_order(
        product_id = "MS1001",
        quantity = 1
    )

    # 상태코드 검증
    assert kb_order_res.status_code == 201
    assert ms_order_res.status_code == 201

    # 데이터 검증
    assert "data" in kb_order_res.json()
    assert "order_id" in kb_order_res.json()["data"]

    kb_order_id = kb_order_res.json()["data"]["order_id"]

    assert "data" in ms_order_res.json()
    assert "order_id" in ms_order_res.json()["data"]

    ms_order_id = ms_order_res.json()["data"]["order_id"]

    # 나의 주문 목록 조회
    response = order_client.get_orders()

    # 상태코드 검증
    assert response.status_code == 200

    body = response.json()

    # 공통 응답 구조(success_response) 검증
    assert body["success"] is True
    assert body["message"] == "주문 목록 조회 성공"
    assert body["error"] is None

    # data 구조 검증
    assert "data" in body
    assert isinstance(body["data"], dict)

    assert len(body["data"]["orders"]) == body["data"]["count"]

    # orders 내부 order_id 검증
    order_ids = {
        order["order_id"]
        for order in body["data"]["orders"]
    }

    assert kb_order_id in order_ids
    assert ms_order_id in order_ids


def test_get_order_detail_success(
        order_client: OrderClient,
        created_order_id: str
):
    """내 주문 상세 조회 성공 검증"""

    product_id = "KB1001"
    quantity = 1

    # 주문 상세 조회
    detail_res = order_client.get_order_detail(created_order_id)

    # 상태코드 검증
    assert detail_res.status_code == 200

    detail_body = detail_res.json()

    # 공통 응답 구조(success_response) 검증
    assert detail_body["success"] is True
    assert detail_body["message"] == "주문 상세 조회 성공"
    assert detail_body["error"] is None

    # data 구조 검증
    assert "data" in detail_body
    assert isinstance(detail_body["data"], dict)

    assert "order_id" in detail_body["data"]
    assert detail_body["data"]["order_id"] == created_order_id

    assert "product_id" in detail_body["data"]
    assert detail_body["data"]["product_id"] == product_id

    assert "quantity" in detail_body["data"]
    assert detail_body["data"]["quantity"] == quantity

    assert "status" in detail_body["data"]
    assert detail_body["data"]["status"] == "PAID"