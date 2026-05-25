# HTML 리포트 생성
test-report:
	pytest --html=reports/shop-backend-api-test-report.html --self-contained-html

# HTML 리포트 생성 (verbose)
test-report-v:
	pytest -v --html=reports/shop-backend-api-test-report.html --self-contained-html

# 커버리지 리포트 터미널 출력
coverage:
	pytest --cov=app --cov-report=term-missing

# HTML 커버리지 리포트 생성
coverage-report:
	pytest --cov=app --cov-report=html:reports/shop-backend-api-coverage-report