import socket
import time
import pickle


HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1235))
s.listen(5)

connected = True

while connected:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")
    full_msg = b''
    new_msg = True  

    while True:
        msg = s.recv(16)
        if  new_msg:
            print(f"new message length: { msg[:HEADERSIZE]}")
            msglen = int(msg[:HEADERSIZE])
            new_msg = False
        
        full_msg += msg

        if len(full_msg)-HEADERSIZE == msglen:
            print("full msg recvd")
            print(full_msg[HEADERSIZE:1])

            
            #d = pickle.loads(full_msg[HEADERSIZE:])
            #print(d)

            new_msg = True
            full_msg = b''
    
    print(full_msg)




    '''
while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")

    
    d = {1: "Hey", 2: "There"}
    msg = pickle.dumps(d)
    #print(msg)

    #msg = "Welcome to the server"
    msg = bytes(f'{len(msg):<{HEADERSIZE}}', "utf-8") + msg

    clientsocket.send(msg)
    while True:
        time.sleep(3)
        msg = f"The time is! {time.time()}"
        msg = f'{len(msg):<{HEADERSIZE}}'+ msg
        clientsocket.send(bytes(msg, "utf-8"))
''' 