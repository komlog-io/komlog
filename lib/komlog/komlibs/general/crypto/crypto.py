'''

crypto.py

This file implement some cryptographic methods used in komlog

'''

import os
from komlog.komfig import logging
from base64 import b64encode, b64decode, urlsafe_b64encode
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def load_public_key(key):
    try:
        pubkey = serialization.load_pem_public_key(
            key,
            backend=default_backend()
        )
        return pubkey if isinstance(pubkey, rsa.RSAPublicKey) else None
    except Exception:
        return None

def load_private_key(key):
    try:
        privkey = serialization.load_pem_private_key(
            key,
            password=None,
            backend=default_backend()
        )
        return privkey if isinstance(privkey, rsa.RSAPrivateKey) else None
    except Exception as e:
        return None

def generate_rsa_key(key_size=4096):
    try:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend()
        )
        return private_key
    except Exception:
        return None

def serialize_private_key(key):
    try:
        pem = key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        return pem
    except Exception:
        return None

def serialize_public_key(key):
    try:
        pem = key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem
    except Exception:
        return None

def decrypt(key, ciphertext):
    try:
        privkey = load_private_key(key)
        plaintext = privkey.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA1()),
                algorithm=hashes.SHA1(),
                label=None
            )
        )
        return plaintext
    except Exception:
        return None

def encrypt(key, plaintext):
    try:
        pubkey = load_public_key(key)
        ciphertext = pubkey.encrypt(plaintext=plaintext,
            padding=padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA1()),
                algorithm=hashes.SHA1(),
                label=None
            )
        )
        return ciphertext
    except Exception:
        return None

def get_hash(message):
    try:
        digest = hashes.Hash(hashes.Whirlpool(), backend=default_backend())
        for i in range(0,30):
            digest.update(message)
        return digest.finalize()
    except Exception:
        return None

def get_hashed_password(password, salt):
    try:
        password = password.encode('utf-8')
        kdf = PBKDF2HMAC(
            algorithm=hashes.Whirlpool(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(password)
    except Exception:
        return None

def verify_password(password, hashed, salt):
    try:
        password = password.encode('utf-8')
        kdf = PBKDF2HMAC(
            algorithm=hashes.Whirlpool(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        kdf.verify(password, hashed)
        return True
    except Exception:
        return False

def get_random_sequence(size):
    try:
        return os.urandom(size)
    except Exception:
        return None

def get_random_string(size):
    try:
        return urlsafe_b64encode(os.urandom(size))[:size].decode('utf-8')
    except Exception:
        return None

def sign_message(key, message):
    try:
        privkey = load_private_key(key)
        signer = privkey.signer(
            padding.PSS(
                mgf=padding.MGF1(hashes.Whirlpool()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.Whirlpool()
        )
        signer.update(message)
        return signer.finalize()
    except Exception as e:
        return None

def verify_signature(key, message, signature):
    try:
        pubkey = load_public_key(key)
        verifier = pubkey.verifier(
            signature,
            padding.PSS(
                mgf=padding.MGF1(hashes.Whirlpool()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.Whirlpool()
        )
        verifier.update(message)
        verifier.verify()
        return True
    except Exception:
        return False

