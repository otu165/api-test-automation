"""
경로 : shop-backend/tests/clients/base_client.py
파일명 : base_client.py

API 테스트 Client 공통 기능을 관리하는 파일

이 파일의 역할:
- FaseAPI TestClient 객체 보관
- Authorization 헤더를 공통으로 생성
- GET/POST 요청 중복 코드를 줄임

"""


from typing import Any

from fastapi.testclient import TestClient
from httpx import Response


class BaseClient:
    """API 테스트 클라이언트 공통 기능을 정의"""

    def __init__(
            self,
            client: TestClient,
            access_token: str | None = None
    ):
        """테스트 클라이언트와 access_token 을 저장함"""

        self.client = client
        self.access_token = access_token


    def _get_headers(self) -> dict[str, str]:
        """Authorization 헤더 생성"""

        headers = {}

        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"

        return headers


    def get(
            self,
            path: str
    ) -> Response:
        """HTTP GET 요청 보내기"""

        return self.client.get(
            url = path,
            headers = self._get_headers()
        )


    def post(
            self,
            path: str,
            payload: dict[str, Any] | None = None
            # payload 는 딕셔너리(key = str, value = Any) 거나 None 일 수 있다. "= None" 은 기본값을 None 으로 지정한 것
    ) -> Response:
        """HTTP POST 요청 보내기"""

        return self.client.post(
            url = path,
            headers = self._get_headers(),
            json = payload
        )