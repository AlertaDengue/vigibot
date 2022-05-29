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

.PHONY:docker-start-ci
docker-start-ci:
	$(DOCKER) up -d --scale base=0

.PHONY:docker-start
docker-start:
	$(DOCKER) up -d ${SERVICES}

.PHONY:docker-stop
docker-stop:
	$(DOCKER) stop ${SERVICES}

.PHONY:docker-start-ci
docker-start-ci:
	$(DOCKER) up -d --scale base=0
	
.PHONY:docker-pytest
docker-pytest:
	$(DOCKER) run --rm ${SERVICES} pytest ./tests/ -vv -s
