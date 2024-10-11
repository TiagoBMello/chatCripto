from Crypto.Cipher import AES
import base64
import hashlib
import os


class EncryptionHandler:
    def __init__(self, chave):
        self.chave = hashlib.sha256(chave.encode()).digest()

    def cipher(self, texto_plano):
        iv = os.urandom(16)
        cipher = AES.new(self.chave, AES.MODE_CBC, iv)

        dados_preenchidos = self._pad(texto_plano)
        dados_criptografados = cipher.encrypt(dados_preenchidos.encode())

        return base64.b64encode(iv + dados_criptografados).decode('utf-8')

    def decrypt(self, mensagem_criptografada):
        dados_decodificados = base64.b64decode(mensagem_criptografada)

        iv = dados_decodificados[:16]
        dados_criptografados = dados_decodificados[16:]

        cipher = AES.new(self.chave, AES.MODE_CBC, iv)
        dados_decriptados = cipher.decrypt(dados_criptografados)

        return self._unpad(dados_decriptados.decode('utf-8'))

    def _pad(self, s):
        tamanho_bloco = AES.block_size
        padding = tamanho_bloco - len(s) % tamanho_bloco
        return s + (chr(padding) * padding)

    def _unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]
class Chat:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def enviar_mensagem(self, sender, recipient, message):
        colecao = self.db_handler.get_collection("messages")
        colecao.insert_one({"from": sender, "to": recipient, "message": message})

    def buscar_mensagens(self, recipient):
        colecao = self.db_handler.get_collection("messages")
        return colecao.find({"to": recipient})