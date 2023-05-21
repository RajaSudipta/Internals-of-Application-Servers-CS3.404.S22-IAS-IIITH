import socket 
import threading 
from server_procedures import * 
 
IP = socket.gethostbyname(socket.gethostname()) 
PORT = 5566 
ADDR = (IP, PORT) 
SIZE = 9026 
FORMAT = "utf-8" 
# DISCONNECT_MSG = "!DISCONNECT" 
 
def handle_client(conn, addr): 
	print(f"[NEW CONNECTION] {addr} connected.") 

	response = conn.recv(SIZE).decode(FORMAT) 
	print(f"[{addr}] {response}") 

	fun_call = eval(response) 
	# print(fun_call) 
	func_name = list(fun_call.keys())[0] 
	# print(func_name) 
	arguments_list = fun_call[func_name] 
	# print(arguments_list) 
	return_msg = "" 
	if func_name == "foo": 
		return_msg = foo(*arguments_list) 
	elif func_name == "bar": 
		return_msg = bar(*arguments_list) 
	elif func_name == "addition": 
		return_msg = addition(*arguments_list) 
	elif func_name == "multiply": 
		return_msg = multiply(*arguments_list) 
	elif func_name == "voidFunc": 
		return_msg = voidFunc(*arguments_list) 
	elif func_name == "univAdd": 
		return_msg = univAdd(*arguments_list) 
	elif func_name == "boolOp": 
		return_msg = boolOp(*arguments_list) 
	elif func_name == "noParam": 
		return_msg = noParam(*arguments_list) 
	elif func_name == "noParamReturn": 
		return_msg = noParamReturn(*arguments_list) 
	elif func_name == "division": 
		return_msg = division(*arguments_list) 
	else: 
		return_msg = "Invalid" 
	conn.send((str(return_msg)).encode(FORMAT))
	conn.close() 

def main(): 
	print("[STARTING] Server is starting...") 
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	server.bind(ADDR) 
	server.listen() 
	print(f"[LISTENING] Server is listening on {IP}: {PORT}") 

	while True: 
		conn, addr = server.accept() 
		thread = threading.Thread(target=handle_client, args=(conn, addr)) 
		thread.start() 
		print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}") 

if __name__ == "__main__": 
	main() 
 
