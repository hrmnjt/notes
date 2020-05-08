'''TIL - today I learned ...

Collection of things that I learnt today.

Usage:
    til ls
    til new [--file-type TEXT] filename
    til sync
    til -h | --help
    til --version

Options:
    -h --help       Show this screen
    --version       Show version
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
from sh.contrib import git
from sh import ErrorReturnCode_1

# Click context settings
CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help']
)
# Directory setup for project
PROJECT_DIR = Path.cwd()
TOPICS_DIR = PROJECT_DIR / 'topics'
PUBLIC_TOPICS_DIR = TOPICS_DIR / 'public'
PRIVATE_TOPICS_DIR = TOPICS_DIR / 'private'
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
    '''Initializes the secrets in local toml configuration

    secrets_init creates a new secret configuration for storing passphrase and
    salt used for encryption and pushing to remote git repository. Salt is
    generated using the generate_key function

    Same passphrase and salt are used for decryption of private notes as well
    '''
    passphrase = getpass(prompt='Please enter a passphrase: ')
    salt = Fernet.generate_key().decode()
    secrets = {
        'passphrase': passphrase,
        'salt': salt
    }
    SECRETS.write_text(toml.dumps(secrets))


def generate_key(passphrase, salt):
    '''Generates passphrase and salt

    generate_key creates a key used for encryption and decryption using
    PBKDF2HMAC algorithm
    '''
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


def note_encrypt(key):
    '''Enrypts private notes before sync

    Iterates through the private notes directory and lists all the markdown
    files; and encrypts the markfown file with the key provided as input
    '''
    f = Fernet(key)
    pathlist = PRIVATE_TOPICS_DIR.glob('**/*.md')
    for path in pathlist:
        path_in_str = str(path)

        with open(path_in_str, 'rb') as file:
            file_data = file.read()
        encrypted_data = f.encrypt(file_data)
        with open(path_in_str, 'wb') as file:
            file.write(encrypted_data)

        print('Encrypted {}'. format(path_in_str))


def note_decrypt(key):
    '''Decrypts private notes after sync

    Iterates through the private notes directory and lists all the markdown
    files; and decrypts file with the key provided as input
    '''
    f = Fernet(key)
    pathlist = PRIVATE_TOPICS_DIR.glob('**/*.md')
    for path in pathlist:
        path_in_str = str(path)

        with open(path_in_str, 'rb') as file:
            encrypted_data = file.read()
        decrypted_data = f.decrypt(encrypted_data)
        with open(path_in_str, 'wb') as file:
            file.write(decrypted_data)

        print('Decrypted {}'. format(path_in_str))


def save_on_git_remote():
    '''Saves notes on remote Git repository

    Uses the Git shell commands to add, commit and push the latest
    '''
    git.add(PUBLIC_TOPICS_DIR)
    git.add(PRIVATE_TOPICS_DIR)
    try:
        print('Commiting notes')
        git.commit(m='Saved notes at {}'.format(datetime.now()))
    except ErrorReturnCode_1:
        print('No changes added to commit')
    finally:
        print('Syncing notes to Git remote')
        git.push('origin', 'master')



@click.group(
    context_settings=CONTEXT_SETTINGS,
    help='''TIL - today I learned ...

    Collection of things that I learnt today.
    '''
)
@click.version_option(
    version='1.0.0; made with <3 by @hrmnjt',
    prog_name='TIL CLI'
)
def til_cli():
    pass


@til_cli.command(
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
    print_tree(TOPICS_DIR)


@til_cli.command(
    short_help='Create new note'
)
@click.argument('filename')
@click.option(
    '--file-type',
    default='public',
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
    new_note_dir = TOPICS_DIR / \
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

    print_tree(TOPICS_DIR)


@til_cli.command(
    short_help='Sync your notes with git remote'
)
def sync():
    '''Synchronises the notes to Git remote

    sync command saves notes to Git remote. Private notes are encrypted before
    saving to remote. Keys are saved on local and used for encryption and
    decryption before sync
    '''
    if SECRETS.exists():
        secrets = toml.load(SECRETS)
    else:
        print('No config file exists; running init flow')
        secrets_init()

    secrets = toml.load(SECRETS)
    key = generate_key(secrets.get('passphrase'), secrets.get('salt'))

    note_encrypt(key)
    save_on_git_remote()
    note_decrypt(key)


if __name__ == '__main__':
    til_cli()
