"""
경로 : shop-backend/app/models.py
파일명 : models.py

API 요청 및 응답 데이터 모델을 관리하는 파일

이 파일의 역할:
- Request 데이터 구조 정의
- Response 데이터 구조 정의
- API 입력값 검증에 사용

"""


from pydantic import BaseModel, EmailStr, Field


class SignUpRequest(BaseModel):
    """회원가입 요청 모델"""

    email: EmailStr
    password: str
    name: str


class SignInRequest(BaseModel):
    """로그인 요청 모델"""

    email: EmailStr
    password: str


class ChargePointRequest(BaseModel):
    """포인트 충전 요청 모델"""

    amount: int = Field(gt=0)   # 0 보다 큰 정수값


class CreateOrderRequest(BaseModel):
    """주문 생성 요청 모델"""

    product_id: str
    quantity: int = Field(gt=0) # 0 보다 큰 정수값


class MessageResponse(BaseModel):
    """공통 메시지 응답 모델 정의"""

    message: str