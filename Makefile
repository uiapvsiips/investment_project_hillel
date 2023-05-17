MANAGE=python manage.py
PIP=pip


install:
	$(PIP) install -r requirements.txt
	$(MANAGE) migrate
run:
	$(MANAGE) runserver

