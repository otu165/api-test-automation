"""
경로 : shop-backend/tests/api/test_order_cancel.py
파일명 : test_order_cancel.py

주문 취소 API 테스트를 담당하는 파일

이 파일의 역할:
- 주문 취소 성공 검증
- 존재하지 않는 주문 취소 실패 검증
- 이미 취소된 주문 재취소 실패 검증
- 주문 취소 시 포인트/상품 재고 복구 검증
- 타인의 주문 취소 실패 검증

"""


from fastapi.testclient import TestClient

from tests.clients.order_client import OrderClient
from tests.clients.point_client import PointClient
from app.constants import error_codes
from app.repositories import product_repository



def test_cancel_order_success(
        order_client: OrderClient,
        created_order_id: str
):
    """주문 취소 성공 응답 검증"""

    # 주문 취소
    cancel_order_res = order_client.cancel_order(created_order_id)

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
    assert cancel_order_body["data"]["order_id"] == created_order_id

    # data > status 검증
    assert "status" in cancel_order_body["data"]
    assert cancel_order_body["data"]["status"] == "CANCELED"


def test_cancel_order_not_found(
        order_client: OrderClient
):
    """존재하지 않는 주문 취소 실패"""

    # 존재하지 않는 주문 취소 요청
    response = order_client.cancel_order(
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
        order_client: OrderClient,
        created_order_id: str
):
    """이미 취소된 주문 재취소 실패 검증"""

    # 주문 취소
    cancel_order_res = order_client.cancel_order(created_order_id)

    # 상태코드 검증
    assert cancel_order_res.status_code == 200

    # 동일 주문 재취소
    double_cancel_order_res = order_client.cancel_order(created_order_id)

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
        order_client: OrderClient,
        point_client: PointClient
):
    """주문 취소 시 계정 포인트 복구 검증"""

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
    cancel_order_res = order_client.cancel_order(order_id)

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


def test_cancel_order_restore_stock(
        order_client: OrderClient
):
    """주문 취소 시 상품 재고 복구 검증"""

    product_id = "KB1001"
    quantity = 1

    # 주문 전 재고 조회
    before_product = product_repository.select_product_by_id(product_id)
    before_stock = before_product["stock"]

    # 주문 생성
    create_order_res = order_client.create_order(
        product_id=product_id,
        quantity=quantity
    )

    # 상태코드 검증
    assert create_order_res.status_code == 201

    create_order_body = create_order_res.json()

    # 데이터 검증
    assert "data" in create_order_body
    assert "order_id" in create_order_body["data"]

    order_id = create_order_body["data"]["order_id"]

    # 주문 후 재고 차감 확인
    after_product = product_repository.select_product_by_id(product_id)
    after_stock = after_product["stock"]

    assert after_stock == before_stock - quantity

    # 주문 취소
    order_cancel_res = order_client.cancel_order(order_id)

    # 상태코드 확인
    assert order_cancel_res.status_code == 200

    # 주문 취소 후 상품 재고 원복 확인
    restored_product = product_repository.select_product_by_id(product_id)

    assert before_stock == restored_product["stock"]



def test_cancel_other_user_order_not_found(
        client: TestClient,
        created_order_id: str,
        second_access_token: str
):
    """내가 아닌 다른 사용자의 주문 취소 실패 검증"""

    # A 사용자 order_id
    a_order_id = created_order_id

    # B 사용자 access_token
    b_access_token = second_access_token

    # B 사용자로 A 사용자의 주문 취소 시도
    b_order_client = OrderClient(client, b_access_token)

    response = b_order_client.cancel_order(a_order_id)

    # 상태코드 검증
    assert response.status_code == 404 # B의 order_id 가 아니므로 요청한 주문을 찾을 수 없음

    body = response.json()

    # 데이터 검증
    assert body["success"] is False
    assert body["message"] == "주문 취소 실패"
    assert body["data"] is None

    # error 검증
    assert "error" in body
    assert isinstance(body["error"], dict)

    # error > code 검증
    assert "code" in body["error"]
    assert body["error"]["code"] == error_codes.ORDER_NOT_FOUND

