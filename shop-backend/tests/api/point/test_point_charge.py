"""
경로 : shop-backend/tests/api/point/test_point_charge.py
파일명 : test_point_charge.py

포인트 충전 API 테스트를 담당하는 파일

이 파일의 역할:
- 포인트 충전 성공 검증
- 포인트 충전 validation 실패 검증

"""


from tests.clients.point_client import PointClient


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
    assert body["success"] is True
    assert body["message"] == "포인트 충전 성공"
    assert body["error"] is None

    # data 구조 검증
    assert "data" in body
    assert isinstance(body["data"], dict)

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

