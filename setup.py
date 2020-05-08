from setuptools import setup

setup(
    name='cli',
    version='1.0',
    py_modules=['cli.py'],
    install_requires=[
        'pip',
        'click',
        'cryptography',
        'sh',
        'toml',
    ],
    entry_points={
        'console_scripts': [
            'cloi = cli.__main__:til_cli',
        ]
    }
)
