"""
경로 : shop-backend/app/sql_queries.py
파일명 : sql_queries.py

SQLite 데이터베이스에서 사용하는 SQL 쿼리를 모아놓은 파일

"""


# ===================== 테이블 ======================

CREATE_USER_TABLE = """
    CREATE TABLE IF NOT EXISTS tb_user (
        user_id TEXT PRIMARY KEY,			-- 회원 ID(PK)
        email TEXT UNIQUE NOT NULL,			-- 이메일
        password TEXT NOT NULL,				-- 비밀번호
        name TEXT NOT NULL,					-- 이름
        point INTEGER NOT NULL DEFAULT 0,	-- 포인트
        created_at TEXT NOT NULL			-- 가입 시간
    )
"""


CREATE_PRODUCT_TABLE = """
    CREATE TABLE IF NOT EXISTS tb_product (
        product_id TEXT PRIMARY KEY,		-- 상품 ID(PK)
        name TEXT NOT NULL,					-- 상품명
        price INTEGER NOT NULL,				-- 가격
        stock INTEGER NOT NULL,				-- 재고
        created_at TEXT NOT NULL			-- 등록 시간
    )
"""


CREATE_ORDER_TABLE = """
    CREATE TABLE IF NOT EXISTS tb_order (
        order_id TEXT PRIMARY KEY,			-- 주문 ID(PK)
        user_id TEXT NOT NULL,				-- 주문 회원 ID
        product_id TEXT NOT NULL,			-- 주문 상품 ID
        quantity INTEGER NOT NULL,			-- 주문 수량
        total_price INTEGER NOT NULL,		-- 총 주문 금액
        status TEXT NOT NULL,				-- 주문 상태(예: PAID)
        created_at TEXT NOT NULL,			-- 주문 시간
        
        FOREIGN KEY(user_id) REFERENCES tb_user(user_id),
        FOREIGN KEY(product_id) REFERENCES tb_product(product_id)
    )
"""


# ===================== tb_user =====================

INSERT_USER = """
    INSERT INTO tb_user (user_id, email, password, name, point, created_at)
    VALUES (?, ?, ?, ?, ?, DATETIME('now'));
"""


SELECT_USER_BY_EMAIL = """
    SELECT email
      FROM tb_user
     WHERE email = ?
"""


SELECT_USER_BY_EMAIL_AND_PASSWORD = """
    SELECT user_id
      FROM tb_user
     WHERE 1=1
       AND email = ?
       AND password = ?
"""


SELECT_USER_BY_ID = """
    SELECT user_id, name, point
      FROM tb_user
     WHERE user_id = ?
"""


UPDATE_USER_POINT = """
    UPDATE tb_user
       SET point = ?
     WHERE user_id = ?
"""


SELECT_USER_POINT_BY_ID = """
    SELECT point
      FROM tb_user
     WHERE user_id = ?
"""


# ===================== tb_product =====================


INSERT_PRODUCT = """
    INSERT OR IGNORE INTO tb_product (product_id, name, price, stock)
    VALUES (?, ?, ?, ?)
"""


SELECT_ALL_PRODUCTS = """
    SELECT product_id, name, price, stock
      FROM tb_product
"""


SELECT_PRODUCT_BY_ID = """
    SELECT product_id, name, price, stock
      FROM tb_product
     WHERE product_id = ?
"""


UPDATE_PRODUCT_STOCK = """
    UPDATE tb_product
       SET stock = ?
     WHERE product_id = ?
"""


# ===================== tb_order =====================

INSERT_ORDER = """
    INSERT INTO tb_order (user_id, product_id, quantity, total_price, status, created_at)
    VALUES (?, ?, ?, ?, ?, DATETIME('now'))
"""


SELECT_ALL_ORDERS = """
    SELECT order_id, user_id, product_id, quantity, total_price, status
      FROM tb_order
"""