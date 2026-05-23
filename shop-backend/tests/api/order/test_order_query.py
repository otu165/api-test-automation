"""
경로 : shop-backend/tests/api/order/test_order_query.py
파일명 : test_order_query.py

주문 조회 API 테스트를 담당하는 파일

이 파일의 역할:
- 내 주문 목록 조회 성공 검증
- 내 주문 상세 조회 성공 검증

"""
from fastapi.testclient import TestClient

from tests.clients.order_client import OrderClient
from app.constants import error_codes
from tests.helpers.assertions import (
    assert_success_response,
    assert_error_response,
    assert_unauthorized_response
)


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
    assert_success_response(
        body = body,
        message = "주문 목록 조회 성공"
    )

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
    assert_success_response(
        body = detail_body,
        message = "주문 상세 조회 성공"
    )

    assert "order_id" in detail_body["data"]
    assert detail_body["data"]["order_id"] == created_order_id

    assert "product_id" in detail_body["data"]
    assert detail_body["data"]["product_id"] == product_id

    assert "quantity" in detail_body["data"]
    assert detail_body["data"]["quantity"] == quantity

    assert "status" in detail_body["data"]
    assert detail_body["data"]["status"] == "PAID"


def test_get_other_user_order_detail_not_found(
        client: TestClient,
        created_order_id: str,      # A 사용자의 order_id
        second_access_token: str    # B 사용자의 token
):
    """타인의 주문 상세 조회 실패 검증"""

    # 타인의 주문(created_order_id) 상세 조회 API 호출
    order_client = OrderClient(
        client = client,
        access_token = second_access_token
    )

    response = order_client.get_order_detail(created_order_id)

    # 상태코드 검증
    assert response.status_code == 404

    body = response.json()

    # 공통 응답 구조(error_response) 검증
    assert_error_response(
        body = body,
        message = "주문 상세 조회 실패",
        code = error_codes.ORDER_NOT_FOUND
    )


def test_get_canceled_order_detail_success(
        order_client: OrderClient,
        created_order_id: str
):
    """취소된 주문 상세 조회 시 CANCELED 상태 검증"""

    # 주문 취소 API 호출
    cancel_res = order_client.cancel_order(created_order_id)

    # 상태코드 검증
    assert cancel_res.status_code == 200

    # 주문 상세 조회 API 호출
    detail_res = order_client.get_order_detail(created_order_id)

    # 상태코드 검증
    assert detail_res.status_code == 200

    detail_body = detail_res.json()

    # 공통 응답 구조(success_response) 검증
    assert_success_response(
        body = detail_body,
        message = "주문 상세 조회 성공"
    )

    # data > order_id 검증
    assert "order_id" in detail_body["data"]
    assert detail_body["data"]["order_id"] == created_order_id

    # data > status 검증
    assert "status" in detail_body["data"]
    assert detail_body["data"]["status"] == "CANCELED"


def test_get_order_detail_not_found(
        order_client: OrderClient
):
    """존재하지 않는 주문 상세 조회 실패 검증"""

    # 주문 상세 조회 API 호출
    response = order_client.get_order_detail(
        order_id = "ORDER_NOT_FOUND"
    )

    # 상태코드 검증
    assert response.status_code == 404

    body = response.json()

    # 공통 응답 구조(error_response) 검증
    assert_error_response(
        body = body,
        message = "주문 상세 조회 실패",
        code = error_codes.ORDER_NOT_FOUND
    )


def test_get_orders_with_canceled_order(
        order_client: OrderClient,
        created_order_id: str
):
    """주문 목록 조회 시 취소된 주문 포함 검증"""

    # 첫 번째 주문 order_id = created_order_id

    # 두 번째 주문 생성
    second_order_res = order_client.create_order(
        product_id = "KB1001",
        quantity = 1
    )

    # 상태코드 검증
    assert second_order_res.status_code == 201

    # 응답에서 order_id 추출
    assert "data" in second_order_res.json()
    assert "order_id" in second_order_res.json()["data"]

    second_order_id = second_order_res.json()["data"]["order_id"]

    # 첫 번째 주문 취소
    cancel_res = order_client.cancel_order(created_order_id)

    # 상태코드 검증
    assert cancel_res.status_code == 200

    # 주문 목록 전체 조회
    orders_res = order_client.get_orders()

    # 상태코드 검증
    assert orders_res.status_code == 200

    orders_body = orders_res.json()

    # 공통 응답 구조(success_response) 검증
    assert_success_response(
        body = orders_body,
        message = "주문 목록 조회 성공",
    )

    # data > orders / count 검증
    assert "orders" in orders_body["data"]
    assert "count" in orders_body["data"]

    orders = orders_body["data"]["orders"]
    cnt = orders_body["data"]["count"]

    # 주문 개수 검증
    assert len(orders) == cnt
    assert cnt == 2

    # 주문 상태 검증
    order_status_map = {
        order["order_id"] : order["status"]
        for order in orders
    }

    assert order_status_map[created_order_id] == "CANCELED" # 첫 번째 주문은 취소 상태
    assert order_status_map[second_order_id] == "PAID"      # 두 번째 주문은 지불됨 상태


def test_get_orders_with_invalid_token(
        client: TestClient
):
    """잘못된 토큰 주문 목록 조회 실패 응답 검증"""

    order_client = OrderClient(
        client = client,
        access_token = "INVALID-TOKEN"
    )

    response = order_client.get_orders()

    # 상태코드 검증
    assert response.status_code == 401

    # 사용자 인증 실패 응답 검증
    assert_unauthorized_response(response.json())


def test_get_order_detail_with_invalid_token(
        client: TestClient,
        created_order_id: str
):
    """잘못된 토큰 주문 상세 조회 실패 응답 검증"""

    order_client = OrderClient(
        client = client,
        access_token = "INVALID-TOKEN"
    )

    response = order_client.get_order_detail(created_order_id)

    # 상태코드 검증
    assert response.status_code == 401

    # 사용자 인증 실패 응답 검증
    assert_unauthorized_response(response.json())
