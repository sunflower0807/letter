import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from hashlib import md5
import sys


def evp_kdf(password, salt, key_size=32, iv_size=16):
    d = b''
    last = b''
    while len(d) < key_size + iv_size:
        last = md5(last + password.encode() + salt).digest()
        d += last
    return d[:key_size], d[key_size:key_size+iv_size]


def encrypt_text(text, password):
    salt = get_random_bytes(8)
    key, iv = evp_kdf(password, salt)

    cipher = AES.new(key, AES.MODE_CBC, iv)

    data = text.encode('utf-8')
    pad_len = 16 - (len(data) % 16)
    padded_data = data + bytes([pad_len] * pad_len)

    ciphertext = cipher.encrypt(padded_data)

    encrypted = b"Salted__" + salt + ciphertext

    return base64.b64encode(encrypted).decode()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python encrypt.py <password>")
        sys.exit(1)

    password = sys.argv[1]

    try:
        with open("plain.txt", "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print("❌ plain.txt not found")
        sys.exit(1)

    encrypted_text = encrypt_text(text, password)

    with open("encrypted.txt", "w", encoding="utf-8") as f:
        f.write(encrypted_text)

    print("💌 Encrypted successfully → encrypted.txt")
