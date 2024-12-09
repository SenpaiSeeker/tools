import base64
import hashlib
import json
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


class ShiftChipher:
    def __init__(self, shift: int = 3, delimiter: str = "/"):
        self.shift = shift
        self.delimiter = delimiter

    def encrypt(self, text: str) -> str:
        encoded = self.delimiter.join(str(ord(char) + self.shift) for char in text)
        return encoded

    def decrypt(self, encoded_text: str) -> str:
        decoded = "".join(chr(int(code) - self.shift) for code in encoded_text.split(self.delimiter))
        return decoded


def save_code(filename, code, method, key):
    try:
        if method == "shift":
            encode = ShiftChipher(shift=key).encrypt(code)
            result = f"exec(__import__('mytools').ShiftChipher(shift={key}).decrypt('{encode}'))"
        elif method == "binary":
            encode = BinaryEncryptor(key=key).encrypt(code)
            result = f"exec(__import__('mytools').BinaryEncryptor(key={key}).decrypt('{encode}'))"
        elif method == "crypto":
            encode = CryptoEncryptor(key=key).encrypt(code)
            result = f"exec(__import__('mytools').CryptoEncryptor(key='{key}').decrypt('{encode}'))"
        else:
            result = code

        with open(filename, "w") as file:
            file.write(result)
    except Exception as e:
        print(f"Error saving file: {e}")
