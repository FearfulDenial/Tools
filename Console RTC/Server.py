import socket
import threading

Host = "127.0.0.1"
Port = 3000

Clients = []

def Broadcast(Message,Sender):
    for Client in Clients:
        if Client != Sender:
            try:
                Client.send(Message)
            except:
                Clients.remove(Client)

def HandleClient(Socket):
    while True:
        try:
            Message = Socket.recv(1024)
            if not Message: break
            Broadcast(Message,Socket)
        except:
            Clients.remove(Socket)
            break
    Socket.close()

def Start():
    Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Server.bind((Host,Port))
    Server.listen(5)
    print("Server Started. Waiting for connections...")

    while True:
        Socket, Address = Server.accept()
        print(f"New Connection from {Address}")
        Clients.append(Socket)
        threading.Thread(target=HandleClient, args=(Socket,)).start()

if __name__ == "__main__": Start()