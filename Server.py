import socket, threading

HOST = "127.0.0.1"
PORT = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
nicknames = []


# broadcast func
def broadcast(message):
    for client in clients:
        client.send(message)

# handle func
def handle(client):
    while True:
        try:
            message = client.recv(2048)
            print(f"{nicknames[clients.index(client)]} says {message}")
            broadcast(message)

        except:
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break




# receive func
def receive():
    while True:
        client,address = server.accept()
        print(f"Connected with {str(address)}!")

        client.send("NICKNAME".encode("utf-8"))
        nickname = client.recv(2048).decode("utf-8")
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of new client is {nickname}")
        broadcast(f"{nickname} joined the chat!\n".encode("utf-8"))
        client.send("You Have Connected to the server".encode("utf-8"))

        thread = threading.Thread(target=handle,args=(client,))
        thread.start()

print("******Server is running******")
receive()

