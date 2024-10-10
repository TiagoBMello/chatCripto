#Contém as classes relacionadas ao chat

import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC # type: ignore
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes # type: ignore
from cryptography.hazmat.backends import default_backend # type: ignore
from cryptography.hazmat.primitives import hashes # type: ignore

class Message:
    def __init__(self, sender: str, receiver: str, content: str):
        self.sender = sender
        self.receiver = receiver
        self.content = content

    def encrypt(self, password: str):
        salt = os.urandom(16)
        key = self.generate_key(password, salt)
        iv = os.urandom(16)
        encryptor = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend()).encryptor()
        encrypted_content = encryptor.update(self.content.encode()) + encryptor.finalize()
        return base64.b64encode(iv + encrypted_content).decode('utf-8'), base64.b64encode(salt).decode('utf-8')

    @staticmethod
    def decrypt(encrypted_content: str, password: str, salt: str):
        encrypted_data = base64.b64decode(encrypted_content)
        iv = encrypted_data[:16]
        encrypted_message = encrypted_data[16:]
        salt_bytes = base64.b64decode(salt)
        key = Message.generate_key(password, salt_bytes)
        decryptor = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend()).decryptor()
        return decryptor.update(encrypted_message) + decryptor.finalize()

    @staticmethod
    def generate_key(password: str, salt: bytes):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(password.encode())


class Chat:
    def __init__(self, db):
        self.db = db

    def send_message(self, sender: str, receiver: str, content: str, password: str):
        message = Message(sender, receiver, content)
        encrypted_content, salt = message.encrypt(password)
        self.db['messages'].insert_one({
            'from': sender,
            'to': receiver,
            'message': encrypted_content,
            'salt': salt
        })

    def fetch_messages(self, receiver: str, password: str):
        messages = self.db['messages'].find({'to': receiver})
        for msg in messages:
            decrypted_message = Message.decrypt(msg['message'], password, msg['salt'])
            print(f"De: {msg['from']} | Para: {msg['to']} | Mensagem: {decrypted_message.decode('utf-8')}")
