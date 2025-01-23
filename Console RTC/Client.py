import socket
import threading

Host = "127.0.0.1"
Port = 3000

def Receive(Socket):
    while True:
        try:
            Message = Socket.recv(1024).decode("utf-8")
            if not Message: break
            print(Message)
        except:
            print("Disconnected")
            break

def Send(Socket):
    while True:
        Message = input()
        Socket.send(Message.encode("utf-8"))

def Start():
    Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Client.connect((Host,Port))
    print("Connected")
    threading.Thread(target=Receive, args=(Client,), daemon=True).start()
    Send(Client)

if __name__ == "__main__": Start()