from pathlib import Path
from cryptography.fernet import Fernet

def load_key():
    """
    Loads the key from the current directory named `key.key`
    """
    return open("key.key", "rb").read()


def decrypt():
    """
    Given a filename (str) and key (bytes), it decrypts the file and write it
    """
    f = Fernet(load_key())

    pathlist = Path('private').glob('**/*.md')
    for path in pathlist:
        # because path is object not string
        path_in_str = str(path)

        with open(path_in_str, "rb") as file:
            # read the encrypted data
            encrypted_data = file.read()
        # decrypt data
        decrypted_data = f.decrypt(encrypted_data)
        # write the original file
        with open(path_in_str, "wb") as file:
            file.write(decrypted_data)


if __name__ == "__main__":
    decrypt()
