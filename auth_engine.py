from cryptography.fernet import Fernet

class FortressSecurity:
    @staticmethod
    def get_cipher(key):
        return Fernet(key)

    @staticmethod
    def encrypt_data(cipher, data):
        return cipher.encrypt(data)

    @staticmethod
    def decrypt_data(cipher, encrypted_data):
        return cipher.decrypt(encrypted_data)
        
