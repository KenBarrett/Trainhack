import socket
import threading
import time

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

class myTrain:
    starttime = 0
    stopct = 0
    stopped = False

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

#runs concurrently for each client
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    train = myTrain()
    while connected:
        msg_length = conn.recv(HEADER).decode()
        if msg_length: #if msg_length is not none
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            if inputAction(msg, conn, train) == False:
                conn.send("Msg recieved".encode(FORMAT))
    conn.close()


def inputAction(msg, conn, train):
    print(train.stopct)
    print(time.time() - train.starttime)
    if float(msg) == 151.1 and train.stopct == 0:
        train.starttime = time.time()
        train.stopct = 1
        return False
    elif float(msg) == 151.1 and train.stopct == 1 and time.time() - train.starttime < 15:
        train.stopct = 2
        return False
    elif float(msg) == 151.1 and train.stopct == 2  and   time.time() - train.starttime < 15:
        conn.send("Train Stopped".encode(FORMAT))
        return True
    else: 
        train.stopct = 0
        return False




def start():
    server.listen()
    print("[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
        
print("[STARTING] server is starting...")
start()