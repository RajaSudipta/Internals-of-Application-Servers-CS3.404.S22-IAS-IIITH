
import socket
import ssl
import string
import sys
from urllib import request
FORMAT = "UTF-8"

while(True):
    host = input("Enter a url (eg. www.iiit.ac.in): ")
    # host = 'www.iiit.ac.in'
    # host = 'www.google.com'
    # host = 'www.allahabadhighcourt.in'
    # request = f"GET / HTTP/1.1\r\nHost: {host}\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8\
    #         \r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0\
    #         \r\nConnection: close\r\n\r\n"
    
    sub_domain=""
    try:
        sub_domain = host.split('/', 1)[1]
    except:
        sub_domain=""
    host=host.split('/',1)[0]
    # print(sub_domain,host)
    # request = f"GET /{sub_domain} HTTP/1.1\r\nHost: {host}\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8\
    #         \r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0\
    #         \r\nConnection: close\r\n\r\n"
    send_str = f"GET /{sub_domain} HTTP/1.1\r\nHost: {host}\r\n"
    accpt = "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8\r\n"
    usr_agnt = "User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0\r\nConnection: close\r\n\r\n"
    request = send_str + accpt + usr_agnt
    port = 80  # 443
    SSL_PORT = 443
    # host = 'www.google.co.in'
    # port = 443
    # host = "www.wellho.net"
    # port = 80  # web

    # create socket
    # print('# Creating socket')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('Failed to create socket')
        sys.exit()

    # print('# Getting remote IP address')
    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print('Hostname could not be resolved. Exiting')
        sys.exit()

    # Connect to remote server
    # print('# Connecting to server, ' + host + ' (' + remote_ip + ')')
    s.connect((remote_ip, port))

    # Send data to remote server
    # print('# Sending data to server')
    # request = "GET /people/faculty HTTPS/1.0\r\n\r\n"
    # request = "GET /people/faculty HTTP/1.1 Host: www.iiit.ac.in"
    # request = "GET /people/faculty HTTP/1.1\r\n"
    # request = "GET /robots.txt HTTP/1.0\n\n"
    # request = "GET / HTTP/1.1"

    try:
        # s.sendall(request)
        s.sendall(request.encode(FORMAT))
    except socket.error:
        print('Send failed')
        sys.exit()

    # # Receive data
    # print('# Receive data from server')
    # # reply = s.recv(4096)
    # reply = s.recv(4096).decode(FORMAT)

    # print (reply)

    # Receive data
    buffered_output = s.recv(1024)
    resppp = buffered_output
    resp = buffered_output
    while (len(buffered_output) > 0):
        buffered_output = s.recv(1024)
        resppp = buffered_output
        resp += buffered_output
    reply_str = resp.decode(FORMAT)
    # print(reply_str)
    ''' extracting the status code '''
    x = reply_str.split("\r\n")
    # print("# " + x[0])
    y = x[0].split(" ")
    status_code = y[1]
    # print("Status Code: " + y[1])
    # print(reply_str)
    # Close the connection when completed

    if((int)(status_code) >= 200 and (int)(status_code) < 300):
        # print("SUCCESS!!")
        '''success, can be continued with port 80'''
        '''extract the html code and dump it'''
        tokenized_string = reply_str.split("\r\n\r\n")
        html_header = tokenized_string[0]
        html_body = tokenized_string[1]
        html_body = html_body[:-1]
        ui = html_body
        html_body.rstrip()
        print(html_body)

    elif((int)(status_code) >= 300 and (int)(status_code) < 400):
        # Redirection Case, need to do ssl
        try:
            new_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            sys.exit()
        try:
            new_sock = ssl.wrap_socket(new_sock, keyfile=None, certfile=None, server_side=False,
                                       cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)
        except:
            sys.exit()
        try:
            remote_ip = socket.gethostbyname(host)
        except socket.gaierror:
            sys.exit()
        new_sock.connect((remote_ip, SSL_PORT))
        try:
            new_sock.sendall(request.encode(FORMAT))
        except socket.error:
            sys.exit()

        '''building the reply string and decode the string'''
        buffered_output = new_sock.recv(1024)
        respp = buffered_output
        resp = buffered_output
        while (len(buffered_output) > 0):
            buffered_output = new_sock.recv(1024)
            resppp = buffered_output
            resp += buffered_output
        reply_str = resp.decode(FORMAT)
        # print(reply_str)

        x = reply_str.split("\r\n")
        y = x[0].split(" ")
        status_code = y[1]
        if((int)(status_code) < 200 and (int)(status_code) >= 400):
            print("Status Code: " + status_code)
        else:
            # print(reply_str)
            tokenized_string = reply_str.split("\r\n\r\n")
            html_header = tokenized_string[0]
            html_body = tokenized_string[1]
            html_body = html_body[:-1]
            ui = html_body
            html_body.rstrip()
            print(html_body)

    # /* in 300, 400 check with ssl, if <200 and >=400, then error. decode try except */

    # s.close()
    # print ("\ndone")


''' 2nd code '''

# import socket
# FORMAT = "utf-8"

# # Set up a TCP/IP socket
# s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# # Connect as client to a selected server
# # on a specified port
# s.connect(("www.wellho.net", 80))
# # s.connect(("www.iiit.ac.in", 443))

# # Protocol exchange - sends and receives
# str = "GET /robots.txt HTTP/1.0\n\n"
# # str = "GET /people/faculty HTTP/1.0\n\n"

# s.send(str.encode(FORMAT))
# # s.send("GET /robots.txt HTTP/1.0\n\n")
# while True:
#         # resp = s.recv(1024)
#         resp = s.recv(1024).decode(FORMAT)
#         if resp == "": break
#         print (resp)

# # Close the connection when completed
# s.close()
# print ("\ndone")
