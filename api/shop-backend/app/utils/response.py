"""
경로 : shop-backend/app/utils/response.py
파일명 : response.py

공통 API 응답 데이터를 생성하는 파일

이 파일의 역할:
- 성공/실패 응답 데이터 생성
- 서비스 전체 응답 형식 통일

공통 응답 구조:
- 성공:
{
    "success" : True,
    "message" : "...",
    "data" : {...},
    "error" : null
}

- 실패:
{
    "success" : False,
    "message" : "...",
    "data" : null,
    "error" : {
        "code" : "...",
        "detail" : "..."
    }
}

"""


from typing import Any


def success_response(
        message: str,
        data: dict[str, Any] | list[Any] | None = None
) -> dict[str, Any]:
    """성공 API 응답을 만드는 함수"""

    return {
        "success" : True,
        "message" : message,
        "data" : data,
        "error" : None
    }


def error_response(
        message: str,
        code: str,
        detail: str
) -> dict[str, Any]:
    """실패 API 응답을 만드는 함수"""

    return {
        "success" : False,
        "message" : message,
        "data" : None,
        "error" : {
            "code" : code,
            "detail" : detail
        }
    }
