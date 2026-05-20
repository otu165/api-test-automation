"""
경로 : shop-backend/tests/api/test_order.py
파일명 : test_order.py

주문 API 테스트를 담당하는 파일

이 파일의 역할:
- 인증된 사용자의 주문 생성 성공 검증
- 잘못된 토큰 요청 실패 검증

"""


from fastapi.testclient import TestClient
from concurrent.futures import ThreadPoolExecutor

from tests.clients.auth_client import AuthClient
from tests.clients.order_client import OrderClient
from tests.clients.point_client import PointClient
from app.constants import error_codes
from app.repositories import product_repository


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
    cancel_order_res = order_client.cancel_order(order_id)

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
    cancel_order_res = order_client.cancel_order(order_id)

    # 상태코드 검증
    assert cancel_order_res.status_code == 200

    # 동일 주문 재취소
    double_cancel_order_res = order_client.cancel_order(order_id)

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
        client: TestClient,
        access_token: str
):
    """주문 취소 시 상품 재고 복구 검증"""

    order_client = OrderClient(client, access_token)

    product_id = "KB1001"
    quantity = 1

    # 주문 전 재고 조회
    before_product = product_repository.select_product_by_id(product_id)
    before_stock = before_product["stock"]

    # 주문 생성
    create_order_res = order_client.create_order(
        product_id = product_id,
        quantity = quantity
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



def test_get_my_orders_success(
        client: TestClient,
        access_token: str
):
    """내 주문 히스토리 조회 API 성공 검증"""

    order_client = OrderClient(client, access_token)

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
        client: TestClient,
        access_token: str
):
    """내 주문 상세 조회 성공 검증"""

    order_client = OrderClient(client, access_token)

    product_id = "KB1001"
    quantity = 1

    # 주문 생성
    create_order_res = order_client.create_order(
        product_id = product_id,
        quantity = quantity
    )

    # 상태코드 검증
    assert create_order_res.status_code == 201

    # 데이터 검증
    create_order_body = create_order_res.json()

    assert create_order_body["success"] is True
    assert "data" in create_order_body
    assert "order_id" in create_order_body["data"]

    order_id = create_order_body["data"]["order_id"]

    # 주문 상세 조회
    detail_res = order_client.get_order_detail(order_id)

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
    assert detail_body["data"]["order_id"] == order_id

    assert "product_id" in detail_body["data"]
    assert detail_body["data"]["product_id"] == product_id

    assert "quantity" in detail_body["data"]
    assert detail_body["data"]["quantity"] == quantity

    assert "status" in detail_body["data"]
    assert detail_body["data"]["status"] == "PAID"


def test_cancel_other_user_order_not_found(
        client: TestClient,
        access_token: str
):
    """내가 아닌 다른 사용자의 주문 취소 실패 검증"""

    # A 사용자(access_token fixture) 로 주문 생성
    A_order_client = OrderClient(client, access_token)

    create_order_res = A_order_client.create_order(
        product_id = "KB1001",
        quantity = 1
    )

    # 상태코드 검증
    assert create_order_res.status_code == 201

    create_order_body = create_order_res.json()

    # 데이터 검증
    assert "data" in create_order_body
    assert "order_id" in create_order_body["data"]

    A_order_id = create_order_body["data"]["order_id"]

    # B 사용자 회원가입 & 로그인
    B_auth_client = AuthClient(client)

    B_email = "B-email@example.com"
    B_password = "1234"

    signup_res = B_auth_client.signup(
        email = B_email,
        password = B_password,
        name = "user B"
    )

    # 상태코드 검증
    assert signup_res.status_code == 201

    signin_res = B_auth_client.signin(
        email = B_email,
        password = B_password
    )

    # 상태코드 검증
    assert signin_res.status_code == 200

    # 데이터 검증
    assert "data" in signin_res.json()
    assert "access_token" in signin_res.json()["data"]
    B_access_token = signin_res.json()["data"]["access_token"]

    # B 사용자로 A 사용자의 주문 취소 시도
    B_order_client = OrderClient(client, B_access_token)

    response = B_order_client.cancel_order(A_order_id)

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


def test_create_order_concurrently_with_limited_stock(
        client: TestClient,
        access_token: str
):
    """
    상품 재고가 1개일 때, 동시 주문 요청 1개 성공 검증
    (동시성 테스트를 위한 테스트 함수)
    """

    product_id = "KB1001"
    request_count = 10

    # (테스트 조건) 키보드 재고를 1개로 강제 설정
    product_repository.update_product_stock(
        product_id = product_id,
        new_stock = 1
    )

    # 내부(로컬) 함수
    # ㄴ 역할 : 주문 요청 1번 보내기
    def request_order():
        order_client = OrderClient(
            client = client,
            access_token = access_token
        )

        return order_client.create_order(
            product_id = product_id,
            quantity = 1
        )

    # 동시에 5번 주문 요청
    with ThreadPoolExecutor(max_workers = request_count) as executor:
        responses = list(
            executor.map(
                lambda _: request_order(),
                range(request_count)
            )
        )

    # response 의 상태코드만 담은 배열 생성
    status_codes = [
        response.status_code
        for response in responses
    ]

    success_count = status_codes.count(201)
    error_count = status_codes.count(400)

    # 성공 주문 개수 확인 (재고가 1개이므로 성공 주문은 반드시 1개여야 함)
    assert success_count == 1

    # 실패 주문 개수 확인
    assert error_count == request_count - 1

    # 상품 최종 재고 확인 (음수일 수 없고, 반드시 0이어야 함)
    product = product_repository.select_product_by_id(product_id)

    assert product["stock"] == 0
