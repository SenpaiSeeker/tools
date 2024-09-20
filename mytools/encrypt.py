import base64
import hashlib
import json
import random
import textwrap

from cryptography import fernet


class CryptoEncryptor:
    def __init__(self, key):
        self.key = hashlib.sha256(key.encode()).digest()
        self.cipher_suite = fernet.Fernet(base64.urlsafe_b64encode(self.key))

    def encrypt(self, data):
        if isinstance(data, dict):
            data = json.dumps(data)
        serialized_data = textwrap.dedent(data).encode("utf-8")
        encrypted_data = self.cipher_suite.encrypt(serialized_data)
        return encrypted_data.decode("utf-8")

    def decrypt(self, encrypted_data):
        try:
            decrypted_data = self.cipher_suite.decrypt(encrypted_data.encode("utf-8"))
            data = decrypted_data.decode("utf-8")
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return data
        except fernet.InvalidToken:
            raise Exception("[ERROR]: KUNCI TIDAK COCOK")

    def logs(self, text):
        random_color = random.choice(
            [
                "\033[91m",
                "\033[92m",
                "\033[93m",
                "\033[94m",
                "\033[95m",
                "\033[96m",
            ]
        )
        reset_color = "\033[0m"
        print(f"{random_color}{text}{reset_color}")

    def running(self, decrypted_data, is_return=False):
        try:
            if is_return:
                return self.de(decrypted_data)
            else:
                exec(self.de(decrypted_data))
        except Exception as error:
            self.logs(error)


class BinaryEncryptor:
    def __init__(self, key: int):
        if not isinstance(key, int) or key < 0:
            raise ValueError("Kunci harus berupa integer positif.")
        self.key = key

    def encrypt(self, plaintext: str):
        encrypted_bits = "".join(format(ord(char) ^ (self.key % 256), "08b") for char in plaintext)
        return encrypted_bits

    def decrypt(self, encrypted_bits: str):
        if len(encrypted_bits) % 8 != 0:
            raise ValueError("Data biner yang dienkripsi tidak valid.")
        decrypted_chars = [chr(int(encrypted_bits[i : i + 8], 2) ^ (self.key % 256)) for i in range(0, len(encrypted_bits), 8)]
        return "".join(decrypted_chars)
