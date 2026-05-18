"""
경로 : shop-backend/app/repositories/order_repository.py
파일명 : order_repository.py

orders 테이블 저장을 담당하는 파일

이 파일의 역할:
- 주문 생성 기능 제공

"""


from app.database import get_connection
from app import sql_queries


def insert_order(
        order_id: str,
        user_id: str,
        product_id: str,
        quantity: int,
        total_price: int
):
    """신규 주문 생성"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        sql_queries.INSERT_ORDER,
        (order_id, user_id, product_id, quantity, total_price, "PAID")
    )

    # cursor.lastrowid = 새롭게 INSERT 한 행의 자동 생성 PK 값을 반환함
    order_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return order_id


def select_all_orders():
    """모든 주문 조회"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(sql_queries.SELECT_ALL_ORDERS)
    orders = cursor.fetchall()

    conn.close()

    return [dict(order) for order in orders]