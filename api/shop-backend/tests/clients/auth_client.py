"""
경로 : shop-backend/tests/clients/auth_client.py
파일명 : auth_client.py

인증 API 테스트 요청을 담당하는 파일

이 파일의 역할:
- 회원가입 API 요청을 보냄
- 로그인 API 요청을 보냄
- 테스트 코드의 API 호출 중복을 줄임

"""


from fastapi.testclient import TestClient


def signup(
        client: TestClient,
        email: str,
        password: str,
        name: str
):
    """회원가입 API 요청을 보냄"""

    return client.post(
        "/auth/signup",
        json = {
            "email" : email,
            "password" : password,
            "name" : name
        }
    )


def signin(
        client: TestClient,
        email: str,
        password: str
):
    """로그인 API 요청을 보냄"""

    return client.post(
        "/auth/signin",
        json = {
            "email" : email,
            "password" : password
        }
    )