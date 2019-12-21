# Makefile

.PHONY: setupnotes
setupnotes:
	rm -rf pyenv
	mkdir -p pyenv
	python3 -m venv ./pyenv
	pip install -r requirements.txt


.PHONY: writenotes
writenotes:
	git pull origin master
	python decryptor.py


.PHONY: savenotes
savenotes:
	python encryptor.py
	git add .
	git commit -m "Saving notes: `date +'%Y-%m-%d %H:%M:%S'`"
	git push origin master
