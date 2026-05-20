"""
경로 : shop-backend/tests/clients/auth_client.py
파일명 : auth_client.py

인증 API 테스트 요청을 담당하는 파일

이 파일의 역할:
- 회원가입 API 요청을 보냄
- 로그인 API 요청을 보냄
- 테스트 코드의 API 호출 중복을 줄임

"""


from httpx import Response
from tests.clients.base_client import BaseClient


class AuthClient(BaseClient):

    def signup(
            self,
            email: str,
            password: str,
            name: str
    ):
        """회원가입 API 요청을 보냄"""

        return self.post(
            "/auth/signup",
            payload = {
                "email" : email,
                "password" : password,
                "name" : name
            }
        )


    def signin(
            self,
            email: str,
            password: str
    ):
        """로그인 API 요청을 보냄"""

        return self.post(
            "/auth/signin",
            payload = {
                "email" : email,
                "password" : password
            }
        )