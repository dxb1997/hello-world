# PyFlink ETL Project Makefile

.PHONY: help install setup clean run demo test lint format

# Default target
help:
	@echo "PyFlink ETL Project"
	@echo "Available targets:"
	@echo "  install    - Install Python dependencies"
	@echo "  setup      - Set up virtual environment and install dependencies"
	@echo "  run        - Run the ETL pipeline"
	@echo "  demo       - Run the complete demo workflow"
	@echo "  clean      - Clean generated files and output"
	@echo "  test       - Run tests (if available)"
	@echo "  lint       - Run code linting"
	@echo "  format     - Format code with black"
	@echo "  help       - Show this help message"

# Install dependencies
install:
	pip install -r requirements.txt

# Set up virtual environment and dependencies
setup:
	python3 -m venv venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r requirements.txt
	@echo "Virtual environment created. Activate with: source venv/bin/activate"

# Run the ETL pipeline
run:
	python etl_pipeline.py

# Run the demo
demo:
	python run_demo.py

# Clean generated files
clean:
	rm -rf data/output/*
	rm -rf __pycache__/
	rm -rf *.pyc
	rm -rf .pytest_cache/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +

# Run tests (placeholder)
test:
	@echo "No tests configured yet. Add pytest configuration to run tests."

# Run linting
lint:
	@echo "Installing flake8 for linting..."
	pip install flake8
	flake8 *.py --max-line-length=100 --ignore=E501,W503

# Format code
format:
	@echo "Installing black for code formatting..."
	pip install black
	black *.py --line-length=100

# Development setup
dev-setup: setup
	./venv/bin/pip install black flake8 pytest
	@echo "Development environment ready!"

# Check environment
check-env:
	@echo "Checking environment..."
	@python3 -c "import sys; print(f'Python version: {sys.version}')"
	@java -version 2>&1 | head -1 || echo "Java not found"
	@echo "Current directory: $(PWD)"
	@echo "Environment check complete."