from pathlib import Path
from cryptography.fernet import Fernet

def load_key():
    """
    Loads the key from the current directory named `key.key`
    """
    return open("key.key", "rb").read()


def encrypt():
    """
    Given a filename (str) and key (bytes), it encrypts the file and write it
    """
    f = Fernet(load_key())

    pathlist = Path('private').glob('**/*.md')
    for path in pathlist:
        # because path is object not string
        path_in_str = str(path)

        with open(path_in_str, "rb") as file:
            # read all file data
            file_data = file.read()
        # encrypt data
        encrypted_data = f.encrypt(file_data)
        # write the encrypted file
        with open(path_in_str, "wb") as file:
            file.write(encrypted_data)


if __name__ == "__main__":
    encrypt()
