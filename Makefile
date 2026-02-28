# GAIA Makefile - Build Automation

.PHONY: help install test lint clean run-server run-desktop dev

help:
	@echo "GAIA Build Commands:"
	@echo "  make install       - Install Python dependencies"
	@echo "  make test          - Run test suite"
	@echo "  make lint          - Run code linters"
	@echo "  make clean         - Remove build artifacts"
	@echo "  make run-server    - Start WebSocket server"
	@echo "  make run-desktop   - Start Electron desktop"
	@echo "  make dev           - Development mode (server + desktop)"

install:
	@echo "Installing GAIA dependencies..."
	pip install -r requirements.txt
	pip install -e .
	@echo "\n✅ Installation complete!"

install-dev:
	@echo "Installing development dependencies..."
	pip install -r requirements.txt
	pip install pytest pytest-cov ruff black mypy
	cd web/desktop && npm install
	@echo "\n✅ Development setup complete!"

test:
	@echo "Running GAIA test suite..."
	pytest tests/ -v --cov=core --cov=overlay --cov=bridge --cov=infrastructure
	@echo "\n✅ Tests complete!"

test-quick:
	@echo "Running quick tests (no coverage)..."
	pytest tests/ -v

lint:
	@echo "Linting Python code..."
	ruff check .
	black --check .
	mypy core overlay bridge infrastructure

format:
	@echo "Formatting code..."
	black .
	ruff check --fix .

clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/ dist/ *.egg-info
	rm -rf .pytest_cache/ .coverage htmlcov/
	rm -rf **/__pycache__/
	find . -name "*.pyc" -delete
	@echo "✅ Clean complete!"

run-server:
	@echo "Starting GAIA WebSocket server..."
	python infrastructure/api/websocket_server.py

run-desktop:
	@echo "Starting GAIA Electron desktop..."
	cd web/desktop && npm start

dev:
	@echo "Starting GAIA in development mode..."
	@echo "Server: http://localhost:8765"
	@echo "Press Ctrl+C to stop"
	@make -j2 run-server run-desktop

init:
	@echo "Initializing GAIA Home instance..."
	python -c "from overlay.cli import init_home; init_home()"

docker-build:
	@echo "Building GAIA Docker image..."
	docker build -t gaia:latest .

docker-run:
	@echo "Running GAIA in Docker..."
	docker-compose up
