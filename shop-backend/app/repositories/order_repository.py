"""
경로 : shop-backend/app/repositories/order_repository.py
파일명 : order_repository.py

orders 테이블 저장을 담당하는 파일

이 파일의 역할:
- 주문 생성 기능 제공

"""
import sqlite3
from typing import Optional

from app.database import get_connection
from app import sql_queries


def insert_order(
        order_id: str,
        user_id: str,
        product_id: str,
        quantity: int,
        total_price: int,
        connection: Optional[sqlite3.Connection] = None
):
    """
    신규 주문 생성

    - connection 이 있으면 같은 트랜잭션 안에서 저장
    - connection 이 없으면 단독 저장
    """

    params = (
        order_id,
        user_id,
        product_id,
        quantity,
        total_price,
        "PAID"
    )

    # connection 이 전달된 경우
    if connection is not None:
        connection.execute(sql_queries.INSERT_ORDER, params)

        return order_id

    # connection 이 전달되지 않은 경우
    connection = get_connection()
    try:
        connection.execute(sql_queries.INSERT_ORDER, params)
        connection.commit()

        return order_id

    finally:
        connection.close()


def select_all_orders():
    """모든 주문 조회"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(sql_queries.SELECT_ALL_ORDERS)
    orders = cursor.fetchall()

    conn.close()

    return [dict(order) for order in orders]


def select_order_by_id(
    order_id: str,
    connection: Optional[sqlite3.Connection] = None
):
    "주문 ID 로 주문 단건 조회"

    # DB 커넥션 전달된 경우
    if connection is not None:
        cursor = connection.cursor()
        cursor.execute(sql_queries.SELECT_ORDER_BY_ID, (order_id, ))

        order = cursor.fetchone()

        return dict(order) if order else None

    # DB 커넥션이 없는 경우
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(sql_queries.SELECT_ORDER_BY_ID, (order_id, ))

        order = cursor.fetchone()

        return dict(order) if order else None

    finally:
        connection.close()


def update_order_stuats(
        order_id: str,
        status: str,
        connection: Optional[sqlite3.Connection] = None
):
    """주문 상태 변경"""

    # DB 커넥션 전달된 경우
    if connection is not None:
        connection.execute(sql_queries.UPDATE_ORDER_STATUS, (status, order_id))
        return

    connection = get_connection()

    try:
        connection.execute(sql_queries.UPDATE_ORDER_STATUS, (status, order_id))
        connection.commit() # 데이터 수정이므로 commit 필요

        return

    finally:
        connection.close()




