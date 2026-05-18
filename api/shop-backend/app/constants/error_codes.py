"""
경로 : shop-backend/app/constants/error_codes.py
파일명 : error_codes.py

API 실패 응답에서 사용할 공통 에러 코드를 모아놓은 파일

이 파일의 역할:
- 서비스 전체에서 사용하는 에러 코드 관리
- 테스트 코드에서 실패 원인을 명확하게 검증 가능케 함

"""


# 부적절한 이메일 입력
INVALID_EMAIL = "INVALID_EMAIL"

# 부적절한 비밀번호 입력
INVALID_PASSWORD = "INVALID_PASSWORD"

# 부적절한 이름 입력
INVALID_NAME = "INVALID_NAME"

# 중복 이메일
DUPLICATED_EMAIL = "DUPLICATED_EMAIL"

# 로그인 시 이메일/비밀번호 틀림
INVALID_CREDENTIALS = "INVALID_CREDENTIALS"

# 일치하는 사용자 없음
USER_NOT_FOUND = "USER_NOT_FOUND"

# 부적절한 충전 금액 (0 이하)
INVALID_POINT_AMOUNT = "INVALID_POINT_AMOUNT"

# 부적절한 주문 수량 (0 이하)
INVALID_ORDER_QUANTITY = "INVALID_ORDER_QUANTITY"

# 일치하는 상품 없음
PRODUCT_NOT_FOUND = "PRODUCT_NOT_FOUND"

# 상품 재고 부족
INSUFFICIENT_STOCK = "INSUFFICIENT_STOCK"

# 사용자 포인트 부족
INSUFFICIENT_POINT = "INSUFFICIENT_POINT"

# 인증 토큰이 없거나 올바르지 않음
UNAUTHORIZED = "UNAUTHORIZED"

# 예상치 못한 서버 에러 발생
INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"

# 부적절한 데이터 포맷 입력 에러
VALIDATION_ERROR = "VALIDATION_ERROR"
