import socket
import json
import sys

OUTPUT_FILE_NAME = "rpc_server.py"
JSON_FILE_NAME = ""

n = len(sys.argv)
if n == 2:
    JSON_FILE_NAME = sys.argv[1]
else:
    print("<< Give your arguements like following >>")
    print("python code_generator_server.py contract.json")
    sys.exit(0)

file1 = open(OUTPUT_FILE_NAME, 'w')

L1 = ["import socket \n",
      "import threading \n",
      "from server_procedures import * \n \n",
      "IP = socket.gethostbyname(socket.gethostname()) \n",
      "PORT = 5566 \n",
      "ADDR = (IP, PORT) \n",
      "SIZE = 9026 \n",
      "FORMAT = \"utf-8\" \n",
      "# DISCONNECT_MSG = \"!DISCONNECT\" \n \n"]
L2 = ["def handle_client(conn, addr): \n",
      "\tprint(f\"[NEW CONNECTION] {addr} connected.\") \n\n",
      "\tresponse = conn.recv(SIZE).decode(FORMAT) \n",
      "\tprint(f\"[{addr}] {response}\") \n\n",
      "\tfun_call = eval(response) \n",
      "\t# print(fun_call) \n",
      "\tfunc_name = list(fun_call.keys())[0] \n",
      "\t# print(func_name) \n",
      "\targuments_list = fun_call[func_name] \n",
      "\t# print(arguments_list) \n",
      "\treturn_msg = \"\" \n"]

file1.writelines(L1)
file1.writelines(L2)

'''dynamically creating the functions according to contract.json'''
# Opening JSON file
f = open(JSON_FILE_NAME)

# returns JSON object as a dictionary
data = json.load(f)

# Iterating through the json list
func_name_list = []
for i in data['remote_procedures']:
    func_name = i['procedure_name']
    func_name_list.append(func_name)
if(len(func_name_list) > 0):
    str = "\tif func_name == \"" + func_name_list[0] + "\"" + ": \n"
    str = str + "\t\treturn_msg = " + func_name_list[0] + "(*arguments_list) \n"
    for j in range(1, len(func_name_list)):
        str = str + "\telif func_name == \"" + func_name_list[j] + "\"" + ": \n"
        str = str + "\t\treturn_msg = " + func_name_list[j] + "(*arguments_list) \n"
    str = str + "\telse: \n"
    str = str + "\t\treturn_msg = \"Invalid\" \n"
str = str + "\tconn.send((str(return_msg)).encode(FORMAT))\n"
str = str + "\tconn.close() \n\n"

file1.write(str)

L3 = ["def main(): \n",
      "\tprint(\"[STARTING] Server is starting...\") \n",
      "\tserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM) \n",
      "\tserver.bind(ADDR) \n",
      "\tserver.listen() \n",
      "\tprint(f\"[LISTENING] Server is listening on {IP}: {PORT}\") \n\n",
      "\twhile True: \n",
      "\t\tconn, addr = server.accept() \n",
      "\t\tthread = threading.Thread(target=handle_client, args=(conn, addr)) \n",
      "\t\tthread.start() \n",
      "\t\tprint(f\"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}\") \n\n"]

L4 = ["if __name__ == \"__main__\": \n",
      "\tmain() \n \n"]

file1.writelines(L3)
file1.writelines(L4)
file1.close()