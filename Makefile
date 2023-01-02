.ONESHELL:


SERVICES:=
# options: dev, prod
ENV:=vigibot

# DOCKER
DOCKER=docker-compose \
	--env-file .env \
	--project-name $(ENV) \
	--file containers/compose.yaml

.PHONY:container-build
container-build:
	$(DOCKER) build ${SERVICES}

.PHONY:container-start
container-start:
	$(DOCKER) up -d ${SERVICES}

.PHONY:container-stop
container-stop:
	$(DOCKER) stop ${SERVICES}

.PHONY:container-exec
container-exec:
	set -e
	$(DOCKER) exec ${ARGS} ${SERVICES} ${CMD}

.PHONY:container-logs
container-logs:
	$(DOCKER) logs --follow --tail 100 ${SERVICES}

.PHONY:container-pytest
container-pytest:
	$(DOCKER) run --rm ${SERVICES} pytest ./tests/ -vv -s

.PHONY:container-pytest-ci
container-pytest-ci:
	$(DOCKER) run --rm ${SERVICES} pytest --ignore-glob='*test_twitter*'

.PHONY: lint
lint: ## formatting linter
	pre-commit install
	pre-commit run --all-files

# Python
.PHONY: clean
clean: ## clean all artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	rm -fr .idea/
	rm -fr */.eggs
	rm -fr db
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -fr {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	find . -name '*.ipynb_checkpoints' -exec rm -rf {} +
	find . -name '*.pytest_cache' -exec rm -rf {} +
