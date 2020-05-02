from setuptools import setup, find_packages

setup(
    name='notes',
    version='0.1',
    py_modules=['notes.py'],
    install_requires=[
        'click',
        'cryptography',
        'sh',
        'toml',
    ],
    entry_points={
        'console_scripts': [
            'notes = notes:notes_cli',
        ]
    }
)
