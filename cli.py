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
import textwrap
# External imports
import click
import toml
import markdown2
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
# File path setup for project
PROJECT_DIR = Path.cwd()
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


def util_generate_key(passphrase, salt):
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


def util_fetch_metadata(til_name):
    '''Fetches and returns til metadata
    '''
    with open(til_name, 'r') as f:
        text = f.read()

    md = markdown2.markdown(text, extras=["metadata"])
    return md.metadata


def util_create_new_til(til_location, til_type):
    '''Creates new til

    Takes parameters location and note_name and creates new til note of
    the type provided
    '''
    til_metadata = '''\
    ---
    type: {}
    date: {}
    ---

    '''.format(til_type, datetime.today().strftime('%Y%m%d'))

    # Create a new til
    til_location.touch()

    # Write the metadata for the til
    til_location.write_text(textwrap.dedent(til_metadata))

    print('A new TIL is created: {}'.format(til_location))
    return


def util_encrypt(key):
    '''Enrypts private TIL topics before sync

    Iterates through the private topics directory and lists all the markdown
    files; and encrypts only private topics with the key provided as input
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


def util_decrypt(key):
    '''Decrypts private TIL topics after sync

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


def util_save_on_git_remote():
    '''Saves all topics on remote Git repository

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



@click.group(context_settings=CONTEXT_SETTINGS,
    help='''TIL - today I learned ...
    ''',
)
@click.version_option(
    version='1.0.0; made with <3 by @hrmnjt',
    prog_name='TIL CLI'
)
def til_cli():
    pass


# @til_cli.command(short_help='List all public and private notes')
# def ls():
#     '''List all public and private notes
#     '''
#     print_tree(TOPICS_DIR)


@til_cli.command(short_help='Create new note')
@click.argument('filename')
@click.option('--topic', default='misc', help='TIL category topic')
@click.option('--type', default='public',
    help='Either public or private learning topic',
)
def new(**kwargs):
    '''Create a new TIL note
    '''
    topic = kwargs['topic']
    til_type = kwargs['type']
    til_name = kwargs['filename']

    topic_dir = PROJECT_DIR / '{}'.format(topic)
    new_til_location = topic_dir / '{}'.format(til_name)

    if topic_dir.exists():
        if new_til_location.exists():
            print('A {} TIL already exists in {} topic'.format(
                til_name, topic
            ))
        else:
            util_create_new_til(new_til_location, til_type)
    else:
        topic_dir.mkdir(parents=True, exist_ok=True)
        util_create_new_til(new_til_location, til_type)

    return



@til_cli.command(short_help='Sync and save your TIL topics')
def sync(**kwargs):
    '''Synchronises and saves the TIL topics to remote Git repository
    '''
    if SECRETS.exists():
        secrets = toml.load(SECRETS)
    else:
        print('No config file exists; running init flow')
        passphrase = getpass(prompt='Please enter a passphrase: ')
        salt = Fernet.generate_key().decode()
        secrets = {
            'passphrase': passphrase,
            'salt': salt
        }
        SECRETS.write_text(toml.dumps(secrets))

    secrets = toml.load(SECRETS)
    key = util_generate_key(secrets.get('passphrase'), secrets.get('salt'))

    for file in PROJECT_DIR.rglob('*.md'):
        metadata = util_fetch_metadata(file)
        print(metadata['type'])

    # util_encrypt(key)
    # util_save_on_git_remote()
    # util_decrypt(key)


if __name__ == '__main__':
    til_cli()
