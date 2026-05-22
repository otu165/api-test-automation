"""
경로 : shop-backend/app/utils/password_validator.py
파일명 : password_validator.py

비밀번호 입력값 검증을 관리하는 파일

이 파일의 역할:
- 비밀번호 패턴 (영어 + 숫자 + 특수문자) 검증

"""

import re

# 특수문자 패턴
SPECIAL_CHAR_PATTERN = r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]"


def validate_password_policy(password:str) -> str:
    """비밀번호 조합 검증"""

    if not re.search(r"[A-Za-z]", password):
        raise ValueError("영문자가 1개 이상 포함되어야 합니다.")

    if not re.search(r"\d", password):
        raise ValueError("숫자가 1개 이상 포함되어야 합니다.")

    if not re.search(SPECIAL_CHAR_PATTERN, password):
        raise ValueError("특수문자가 1개 이상 포함되어야 합니다.")

    return password