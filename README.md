# Today I leaned ...

## Categories

- [Category name](#category-name)

---

## Category name

- [Placeholder TIL](#placeholder-link)

---

## Installation

I've create a CLI for my convenience and it can be setup using the below steps.

```bash
# Create a new virtualenv
python3 -m venv /path/to/new/virtual/environment

# Activating new virtualenv
source /path/to/new/virtual/environment/bin/activate

# Installation
pip install --editable .

# Interact with notes CLI
cli --version
# TIL CLI, version 1.0.0; with <3 by @hrmnjt
```

## Usage

```bash
cli
# Usage: cli [OPTIONS] COMMAND [ARGS]...

#   TIL - today I learned ...

# Options:
#   --version   Show the version and exit.
#   -h, --help  Show this message and exit.

# Commands:
#   new   Create new note
#   sync  Sync and save your TIL topics

cli new --help
# Usage: cli new [OPTIONS] FILENAME

# Options:
#   --topic TEXT  TIL category topic
#   --type TEXT   public or private
#   -h, --help    Show this message and exit

cli sync --help
# Usage: cli sync [OPTIONS]

# Options:
#   -h, --help  Show this message and exit.
```


## Thanks

#### Need for this project

TIL CLI is a command line utility created to **publicly saved private notes**.
I created it to:
- write private topics: generally unfinished ideas or scratch file during
development which generally don't deserve a blog
- free hosting yet secure: wanted to store my notes on a server which I don't
own but is publicly available for me sync between devices
- minimal and no-lock: functionality is complete for fast note-taking which
could be moved to another better solution at any day. No lock in!

#### Ideas

This project copies ideas from [pimterry Notes](https://github.com/pimterry/notes)
and [jbranchaud til](https://github.com/jbranchaud/til) with few details added
on top to save private notes

#### Libraries
Lastly, thanks to people who created and maintain `click`, `cryptography`,
`toml` and `sh` packages. Without those this program was not possible.
