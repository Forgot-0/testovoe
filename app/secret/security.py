import hashlib
from cryptography.fernet import Fernet

from app.secret.config import secret_config

cipher = Fernet(secret_config.SECRET_KEY.encode())

def hash_key(key: str) -> str:
    return hashlib.sha256(key.encode()).hexdigest()

def hash_passphrase(key: str) -> str:
    return hashlib.sha256(key.encode()).hexdigest()

def encrypt_data(data: str) -> str:
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data: str) -> str:
    return cipher.decrypt(encrypted_data.encode()).decode()
