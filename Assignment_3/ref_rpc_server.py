import socket
import threading
import ast
from server_precodeures import *

IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        response = conn.recv(SIZE).decode(FORMAT)
        if response == DISCONNECT_MSG:
            connected = False

        print(f"[{addr}] {response}")
        # msg = f"Msg received: {msg}"

        fun_call = ast.literal_eval(response)
        print(fun_call)
        func_name = list(fun_call.keys())[0]
        print(func_name)
        arguments_list = fun_call[func_name]
        print(arguments_list)
        return_msg = ""
        if func_name == "multiply":
            return_msg = multiply(*arguments_list)
        elif func_name == "addition":
            return_msg = addition(*arguments_list)
        else:
            return_msg = "Invalid"
        # conn.send(return_msg.encode(FORMAT))
        conn.send(return_msg.encode(FORMAT))

    conn.close()


def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


if __name__ == "__main__":
    main()
