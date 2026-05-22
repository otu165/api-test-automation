"""
경로 : shop-backend/app/routers/order_router.py
파일명 : order_router.py

주문 생성 API 라우터를 관리하는 파일

이 파일의 역할:
- 주문 생성 API endpoint 정의
- 주문 히스토리 조회 API endpoint 정의

"""

from fastapi import APIRouter, Depends

from app.schemas.models import CreateOrderRequest
from app.services import order_service
from app.utils.auth import get_current_user_id


router = APIRouter(prefix="/orders", tags = ["Orders"])


@router.post(
    path = "",
    status_code = 201,
    summary = "상품 주문",
    description = "로그인한 사용자가 상품을 주문한다."
)
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


@router.get(
    path = "",
    summary = "내 주문 목록 조회",
    description = "로그인한 사용자의 주문 목록을 조회한다."
)
def get_orders(
        current_user_id: str = Depends(get_current_user_id)
):
    """내 주문 히스토리 조회 API"""

    return order_service.select_orders(current_user_id)


@router.get(
    path = "/{order_id}",
    summary = "내 주문 상세 조회",
    description = "로그인한 사용자의 order_id 와 일치하는 주문 상세 정보를 조회한다.")
def get_order_detail(
        order_id: str,
        current_user_id: str = Depends(get_current_user_id)
):
    """내 주문 상세 조회 API"""
    return order_service.select_order_detail(
        order_id = order_id,
        user_id = current_user_id
    )


@router.post(
    path = "/{order_id}/cancel",
    summary = "주문 취소",
    description = "로그인한 사용자의 order_id 와 일치하는 주문을 취소한다. 주문 취소 시 계정 포인트와 상품 재고가 복구된다.")
def cancel_order(
        order_id: str,
        current_user_id: str = Depends(get_current_user_id)
):
    """주문 취소 API"""

    return order_service.cancel_order(
        order_id = order_id,
        user_id = current_user_id
    )


