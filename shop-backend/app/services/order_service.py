"""
경로 : shop-backend/app/services/order_service.py
파일명 : order_service.py

주문 생성 비즈니스 로직을 담당하는 파일

이 파일의 역할:
- 주문 요청 사용자 검증
- 주문 상품 검증
- 상품의 재고, 사용자의 포인트 검증
- 주문 생성에 필요한 계산 처리

"""

import uuid
from fastapi import status

from app.utils.response import success_response
from app.constants import error_codes
from app.exceptions.api_exception import ApiException
from app.repositories import user_repository, product_repository, order_repository
from app.database import get_connection


def insert_order(
        user_id: str,
        product_id: str,
        quantity: int
):
    """신규 주문 생성"""

    # 구매 개수가 양의 정수인지 확인
    if quantity <= 0:
        raise ApiException(
            status_code = status.HTTP_400_BAD_REQUEST,
            message = "주문 실패",
            code = error_codes.INVALID_ORDER_QUANTITY,
            detail = "상품을 1개 이상 구매해주세요."
        )

    # 유저 존재 확인
    user = user_repository.select_user_by_id(user_id)

    if user is None:
        raise ApiException(
            status_code = status.HTTP_404_NOT_FOUND,
            message = "주문 실패",
            code = error_codes.USER_NOT_FOUND,
            detail = "요청된 사용자를 찾을 수 없습니다."
        )

    # 상품 존재 확인
    product = product_repository.select_product_by_id(product_id)

    if product is None:
        raise ApiException(
            status_code = status.HTTP_404_NOT_FOUND,
            message = "주문 실패",
            code = error_codes.PRODUCT_NOT_FOUND,
            detail = "요청된 상품을 찾을 수 없습니다."
        )

    # 총 가격 계산 (가격 X 수량)
    total_price = product["price"] * quantity

    # 상품 재고 확인
    if product["stock"] < quantity:
        raise ApiException(
            status_code = status.HTTP_400_BAD_REQUEST,
            message = "주문 실패",
            code = error_codes.INSUFFICIENT_STOCK,
            detail = "요청된 상품의 재고가 부족합니다."
        )

    # 잔여 포인트 확인
    if user["point"] < total_price:
        raise ApiException(
            status_code = status.HTTP_400_BAD_REQUEST,
            message = "주문 실패",
            code = error_codes.INSUFFICIENT_POINT,
            detail = "사용자 계정의 잔여 포인트가 부족합니다."
        )

    conn = get_connection()

    try:

        # 포인트 차감
        new_point = user["point"] - total_price
        user_repository.update_user_point(user_id, new_point, conn)

        # 재고 차감
        new_stock = product["stock"] - quantity
        product_repository.update_product_stock(product_id, new_stock, conn)

        # order_id 생성
        order_id = str(uuid.uuid4())

        # 주문 생성 (DB에 기록)
        order_id = order_repository.insert_order(
            order_id, user_id, product_id, quantity, total_price, conn
        )

        conn.commit()

        # 결과 반환
        return success_response(
            message="주문 성공",
            data={
                "order_id": order_id,
                "user_id": user_id,
                "product_id": product_id,
                "quantity": quantity,
                "total_price": total_price,
                "status": "PAID"
            }
        )

    except ApiException:
        conn.rollback()
        raise # 예외 응답 형태는 기존 예외 처리 흐름에 맡긴다
    except Exception:
        conn.rollback()
        raise ApiException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            message = "주문 실패",
            code = error_codes.INTERNAL_SERVER_ERROR,
            detail = "서버 내부 오류가 발생했습니다."
        )

    finally:
        conn.close()


def cancel_order(order_id: str):
    """주문 취소"""

    conn = get_connection()

    try:
        # 주문 존재 확인
        order = order_repository.select_order_by_id(order_id, conn)

        if order is None:
            raise ApiException(
                status_code = status.HTTP_404_NOT_FOUND,
                message = "주문 취소 실패",
                code = error_codes.ORDER_NOT_FOUND,
                detail = "요청된 주문을 찾을 수 없습니다."
            )

        # (취소 전) 현재 주문 상태 확인
        if order["status"] == "CANCELED":
            raise ApiException(
                status_code = status.HTTP_400_BAD_REQUEST,
                message = "주문 취소 실패",
                code = error_codes.ORDER_ALREADY_CANCELED,
                detail = "이미 취소된 주문입니다."
            )

        # 주문을 한 사용자 조회
        user = user_repository.select_user_by_id(order["user_id"])

        if user is None:
            raise ApiException(
                status_code = status.HTTP_404_NOT_FOUND,
                message = "주문 취소 실패",
                code = error_codes.USER_NOT_FOUND,
                detail = "주문한 사용자를 찾을 수 없습니다."
            )

        # 주문 금액만큼 포인트 복구
        restored_point = user["point"] + order["total_price"]

        user_repository.update_user_point(
            user_id = order["user_id"],
            new_point = restored_point,
            connection = conn
        )

        # 주문 상품 조회
        product = product_repository.select_product_by_id(order["product_id"])

        if product is None:
            raise ApiException(
                status_code = status.HTTP_404_NOT_FOUND,
                message = "주문 취소 실패",
                code = error_codes.PRODUCT_NOT_FOUND,
                detail = "주문한 상품을 찾을 수 없습니다."
            )

        # 주문 수량만큼 상품 재고 복구

        restored_stock = product["stock"] + order["quantity"]

        product_repository.update_product_stock(
            product_id=order["product_id"],
            new_stock=restored_stock,
            connection=conn
        )

        # 주문 상태 변경
        order_repository.update_order_stuats(
            order_id,
            "CANCELED",
            conn
        )

        conn.commit()

        # (취소 후) 변경된 주문 조회
        canceled_order = order_repository.select_order_by_id(order_id, conn)

        return success_response(
            message = "주문 취소 성공",
            data = canceled_order
        )

    except ApiException:
        conn.rollback()
        raise

    except Exception:
        conn.rollback()
        raise ApiException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            message = "주문 취소 실패",
            code = error_codes.INTERNAL_SERVER_ERROR,
            detail = "서버 내부 오류가 발생했습니다."
        )

    finally:
        conn.close()


def select_orders(user_id: str):
    """내 주문 목록 조회"""

    orders = order_repository.select_orders_by_user_id(user_id)

    return success_response(
        message = "주문 목록 조회 성공",
        data = {
            "orders" : orders,
            "count" : len(orders)
        }
    )



def select_order_detail(
        order_id: str,
        user_id: str
) -> dict:
    """내 주문 상세 조회"""

    order = order_repository.select_order_by_id_and_user_id(
        order_id = order_id,
        user_id = user_id
    )

    if order is None:
        raise ApiException(
            status_code = status.HTTP_404_NOT_FOUND,
            message = "주문 상세 조회 실패",
            code = error_codes.ORDER_NOT_FOUND,
            detail = "요청된 주문을 찾을 수 없습니다."
        )

    return success_response(
        message = "주문 상세 조회 성공",
        data = order
    )