.DEFAULT_GOAL := help

.PHONY: help install test deploy run down clean

help:
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install all dependencies required for the service.
	@# Check if Python 3 is installed
	@if ! command -v python3 &> /dev/null; then \
		echo "\033[31mError: python3 is not installed.\033[0m"; \
		echo "Please install Python 3 to continue."; \
		exit 1; \
	fi
	@# Check if pip is installed
	@if ! python3 -m pip --version &> /dev/null; then \
		echo "\033[31mError: pip3 is not installed for Python 3.\033[0m"; \
		echo "Please install pip3."; \
		exit 1; \
	fi
	@if ! npm  --version &> /dev/null; then \
		echo "Please install NodeJS & npm."; \
	fi
	
	npm i -g vercel

test: ## Run all tests using pytest.
	@echo "Running tests..."
	@# Check if pytest is installed
	@if ! python3 -m pytest --version &> /dev/null; then \
		echo "\033[31mError: pytest is not installed.\033[0m"; \
		echo "Please install it by adding 'pytest' to your requirements.txt and running 'make install'."; \
		exit 1; \
	fi

	python3 -m pytest test/test_agent.py

run: ## Run the service and all related services in Docker.
	vercel dev

deploy: ## Run the service and all related services in Docker.
	vercel build
	vercel deploy

down: ## Stop all running services started with 'make run'.
	echo "..."

clean: ## Stop services AND remove all associated containers, networks, and volumes.
	
	rm conversations.json
	rm -rf .vercel

