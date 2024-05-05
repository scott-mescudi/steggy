from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import scrypt


def encrypt_AES256(file_path, password):
    """Encrypt a file using AES256 encryption."""
    with open(file_path, 'rb') as f:
        file_data = f.read()

    salt = get_random_bytes(16)
    key = scrypt(password, salt=salt, key_len=32, N=2**14, r=8, p=1)
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.iv + cipher.encrypt(pad(file_data, AES.block_size))
    encrypted_data = ciphertext + salt
    
    return encrypted_data

def decrypt_AES256(encrypted_data, password):
    """Decrypt AES256 encrypted data."""
    try:
        salt = encrypted_data[-16:]
        iv = encrypted_data[:16]
        ciphertext = encrypted_data[16:-16]

        key = scrypt(password, salt=salt, key_len=32, N=2**14, r=8, p=1)
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)

        return decrypted_data
    except Exception as e:
        print("Decryption failed:", e)
        return None
