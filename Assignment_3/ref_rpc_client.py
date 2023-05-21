import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

# global client = ""

def rpc_connector(func_name, param_list):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")
    msg_dict_string = str({func_name: param_list})
    client.send(msg_dict_string.encode(FORMAT))
    return_msg = client.recv(SIZE).decode(FORMAT)
    return return_msg


'''have to create these methods dynamically according to server_procedure.py'''
def multiply(param1, param2):
    func_name = "multiply"
    return rpc_connector(func_name, [param1, param2])
    # res = rpc_connector(func_name, [param1, param2])
    # return res

def addition(param1, param2):
    func_name = "addition"
    return rpc_connector(func_name, [param1, param2])
    # res = rpc_connector(func_name, [param1, param2])
    # return res


def main():
    s = ""
    # client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client.connect(ADDR)
    # print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")

    # connected = True
    # while connected:
    #     msg = input("> ")

    #     client.send(msg.encode(FORMAT))

    #     if msg == DISCONNECT_MSG:
    #         connected = False
    #     else:
    #         msg = client.recv(SIZE).decode(FORMAT)
    #         print(f"[SERVER] {msg}")


if __name__ == "__main__":
    main()
