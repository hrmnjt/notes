"""Notes - Note down privately!

Usage:
    notes.py [public | private] <fn>
    notes.py sync
    notes.py -h | --help
    notes.py -v | --version

Options:
    -h --help     Show this screen
    -v --version  Show version
"""

from docopt import docopt
from pathlib import Path

def tree(directory):
    print(f'{directory}')
    for path in sorted(directory.rglob('*')):
        depth = len(path.relative_to(directory).parts)
        spacer = '|--' * depth
        if path.is_file():
            print(f'{spacer}{path.name}')
        else:
            print(f'{spacer}{path.name}')


def notes():
    arguments = docopt(__doc__, version='Notes 1.0')
    print(arguments)

    ''' Checking the type of note

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
    config_file = notes_dir / 'config.yml'
    new_note_dir = notes_dir / '{}'.format(new_file_type)
    new_note_name = notes_dir / '{}'.format(new_file_type) / '{}.md'.format(arguments['<fn>'])

    print("Project directory: {}".format(project_dir))
    print("Notes directory: {}".format(notes_dir))
    print("New note directory: {}".format(new_note_dir))
    print("New note: {}".format(new_note_name))

    print("Creating a new {} note as {}".format(new_file_type, new_note_name))

    new_note_name.touch()

    print("Listing the file directory:")
    tree(notes_dir)

    if config_file.exists():
        print("Config file exist as {}".format(config_file))
    else:
        print("Creating config file as {}".format(config_file))
        config_file.touch()


if __name__ == "__main__":
    notes()
