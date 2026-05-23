"""
경로 : shop-backend/tests/helpers/assertions.py
파일명 : assertions.py

테스트 공통 assertion 함수를 관리하는 파일

이 파일의 역할:
- 공통 성공 응답(success_response) 구조 검증
- 공통 실패 응답(error_response) 구조 검증

"""


from app.constants import error_codes


def assert_success_response(
        body: dict,
        message: str
):
    """공통 성공 응답 구조 검증"""

    assert body["success"] is True
    assert body["message"] == message
    assert body["error"] is None

    assert "data" in body
    assert isinstance(body["data"], dict)


def assert_error_response(
        body: dict,
        message: str,
        code: str
):
    """공통 실패 응답 구조 검증"""

    assert body["success"] is False
    assert body["message"] == message
    assert body["data"] is None

    assert "error" in body
    assert isinstance(body["error"], dict)

    assert "code" in body["error"]
    assert body["error"]["code"] == code


def assert_unauthorized_response(body: dict):
    """사용자 인증 실패 응답 검증"""

    assert_error_response(
        body = body,
        message = "사용자 인증 실패",
        code = error_codes.UNAUTHORIZED
    )


def assert_validation_error_response(body: dict):
    """Validation 실패 응답 검증"""

    assert_error_response(
        body = body,
        message = "부적절한 데이터 입력",
        code = error_codes.VALIDATION_ERROR
    )
