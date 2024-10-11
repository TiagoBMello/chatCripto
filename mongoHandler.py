from pymongo import MongoClient

class MongoHandler:
    def __init__(self, connection_string=None):
        if connection_string is None:
            self.connection_string = ""
        else:
            self.connection_string = connection_string
        self.client = None
        self.db = None

    def connect(self):
        self.client = MongoClient(self.connection_string)
        self.db = self.client.get_database("sua_colecao")
        print("Conectado ao banco de dados.")

    def autenticar(self, email, password):
        colecao = self.db.get_collection("users")
        usuario = colecao.find_one({"email": email, "password": password})
        return usuario is not None

    def get_collection(self, sua_colecao):
        return self.db.get_collection(sua_colecao)
