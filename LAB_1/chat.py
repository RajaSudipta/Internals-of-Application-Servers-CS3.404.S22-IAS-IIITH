import socket

print("Press s for Server and c for Client!")
typ = input("Enter your choice: ")

if(typ == 's'):
    ServerSocket = socket.socket()

    ServerSocket.bind((socket.gethostname(), 8080))
    ServerSocket.listen()
    print("Listening...!!")
    clientSocket, addr = ServerSocket.accept()
    print('Client got connected!!')
    while 1:
        message = clientSocket.recv(1024)
        message = message.decode('ascii')
        print('Client: ', message)
        msg = input("Server: ")
        msg = "GET / HTTP/1.1\r\n" + msg + "\r\n"

        clientSocket.send(msg.encode('ascii'))

    clientSocket.close()

    ServerSocket.close()

elif(typ == 'c'):
    sock = socket.socket()
    sock.connect((socket.gethostname(), 8080))
    print("Connected...!!")
    while 1:
        msg = input("Client: ")
        msg = "GET / HTTP/1.1\r\n" + msg + "\r\n"
        sock.send(msg.encode())
        msg = sock.recv(1024)
        msg = msg.decode('ascii')
        print("Server: ", msg)

    sock.close()
else:
    print("Incorrect Choice")
