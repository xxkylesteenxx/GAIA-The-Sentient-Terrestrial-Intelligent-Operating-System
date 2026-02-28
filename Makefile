.PHONY: help install test lint format clean run dev docker-up docker-down

# Default target
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	pip install -r requirements.txt
	pip install -e .

test: ## Run tests with coverage
	pytest tests/ -v --cov=core --cov=overlay --cov=infrastructure --cov-report=term --cov-report=html

test-quick: ## Run tests without coverage
	pytest tests/ -v

lint: ## Run linting checks
	flake8 core/ overlay/ infrastructure/ bridge/ --count --max-line-length=100 --statistics
	mypy core/ overlay/ --ignore-missing-imports

format: ## Format code with black
	black core/ overlay/ infrastructure/ bridge/ tests/

clean: ## Clean build artifacts and cache
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ .coverage htmlcov/ .pytest_cache/ .mypy_cache/

run: ## Run WebSocket server
	python -m infrastructure.api.websocket_server

dev: ## Run in development mode with auto-reload
	python -m infrastructure.api.websocket_server --reload

docker-up: ## Start Docker Compose services
	docker-compose up -d

docker-down: ## Stop Docker Compose services
	docker-compose down

docker-logs: ## View Docker logs
	docker-compose logs -f gaia-core

docker-build: ## Build Docker image
	docker-compose build

electron: ## Run Electron desktop app
	cd web/desktop && npm install && npm start

all: clean install test lint ## Run full build pipeline
