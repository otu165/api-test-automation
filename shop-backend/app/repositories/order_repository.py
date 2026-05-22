"""
경로 : shop-backend/app/repositories/order_repository.py
파일명 : order_repository.py

orders 테이블 저장을 담당하는 파일

이 파일의 역할:
- 주문 생성 기능 제공

"""
import sqlite3
from typing import Optional

from app.core.database import get_connection
from app.core import sql_queries


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
    """주문 ID 로 주문 단건 조회"""

    # DB 커넥션 전달된 경우
    if connection is not None:
        cursor = connection.cursor()
        cursor.execute(sql_queries.SELECT_ORDER_BY_ID, (order_id,))

        order = cursor.fetchone()

        return dict(order) if order else None

    # DB 커넥션이 없는 경우
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(sql_queries.SELECT_ORDER_BY_ID, (order_id,))

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



def select_orders_by_user_id(
        user_id: str
):
    """user_id 와 일치하는 주문 목록 조회"""

    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(
            sql_queries.SELECT_ORDERS_BY_USER_ID,
            (user_id, )
        )

        orders = cursor.fetchall()

        return [dict(order) for order in orders]

    finally:
        connection.close()



def select_order_by_id_and_user_id(
        order_id: str,
        user_id: str,
        connection: Optional[sqlite3.Connection] = None
):
    """
    order_id & user_id 로 주문 단건 조회
    (order_id 만 사용해도 단건 조회가 가능하지만, order_id 를 알아내면
    타인의 주문도 조회 가능한 보안상의 이슈가 있기 때문에 user_id 를 함께 조건으로 사용한다)
    """

    params = (
        user_id,
        order_id
    )

    if connection is not None:
        cursor = connection.cursor()
        cursor.execute(sql_queries.SELECT_ORDER_BY_ID_AND_USER_ID, params)

        order = cursor.fetchone()

        return dict(order) if order else None

    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(sql_queries.SELECT_ORDER_BY_ID_AND_USER_ID, params)

        order = cursor.fetchone()

        return dict(order) if order else None

    finally:
        connection.close()

