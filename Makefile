IMAGE_TAG := "rossweir-zendesk:latest"
PYTHON := python -m
SRC_DIRS := zendesk_search tests
RUN := docker \
	run \
	--rm \
	-it \
	-w /app \
	$(IMAGE_TAG)

# Run outside docker, inside a venv maybe.
ifeq ($(SYSTEM), 1)
	RUN =
endif

# Running in a CI environment.
ifeq ($(CI), true)
	RUN =
endif

build:
	docker build -t $(IMAGE_TAG) .

clean:
	docker rmi $(IMAGE_TAG)

shell:
	$(RUN) /bin/sh

fmt:
	$(RUN) black $(SRC_DIRS)

lint:
	$(RUN) $(PYTHON) isort $(SRC_DIRS)
	$(RUN) $(PYTHON) pylint $(SRC_DIRS)

typecheck:
	$(RUN) $(PYTHON) mypy $(SRC_DIRS)

test: test-unit

test-%:
	$(RUN) $(PYTHON) pytest tests/$(*)

test-cov:
	$(RUN) $(PYTHON) pytest --cov=zendesk_search tests/
	$(RUN) coveralls --service=github

run:
	$(RUN) $(PYTHON) zendesk_search