"""
경로 : shop-backend/app/exceptions/exception_handlers.py
파일명 : exception_handlers.py

서비스 공통 예외 처리 핸들러를 관리하는 파일

이 파일의 역할:
- ApiException 발생 시 공통 실패 응답 반환
- API 실패 응답 구조 통일

"""

from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.api_exception import ApiException
from app.utils.response import error_response


def api_exception_handler(
        request: Request,
        exception: ApiException
) -> JSONResponse:
    """
    ApiException 을 처리하는 전역 예외 핸들러 함수

    쉽게 말하면:
    Service 에서 ApiException 이 발생했을 때,
    FastAPI 가 기본 응답을 만들지 않고 이 함수로 예외를 넘긴다.

    이 함수는 전달받은 예외 정보를 이용해
    프로젝트의 공통 실패 응답 구조를 만들어 반환한다.
    """

    return JSONResponse(
        status_code = exception.status_code,
        content = error_response(
            message = exception.message,
            code = exception.code,
            detail = exception.detail
        )
    )