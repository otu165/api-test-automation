"""
경로 : shop-backend/tests/clients/order_client.py
파일명 : order_client.py

주문 API 테스트 요청을 담당하는 파일

이 파일의 역할:
- 주문 생성 API 요청을 보냄
- 테스트 코드의 API 호출 중복을 줄임

"""


from tests.clients.base_client import BaseClient


class OrderClient(BaseClient):

    def create_order(
            self,
            product_id: str,
            quantity: int,
    ):
        """주문 생성 API 요청"""

        return self.post(
            "/orders",
            payload = {
                "product_id" : product_id,
                "quantity" : quantity
            }
        )