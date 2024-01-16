.PHONY: help

.DEFAULT_GOAL := help
runner := $(shell whoami)

PV := $(shell command -v pv || command -v pipebench || echo cat)
DOCKER_DEV := docker compose
PRODUCTION_DOCKER:= docker-compose -f docker-compose-prod.yml

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build developer containers for services (backend, frontend, ...)
	$(DOCKER_DEV) build

up: ## Run developer containers
	$(DOCKER_DEV) up

up-prod: ## Run production containers
	$(PRODUCTION_DOCKER) up

build-prod: ## Build production containers
	$(PRODUCTION_DOCKER) build

down: ## Stop and remove all service containers
	$(DOCKER_DEV) down --remove-orphans

migrate: ## Run migrate command in api container.
	$(DOCKER_DEV) run --rm app python manage.py migrate

makemigrations: ## Run makemigrations command in api container.
	$(DOCKER_DEV) run --rm app python manage.py makemigrations
	sudo -S chown -R $(runner):$(runner) ../DAI/*

mergemigrations: ## Run make merge migrations command in api container.
	$(DOCKER_DEV) run  --rm backend python manage.py makemigrations --merge
	sudo -S chown -R $(runner):$(runner) ../DAI/*

api-createsuperuser: ## Create new superadmin user.
	$(DOCKER_DEV) run --rm app python manage.py createsuperuser

api-startproject:  ## Create new backend project, expects name argument.
	$(DOCKER_DEV) run --rm app django-admin startproject '$(name)' .

api-newapp: ## Create new backend app, expects name argument.
	$(DOCKER_DEV) run --rm app python manage.py startapp '$(name)' .

docker_stop_all_containers: ## Stop all docker running containers
	docker container stop $(shell docker container ls -aq)

docker_rm_all_containers: docker_stop_all_containers ## Stop and remove all docker running containers
	docker container rm $(shell docker container ls -aq)

mongodump:  ## Export database
	$(DOCKER_DEV) up mongo
	docker compose run mongo mongodump --host=127.0.0.1 --port=27017 --db shop
