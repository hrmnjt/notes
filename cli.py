'''TIL command line interface (CLI)
'''

# External packages
import click

# Source code
from til import TodayILearned

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS, help='TIL - today I learned ...')
@click.version_option(version='1.0.0; with <3 by @hrmnjt', prog_name='TIL CLI')
def til_cli():
    pass


@til_cli.command(short_help='Create new note')
@click.argument('filename')
@click.option('--topic', default='misc', help='TIL category topic')
@click.option('--type', default='public', help='public or private')
def new(**kwargs):
    til_name = kwargs['filename']
    til_topic = kwargs['topic']
    til_type = kwargs['type']

    til = TodayILearned()
    til.create(til_topic, til_name, til_type)


@til_cli.command(short_help='Sync and save your TIL topics')
def sync():
    print('Syncing shit....')


if __name__ == '__main__':
    til_cli()
