import socket

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname()) # can be changed to connected to diff devices
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
ADDR = (SERVER,PORT)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)



def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length)) #add passing to message to ensure it is a multiple of 64
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))


connected = True
while connected:
    msg = input("Type in radio frequency to send or exit to disconnect: ")
    if msg != "exit":
        send(msg)
    else:
        connected = False
        send(DISCONNECT_MESSAGE)
