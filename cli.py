'''TIL - today I learned ...

Collection of things that I learned, which could help if documented but are
not worth a blog

'''

import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS, help='TIL - today I learned ...')
@click.version_option(version='1.0.0; with <3 by @hrmnjt', prog_name='TIL CLI')
def til_cli():
    pass


@til_cli.command(short_help='List all public and private notes')
def ls():
    print('Listing shit....')


@til_cli.command(short_help='Create new note')
@click.argument('filename')
@click.option('--topic', default='misc', help='TIL category topic')
@click.option('--type', default='public', help='public or private')
def new(**kwargs):
    print('Creating new shit....')


@til_cli.command(short_help='Sync and save your TIL topics')
def sync(**kwargs):
    print('Syncing shit....')



if __name__ == '__main__':
    til_cli()
