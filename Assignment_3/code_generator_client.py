import socket
import json
import sys

OUTPUT_FILE_NAME = "rpc_client.py"
JSON_FILE_NAME = ""

n = len(sys.argv)
if n == 2:
    JSON_FILE_NAME = sys.argv[1]
else:
    print("<< Give your arguements like following >>")
    print("python code_generator_client.py contract.json")
    sys.exit(0)

L1 = ["import socket \n\n",
     "IP = socket.gethostbyname(socket.gethostname()) \n",
     "PORT = 5566 \n", 
     "ADDR = (IP, PORT) \n", 
     "SIZE = 9026 \n",
     "FORMAT = \"utf-8\" \n", 
     "# DISCONNECT_MSG = \"!DISCONNECT\" \n \n"]

L2 = ["def rpc_connector(func_name, param_list): \n",
     "\tclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM) \n",
     "\t# client.settimeout(10) \n",
     "\tclient.connect(ADDR) \n",
     "\tprint(f\"[CONNECTED] Client connected to server at {IP}: {PORT}\") \n",
     "\tmsg_dict_string = str({func_name: param_list}) \n",
     "\tclient.send(msg_dict_string.encode(FORMAT)) \n",
     "\treturn_msg = client.recv(SIZE).decode(FORMAT) \n",
     "\treturn return_msg \n \n"]

L3 = ["def main(): \n",
      "\ts = \" \" \n \n"]

L4 = ["if __name__ == \"__main__\": \n",
      "\tmain() \n \n"]

file1 = open(OUTPUT_FILE_NAME, 'w')
file1.writelines(L1)
file1.writelines(L2)

'''dynamically creating the functions according to contract.json'''
# Opening JSON file
f = open(JSON_FILE_NAME)

# returns JSON object as a dictionary
data = json.load(f)

# Iterating through the json list
for i in data['remote_procedures']:
    func_name = i['procedure_name']
    return_type = i['return_type']
    if return_type == "string":
        return_type = "str"
    if(return_type == "NoneType" or return_type == "None"):
        return_type = ""
    # print(func_name)
    # print(return_type)
    param_name_list = []
    param_type_list = []
    for j in i['parameters']:
        param_name = j['parameter_name']
        param_name_list.append(param_name)
        param_type = j['data_type']
        if(param_type == "string"):
            param_type = "str"
        param_type_list.append(param_type)
        # print(param_name)
        # print(param_type)

    str = "def " + func_name + "("
    length = len(param_name_list)
    if(length > 0) :
        for k in range(length - 1):
            str = str + param_name_list[k] + ", "
        str = str + param_name_list[length-1]
    str = str + "): \n"
    str = str + "\tfunc_name = " + "\"" + func_name + "\" \n" 
    # str = str + "\treturn rpc_connector(func_name, ["
    str = str + "\treturn " + return_type + "(rpc_connector(func_name, ["
    if(length > 0):
        for k in range(length - 1):
            # str = str + param_name_list[k] + ", "
            str = str + param_type_list[k] + "(" + param_name_list[k] + ")" +  ", "
        # str = str + param_name_list[length-1]
        str = str + param_type_list[length-1] + "(" + param_name_list[length-1] + ")"
    str = str + "])) \n\n"

    # print(str)
    file1.write(str)


# Closing file
f.close()

file1.writelines(L3)
file1.writelines(L4)
file1.close()

# IP = socket.gethostbyname(socket.gethostname())
# PORT = 5566
# ADDR = (IP, PORT)
# SIZE = 1024
# FORMAT = "utf-8"
# DISCONNECT_MSG = "!DISCONNECT"

# # global client = ""


# def rpc_connector(func_name, param_list):
#     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client.connect(ADDR)
#     print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")
#     msg_dict_string = str({func_name: param_list})
#     client.send(msg_dict_string.encode(FORMAT))
#     return_msg = client.recv(SIZE).decode(FORMAT)
#     return return_msg


# '''have to create these methods dynamically according to server_procedure.py'''


# def multiply(param1, param2):
#     func_name = "multiply"
#     return rpc_connector(func_name, [param1, param2])
#     # res = rpc_connector(func_name, [param1, param2])
#     # return res


# def addition(param1, param2):
#     func_name = "addition"
#     return rpc_connector(func_name, [param1, param2])
#     # res = rpc_connector(func_name, [param1, param2])
#     # return res


# def main():
#     s = ""
#     # client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     # client.connect(ADDR)
#     # print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")

#     # connected = True
#     # while connected:
#     #     msg = input("> ")

#     #     client.send(msg.encode(FORMAT))

#     #     if msg == DISCONNECT_MSG:
#     #         connected = False
#     #     else:
#     #         msg = client.recv(SIZE).decode(FORMAT)
#     #         print(f"[SERVER] {msg}")


# if __name__ == "__main__":
#     main()
