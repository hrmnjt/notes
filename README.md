# Notes

Note down privately!

## Installation

Easiest approach (at this time) is to follow a 3 step approach:

#### Step 1 - Fork and cleanup

[Fork this repository](https://github.com/hrmnjt/notes) and clone your fork to 
local.

Run a cleanup of my notes (if existing)
```bash
rm -rf ./notes/public/*
rm -rf ./notes/private/*
```

#### Step 2 - Create python virtual environment

```bash
# Create a new virtualenv
python3 -m venv /path/to/new/virtual/environment
```

#### Step 3 - Install using setuptools

```bash
# Activating new virtualenv
source /path/to/new/virtual/environment/bin/activate

# Installation
pip install --editable .

# Interact with notes CLI
notes
# Notes is a command line utility created to publicly save private notes which
# are created as scratch files during development on a particular project.

# Usage:
#     notes ls
#     notes new [--file-type TEXT] filename
#     notes sync
#     notes -h | --help
#     notes --version

# Options:
#     -h --help       Show this screen
#     --version       Show version
```

## Usage

Print usage or help text
```bash
notes
```

Listing existing notes
```bash
notes ls
```

Creating a new private note - `new-priv-note`
```bash
notes new newnote1
# OR
notes new --file-type private new-priv-note
```

Creating a new public note - `new-pub-note`
```bash
notes new --file-type public new-pub-note
```

Syncing notes or create a checkpoint
```bash
notes sync
```

## Motivation

Notes is a command line utility created to **publicly saved private notes**. 
Notes was created because I wanted to:
- write private notes: generally unfinished ideas or scratch file during 
development
- free hosting yet secure: wanted to store my notes on a server which I don't 
own but is publicly available for me sync between devices
- minimal and no-lock: functionality is complete for fast note-taking which 
could be moved to another better solution at any day. No lock in!

Notes is very minimal (including the documentation) and I would intend to keep 
it minimal.

```bash
scc notes.py setup.py secrets.toml .editorconfig .gitignore requirements.txt README.md
# ───────────────────────────────────────────────────────────────────────────────
# Language                 Files     Lines   Blanks  Comments     Code Complexity
# ───────────────────────────────────────────────────────────────────────────────
# Python                       2       279       24        58      197         13
# Markdown                     1       147       35         0      112          0
# Plain Text                   1         7        0         0        7          0
# TOML                         1         2        0         0        2          0
# gitignore                    1        13        4         4        5          0
# ───────────────────────────────────────────────────────────────────────────────
# Total                        6       448       63        62      323         13
# ───────────────────────────────────────────────────────────────────────────────
# Estimated Cost to Develop $8,246
# Estimated Schedule Effort 2.477815 months
# Estimated People Required 0.394225
# ───────────────────────────────────────────────────────────────────────────────
```
_Output using [scc](https://github.com/boyter/scc)_

I would like to thank creator and contributors of `python3`, `pathlib`, `toml`, 
`cryptography`, `sh` and `click`

## TODO

- [ ] Make notes faster
- [ ] Remove the hard-coded logic for git sync

## Troubleshooting

#### How to fork and clone

[Github help to fork](https://help.github.com/en/github/getting-started-with-github/fork-a-repo)  
[Github help to clone](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository)

#### Git sync doesn't work

Please ensure the remote name is `origin` and branch name is `master`
```bash
git remote -v
# origin  git@github.com:<your_name>/notes.git (fetch)
# origin  git@github.com:<your_name>/notes.git (push)

git branch -v
# * master                   44e48ce Updating markdown details
# ...
```

#### Don't want setuptools integration

If you intend to not use `setuptools` integration, please use CLI using 
`python notes.py` instead of `notes`.
