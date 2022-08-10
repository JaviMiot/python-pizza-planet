

override SHELL := /bin/bash

.PHONY: help
help: ## Show this help message.
	@echo 'Usage:'
	@echo '  make [target] ...'
	@echo
	@echo 'Targets:'
	@grep --no-filename -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	 sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: init_db
init_db: ## Init db and populate with faker data.
	python manage.py db init && \
	python manage.py db migrate && \
	python manage.py db upgrade

.PHONY: faker_db
faker_db: ## Populate db with faker data
	python manage.py seed run --root app/seeds