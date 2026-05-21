"""
경로 : shop-backend/app/services/point_service.py
파일명 : point_service.py

포인트 조회 및 충전 비즈니스 로직을 담당하는 파일

이 파일의 역할:
- 사용자 포인트 조회, 충전
- 존재하지 않는 사용자 검증

"""

import logging
from fastapi import status

from app.repositories import user_repository
from app.utils.response import success_response
from app.exceptions.api_exception import ApiException
from app.constants import error_codes


logger = logging.getLogger(__name__)


def update_point(
        user_id: str,
        amount: int
) -> dict:
    """포인트 충전"""

    logger.info(
        "포인트 충전 요청: user_id = %s, amount = %s",
        user_id,
        amount
    )

    # 충전 금액이 양의 정수값인지 확인
    if amount <= 0:
        logger.warning(
            "포인트 충전 실패 - 부적절한 포인트 입력: amount = %s", amount
        )

        raise ApiException(
            status_code = status.HTTP_400_BAD_REQUEST,
            message = "포인트 충전 실패",
            code = error_codes.INVALID_POINT_AMOUNT,
            detail = "포인트는 1원 이상 충전 가능합니다."
        )

    # 유저 존재 확인
    user = user_repository.select_user_by_id(user_id)

    if user is None:
        logger.warning(
            "포인트 충전 실패 - 사용자 없음: user_id = %s", user_id
        )

        raise ApiException(
            status_code = status.HTTP_404_NOT_FOUND,
            message = "포인트 충전 실패",
            code = error_codes.USER_NOT_FOUND,
            detail = "요청된 사용자를 찾을 수 없습니다."
        )

    # 기존 포인트 + 충전 금액 계산
    new_point = user["point"] + amount

    # DB 에 새로운 포인트 저장
    user_repository.update_user_point(user_id, new_point)

    # 결과 반환
    logger.info(
        "포인트 충전 성공: user_id = %s, point = %s",
        user_id,
        new_point
    )

    return success_response(
        message = "포인트 충전 성공",
        data = {
            "user_id": user_id,
            "charged_amount": amount,
            "new_point": new_point
        }
    )


def select_point(user_id: str):
    """포인트 조회"""

    logger.info(
        "포인트 조회 요청: user_id = %s", user_id
    )

    # 유저 존재 확인
    user = user_repository.select_user_by_id(user_id)

    if user is None:
        logger.warning(
            "포인트 조회 실패 - 사용자 없음: user_id = %s", user_id
        )

        raise ApiException(
            status_code = status.HTTP_404_NOT_FOUND,
            message = "포인트 조회 실패",
            code = error_codes.USER_NOT_FOUND,
            detail = "요청된 사용자를 찾을 수 없습니다."
        )

    data = user_repository.select_user_point_by_id(user_id)

    # 결과 반환
    logger.info(
        "포인트 조회 성공: user_id = %s, point = %s",
        user_id,
        data["point"]
    )

    return success_response(
        message = "포인트 조회 성공",
        data = {
            "point" : data["point"]
        }
    )