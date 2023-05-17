PIP=pip
PYTHON=python
SNAPSHOT_LIMIT=3
DB_NAME=db.sqlite3
MAIN_REPO=/opt/danix/
ROOT_FS=danixfs.tar.gz
DANIX_PATH=$(shell pwd)
REPO_NAME=https://silvavinicius.com.br/danixfs/

config:

	@mkdir $(MAIN_REPO) > /dev/null 2>&1
	@mkdir $(MAIN_REPO)/.snapshot > /dev/null 2>&1

	@echo REPO_NAME=$(REPO_NAME)      >> $(DANIX_PATH)/.env
	@echo MAIN_REPO=$(MAIN_REPO)      >> $(DANIX_PATH)/.env
	@echo ROOT_FS=$(ROOT_FS)        >> $(DANIX_PATH)/.env
	@echo SNAPSHOT_LIMIT=$(SNAPSHOT_LIMIT) >> $(DANIX_PATH)/.env
	
	@touch $(DANIX_PATH)/db/$(DB_NAME) > /dev/null 2>&1
	@$(PIP) install -r $(DANIX_PATH)/requirements.txt > /dev/null 2>&1

	$(PYTHON) $(DANIX_PATH)/manage.py migrate

	@alias sudo='sudo '
	@alias danix="python main.py"

	@echo Danix configured successfully! Please run danix -h or python main.py -h

clean:

	@rm -r $(MAIN_REPO) > /dev/null 2>&1
	@rm $(DANIX_PATH)/db/$(DB_NAME) > /dev/null 2>&1
	@rm $(DANIX_PATH)/.env
	@echo Danix cleaned!