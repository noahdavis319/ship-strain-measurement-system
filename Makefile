
clean:
	rm -rf venv

create-dev-environment:
	python3 -m venv venv

install-dependencies:
	@if [ -d "./venv" ]; then \
		echo "Installing dependencies from requirements.txt"; \
		./venv/bin/pip install -r requirements.txt; \
	fi

sphinx:
	cd ./docs && make html
