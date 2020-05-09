'''TIL - today I learned ...
'''
import base64
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


    def generate_key(self, passphrase, salt):
        password = passphrase.encode()
        salt = salt.encode()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return(key)


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
        f = Fernet(self.generate_key(secrets.get('passphrase'), secrets.get('salt')))

        PRIVATE_TIL = self.PROJECT_DIR / 'private'

        # for path in PRIVATE_TIL.glob('**/*.md'):
        #     path_in_str = str(path)

        #     with open(path_in_str, 'rb') as filename:
        #         file_data = filename.read()
        #     encrypted_data = f.encrypt(file_data)
        #     with open(path_in_str, 'wb') as filename:
        #         filename.write(encrypted_data)

        #     print('Encrypted {}'. format(path_in_str))

        print("Saving on git remote")

        for path in PRIVATE_TIL.glob('**/*.md'):
            path_in_str = str(path)

            with open(path_in_str, 'rb') as file:
                encrypted_data = file.read()
            decrypted_data = f.decrypt(encrypted_data)
            with open(path_in_str, 'wb') as file:
                file.write(decrypted_data)

            print('Decrypted {}'. format(path_in_str))

        return