#!/usr/bin/python
import os
__author__ = 'saipc'
import socket
import sys

HOST = ''
PORT = 8080
# create a socket connection to listen on specified port
# set up the socket
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print 'Serving HTTP on port %s ...' % PORT

is_send_404 = True
http_404_response = """HTTP/1.1 404 Not Found

<!doctype html>
<head><title>Not Found</title></head>
<body>Hey, couldn't find what you were looking for. Sorry!</body>
</html>
"""

http_response = """HTTP/1.1 200 OK

Hello
"""

while True:
    try:
        client_connection, client_address = listen_socket.accept()
        data = client_connection.recv(1024)
        if is_send_404:
            client_connection.sendall(http_404_response + data)
        else:
            client_connection.sendall(http_response + data)
        # time.sleep(30) # proof that its concurrent
        client_connection.close()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
