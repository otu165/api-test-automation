"""
경로 : shop-backend/app/repositories/user_repository.py
파일명 : user_repository.py

users 테이블 조회 및 저장을 담당하는 파일

이 파일의 역할:
- 사용자 생성 기능 제공
- 사용자 조회 기능 제공 (email, user_id 기준)

"""
from app.database import get_connection
from app import sql_queries


def insert_user(user_id: str, email: str, password: str, name: str):
    """신규 유저 회원가입"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(sql_queries.INSERT_USER, (user_id, email, password, name, 1000))

    conn.commit()
    conn.close()


def select_user_by_email(email: str):
    """{email} 로 유저 존재 확인"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(sql_queries.SELECT_USER_BY_EMAIL, (email,))
    user = cursor.fetchone()

    conn.close()

    return dict(user) if user else None


def select_user_by_email_and_password(email: str, password: str):
    """유저 로그인"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(sql_queries.SELECT_USER_BY_EMAIL_AND_PASSWORD, (email, password))
    user_id = cursor.fetchone()

    conn.close()

    return dict(user_id) if user_id else None


def select_user_by_id(user_id: str):
    """{user_id} 로 유저 존재 확인"""
    conn = get_connection()
    cursor = conn.cursor()

    # execute() 2 번째 인자는 반드시 "튜플" 또는 "리스트" 여야 한다.
    # (user_id) 는 단순 문자열 취급이므로 쉼표를 포함하여 (user_id,) 로 작성해야 함
    cursor.execute(sql_queries.SELECT_USER_BY_ID, (user_id,))
    user = cursor.fetchone()

    conn.close()

    return dict(user) if user else None


def update_user_point(user_id: str, new_point: int):
    """유저 포인트 갱신"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(sql_queries.UPDATE_USER_POINT, (new_point, user_id))

    conn.commit()
    conn.close()


def select_user_point_by_id(user_id: str):
    """유저 포인트 조회"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(sql_queries.SELECT_USER_POINT_BY_ID, (user_id,))
    point = cursor.fetchone()

    conn.close()

    return dict(point) if point else None