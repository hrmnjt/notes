'''TIL CLI setup details
'''

from setuptools import setup

setup(
    name='til',
    version='1.0',
    install_requires=[
        'click',
    ],
    entry_points={'console_scripts': ['cli = cli:til_cli']}
)
