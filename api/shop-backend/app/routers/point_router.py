"""
경로 : shop-backend/app/routers/point_router.py
파일명 : point_router.py

포인트 조회 및 충전 API 라우터를 관리하는 파일

이 파일의 역할:
- 포인트 조회 API endpoint 정의
- 포인트 충전 API endpoint 정의

"""


from fastapi import APIRouter, Depends

from app.models import ChargePointRequest
from app.services import point_service
from app.utils.auth import get_current_user_id


router = APIRouter(prefix = "/points", tags = ["Points"])


@router.post("/charge")
def charge_point(
        request: ChargePointRequest,
        current_user_id: str = Depends(get_current_user_id)
):
    """포인트 충전 API"""

    return point_service.update_point(
        user_id = current_user_id,
        amount = request.amount
    )