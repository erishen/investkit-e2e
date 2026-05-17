# Makefile for E2E Tests

.PHONY: install test test-all test-asset-lens test-ts-demo test-solo-chat test-stock-analyzer test-investkit-utils clean report lint typecheck

install:
	pip install -e .
	playwright install

test:
	pytest -v

test-all:
	pytest -v --headed=false

test-asset-lens:
	pytest -v -m asset_lens

test-ts-demo:
	pytest -v -m ts_demo

test-solo-chat:
	pytest -v -m solo_chat

test-stock-analyzer:
	pytest -v -m stock_analyzer

test-investkit-utils:
	pytest -v -m investkit_utils

test-ui:
	pytest -v -m ui

test-api:
	pytest -v -m api

test-parallel:
	pytest -v -n auto

test-headed:
	pytest -v --headed

test-debug:
	pytest -v --headed --slowmo=500

report:
	pytest --html=report.html --self-contained-html

clean:
	rm -rf test-results/
	rm -rf .pytest_cache/
	rm -rf __pycache__/
	rm -f report.html

lint:
	ruff check tests/
	ruff format tests/

typecheck:
	mypy tests/
