'''TIL - today I learned ...
'''
import base64
import datetime
from getpass import getpass
from pathlib import Path
import toml
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from sh.contrib import git
from sh import ErrorReturnCode_1

class TodayILearned():

    def __init__(self):
        self.PROJECT_DIR = Path.cwd()
        self.SECRETS = self.PROJECT_DIR / 'secrets.toml'
        super().__init__()


    def create(self, til_topic, til_name, til_type):
        # Assign the topic directory
        if til_type == 'private':
            TOPIC_DIR = self.PROJECT_DIR / 'private'
        else:
            TOPIC_DIR = self.PROJECT_DIR / '{}'.format(til_topic)
        # Create directory if doesn't exist
        if not TOPIC_DIR.exists():
            TOPIC_DIR.mkdir(parents=True, exist_ok=True)
        # Create TIL file
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

        secrets = toml.load(self.SECRETS)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=secrets.get('salt').encode(),
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(
            kdf.derive(secrets.get('passphrase').encode()))
        f = Fernet(key)

        PRIVATE_TIL_DIR = self.PROJECT_DIR / 'private'

        for path in PRIVATE_TIL_DIR.glob('**/*.md'):
            path_in_str = str(path)

            with open(path_in_str, 'rb') as filename:
                file_data = filename.read()
            encrypted_data = f.encrypt(file_data)
            with open(path_in_str, 'wb') as filename:
                filename.write(encrypted_data)

            print('Encrypted {}'. format(path_in_str))

        git.add('--all')
        try:
            git.commit(m='Saved encrypted TILs at {}'.format(datetime.now()))
        except ErrorReturnCode_1:
            print('No changes added to commit')
        finally:
            print('Syncing notes to Git remote')
            # git.push('origin', 'master')

        for path in PRIVATE_TIL_DIR.glob('**/*.md'):
            path_in_str = str(path)

            with open(path_in_str, 'rb') as file:
                encrypted_data = file.read()
            decrypted_data = f.decrypt(encrypted_data)
            with open(path_in_str, 'wb') as file:
                file.write(decrypted_data)

            print('Decrypted {}'. format(path_in_str))

        return
