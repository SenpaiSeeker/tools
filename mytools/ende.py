import base64
import hashlib
import json
import random
import textwrap

from cryptography import fernet


class FARNET:
    def __init__(self, key):
        self.key = hashlib.sha256(key.encode()).digest()
        self.cipher_suite = fernet.Fernet(base64.urlsafe_b64encode(self.key))

    def en(self, data, is_dict=False):
        serialized_data = json.dumps(data).encode("utf-8") if is_dict else textwrap.dedent(data).encode("utf-8")
        encrypted_data = self.cipher_suite.encrypt(serialized_data)
        return encrypted_data

    def de(self, encrypted_data, is_dict=False):
        try:
            decrypted_data = self.cipher_suite.decrypt(encrypted_data)
            data = decrypted_data.decode("utf-8")
            return json.loads(data) if is_dict else data
        except fernet.InvalidToken:
            raise Exception(f"[ERROR]: KUNCI - [{self.key}] - TIDAK COCOK")

    def logs(self, text):
        random_color = random.choice(["\033[91m", "\033[92m", "\033[93m", "\033[94m", "\033[95m", "\033[96m"])
        reset_color = "\033[0m"
        print(f"{random_color}{text}{reset_color}")

    def run(self, decrypted_data):
        try:
            exec(self.de(decrypted_data))
        except Exception as error:
            self.logs(error)
