"""
경로 : shop-backend/app/exceptions/api_exception.py
파일명 : api_exception.py

API 실패 상황을 표현하기 위한 커스텀 예외 클래스 파일

이 파일의 역할:
- 서비스 전체에서 사용할 공통 예외 클래스 정의
- HTTP 상태 코드, 메시지, 에러 코드, 상세 내용을 하나의 객체로 묶어 관리

"""

class ApiException(Exception):

    def __init__(
            self,
            status_code: int,
            message: str,
            code: str,
            detail: str
    ):
        self.status_code = status_code
        self.message = message
        self.code = code
        self.detail = detail

        # 부모 Exception 클래스에도 detail 전달
        # (로그나 디버깅 도구에서 예외 메시지 확인이 쉬워짐)
        super().__init__(detail)