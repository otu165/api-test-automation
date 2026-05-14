"""
경로 : shop-backend/app/constants/error_codes.py
파일명 : error_codes.py

API 실패 응답에서 사용할 공통 에러 코드를 모아놓은 파일

이 파일의 역할:
- 서비스 전체에서 사용하는 에러 코드 관리
- 테스트 코드에서 실패 원인을 명확하게 검증 가능케 함

"""


# 중복 이메일
EMAIL_ALREADY_EXISTS = "EMAIL_ALREADY_EXISTS"

# 로그인 시 이메일/비밀번호가 틀림
INVALID_CREDENTIALS = "INVALID_CREDENTIALS"

# 사용자를 찾을 수 없음
USER_NOT_FOUND = "USER_NOT_FOUND"

# 상품을 찾을 수 없음
PRODUCT_NOT_FOUND = "PRODUCT_NOT_FOUND"

# 상품 재고 부족
INSUFFICIENT_STOCK = "INSUFFICIENT_STOCK"

# 상품 구매에 필요한 포인트 부족
INSUFFICIENT_POINT = "INSUFFICIENT_POINT"
