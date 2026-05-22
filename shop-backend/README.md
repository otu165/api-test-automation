# Shop Backend

[![Tests](https://github.com/otu165/api-test-automation/actions/workflows/shop-backend.yml/badge.svg)](https://github.com/otu165/api-test-automation/actions/workflows/shop-backend.yml)

FastAPI 기반 쇼핑몰 백엔드 API 및 자동화 테스트 프로젝트

<br/>

---


## 프로젝트 구조

```text
shop-backend/
├── app/
│   ├── constants/       # 에러 코드, 상수
│   ├── exceptions/      # 공통 예외 처리
│   ├── repositories/    # DB 조회 및 저장 로직
│   ├── routers/         # API 라우터
│   ├── services/        # 비즈니스 로직 처리
│   ├── utils/           # JWT, password hash 등 공통 유틸
│   ├── core/            # DB 연결 및 SQL 관리
│   ├── schemas/         # Request / Response 모델
│   └── main.py
│
├── tests/
│   ├── api/             # API 테스트
│   │   ├── auth/        # 회원가입, 로그인 테스트
│   │   ├── order/       # 주문 생성, 취소, 조회, 동시성 테스트
│   │   └── point/       # 포인트 조회 테스트
│   ├── clients/         # 테스트용 API client
│   └── conftest.py      # fixture 및 테스트 DB 초기화
│
├── pytest.ini           # pytest 설정
├── requirements.txt     # 프로젝트 의존성 관리
└── README.md
```

<br/>

---

## 기술 스택

- Python 3.13
- FastAPI (REST API 구현)
- SQLite (DB)
- Pytest (API 테스트)
- JWT (사용자 인증)
- GitHub Actions (테스트 자동 실행)

<br/>

---

## 주요 기능

### 인증

| 기능      | 내용                          |
|---------|-----------------------------|
| 회원가입    | 사용자 회원가입 API 구현             |
| 로그인     | 이메일 / 비밀번호 로그인 API 구현       |
| JWT 인증  | access_token 발급 및 사용자 인증 처리 |
| 입력 검증   | 이메일 형식 및 길이, 비밀번호 길이 검증     |
| 비밀번호 해싱 | bcrypt 기반 비밀번호 해싱 저장 및 검증   |

<br/>

### 포인트

| 기능 | 내용 |
|------|------|
| 포인트 조회 | 현재 로그인 사용자의 포인트 조회 |
| 포인트 충전 | 사용자 포인트 충전 |

<br/>

### 주문

| 기능 | 내용 |
|------|------|
| 주문 생성 | 상품 주문 API 구현 |
| 주문 취소 | 주문 취소 API 구현 |
| 주문 상태 관리 | PAID / CANCELED 상태 관리 |
| 포인트 복구 | 주문 취소 시 차감 포인트 복구 |
| 재고 복구 | 주문 취소 시 상품 재고 복구 |
| 내 주문 목록 조회 | 현재 로그인 사용자의 주문 목록 조회 |
| 내 주문 상세 조회 | 현재 로그인 사용자의 주문 상세 조회 |
| 권한 검증 | 로그인 사용자만 자신의 주문 조회 및 취소 가능 |

<br/>

---

## 테스트 코드

pytest 를 사용해 API 테스트 작성

| 구분 | 테스트 내용                                                |
|------|-------------------------------------------------------|
| 인증 | 회원가입/로그인 성공, 입력 검증 실패, 중복 이메일, 잘못된 비밀번호, 존재하지 않는 이메일  |
| 포인트 | 포인트 조회 성공, 잘못된 토큰 요청 실패                               |
| 주문 생성 | 주문 생성 성공, 잘못된 토큰 요청 실패, 존재하지 않는 상품 주문 실패, 주문 수량 검증 실패 |
| 주문 취소 | 주문 취소 성공, 존재하지 않는 주문 취소 실패, 이미 취소된 주문 재취소 실패          |
| 주문 복구 | 주문 취소 시 포인트/재고 복구                                     |
| 주문 조회 | 내 주문 목록 조회, 내 주문 상세 조회                                |
| 권한 검증 | 타인의 주문 취소 실패                                          |
| 동시성 | 재고 1개 상품에 대한 동시 주문 요청 검증                              |

<br/>

### 테스트 fixture

| fixture | 역할 |
|---------|------|
| client | FastAPI TestClient 생성 |
| reset_test_database | 각 테스트 실행 전 테스트 DB 초기화 |
| signed_up_user | 테스트용 회원가입 사용자 생성 |
| access_token | 테스트용 JWT access_token 생성 |
| order_client | 인증된 주문 API 테스트 클라이언트 생성 |
| point_client | 인증된 포인트 API 테스트 클라이언트 생성 |
| created_order_id | 테스트용 주문 생성 후 order_id 반환 |
| second_access_token | 두 번째 테스트 사용자 access_token 생성 |


<br/>

---

## CI / GitHub Actions / 테스트 리포트

GitHub Actions 를 사용해 main 브랜치 push 시 자동으로 테스트 실행

- pytest 자동 실행
- pytest-html 을 사용해 테스트 결과를 HTML 리포트로 생성
- HTML 리포트 artifact 다운로드 가능

<br/>

---

## 실행 방법

### 패키지 설치

```bash
pip install -r requirements.txt
```


### 서버 실행

```bash
uvicorn app.main:app --reload
```


### 전체 테스트 실행
```bash
pytest
```

<br/>
