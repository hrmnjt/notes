# Makefile
# https://www.gnu.org/software/make/manual/make.html

SHELL = /bin/bash

.PHONY: clean
clean:
	rm -rf ./notes/public/*
	rm -rf ./notes/private/*
	rm -rf ./config

.PHONY: cleanpy
cleanpy:
	rm -rf pyenv
	python3 -m venv pyenv
