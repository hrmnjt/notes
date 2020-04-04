'''Notes - Note down privately!

Notes is a command line utility created to publically save private notes which
are created as scratch files during developement on a particular project.

Usage:
    notes.py ls
    notes.py new [--file-type TEXT] filename
    notes.py sync
    notes.py -h | --help
    notes.py --version

Options:
    -h --help       Show this screen
    --version       Show version

Work in progress by @hrmnjt
'''

# Internal imports
import base64
from datetime import datetime
from getpass import getpass
from os import urandom
from pathlib import Path
# External imports
import click
import toml
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Click context settings
CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help']
)
# Directory setup for project
PROJECT_DIR = Path.cwd()
NOTES_DIR = PROJECT_DIR / 'notes'
PRIVATE_NOTES_DIR = PROJECT_DIR / 'notes' / 'private'
SECRETS = PROJECT_DIR / 'secrets.toml'


def print_tree(directory):
    '''Prints the directory contents

    print_tree is a utility function which prints the directory structure on
    command line similar to UNIX tree binary but with very basic functionality
    Link to (actual) tree - https://linux.die.net/man/1/tree

    This utility is used to print the notes directory structure when doing
    operations with new or existing notes
    '''
    print('\n{}'.format(directory))
    for path in sorted(directory.rglob('*')):
        depth = len(path.relative_to(directory).parts)
        spacer = '|-- ' * depth
        if path.is_file():
            print('{}{}'.format(spacer, path.name))
        else:
            print('{}{}'.format(spacer, path.name))
    print()


def secrets_init():
    passphrase = getpass(prompt='Please enter a passphrase: ')
    salt = Fernet.generate_key().decode()
    print('salt {}'.format(salt))
    secrets = {
        'passphrase': passphrase,
        'salt': salt
    }
    SECRETS.write_text(toml.dumps(secrets))


def generate_key(passphrase, salt):
    password = passphrase.encode()
    salt = salt.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return(key)

# def note_encrypt(note, password):
def note_encrypt(key):
    print(key)


def note_decrypt(note):
    pass


def push_to_git():
    pass


def pull_from_git():
    pass


@click.group(
    context_settings=CONTEXT_SETTINGS,
    help='''Notes - Note down privately!

    Notes is a command line utility created to publically save private notes
    which are created as scratch files during developement on an idea/thought.

    Work in progress by @hrmnjt
    '''
)
@click.version_option(version='0.1.0; right now in making')
def notes_cli():
    pass


@notes_cli.command(
    short_help='List all public and private notes'
)
def ls():
    '''List all public and private notes

    Command line option `ls` is used to list the notes existing in NOTES_DIR.
    It used the common utility `print_tree` to print the list.

    \b
    Outer project structure:
    .                   # project root corresponds to project_dir
    +-- notes           # notes folder corresponds to notes_dir
    |   +-- public      # public notes
    |   +-- private     # private notes
    '''
    print_tree(NOTES_DIR)


@notes_cli.command(
    short_help='Create new note'
)
@click.argument('filename')
@click.option(
    '--file-type',
    default='private',
    help='Either public or private',
)
def new(**kwargs):
    '''Creates a new note if it doesn't exist

    new command creates public or private note based on the `--file-type`
    option and expects FILENAME to be provided as the argument.

    New note name is decided based on the FILENAME variable irrespective of
    it being public or private
    '''

    date_today = datetime.today().strftime('%Y%m%d')
    new_note_type = kwargs['file_type']
    new_note_dir = NOTES_DIR / \
        '{}'.format(new_note_type) / \
        '{}'.format(kwargs['filename'])
    new_note_name = new_note_dir / \
        '{}.md'.format(date_today)

    if new_note_dir.exists():
        if new_note_name.exists():
            print('A {} note already exists as {}'. format(
                new_note_type, new_note_name))
        else:
            new_note_name.touch()
            print('Created a new {} as {}'.format(new_note_type, new_note_name))
    else:
        new_note_dir.mkdir(parents=True, exist_ok=True)
        new_note_name.touch()
        print('Created a new {} as {}'.format(new_note_type, new_note_name))

    print_tree(NOTES_DIR)


@notes_cli.command()
def sync():

    if SECRETS.exists():
        secrets = toml.load(SECRETS)
    else:
        print('No config file exists; running init flow')
        secrets_init()

    secrets = toml.load(SECRETS)
    key = generate_key(secrets.get('passphrase'), secrets.get('salt'))
    note_encrypt(key)


if __name__ == '__main__':
    notes_cli()
