
build: .install-dependencies .sphinx
	@echo "Building project wheel"
	./venv/bin/python3 setup.py sdist bdist_wheel
	@echo "Deleting ssms.egg-info from project source"
	rm -rf ./src/main/python/ssms.egg-info

prepare: .create-dev-environment .install-dependencies

install:
	@if [ -d "./venv" ]; then \
  		if [ -d "./dist" ]; then \
  			./venv/bin/pip install dist/*.whl --upgrade --force-reinstall; \
  		else \
  		  	make build; \
  		fi \
  	else \
  	  make all; \
  	fi

all: clean prepare build install

clean:
	@echo "Removing ./venv"
	@rm -rf ./venv
	@echo "Removing ./build"
	@rm -rf ./build
	@echo "Removing ./dist"
	@rm -rf ./dist

list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

.create-dev-environment:
	@if [ -d "./venv" ]; then \
  		echo "Environment already exists. Run \"make clean\" first."; \
	else \
		echo "Creating virtual environment."; \
		python3 -m venv venv; \
  	fi

.install-dependencies:
	@if [ -d "./venv" ]; then \
		echo "Installing dependencies from requirements.txt"; \
		./venv/bin/pip install -r requirements.txt; \
	else \
	  	make prepare; \
	fi

.sphinx:
	@if [ -d "./venv" ]; then \
		cd ./docs && make html; \
	fi
