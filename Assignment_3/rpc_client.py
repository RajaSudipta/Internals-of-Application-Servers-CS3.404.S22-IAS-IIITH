import socket 

IP = socket.gethostbyname(socket.gethostname()) 
PORT = 5566 
ADDR = (IP, PORT) 
SIZE = 9026 
FORMAT = "utf-8" 
# DISCONNECT_MSG = "!DISCONNECT" 
 
def rpc_connector(func_name, param_list): 
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	# client.settimeout(10) 
	client.connect(ADDR) 
	print(f"[CONNECTED] Client connected to server at {IP}: {PORT}") 
	msg_dict_string = str({func_name: param_list}) 
	client.send(msg_dict_string.encode(FORMAT)) 
	return_msg = client.recv(SIZE).decode(FORMAT) 
	return return_msg 
 
def foo(par_1): 
	func_name = "foo" 
	return str(rpc_connector(func_name, [int(par_1)])) 

def bar(par_1, par_2): 
	func_name = "bar" 
	return int(rpc_connector(func_name, [int(par_1), str(par_2)])) 

def addition(par_1, par_2): 
	func_name = "addition" 
	return int(rpc_connector(func_name, [int(par_1), int(par_2)])) 

def multiply(par_1, par_2): 
	func_name = "multiply" 
	return int(rpc_connector(func_name, [int(par_1), int(par_2)])) 

def voidFunc(par_1): 
	func_name = "voidFunc" 
	return (rpc_connector(func_name, [str(par_1)])) 

def univAdd(par_1, par_2): 
	func_name = "univAdd" 
	return float(rpc_connector(func_name, [int(par_1), float(par_2)])) 

def boolOp(par_1, par_2): 
	func_name = "boolOp" 
	return bool(rpc_connector(func_name, [bool(par_1), bool(par_2)])) 

def noParam(): 
	func_name = "noParam" 
	return bool(rpc_connector(func_name, [])) 

def noParamReturn(): 
	func_name = "noParamReturn" 
	return (rpc_connector(func_name, [])) 

def division(par_1, par_2): 
	func_name = "division" 
	return float(rpc_connector(func_name, [float(par_1), int(par_2)])) 

def main(): 
	s = " " 
 
if __name__ == "__main__": 
	main() 
 
