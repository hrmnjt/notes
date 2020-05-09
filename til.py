'''TIL - today I learned ...
'''

from getpass import getpass
from pathlib import Path
import toml
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class TodayILearned():

    def __init__(self):
        self.PROJECT_DIR = Path.cwd()
        self.SECRETS = self.PROJECT_DIR / 'secrets.toml'
        super().__init__()


    def create(self, til_topic, til_name, til_type):
        if til_type == 'private':
            TOPIC_DIR = self.PROJECT_DIR / 'private'
        else:
            TOPIC_DIR = self.PROJECT_DIR / '{}'.format(til_topic)

        if not TOPIC_DIR.exists():
            TOPIC_DIR.mkdir(parents=True, exist_ok=True)

        TIL_FILE = TOPIC_DIR / '{}'.format(til_name)

        if TIL_FILE.exists():
            print('{} exists'.format(TIL_FILE))
        else:
            TIL_FILE.touch()
            print('Created {}'.format(TIL_FILE))

        return


    def save(self):
        if self.SECRETS.exists():
            secrets = toml.load(self.SECRETS)
        else:
            print('No config file exists; running init flow')
            passphrase = getpass(prompt='Please enter a passphrase: ')
            salt = Fernet.generate_key().decode()
            secrets = {
                'passphrase': passphrase,
                'salt': salt
            }
            self.SECRETS.write_text(toml.dumps(secrets))
