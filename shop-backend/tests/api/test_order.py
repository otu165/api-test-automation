"""
경로 : shop-backend/tests/api/test_order.py
파일명 : test_order.py

주문 API 테스트를 담당하는 파일

이 파일의 역할:
- 인증된 사용자의 주문 생성 성공 검증
- 잘못된 토큰 요청 실패 검증

"""


from fastapi.testclient import TestClient

from tests.clients.order_client import OrderClient
from tests.clients.point_client import PointClient
from app.constants import error_codes


def test_create_order_success(
        client: TestClient,
        access_token: str
):
    """주문 생성 성공 응답 검증"""

    product_id = "KB1001"
    quantity = 1

    order_client = OrderClient(client, access_token)

    response = order_client.create_order(
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


def test_create_order_with_not_found_product(
        client: TestClient,
        access_token: str
):
    """존재하지 않는 상품 주문 실패 응답 검증"""

    order_client = OrderClient(client, access_token)

    response = order_client.create_order(
        product_id = "NOTFOUND",
        quantity = 1
    )

    # 상태코드 검증
    assert response.status_code == 404

    body = response.json()

    # 실패 응답 구조 검증
    assert body["success"] is False
    assert body["message"] == "주문 실패"
    assert body["data"] is None

    # error 검증
    assert "error" in body
    assert isinstance(body["error"], dict)

    # error > code 검증
    assert "code" in body["error"]
    assert body["error"]["code"] == error_codes.PRODUCT_NOT_FOUND


def test_create_order_with_zero_quantity(
        client: TestClient,
        access_token: str
):
    """주문 수량 0 입력 시 validation 실패 응답 검증"""

    order_client = OrderClient(client, access_token)

    response = order_client.create_order(
        product_id = "MS1001",
        quantity = 0
    )

    # 상태코드 검증
    assert response.status_code == 422

    body = response.json()

    # 공통 응답 구조(error_response) 검증
    assert body["success"] is False
    assert body["message"] == "부적절한 데이터 입력"
    assert body["data"] is None

    # error 구조 검증
    assert "error" in body
    assert isinstance(body["error"], dict)

    # error > code 검증
    assert "code" in body["error"]
    assert body["error"]["code"] == error_codes.VALIDATION_ERROR



def test_cancel_order_success(
        client: TestClient,
        access_token: str
):
    """주문 취소 성공 응답 검증"""

    order_client = OrderClient(client, access_token)

    # 주문 생성
    create_order_res = order_client.create_order(
        product_id = "MS1001",
        quantity = 1
    )

    # 상태코드 확인
    assert create_order_res.status_code == 201

    create_order_body = create_order_res.json()

    # 데이터 확인
    assert "data" in create_order_body
    assert "order_id" in create_order_body["data"]

    order_id = create_order_body["data"]["order_id"]

    # 주문 취소
    cancel_order_res = order_client.create_order_cancel(order_id)

    # 상태코드 확인
    assert cancel_order_res.status_code == 200

    cancel_order_body = cancel_order_res.json()

    # 공통 응답 구조(success_response) 검증
    assert cancel_order_body["success"] is True
    assert cancel_order_body["message"] == "주문 취소 성공"
    assert cancel_order_body["error"] is None

    # data 구조 검증
    assert "data" in cancel_order_body
    assert isinstance(cancel_order_body["data"], dict)

    # data > order_id 검증
    assert "order_id" in cancel_order_body["data"]
    assert cancel_order_body["data"]["order_id"] == order_id

    # data > status 검증
    assert "status" in cancel_order_body["data"]
    assert cancel_order_body["data"]["status"] == "CANCELED"


def test_cancel_order_not_found(
        client: TestClient,
        access_token: str
):
    """존재하지 않는 주문 취소 실패"""

    order_client = OrderClient(client, access_token)

    # 존재하지 않는 주문 취소 요청
    response = order_client.create_order_cancel(
        order_id = "ORDER-NOT-FOUND"
    )

    # 응답 검증
    assert response.status_code == 404

    body = response.json()

    # 공통 응답 구조(error_response) 검증
    assert body["success"] is False
    assert body["message"] == "주문 취소 실패"
    assert body["data"] is None

    # error 구조 검증
    assert "error" in body
    assert isinstance(body["error"], dict)

    # error > code 검증
    assert "code" in body["error"]
    assert body["error"]["code"] == error_codes.ORDER_NOT_FOUND



def test_cancel_order_already_canceled(
        client: TestClient,
        access_token: str
):
    """이미 취소된 주문 재취소 실패 검증"""

    order_client = OrderClient(client, access_token)

    # 주문 생성
    create_order_res = order_client.create_order(
        product_id = "MS1001",
        quantity = 1
    )

    # 상태코드 검증
    assert create_order_res.status_code == 201

    # order_id 꺼내기
    create_order_body = create_order_res.json()

    assert "data" in create_order_body
    assert "order_id" in create_order_body["data"]

    order_id = create_order_body["data"]["order_id"]

    # 주문 취소
    cancel_order_res = order_client.create_order_cancel(order_id)

    # 상태코드 검증
    assert cancel_order_res.status_code == 200

    # 동일 주문 재취소
    double_cancel_order_res = order_client.create_order_cancel(order_id)

    # 상태코드 검증
    assert double_cancel_order_res.status_code == 400

    dco_body = double_cancel_order_res.json()

    # 공통 응답 구조(error_response) 검증
    assert dco_body["success"] is False
    assert dco_body["message"] == "주문 취소 실패"
    assert dco_body["data"] is None

    # error 구조 검증
    assert "error" in dco_body
    assert isinstance(dco_body["error"], dict)

    # error > code 검증
    assert "code" in dco_body["error"]
    assert dco_body["error"]["code"] == error_codes.ORDER_ALREADY_CANCELED



def test_cancel_order_restore_point(
        client: TestClient,
        access_token: str
):
    """주문 취소 시 계정 포인트 복구 검증"""

    point_client = PointClient(client, access_token)

    # 포인트 조회
    before_point_res = point_client.get_point()

    # 상태코드 검증
    assert before_point_res.status_code == 200

    before_point_body = before_point_res.json()

    # 응답 검증
    assert "data" in before_point_body
    assert "point" in before_point_body["data"]

    before_point = before_point_body["data"]["point"]

    # 주문 생성
    order_client = OrderClient(client, access_token)

    create_order_res = order_client.create_order(
        product_id = "KB1001",
        quantity = 1
    )

    # 상태코드 검증
    assert create_order_res.status_code == 201

    create_order_body = create_order_res.json()

    # 데이터 검증
    assert "data" in create_order_body
    assert "order_id" in create_order_body["data"]
    assert "total_price" in create_order_body["data"]

    order_id = create_order_body["data"]["order_id"]
    total_price = create_order_body["data"]["total_price"]

    # 주문 후 포인트 차감 검증
    after_point_res = point_client.get_point()

    # 상태코드 검증
    assert after_point_res.status_code == 200

    after_point_body = after_point_res.json()

    # 응답 검증
    assert "data" in after_point_body
    assert "point" in after_point_body["data"]

    after_point = after_point_body["data"]["point"]

    assert after_point == before_point - total_price

    # 주문 취소
    cancel_order_res = order_client.create_order_cancel(order_id)

    # 상태코드 확인
    assert cancel_order_res.status_code == 200

    # 포인트 복구 확인
    restored_point_res = point_client.get_point()

    # 상태코드 확인
    assert restored_point_res.status_code == 200

    restored_point_body = restored_point_res.json()

    # 데이터 확인
    assert "data" in restored_point_body
    assert "point" in restored_point_body["data"]
    assert restored_point_body["data"]["point"] == before_point


