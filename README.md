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
pip install -r requirements.txt
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
- [ ] Tidy up
- [ ] Docs
- [ ] Improve the project structure. Fixate on design decisions
- [ ] Add CLI tool and args for usage
- [ ] Requirement management
- [ ] Features
    - [ ] Add options to CRUD notes
    - [ ] Add different key options
    - [ ] Add different encryption formats
    - [ ] Find notes
    - [ ] Interactive mode
    - [ ] Custom backup providers - git based
- [ ] Improve code convention and style
    - [ ] Add comments
    - [ ] Unit tests
    - [ ] DRY
    - [ ] Contribution guidelines
- [ ] Packaging
