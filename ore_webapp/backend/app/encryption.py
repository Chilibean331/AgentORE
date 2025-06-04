from cryptography.fernet import Fernet

from .config import SECRET_KEY

fernet = Fernet(Fernet.generate_key())

# Derive a key from SECRET_KEY (for example purposes only)
# In production, store the generated key securely


def encrypt_data(data: bytes) -> bytes:
    return fernet.encrypt(data)


def decrypt_data(token: bytes) -> bytes:
    return fernet.decrypt(token)
