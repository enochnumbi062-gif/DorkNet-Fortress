import secrets
import string
import pyotp
from cryptography.fernet import Fernet

class FortressSecurity:
    @staticmethod
    def generate_secure_password(length=24):
        """Génère un mot de passe inviolable."""
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    @staticmethod
    def get_cipher(key):
        """Initialise le moteur de chiffrement."""
        return Fernet(key)

    @staticmethod
    def encrypt_data(cipher, data):
        """Chiffre les données binaires."""
        return cipher.encrypt(data)
      
