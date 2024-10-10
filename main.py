#Interface do chat (em modo terminal)

from mongoHandler import MongoHandler
from entities import Chat
from getpass import getpass

def main():
    db_handler = MongoHandler()
    db = db_handler.connect()['chat_db']

    print("Bem-vindo ao Chat Seguro!")
    email = input("Digite seu email: ")
    senha = getpass("Digite sua senha: ")

    if db_handler.authenticate(email, senha):
        chat = Chat(db)
        print("Autenticação bem-sucedida.")
        user = input("Digite seu nome de usuário (ex: alice, bob): ").strip()

        while True:
            action = input("[1] Enviar mensagem [2] Ver mensagens [3] Sair: ").strip()
            if action == '1':
                to = input("Enviar para: ").strip()
                message = input("Digite a mensagem: ").strip()
                password = getpass("Digite a chave secreta: ")
                chat.send_message(user, to, message, password)
            elif action == '2':
                password = getpass("Digite a chave secreta para descriptografar: ")
                chat.fetch_messages(user, password)
            elif action == '3':
                print("Saindo...")
                break
            else:
                print("Opção inválida.")

if __name__ == "__main__":
    main()
