install_requirements:
	@python_install/bin/pip install pipreqs nose
	@python_install/bin/pip install -r requirements.txt

python_install:
	@pip install --upgrade --user virtualenv
	@virtualenv `which python3` python_install

tmp:
	@mkdir tmp

dev_environment: python_install install_requirements

install: dev_environment

update_requirements_file: dev_environment
	@python_install/bin/pipreqs --use-local --savepath requirements.txt $(PWD)

tests: dev_environment
	@python_install/bin/python main_app.py -d

clean_dev:
	@rm -rf python_install

clean_logs:
	@rm -rf logs/*log

clean_tmp:
	@rm -rf tmp

clean_sessions:
	@find run/* -type d | xargs -I{} rm -rf {}

clean_bin:
	@rm -rf bin/*
	@touch bin/empty

clean: clean_logs clean_sessions clean_tmp

clean_all: clean clean_dev

.PHONY: install dev_environment install_requirements update_requirements_file tests clean_logs clean_sessions clean_dev clean_all clean_tmp clean_bin clean
