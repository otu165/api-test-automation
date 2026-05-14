"""
경로 : shop_backend/app/sql_queries.py
파일명 : sql_queries.py

SQLite 데이터베이스에서 사용하는 SQL 쿼리를 모아놓은 파일

"""


CREATE_USERS_TABLE = """
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        point INTEGER NOT NULL
    );
"""

CREATE_PRODUCTS_TABLE = """
    CREATE TABLE IF NOT EXISTS products (
        product_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        price INTEGER NOT NULL,
        stock INTEGER NOT NULL
    );
"""

CREATE_ORDERS_TABLE = """
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        product_id TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        total_price INTEGER NOT NULL,
        status TEXT NOT NULL
    );
"""