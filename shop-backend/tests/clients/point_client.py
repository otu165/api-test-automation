"""
경로 : shop-backend/tests/clients/point_client.py
파일명 : point_client.py

포인트 API 테스트 요청을 담당하는 파일

이 파일의 역할:
- 포인트 조회 API 요청을 보냄
- Authorization 헤더 포함 요청을 보냄
- 테스트 코드의 API 호출 중복을 줄임

"""


from tests.clients.base_client import BaseClient


class PointClient(BaseClient):

    def get_point(self):
        """포인트 조회 API 요청"""

        return self.get(
            "/points",
        )


    def charge_point(
            self,
            amount: int
    ):
        """포인트 충전 API 요청"""

        return self.post(
            "/points/charge",
            payload = {
                "amount" : amount
            }
        )
