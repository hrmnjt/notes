'''Notes - Note down privately!

Notes is a command line utility created to publically save private notes which
are created as scratch files during developement on a particular project.

Usage:
    notes.py [public | private] <fn>
    notes.py list
    notes.py sync
    notes.py -h | --help
    notes.py -v | --version

Options:
    -h --help     Show this screen
    -v --version  Show version

Work in progress by @hrmnjt
'''

from pathlib import Path


def NotesCommandLineInterface():
    pass


def ListNotes(directory):
    print('\n{}'.format(directory))
    for path in sorted(directory.rglob('*')):
        depth = len(path.relative_to(directory).parts)
        spacer = '|-- ' * depth
        if path.is_file():
            print('{}{}'.format(spacer, path.name))
        else:
            print('{}{}'.format(spacer, path.name))
    print()


def ConfigurationManagement():

    # TODO: add exception handling and bring some grace
    # TODO: DRY
    project_dir = Path.cwd()
    notes_dir = project_dir / 'notes'
    config_file = project_dir / 'config'
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


def CreateNewNotes():

    # TODO: add exception handling and bring some grace
    # TODO: DRY
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
    ListNotes(notes_dir)


def SyncNotes():
    pass


if __name__ == '__main__':

    # TODO: DRY
    # Project structure
    # .                       # project root corresponds to project_dir
    # +-- notes               # notes folder corresponds to notes_dir
    # |   +-- public          # public notes
    # |   +-- private         # private notes
    project_dir = Path.cwd()
    notes_dir = project_dir / 'notes'

    # TODO: move ListNotes to a section as per the CLI logic
    # Default operation as of now is to list notes directory
    ListNotes(notes_dir)
