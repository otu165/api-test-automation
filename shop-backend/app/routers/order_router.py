"""
경로 : shop-backend/app/routers/order_router.py
파일명 : order_router.py

주문 생성 API 라우터를 관리하는 파일

이 파일의 역할:
- 주문 생성 API endpoint 정의
- 주문 히스토리 조회 API endpoint 정의

"""

from fastapi import APIRouter, Depends

from app.models import CreateOrderRequest
from app.services import order_service
from app.utils.auth import get_current_user_id


router = APIRouter(prefix="/orders", tags = ["Orders"])


@router.post("", status_code = 201)
def create_order(
        request: CreateOrderRequest,
        current_user_id: str = Depends(get_current_user_id)
):
    """상품 구매 API"""

    return order_service.insert_order(
        user_id = current_user_id,
        product_id = request.product_id,
        quantity = request.quantity
    )


@router.get("")
def get_orders():
    """주문 히스토리 조회 API"""

    return order_service.select_orders()


@router.post("/{order_id}/cancel")
def cancel_order(
        order_id: str,
        current_user_id: str = Depends(get_current_user_id)
):
    """주문 취소 API"""

    return order_service.cancel_order(order_id)
