# import hashlib
# from cryptography.fernet import Fernet
# import os


# def hash_key(key: str) -> str:
#     return hashlib.sha256(key.encode()).hexdigest()

# def hash_passphrase(key: str) -> str:
#     return hashlib.sha256(key.encode()).hexdigest()

# def encrypt_data(data: str) -> str:
#     fernet = get_fernet()
#     return fernet.encrypt(data.encode()).decode()

# def decrypt_data(encrypted_data: str) -> str:
#     fernet = get_fernet()
#     return fernet.decrypt(encrypted_data.encode()).decode()

def hash_key(key: str) -> str:
    return "hash" + key

def hash_passphrase(passphrase: str) -> str:
    return "hash" + passphrase

def encrypt_data(data: str) -> str:
    return "encrypted" + data

def decrypt_data(encrypted_data: str) -> str:
    return encrypted_data.replace("encrypted", "")