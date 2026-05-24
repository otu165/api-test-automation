"""
경로 : shop-backend/tests/api/point/test_point_charge.py
파일명 : test_point_charge.py

포인트 충전 API 테스트를 담당하는 파일

이 파일의 역할:
- 포인트 충전 성공 검증
- 포인트 충전 validation 실패 검증

"""


from fastapi.testclient import TestClient

from app.utils.auth import create_access_token
from app.constants import error_codes

from tests.clients.point_client import PointClient
from tests.helpers.assertions import (
    assert_success_response,
    assert_error_response,
    assert_unauthorized_response,
    assert_validation_error_response
)

import pytest

pytestmark = pytest.mark.point


def test_charge_point_success(
        point_client: PointClient
):
    """포인트 충전 성공 응답 검증"""

    amount = 1000 # 1000 포인트 충전
    response = point_client.charge_point(amount)

    # 상태코드 검증
    assert response.status_code == 200

    body = response.json()

    # 공통 응답 구조(success_response) 검증
    assert_success_response(
        body = body,
        message = "포인트 충전 성공"
    )

    # data > point 검증
    assert "charged_amount" in body["data"]
    assert isinstance(body["data"]["charged_amount"], int)
    assert body["data"]["charged_amount"] == amount


def test_charge_point_increase_balance(
        point_client: PointClient
):
    """포인트 충전 후 잔액 증가 검증"""

    # 1. 포인트 조회
    before_res = point_client.get_point()

    # 상태코드 검증
    assert before_res.status_code == 200

    # point 꺼내기
    assert "data" in before_res.json()
    assert "point" in before_res.json()["data"]
    before_point = before_res.json()["data"]["point"]

    # 2. 포인트 충전
    amount = 1000

    charge_res = point_client.charge_point(amount)

    # 상태코드 검증
    assert charge_res.status_code == 200

    # 3. (충전 후) 포인트 재 조회
    after_res = point_client.get_point()

    # 상태코드 검증
    assert after_res.status_code == 200

    # point 꺼내기
    assert "data" in after_res.json()
    assert "point" in after_res.json()["data"]
    after_point = after_res.json()["data"]["point"]

    # 충전 후 포인트 검증
    assert before_point + amount == after_point


def test_charge_point_with_zero_amount(
        point_client: PointClient
):
    """포인트 충전 금액 = 0 인 경우, validation 실패 검증"""

    response = point_client.charge_point(0)

    # 상태코드 검증
    assert response.status_code == 422

    # 부적절한 데이터 입력 응답 검증
    assert_validation_error_response(response.json())


def test_charge_point_with_negative_amount(
        point_client: PointClient
):
    """포인트 충전 금액이 음수인 경우, validation 실패 검증"""

    response = point_client.charge_point(-1)

    # 상태코드 검증
    assert response.status_code == 422

    # 부적절한 데이터 입력 응답 검증
    assert_validation_error_response(response.json())


def test_charge_point_with_invalid_token(
        client: TestClient
):
    """잘못된 토큰 포인트 충전 실패 응답 검증"""

    point_client = PointClient(
        client = client,
        access_token = "INVALID_TOKEN"
    )

    # 포인트 충전 API 요청
    response = point_client.charge_point(1000)

    # 상태코드 검증
    assert response.status_code == 401

    # 사용자 인증 실패 응답 검증
    assert_unauthorized_response(response.json())


def test_charge_point_multiple_times(
        point_client: PointClient
):
    """포인트 여러 번 충전 시 누적 증가 검증"""

    # (포인트 충전 이전) 계정 포인트 조회
    before_res = point_client.get_point()
    assert before_res.status_code == 200

    before_point = before_res.json()["data"]["point"]

    first_charge_amount = 500
    second_charge_amount = 1000

    # 첫 번째 포인트 충전
    first_charge_res = point_client.charge_point(first_charge_amount)
    assert first_charge_res.status_code == 200

    # 두 번째 포인트 충전
    second_charge_res = point_client.charge_point(second_charge_amount)
    assert second_charge_res.status_code == 200

    # (포인트 충전 이후) 계정 포인트 조회
    after_res = point_client.get_point()
    assert after_res.status_code == 200

    after_point = after_res.json()["data"]["point"]

    # 포인트 충전량 검증
    assert before_point + first_charge_amount + second_charge_amount == after_point


def test_charge_point_with_not_found_user_token(
        client: TestClient
):
    """DB 에 존재하지 않는 user_id 를 가진 토큰으로 포인트 충전 실패 응답 검증"""

    # DB 에 존재하지 않는 user_id 로 JWT 생성
    access_token = create_access_token(
        user_id = "not-found-user-id"
    )

    # 포인트 충전 API 호출
    response = client.post(
        "/points/charge",
        headers = {
            "Authorization" : f"Bearer {access_token}"
        },
        json = {
            "amount" : 1000
        }
    )

    # 상태코드 검증
    assert response.status_code == 404

    # 사용자 없음 응답 검증
    assert_error_response(
        body = response.json(),
        message = "포인트 충전 실패",
        code = error_codes.USER_NOT_FOUND
    )
