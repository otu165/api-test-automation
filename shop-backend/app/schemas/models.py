"""
경로 : shop-backend/app/schemas/models.py
파일명 : models.py

API 요청 및 응답 데이터 모델을 관리하는 파일

이 파일의 역할:
- Request 데이터 구조 정의
- Response 데이터 구조 정의
- API 입력값 검증에 사용

"""


from pydantic import BaseModel, EmailStr, Field, field_validator

from app.utils.password_validator import validate_password_policy


class SignUpRequest(BaseModel):
    """회원가입 요청 모델"""

    email: EmailStr = Field(
        max_length = 254,
        examples = ["user@example.com"],
        description = "사용자 이메일"
    )

    password: str = Field(
        min_length = 8,
        max_length = 72,
        examples = ["test1234!"],
        description = "사용자 비밀번호"
    )

    name: str = Field(
        examples = ["홍길동"],
        description = "사용자 이름"
    )

    @field_validator("password")
    @classmethod
    def validate_password(_cls, password: str) -> str:
        """비밀번호 조합 검증"""

        return validate_password_policy(password)


class SignInRequest(BaseModel):
    """로그인 요청 모델"""

    email: EmailStr = Field(
        max_length = 254,
        examples = ["user@example.com"],
        description = "로그인 이메일"
    )

    password: str = Field(
        min_length = 8,
        max_length = 72,
        examples = ["test1234!"],
        description = "로그인 비밀번호"
    )

    @field_validator("password")
    @classmethod
    def validate_password(_cls, password: str) -> str:
        """비밀번호 조합 검증"""

        return validate_password_policy(password)


class ChargePointRequest(BaseModel):
    """포인트 충전 요청 모델"""

    amount: int = Field(
        gt = 0, # 0 보다 큰 정수값이 입력되어야 함
        examples = [1000],
        description = "충전할 포인트"
    )


class CreateOrderRequest(BaseModel):
    """주문 생성 요청 모델"""

    product_id: str = Field(
        examples = ["KB1001"],      # API 문서에 노출될 product_id 예시
        description = "주문할 상품 ID" # API 문서에 노출될 product_id 설명
    )

    quantity: int = Field(
        gt = 0, # 0 보다 큰 정수값이 입력되어야 함
        examples = [1],
        description = "주문 수량"
    )


class MessageResponse(BaseModel):
    """공통 메시지 응답 모델 정의"""

    message: str