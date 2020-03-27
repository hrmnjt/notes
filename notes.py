'''Notes - Note down privately!

TODO: add description
Usage:
    notes.py [public | private] <fn>
    notes.py sync
    notes.py -h | --help
    notes.py -v | --version

Options:
    -h --help     Show this screen
    -v --version  Show version

TODO: update description
TODO: improve commentary
'''

from docopt import docopt, DocoptExit
from pathlib import Path


# Utility function - print tree
def tree(directory):
    print('\n{}'.format(directory))
    for path in sorted(directory.rglob('*')):
        depth = len(path.relative_to(directory).parts)
        spacer = '|-- ' * depth
        if path.is_file():
            print('{}{}'.format(spacer, path.name))
        else:
            print('{}{}'.format(spacer, path.name))
    print()


def notes():
    # TODO: replace docopt with argparse
    try:
        docargs = docopt(__doc__, version='Notes 1.0')
    except DocoptExit:
        print('Something went wrong with docopt')
    else:
        arguments = docopt(__doc__, version='Notes 1.0')
        print(docargs)
        print(arguments)
        print(docopt(__doc__, version='Notes 1.0'))

    '''Checking the type of note

    As per the logic gate combinations:
    True | True = True
    True | False = True
    False | True = True
    False | False = False

    Hence, default note type would be private
    '''

    if (arguments['public'] | arguments['private']) == False:
        new_file_type = 'private'
    elif arguments['public'] == True:
        new_file_type = 'public'
    else:
        new_file_type = 'private'


    '''Creating the directory variables that would be used in project

    Structure of project:
    .                       # project_dir
    +-- notes               # notes_dir
    |   +-- public          # new_note_dir if new_file_type = public
    |   +-- private         # new_note_dir if new_file_type = private

    New note would be created with the name as argument inside either public
    or private notes directory
    '''
    project_dir = Path.cwd()
    notes_dir = project_dir / 'notes'
    config_file = project_dir / 'config'
    new_note_dir = notes_dir / '{}'.format(new_file_type)
    new_note_name = notes_dir / '{}'.format(new_file_type) / '{}.md'.format(arguments['<fn>'])

    print('Project directory: {}'.format(project_dir))
    print('Notes directory: {}'.format(notes_dir))
    print('New note directory: {}'.format(new_note_dir))
    print('New note: {}'.format(new_note_name))

    print('Creating a new {} note as {}'.format(new_file_type, new_note_name))

    new_note_name.touch()

    print('Listing the file directory:')
    tree(notes_dir)

    '''Checking the configuration file
    - Creating new if it doesn't exist and expect passphrase from user
    - Read passphrase from the configuration file
    '''
    if config_file.exists():
        print('Config file exist as {}'.format(config_file))
        f = open(config_file, 'r')
        if f.mode == 'r':
            passphrase = f.read()
            print(passphrase)
        f.close()

    else:
        print('Creating config file as {}'.format(config_file))
        passphrase = input('Please enter a passphrase:\n')
        f = open(config_file, 'w')
        if f.mode == 'w':
            f.write(passphrase)
        f.close()


if __name__ == '__main__':
    # notes()

    # TODO: remove redundancy and bring some grace
    project_dir = Path.cwd()
    notes_dir = project_dir / 'notes'
    config_file = project_dir / 'config'
    # new_note_dir = notes_dir / '{}'.format(new_file_type)
    # new_note_name = notes_dir / '{}'.format(new_file_type) / '{}.md'.format(arguments['<fn>'])

    tree(notes_dir)
