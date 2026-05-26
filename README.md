# api-test-automation

API 테스트 자동화 프로젝트를 직접 구축하며
테스트 구조 설계, API 성공/실패 검증, 동시성, 테스트 커버리지, CI 파이프라인을 학습하기 위한 레포지토리

<br/>

---

## 프로젝트

| 구분 | 설명 | CI |
|-----|-----|----|
| [shop-backend](./shop-backend) | FastAPI 기반 쇼핑몰 API 테스트 자동화 | [![Tests](https://github.com/otu165/api-test-automation/actions/workflows/shop-backend.yml/badge.svg)](https://github.com/otu165/api-test-automation/actions/workflows/shop-backend.yml) |

<br/>

---

## 핵심 기술 스택

- Python
- Pytest
- FastAPI
- SQLite
- JWT
- GitHub Actions
- Pytest-cov

<br/>

---

## 학습 목표

- API 자동화 테스트
- 인증(Authentication) 및 인가(Authorization) 테스트
- 에러 처리 및 예외 검증
- 동시성(Concurrency) 및 엣지 케이스(Edge Case) 테스트
- 테스트 커버리지 및 CI 파이프라인
- 자동화 테스트 유지보수성 (Fixture, Helper, Marker 구조)

<br/>

---

## 레포지토리 구조

```text
api-test-automation/
├── shop-backend/
└── README.md
```

<br/>

---

## 진행 상황

- [x] shop-backend
