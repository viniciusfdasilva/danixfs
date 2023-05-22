PIP=pip
PYTHON=python
SNAPSHOT_LIMIT=3
DB_NAME=db.sqlite3
MAIN_REPO=/opt/danix/
ROOT_FS=danixfs.tar.gz
DANIX_PATH=/usr/share/danix
REPO_NAME=https://silvavinicius.com.br/danixfs/

ENV_GENERIC_ERROR=Error!
ENV_NOT_FOUND=Environment does not exist!
ENV_REMOVED=Environment removed successfully!
ENV_STARTED=Environment started successfully!
ENV_STOPPED=Environment stopped successfully!
ENV_STOPPED_ERROR=Error! The environment is stopped!
ENV_PATTERN_ERROR=Environment name pattern contains in multiples environments


install:

ifneq ($(shell id -u), 0)

	@echo "You are not root, run this target as root please"
	@exit 0

else
	

	@mkdir   $(DANIX_PATH) 2>&1
	@cp -r * $(DANIX_PATH) 2>&1

	@mkdir $(MAIN_REPO) > /dev/null 2>&1
	@mkdir $(MAIN_REPO)/.snapshots > /dev/null 2>&1

	@touch $(DANIX_PATH)/.env 2>&1

	@echo REPO_NAME=$(REPO_NAME)      >> $(DANIX_PATH)/.env
	@echo MAIN_REPO=$(MAIN_REPO)      >> $(DANIX_PATH)/.env
	@echo ROOT_FS=$(ROOT_FS)          >> $(DANIX_PATH)/.env
	@echo SNAPSHOT_LIMIT=$(SNAPSHOT_LIMIT) >> $(DANIX_PATH)/.env
	@echo ENV_NOT_FOUND=$(ENV_NOT_FOUND) >> $(DANIX_PATH)/.env
	@echo ENV_GENERIC_ERROR=$(ENV_GENERIC_ERROR) >> $(DANIX_PATH)/.env
	@echo ENV_STOPPED_ERROR=$(ENV_STOPPED_ERROR) >> $(DANIX_PATH)/.env
	@echo ENV_PATTERN_ERROR=$(ENV_PATTERN_ERROR) >> $(DANIX_PATH)/.env
	@echo ENV_REMOVED=$(ENV_REMOVED) >> $(DANIX_PATH)/.env
	@echo ENV_STARTED=$(ENV_STARTED) >> $(DANIX_PATH)/.env
	@echo ENV_STOPPED=$(ENV_STOPPED) >> $(DANIX_PATH)/.env
	
	@touch $(DANIX_PATH)/db/$(DB_NAME) > /dev/null 2>&1
	@$(PIP) install -r $(DANIX_PATH)/requirements.txt > /dev/null 2>&1

	@$(PYTHON) $(DANIX_PATH)/manage.py migrate

	@echo "alias danix='sudo python $(DANIX_PATH)/main.py'" >> ~/.bashrc
	@echo "alias danixconfig='make -C $(DANIX_PATH) config'" >> ~/.bashrc
	@echo "alias danixclean='make -C $(DANIX_PATH) clean'" >> ~/.bashrc
	@echo "Installation successfully!!!"
endif
	


config:

	@mkdir $(MAIN_REPO) > /dev/null 2>&1
	@mkdir $(MAIN_REPO)/.snapshots > /dev/null 2>&1

	@echo touch $(DANIX_PATH)/.env

	@echo REPO_NAME=$(REPO_NAME)      >> $(DANIX_PATH)/.env
	@echo MAIN_REPO=$(MAIN_REPO)      >> $(DANIX_PATH)/.env
	@echo ROOT_FS=$(ROOT_FS)        >> $(DANIX_PATH)/.env
	@echo SNAPSHOT_LIMIT=$(SNAPSHOT_LIMIT) >> $(DANIX_PATH)/.env
	@echo ENV_NOT_FOUND=$(ENV_NOT_FOUND) >> $(DANIX_PATH)/.env
	@echo ENV_GENERIC_ERROR=$(ENV_GENERIC_ERROR) >> $(DANIX_PATH)/.env
	@echo ENV_STOPPED_ERROR=$(ENV_STOPPED_ERROR) >> $(DANIX_PATH)/.env
	@echo ENV_PATTERN_ERROR=$(ENV_PATTERN_ERROR) >> $(DANIX_PATH)/.env
	@echo ENV_REMOVED=$(ENV_REMOVED) >> $(DANIX_PATH)/.env
	@echo ENV_STARTED=$(ENV_STARTED) >> $(DANIX_PATH)/.env
	@echo ENV_STOPPED=$(ENV_STOPPED) >> $(DANIX_PATH)/.env
	
	@touch $(DANIX_PATH)/db/$(DB_NAME) > /dev/null 2>&1
	@$(PIP) install -r $(DANIX_PATH)/requirements.txt > /dev/null 2>&1

	@$(PYTHON) $(DANIX_PATH)/manage.py migrate

aliases:
	@alias sudo='sudo '
	@alias danix="python main.py"
	@echo  Please run danix -h or python main.py -h

clean:

	@rm -r $(MAIN_REPO) > /dev/null 2>&1
	@rm $(DANIX_PATH) > /dev/null 2>&1
	@echo Danix cleaned!