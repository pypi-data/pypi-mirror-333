import hashlib

def hash_password(password):
    # 创建一个哈希对象
    hasher = hashlib.sha256()
    # 提供密码的字节
    hasher.update(password.encode('utf-8'))
    # 获取16进制的哈希值
    hashed_password = hasher.hexdigest()
    return hashed_password

def encrypt_simple(text):
    encrypted_text = ""
    if text:
        for char in text:
            encrypted_text += chr(ord(char) + 1)
        return encrypted_text

def decrypt_simple(text):
    decrypted_text = ""
    if text:
        for char in text:
            decrypted_text += chr(ord(char) - 1)
        return decrypted_text


