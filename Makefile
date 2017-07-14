install_requirements:
	@python_install/bin/pip install pipreqs nose
	@python_install/bin/pip install -r requirements.txt

python_install:
	@sudo pip install virtualenv
	@virtualenv python_install
