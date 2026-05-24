"""
경로 : shop-backend/tests/test_health.py
파일명 : test_health.py

서버 상태 확인 API 테스트를 담당하는 파일

이 파일의 역할:
- FastAPI 앱이 정상 응답하는지 검증
- pytest 실행 환경 정상 검증

"""


from fastapi.testclient import TestClient
from app.main import app

import pytest

pytestmark = pytest.mark.health


# FastAPI 서버를 테스트용으로 실행하는 가짜 클라이언트 생성
# (서버 실행 없이 python 내부에서 직접 API 호출)
client = TestClient(app)


def test_health_check():
    """서버 상태 확인 API 검증"""

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message" : "Shop Backend Server is running"
    }
