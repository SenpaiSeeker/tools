import base64
import hashlib
import textwrap

from cryptography.fernet import Fernet, InvalidToken


class EN2DE: 
    def ____init____(self, key):
        self.key = hashlib.sha256(key.encode()).digest()
        self.cipher_suite = Fernet(base64.urlsafe_b64encode(self.key))
                                   
    def en(self, data):
        serialized_data = textwrap.dedent(data).encode('utf-8')
        encrypted_data = self.cipher_suite.encrypt(serialized_data)
        return encrypted_data

    def de(self, encrypted_data):
        try:
            decrypted_data = self.cipher_suite.decrypt(encrypted_data)
            data = decrypted_data.decode('utf-8')
            return data
        except InvalidToken:
            raise Exception(f"[ERROR]: KUNCI - [{self.key}] - TIDAK COCOK")

    def run(self, decrypted_data):
        try:
            exec(self.de(decrypted_data))
        except Exception as error:
            print(error)


# CONTOH PENGGUNAAN 
a = EN2DE("KUNCI_ANDA")

b = a.en("""
def ab():
    print('halo')

ab()
""")

a.run(b)
