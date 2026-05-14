"""
경로 : shop_backend/app/sql_queries.py
파일명 : sql_queries.py

SQLite 데이터베이스에서 사용하는 SQL 쿼리를 모아놓은 파일

"""


# ===================== 테이블 ======================

CREATE_USERS_TABLE = """
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,      -- 고유 번호(PK)
        email TEXT UNIQUE NOT NULL,    -- 이메일
        password TEXT NOT NULL,        -- 비밀번호
        name TEXT NOT NULL,            -- 이름
        point INTEGER NOT NULL         -- 포인트
    );
"""


CREATE_PRODUCTS_TABLE = """
    CREATE TABLE IF NOT EXISTS products (
        product_id TEXT PRIMARY KEY,    -- 상품 고유값(PK)
        name TEXT NOT NULL,             -- 상품 이름
        price INTEGER NOT NULL,         -- 가격
        stock INTEGER NOT NULL          -- 재고
    );
"""


CREATE_ORDERS_TABLE = """
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT, -- 주문 번호(PK, 자동 증가)
        user_id TEXT NOT NULL,                      -- 주문한 유저
        product_id TEXT NOT NULL,                   -- 구매한 상품
        quantity INTEGER NOT NULL,                  -- 구매 개수
        total_price INTEGER NOT NULL,               -- 총 가격
        status TEXT NOT NULL                        -- 상태(예: PAID)
    );
"""


# ===================== users =====================

INSERT_USER = """
    INSERT INTO users (user_id, email, password, name, point)
    VALUES (?, ?, ?, ?, ?);
"""


SELECT_USER_BY_EMAIL = """
    SELECT email
      FROM users
     WHERE email = ?
"""


SELECT_USER_BY_EMAIL_AND_PASSWORD = """
    SELECT user_id
      FROM users
     WHERE 1=1
       AND email = ?
       AND password = ?
"""


SELECT_USER_BY_ID = """
    SELECT user_id, name, point
      FROM users
     WHERE user_id = ?
"""


UPDATE_USER_POINT = """
    UPDATE users
       SET point = ?
     WHERE user_id = ?
"""


# ===================== products =====================

SELECT_ALL_PRODUCTS = """
    SELECT product_id, name, price, stock
      FROM products
"""


SELECT_PRODUCT_BY_ID = """
    SELECT product_id, name, price, stock
      FROM products
     WHERE product_id = ?
"""


UPDATE_PRODUCT_STOCK = """
    UPDATE products
       SET stock = ?
     WHERE product_id = ?
"""


# ===================== orders =====================

INSERT_ORDER = """
    INSERT INTO orders (user_id, product_id, quantity, total_price, status)
    VALUES (?, ?, ?, ?, ?)
"""


SELECT_ALL_ORDERS = """
    SELECT order_id, user_id, product_id, quantity, total_price, status
      FROM orders
"""