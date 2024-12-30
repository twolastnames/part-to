
all: build

VENV_BASE=venv
VENV=$(VENV_BASE)/bin/activate

NENV_BASE=nenv
NENV=$(NENV_BASE)/bin/activate

PROJECT=project
NODE_BASE=project/parttofe/partto
NODE_SOURCE=$(NODE_BASE)/src
NODE_BUILD=$(NODE_BASE)/build
NODE_MODULES=$(NODE_BASE)/node_modules

WITH_VENV=. $(VENV) &&
WITH_ENV=$(WITH_VENV) . $(NENV) &&

GIT_HOOKS_PATH=githooks

$(VENV):
	git config core.hooksPath $(GIT_HOOKS_PATH)
	python3 -m pip install virtualenv
	virtualenv $(VENV_BASE)
	$(WITH_VENV) python3 -m pip install -r requirements.txt

$(NENV): $(VENV)
	$(WITH_VENV) echo nodeenv using virtulenv $(VIRTUAL_ENV)
	$(WITH_VENV) nodeenv $(NENV_BASE) --node=20.10.0

$(NODE_BUILD): $(VENV) project/parttofe/partto/node_modules $(NENV) $(shell find ${NODE_SOURCE} -type f)
	$(WITH_ENV) node -v && cd $(NODE_BASE) && npm run build

build: $(VENV) $(NENV) $(NODE_BUILD)

clean:
	rm -rf $(NODE_BUILD) $(NENV_BASE) $(VENV_BASE) $(NODE_MODULES)

insertdefaultrecipes:
	${WITH_ENV} python3 project/manage.py insertrecipe recipeexamples/*

demo: $(NENV) test migrate insertdefaultrecipes runback

runback: $(VENV) $(NENV) $(NODE_BUILD) migrate
	$(WITH_ENV) cd project && python3 manage.py runserver $(ARGUMENTS)

runfront: $(VENV) $(NENV) $(NODE_BUILD)
	$(WITH_ENV) cd $(NODE_SOURCE) && npm run start

runstorybook: $(VENV) $(NENV) $(NODE_BUILD)
	$(WITH_ENV) cd $(NODE_SOURCE) && npm run storybook

project/parttofe/partto/node_modules: $(NENV) project/parttofe/partto/package-lock.json
	$(WITH_ENV) cd $(NODE_SOURCE) && npm ci

testfront: $(NENV) project/parttofe/partto/node_modules
	$(WITH_ENV) cd $(NODE_SOURCE) && npm run test -- --watchAll=false $(ARGUMENTS)

testback: $(NENV) $(NODE_BUILD)
	$(WITH_ENV) cd $(PROJECT) && python3 manage.py test parttobe$(ARGUMENTS)

command: $(NENV)
	$(WITH_ENV) python3 project/manage.py $(ARGUMENTS)

checkformat:
	$(WITH_ENV) black --check . && cd $(NODE_SOURCE) && npm run checkformat

format: $(NENV)
	$(WITH_ENV) black . && cd $(NODE_SOURCE) && npm run format

migrate: $(NENV)
	$(WITH_ENV) python3 project/manage.py migrate

updateapi: $(NENV)
	$(WITH_ENV) python3 project/manage.py updateapi

release: $(NENV)
	$(WITH_ENV) ./bin/release.py

test: testfront testback

