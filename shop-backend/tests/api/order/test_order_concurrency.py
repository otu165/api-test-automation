"""
경로 : shop-backend/tests/api/order/test_order_concurrency.py
파일명 : test_order_concurrency.py

동시성 주문 API 테스트를 담당하는 파일

이 파일의 역할:
- 재고가 1개인 상품에 대한 동시 주문 요청 검증 (초과 주문 방어 검증)

"""


from concurrent.futures import ThreadPoolExecutor

from tests.clients.order_client import OrderClient
from app.repositories import product_repository

import pytest

pytestmark = [
    pytest.mark.order,
    pytest.mark.slow
]


def test_create_order_concurrently_with_limited_stock(
        order_client: OrderClient
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

        return order_client.create_order(
            product_id = product_id,
            quantity = 1
        )

    # 동시에 request_count 번 주문 요청
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
