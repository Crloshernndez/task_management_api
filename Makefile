GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
BLUE := \033[0;34m
CYAN := \033[0;36m
NC := \033[0m

# --- Variables de Configuración ---
API_SERVICE_NAME := api
DOCKER_COMPOSE_FILE := docker-compose.yml
PYTHON_ENTRYPOINT := python -m uvicorn app.main:app

# Detectar si Docker está corriendo
DOCKER_RUNNING := $(shell docker-compose ps -q ${API_SERVICE_NAME} 2>/dev/null)

# Definir comandos según el entorno
ifdef DOCKER_RUNNING
    CMD_PREFIX := docker-compose exec ${API_SERVICE_NAME}
    FLAKE8_CMD := $(CMD_PREFIX) flake8
    MYPY_CMD := $(CMD_PREFIX) mypy
else
    CMD_PREFIX :=
    FLAKE8_CMD := flake8
    MYPY_CMD := mypy
endif

# --- Pseudo Targets ---
.PHONY: help setup dev venv clean clean-all

# --- Docker Targets ---
.PHONY: build up down restart logs logs-api shell db-upgrade db-downgrade db-reset

# --- Local Targets ---
.PHONY: install install-dev run run-prod test test-clean test-cov test-watch
.PHONY: lint format format-check sort-imports type-check security-check

## Default target
help:
	@echo "${GREEN}Comandos disponibles:${NC}"
	@echo ""
	@echo "  ${GREEN}help${NC}           - Muestra esta ayuda."
	@echo "  ${GREEN}build${NC}          - Construye la imagen Docker de la aplicación."
	@echo "  ${GREEN}start${NC}          - Inicia los contenedores (construye la imagen si es necesario)."
	@echo "  ${GREEN}stop${NC}           - Detiene y elimina los contenedores."
	@echo "  ${GREEN}restart${NC}        - Reinicia los contenedores."
	@echo "  ${GREEN}lint${NC}           - Ejecuta el linter (Flake8) dentro del contenedor."
	@echo "  ${GREEN}install-deps${NC}   - Instala las dependencias en el entorno virtual local."
	@echo "  ${GREEN}run-local${NC}      - Ejecuta la aplicación localmente (sin Docker)."
	@echo "  ${GREEN}clean${NC}          - Limpia el entorno (elimina entorno virtual, caché, etc.)."
	@echo ""
# ------------------------------------------------------------------------------
# ENVIRONMENT SETUP (LOCAL)
# ------------------------------------------------------------------------------

venv: ## Create virtual environment
	python3 -m venv venv
	@echo "Activate with: source venv/bin/activate"

install: ## Install production dependencies
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install -r requirements-dev.txt
	pre-commit install

install-deps: install install-dev
	@echo "installing all dependencies"

setup: venv install-dev ## Complete setup for new developers
	@echo ""
	@echo "✅ Setup complete! Use 'source venv/bin/activate' and 'make dev' to start."
	@echo ""

dev: install-dev run ## Quick development start

# ------------------------------------------------------------------------------
# LOCAL SERVER (WITHOUT DOCKER)
# ------------------------------------------------------------------------------

run-local: ## Run the development server
	${PYTHON_ENTRYPOINT} --reload --host 0.0.0.0 --port 8000

# ------------------------------------------------------------------------------
# DOCKER COMMANDS (DOCKER-COMPOSE)
# ------------------------------------------------------------------------------

build: ## Build Docker images
	docker-compose -f $(DOCKER_COMPOSE_FILE) build

start: build ## Start all services
	docker-compose -f $(DOCKER_COMPOSE_FILE) up -d

stop: ## Stop and remove all services
	docker-compose -f $(DOCKER_COMPOSE_FILE) down

restart: stop start ## Restart all services
	@echo "${GREEN}Restarting Docker services...${NC}"

logs: ## Show logs from all services
	docker-compose logs -f

logs-api: ## Show logs specifically for the API container
	docker-compose logs -f ${API_SERVICE_NAME}

shell: ## Connect to the API container terminal
	docker-compose exec ${API_SERVICE_NAME} /bin/bash

# ------------------------------------------------------------------------------
# CODE QUALITY
# ------------------------------------------------------------------------------

lint: ## Run linters (Flake8 and MyPy) - Docker or local
	$(FLAKE8_CMD) app tests
	$(MYPY_CMD) app
