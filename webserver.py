#!/usr/bin/python
__author__ = 'saipc'

import socket
import sys
import re

# set this to the port specified on command line
# or default to 8080
HOST = ''
PORT = sys.argv[1] if len(sys.argv) > 1 else 8080
# create a socket connection to listen on specified port
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print 'Serving HTTP on port %s ...' % PORT

is_send_404 = True
http_404_response = """\
HTTP/1.1 404 Not Found

<!doctype html>
<head><title>Not Found</title></head>
<body>Hey, couldn't find what you were looking for. Sorry!</body>
</html>
"""

r = re.compile("(GET|POST)(.*)(HTTP/1.1)", re.IGNORECASE)
exec_r = re.compile("(/exec/)(.*)", re.IGNORECASE)
while True:
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)
    headers = request.split("\r\n")
    print headers
    if "/exec" in request:
        is_send_404 = False
    else:
        is_send_404 = True
    # print request
    parts = r.search(headers[0]).groups()
    print parts[1]
    command = exec_r.search(parts[1]).groups()[1]
    if command:
        # execute as a linux command
        pass

    # Multiline string yay!
    http_response = """\
HTTP/1.1 200 OK

Hello, World!
"""

    if "gzip" in request:
        # encode with gzip, do nothing for now
        pass

    if is_send_404:
        client_connection.sendall(http_404_response)
    else:
        client_connection.sendall(http_response)
    client_connection.close()

