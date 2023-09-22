.PHONY: help

DOCKER_DEV := docker compose -f docker-compose.yml

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build developer containers for services (backend, frontend, ...)
	$(DOCKER_DEV) pull
	$(DOCKER_DEV) build

up: ## Run developer containers (all services)
	$(DOCKER_DEV) up

p0: ## Run P0
	docker compose run app python hola_mundo.py