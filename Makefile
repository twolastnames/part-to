
all: build

VENV_BASE=venv
VENV=$(VENV_BASE)/bin/activate

NENV_BASE=nenv
NENV=$(NENV_BASE)/bin/activate

PROJECT=project
NODE_BASE=project/parttofe/partto
NODE_SOURCE=$(NODE_BASE)/src
NODE_MODULES=$(NODE_BASE)/node_modules
NODE_BUILD=$(NODE_BASE)/build
NODE ?=node
NPM ?=npm

WITH_VENV=. $(VENV) &&
WITH_ENV=$(WITH_VENV) . $(NENV) &&

GIT_HOOKS_PATH=githooks

VENV_CHECK := $(shell command -v virtualenv 2> /dev/null)

$(VENV):
	-python3 -m venv venv
	. $(VENV_BASE)/bin/activate
	if [ -d ".git" ]; then git config core.hooksPath $(GIT_HOOKS_PATH); fi
	$(WITH_VENV) python3 -m pip install -r requirements.txt

$(NENV): $(VENV)
	echo nenv run
	$(WITH_VENV) echo nodeenv using virtulenv $(VIRTUAL_ENV)
	$(WITH_VENV) nodeenv $(NENV_BASE) --node=20.19.2

$(NODE_MODULES): $(VENV)  $(NENV) project/parttofe/partto/package-lock.json
	$(WITH_ENV) cd $(NODE_BASE) && $(NODE_ENV_PATH) $(NPM) ci

$(NODE_BUILD): $(VENV) $(NENV) $(shell find ${NODE_SOURCE} -type f) $(NODE_MODULES)
	$(WITH_ENV) $(NODE) -v && cd $(NODE_BASE) && $(NODE) ./node_modules/.bin/react-scripts build

build: $(VENV) $(NENV) $(NODE_BUILD)

clean:
	rm -rf $(NODE_BUILD) $(NODE_MODULES) $(NENV_BASE) $(VENV_BASE)

insertdefaultrecipes:
	${WITH_ENV} python3 project/manage.py insertrecipe recipeexamples/*

full: $(NENV) test migrate insertdefaultrecipes runback

runback: $(VENV) $(NENV) $(NODE_BUILD) migrate
	$(WITH_ENV) cd project && python3 manage.py runserver $(ARGUMENTS)

runfront: $(VENV) $(NENV) $(NODE_BUILD)
	$(WITH_ENV) cd $(NODE_SOURCE) && REACT_APP_PART_TO_API_BASE=http://localhost:8000 $(NPM) run start

runstorybook: $(VENV) $(NENV) $(NODE_BUILD)
	$(WITH_ENV) cd $(NODE_SOURCE) && npm run storybook

testfront: $(NENV) project/parttofe/partto/node_modules
	$(WITH_ENV) cd $(NODE_SOURCE) && npm run test -- --watchAll=false $(ARGUMENTS)

testback: $(NENV) $(NODE_BUILD)
	$(WITH_ENV) cd $(PROJECT) && PYTHONHASHSEED=18 python3 manage.py test parttobe$(ARGUMENTS)

command: $(NENV)
	$(WITH_ENV) python3 project/manage.py $(ARGUMENTS)

checkformat:
	$(WITH_ENV) black --check . && cd $(NODE_SOURCE) && npm run checkformat

format: $(NENV) $(NODE_MODULES)
	$(WITH_ENV) black . && cd $(NODE_SOURCE) && npm run format

migrate: $(NENV)
	$(WITH_ENV) python3 project/manage.py migrate

updateapi: $(NENV)
	$(WITH_ENV) python3 project/manage.py updateapi

release: $(NENV)
	$(WITH_ENV) ./bin/release.py

image: $(NENV)
	sudo bash -c "${WITH_ENV} docker build -t twolastnames/part-to ."

test: testfront testback

enterimage: $(VENV) migrate
	cd project && PART_TO_DATA_DIRECTORY=/var/partto ../venv/bin/gunicorn --bind :20222 --workers 4 --access-logfile $(PART_TO_DATA_DIRECTORY)/partto.out.log --error-logfile $(PART_TO_DATA_DIRECTORY)/partto.err.log --log-level debug project.wsgi

