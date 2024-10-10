#Gerencia a conexão com o MongoDB e autentica os usuários

from pymongo import MongoClient

class MongoHandler:
    def __init__(self, connection_string=None):
        if connection_string is None:
            # Substitua pelo seu string de conexão
            self.connection_string = "mongodb://localhost:27017/"
        else:
            self.connection_string = connection_string

    def connect(self):
        return MongoClient(self.connection_string)

    def authenticate(self, email: str, senha: str) -> bool:
        db = self.connect()['chat_db']
        user = db['users'].find_one({"email": email})
        if user and user['password'] == senha:
            return True
        return False
