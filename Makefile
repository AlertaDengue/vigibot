.ONESHELL:


SERVICES:=
# options: dev, prod
ENV:=vigibot

# DOCKER
DOCKER=docker-compose \
	--env-file .env \
	--project-name $(ENV) \
	--file docker/compose-$(ENV).yaml

.PHONY:docker-build
docker-build:
	$(DOCKER) build ${SERVICES}

.PHONY:docker-start
docker-start:
	$(DOCKER) up -d ${SERVICES}

.PHONY:docker-stop
docker-stop:
	$(DOCKER) stop ${SERVICES}

.PHONY:docker-logs
docker-logs:
	$(DOCKER) logs --follow --tail 100 ${SERVICES}

.PHONY:docker-pytest
docker-pytest:
	$(DOCKER) run --rm ${SERVICES} pytest ./tests/ -vv -s

.PHONY:docker-pytest-ci
docker-pytest-ci:
	$(DOCKER) run --rm ${SERVICES} pytest --ignore-glob='*test_twitter*'

.PHONY: lint
lint: ## formatting linter
	pre-commit install
	pre-commit run --all-files
