# Shop Backend

FastAPI 기반 API 및 pytest 자동화 테스트 프로젝트

## 기술 스택

- Python
- FastAPI
- SQLite
- pytest
- JWT Authentication

---

## 주요 기능

- 회원가입 / 로그인 API
- JWT 기반 인증 처리
- 포인트 조회 API
- 주문 생성 API
- pytest 기반 API 자동화 테스트
- 테스트 전용 DB 분리

---

## 프로젝트 구조

```text
shop-backend/
├── app/
│   ├── constants/
│   ├── exceptions/
│   ├── repositories/
│   ├── routers/
│   ├── services/
│   ├── utils/
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── sql_queries.py
│
├── tests/
│   ├── api/
│   ├── clients/
│   └── conftest.py
│
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## 실행 방법

### 패키지 설치

```bash
pip install -r requirements.txt
```

### FastAPI 서버 실행

```bash
uvicorn app.main:app --reload
```

### pytest 실행
```bash
pytest
```
