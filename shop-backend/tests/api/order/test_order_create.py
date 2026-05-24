"""
경로 : shop-backend/tests/api/order/test_order_create.py
파일명 : test_order_create.py

주문 생성 API 테스트를 담당하는 파일

이 파일의 역할:
- 인증된 사용자의 주문 생성 성공 검증
- 잘못된 토큰 요청 실패 검증
- 존재하지 않는 상품 주문 실패 검증
- 주문 수량 validation 실패 검증

"""


from fastapi.testclient import TestClient

from tests.clients.order_client import OrderClient
from tests.clients.point_client import PointClient
from app.constants import error_codes
from app.repositories import product_repository
from tests.helpers.assertions import (
    assert_success_response,
    assert_error_response,
    assert_unauthorized_response,
    assert_validation_error_response
)

import pytest

pytestmark = pytest.mark.order


def test_create_order_success(
        order_client: OrderClient
):
    """주문 생성 성공 응답 검증"""

    product_id = "KB1001"
    quantity = 1

    response = order_client.create_order(
        product_id = product_id,
        quantity = quantity
    )

    # 상태코드 검증
    assert response.status_code == 201

    body = response.json()

    # 공통 응답 구조(success_response) 검증
    assert_success_response(
        body = body,
        message = "주문 성공"
    )

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
    order_client = OrderClient(
        client,
        access_token = "invalid-token"
    )

    response = order_client.create_order(
        product_id = "KB1001",
        quantity = 1
    )

    # 상태코드 검증
    assert response.status_code == 401

    # 사용자 인증 실패 응답 검증
    assert_unauthorized_response(response.json())


def test_create_order_with_not_found_product(
        order_client: OrderClient
):
    """존재하지 않는 상품 주문 실패 응답 검증"""

    response = order_client.create_order(
        product_id = "NOTFOUND",
        quantity = 1
    )

    # 상태코드 검증
    assert response.status_code == 404

    body = response.json()

    # 실패 응답 구조 검증
    assert_error_response(
        body = body,
        message = "주문 실패",
        code = error_codes.PRODUCT_NOT_FOUND
    )


def test_create_order_with_zero_quantity(
        order_client: OrderClient
):
    """주문 수량 0 입력 시 validation 실패 응답 검증"""

    response = order_client.create_order(
        product_id = "MS1001",
        quantity = 0
    )

    # 상태코드 검증
    assert response.status_code == 422

    # 부적절한 데이터 입력 응답 검증
    assert_validation_error_response(response.json())


def test_create_order_with_insufficient_stock(
        order_client: OrderClient
):
    """재고 부족 상품 주문 실패 응답 검증"""

    product_id = "KB1001"

    # 테스트 조건 : 상품 재고를 0개로 강제 업데이트
    product_repository.update_product_stock(
        product_id = product_id,
        new_stock = 0
    )

    # 상품 주문 API 요청
    response = order_client.create_order(
        product_id = product_id,
        quantity = 1
    )

    # 상태코드 검증
    assert response.status_code == 400

    body = response.json()

    # 공통 응답 구조(error_response) 검증
    assert_error_response(
        body = body,
        message = "주문 실패",
        code = error_codes.INSUFFICIENT_STOCK
    )


def test_create_order_with_insufficient_point(
        order_client: OrderClient,
        point_client: PointClient
):
    """포인트 부족으로 인한 주문 실패 응답 검증"""

    product_id = "KB1001"

    # 계정 포인트 조회
    point_res = point_client.get_point()

    # 상태코드 검증
    assert point_res.status_code == 200

    # 응답 body 에서 현재 포인트 조회
    point_body = point_res.json()
    assert "data" in point_body
    assert "point" in point_body["data"]

    user_point = point_body["data"]["point"]

    # 상품 가격 조회
    product = product_repository.select_product_by_id(product_id)

    assert product is not None
    assert "price" in product

    product_price = product["price"]

    # 사용자가 살 수 없는 수량으로 계산
    quantity = user_point // product_price + 1

    # 상품 주문 API 호출
    order_res = order_client.create_order(
        product_id = product_id,
        quantity = quantity
    )

    # 상태코드 검증
    assert order_res.status_code == 400

    order_body = order_res.json()

    # 공통 응답 구조(error_response) 검증
    assert_error_response(
        body = order_body,
        message = "주문 실패",
        code = error_codes.INSUFFICIENT_POINT
    )


def test_create_order_with_negative_quantity(
        order_client: OrderClient
):
    """주문 수량 음수 입력 시 validation 실패 응답 검증"""

    # 주문 생성 API 호출
    response = order_client.create_order(
        product_id = "KB1001",
        quantity = -1 # 음수
    )

    # 상태코드 검증
    assert response.status_code == 422

    # 부적절한 데이터 입력 응답 검증
    assert_validation_error_response(response.json())

