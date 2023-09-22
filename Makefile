.PHONY: help

.DEFAULT_GOAL := help
runner=$(shell whoami)

PV := $(shell command -v pv || command -v pipebench || echo cat)
DOCKER_DEV := docker compose -f docker-compose.yml

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build developer containers for services (backend, frontend, ...)
	$(DOCKER_DEV) pull
	$(DOCKER_DEV) build

up: ## Run developer containers (all services)
	$(DOCKER_DEV) up

down: ## Stop and remove all service containers
	$(DOCKER_DEV) down --remove-orphans

migrate: ## Run migrate command in api container.
	$(DOCKER_DEV) run --rm api python manage.py migrate

makemigrations: ## Run makemigrations command in api container.
	$(DOCKER_DEV) run --rm api python manage.py makemigrations
	sudo -S chown -R $(runner):$(runner) -Rf sips-api/*

mergemigrations: ## Run make merge migrations command in api container.
	$(DOCKER_DEV) run  --rm api python manage.py makemigrations --merge
	sudo -S chown -R $(runner):$(runner) -Rf sips-api/*

api-createsuperuser: ## Create new superadmin user.
	$(DOCKER_DEV) run --rm api python manage.py createsuperuser

api-newapp: ## Create new backend app, expects name argument.
	$(DOCKER_DEV) run --rm api python manage.py startapp '$(name)'
	mkdir ./backend/src/$(name)/tests/
	touch ./backend/src/$(name)/serializers.py
	touch ./backend/src/$(name)/tests/test_$(name).py
	touch ./backend/src/$(name)/factory.py
	rm -r ./backend/src/$(name)/admin.py
	rm -r ./backend/src/$(name)/apps.py
	rm -r ./backend/src/$(name)/tests.py
	sudo chown -R $(runner):$(runner) ./backend/src/$(name)

docker_stop_all_containers: ## Stop all docker running containers
	docker container stop $(shell docker container ls -aq)

docker_rm_all_containers: docker_stop_all_containers ## Stop and remove all docker running containers
	docker container rm $(shell docker container ls -aq)

p0: ## Run P0
	docker compose run app python hola_mundo.py

p1: ## Run P1
	docker compose run backend python main.py
