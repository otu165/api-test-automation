"""
경로 : shop-backend/app/utils/auth.py
파일명 : auth.py

JWT 토큰 생성 및 검증 기능을 관리하는 파일

이 파일의 역할:
- JWT Access Token 생성 기능 제공
- JWT 토큰 payload 생성 기능 제공

"""

import os
from dotenv import load_dotenv

from jose import jwt, JWTError
from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


load_dotenv()


# JWT 서명에 사용할 비밀키
SECRET_KEY = os.getenv("SECRET_KEY")

if SECRET_KEY is None:
    raise ValueError("SECRET_KEY 가 정의되지 않았습니다.")

# JWT 암호화 방식
ALGORITHM = "HS256"

# access_token 만료 시간(분)
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(user_id: str) -> str:
    """
    JWT access token 생성 함수
    (user_id 를 받아서 JWT access_token 생성)
    """

    # 현재 시간
    now = datetime.now(UTC)

    # 만료 시간 계산
    expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # JWT 안에 넣을 데이터 (payload)
    # payload 에는 "서버가 이후 인증/권한 처리에 필요한 최소 정보"를 넣는다.
    payload = {
        "user_id" : user_id,    # 사용자 ID
        "exp" : expire          # 만료 시간
    }

    # JWT 생성
    access_token = jwt.encode(
        payload,                # payload 데이터
        SECRET_KEY,             # 비밀키
        algorithm = ALGORITHM   # 암호화 알고리즘
    )

    # 생성한 JWT 반환
    # ㄴ 토큰 예시) eyJhbGciOiJIUzI1NiIs...
    return access_token



def verify_access_token(token: str):
    """
    JWT access_token 검증 함수
    (JWT token 검증 후 user_id 반환)
    """

    try:
        # JWT 해석(decode) ** 핵심 **
        payload = jwt.decode(
            token,                      # 검증할 토큰
            SECRET_KEY,                 # 비밀키
            algorithms = [ALGORITHM]    # 허용 알고리즘
        )

        # payload 안의 user_id 꺼내기
        user_id = payload.get("user_id")

        # user_id 없으면 에러
        if user_id is None:
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "유효하지 않은 토큰입니다."
            )

        # 정상이라면 user_id 반환
        return user_id

    except JWTError:
        # JWT 검증 실패
        # ㄴ 예시) 토큰 위조, 만료, 형식 오류, 비밀키 불일치 등...

        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "토큰 검증 실패"
        )


# Authorization: Bearer <token> 형식의 Header 를 읽는 도구
security = HTTPBearer()

def get_current_user_id(
        credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """현재 로그인한 사용자의 user_id 를 반환하는 함수"""

    # Header 에서 token 문자열만 꺼내기
    token = credentials.credentials

    # token 검증 후 user_id 반환
    return verify_access_token(token)

