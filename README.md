# Notes

Git backed private encrypted note-taking. Awesomeness coming soon

## Usage

Prerequisites:
- Git
- Python3 and [`venv`](https://docs.python.org/3/library/venv.html#module-venv) package

Clone this repository (first time only) and create virtual environment
```bash
git clone git@github.com:hrmnjt/notes.git notes
cd notes
python3 -m venv ./pyenv
```

Activating virtual environment
```bash
source ./pyenv/bin/activate
```

Generating fernet key (first time only)
```python
python generator.py
```

Pulling and decrypting notes
```python
git pull origin master
python decryptor.py
```

Pushing post making changes
```python
python encryptor.py
git add .
git commit -m "Updating notes - `date +'%Y-%m-%d %H:%M:%S'`"
git push origin master
```

## TODO
- [ ] Add makefile and improve Dx
- [ ] CLI and arguments for the notes
- [ ] Abstract the codebase and create module
- [ ] Add different encryption formats
- [ ] Add different key options
- [ ] ...
