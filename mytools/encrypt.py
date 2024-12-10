import base64
import hashlib
import textwrap
from mytools.logger import LoggerHandler

log = LoggerHandler()


class BytesCipher:
    def __init__(self, key: int):
        if not isinstance(key, int):
            raise ValueError("Key harus berupa integer.")
        self.key = key

    def _xor_encrypt_decrypt(self, data: bytes):
        key_bytes = self.key.to_bytes((self.key.bit_length() + 7) // 8, byteorder="big")
        return bytes([data[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(data))])

    def encrypt(self, data: str):
        serialized_data = textwrap.dedent(data).encode("utf-8")
        encrypted_data = self._xor_encrypt_decrypt(serialized_data)
        return base64.urlsafe_b64encode(encrypted_data).decode("utf-8")

    def decrypt(self, encrypted_data: str):
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode("utf-8"))
            decrypted_bytes = self._xor_encrypt_decrypt(encrypted_bytes)
            return decrypted_bytes.decode("utf-8")
        except (ValueError, UnicodeDecodeError) as error:
            raise Exception(f"\033[1;31m[ERROR] \033[1;35m|| \033[1;37m{error}\033[0m")


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

def run_code(method: str, key: int, encrypted_data: str):
    try:
        if method == "shift":
            result = ShiftChipher(shift=key).decrypt(encrypted_data)
        elif method == "binary":
            result = BinaryEncryptor(key=key).decrypt(encrypted_data)
        elif method == "bytes":
            result = BytesCipher(key=key).decrypt(encrypted_data)
        else:
            result = code
        return exec(result)
    except Exception as e:
        log.error(e)
        

def save_code(filename, code, method, key):
    try:
        if method == "shift":
            encode = ShiftChipher(shift=key).encrypt(code)
            result = f"exec(__import__('mytools').ShiftChipher(shift={key}).decrypt('{encode}'))"
        elif method == "binary":
            encode = BinaryEncryptor(key=key).encrypt(code)
            result = f"exec(__import__('mytools').BinaryEncryptor(key={key}).decrypt('{encode}'))"
        elif method == "bytes":
            encode = BytesCipher(key=key).encrypt(code)
            result = f"exec(__import__('mytools').CryptoEncryptor(key='{key}').decrypt('{encode}'))"
        else:
            result = code

        with open(filename, "w") as file:
            file.write(result)
    except Exception as e:
        print(f"Error saving file: {e}")
