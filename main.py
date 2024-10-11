from entities import Chat, EncryptionHandler
from mongoHandler import MongoHandler


def main():
    db_handler = MongoHandler()
    db_handler.connect()
    email = input("Digite seu email: ")
    password = input("Digite sua senha: ")

    if db_handler.autenticar(email, password):
        print("Autenticado com sucesso.")
        chat = Chat(db_handler)
        chave_secreta = input("Digite sua chave secreta compartilhada: ")
        encryption = EncryptionHandler(chave_secreta)

        while True:
            print("\n1. Enviar uma mensagem\n2. Recuperar mensagens\n3. Sair")
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                remetente = input("De: ")
                destinatario = input("Para: ")
                mensagem = input("Mensagem: ")
                mensagem_criptografada = encryption.cipher(mensagem)
                chat.enviar_mensagem(remetente, destinatario, mensagem_criptografada)

            elif opcao == "2":
                destinatario = input("Para: ")
                mensagens = chat.buscar_mensagens(destinatario)
                for msg in mensagens:
                    mensagem_decriptada = encryption.decrypt(msg["message"])
                    print(f"De: {msg['from']} - Mensagem: {mensagem_decriptada}")

            elif opcao == "3":
                print("Saindo.")
                break


if __name__ == "__main__":
    main()
