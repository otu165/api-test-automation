"""
경로 : shop-backend/app/database.py
파일명 : database.py

SQLite 데이터베이스 커넥션 및 초기화를 담당하는 파일

이 파일의 역할:
- SQLite 데이터베이스 커넥션 생성
- 서비스 실행 시 필요한 테이블 생성

"""

import os
import sqlite3

from app import sql_queries


# SQLite 데이터베이스 파일명 정의
# 이미 정의된 DATABASE_NAME 환경변수가 있으면 그 값 사용 (없으면 기본값으로 shop.db 사용)
DATABASE_NAME = os.getenv("DATABASE_NAME", "shop.db")


def get_connection():
    """SQLite 데이터베이스 커넥션 생성"""
    connection = sqlite3.connect(DATABASE_NAME)

    # 컬럼명을 기준으로 데이터 조회 가능하게 세팅
    # ex) row["user_id"], row["name"] .. 처럼 컬럼명으로 접근할 수 있음
    connection.row_factory = sqlite3.Row

    return connection


def init_db():
    """서비스 실행 시 필요한 테이블 생성"""

    # DB 연결
    conn = get_connection()
    cursor = conn.cursor()

    # users, products, orders 테이블 생성
    cursor.execute(sql_queries.CREATE_USERS_TABLE)
    cursor.execute(sql_queries.CREATE_PRODUCTS_TABLE)
    cursor.execute(sql_queries.CREATE_ORDERS_TABLE)

    # 기본 상품 데이터 추가
    products = [
        ("KB1001", "키보드", 500, 500),
        ("MS1001", "마우스", 300, 500)
    ]

    cursor.executemany(sql_queries.INSERT_PRODUCT, products)

    # 변경된 내용 저장 후 DB 연결 종료
    conn.commit()
    conn.close()