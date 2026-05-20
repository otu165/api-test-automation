"""
경로 : shop-backend/app/repositories/product_repository.py
파일명 : product_repository.py

products 테이블 조회를 담당하는 파일

이 파일의 역할:
- 상품 ID 기준 조회 기능 제공

"""


import sqlite3
from typing import Optional

from app.database import get_connection
from app import sql_queries


def select_all_products():
    """모든 상품 조회"""

    conn = get_connection()
    cursor = conn.cursor()

    # cursor.fetchall() = 조회된 모든 행(row)을 리스트로 가져온다.
    # (조회 결과 예시_리스트 안에 Row 객체들이 들어있음)
    # products = [
    #     Row(product_id="KB1001", name="키보드", price=500, stock=10),
    #     Row(product_id="MS1001", name="마우스", price=300, stock=5)
    # ]
    cursor.execute(sql_queries.SELECT_ALL_PRODUCTS)
    products = cursor.fetchall()

    conn.close()

    # Row 객체 리스트를 JSON 응답에 적합한 딕셔너리 리스트로 변환하여 반환
    # (반환 값 예시)
    # [
    #     {
    #         "product_id": "KB1001",
    #         "name": "키보드",
    #         "price": 500,
    #         "stock": 10
    #     }
    # ]
    return [dict(product) for product in products]


def select_product_by_id(product_id: str):
    """{product_id} 로 상품 존재 확인"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(sql_queries.SELECT_PRODUCT_BY_ID, (product_id,))
    product = cursor.fetchone()

    conn.close()

    return dict(product) if product else None


def update_product_stock(
        product_id: str,
        new_stock: int,
        connection: Optional[sqlite3.Connection] = None
):
    """
    상품 재고 갱신

    - connection 이 전달되면, 다른 DB 작업들과 같은 트랜잭션 안에서 실행한다.
    - connection 이 없으면, 기존처럼 함수 혼자 DB 연결을 만들어서 사용한다.
    """

    # connection 이 전달된 경우
    if connection is not None:
        connection.execute(
            sql_queries.UPDATE_PRODUCT_STOCK,
            (new_stock, product_id)
        )
        return

    # connection 이 전달되지 않은 경우
    connection = get_connection()

    try:
        connection.execute(
            sql_queries.UPDATE_PRODUCT_STOCK,
            (new_stock, product_id)
        )

        connection.commit()

    finally:
        connection.close()


def decrease_product_stock_if_enough(
        product_id: str,
        quantity: int,
        connection: Optional[sqlite3.Connection]
) -> bool:
    """
    상품 재고가 충분할 때만 상품 재고 차감
    반환값:
    - True : 재고 차감 성공
    - False : 재고 부족으로 차감 실패
    """

    cursor = connection.execute(
        sql_queries.DECREASE_PRODUCT_STOCK_IF_ENOUGH,
        (quantity, product_id, quantity)
    )

    # rowcount = 직전에 실행한 SQL 이 실제로 영향을 준 행(row) 개수
    return cursor.rowcount == 1
