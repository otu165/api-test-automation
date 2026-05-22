"""
경로 : shop-backend/app/utils/password.py
파일명 : password.py

비밀번호 해싱 및 검증 기능을 관리하는 파일

이 파일의 역할:
- 비밀번호를 bcrypt 해시값으로 변환
- 입력된 비밀번호와 DB에 저장된 해시값 일치 여부 검증

"""


from passlib.context import CryptContext


# 비밀번호 해싱 정책을 정하는 객체
pwd_context = CryptContext(
    schemes = ["bcrypt"],   # 비밀번호 해싱 알고리즘을 bcrypt 로 지정
    deprecated = "auto"     # 오래된 해싱 방식을 자동 deprecated 처리
)


def hash_password(password: str) -> str:
    """비밀번호를 bcrypt 해시값으로 변환"""

    return pwd_context.hash(password)


def verify_password(
        plain_password: str,
        hashed_password: str
) -> bool:
    """입력 비밀번호와 저장된 해시값 일치 여부 검증"""

    return pwd_context.verify(
        plain_password,
        hashed_password
    )