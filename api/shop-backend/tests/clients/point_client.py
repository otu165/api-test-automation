"""
경로 : shop-backend/tests/clients/point_client.py
파일명 : point_client.py

포인트 API 테스트 요청을 담당하는 파일

이 파일의 역할:
- 포인트 조회 API 요청을 보냄
- Authorization 헤더 포함 요청을 보냄
- 테스트 코드의 API 호출 중복을 줄임

"""


from fastapi.testclient import TestClient


def get_point(
        client: TestClient,
        access_token: str | None = None
):
    """포인트 조회 API 요청"""

    headers = {}

    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"

    return client.get(
        "/points/points",
        headers = headers
    )
