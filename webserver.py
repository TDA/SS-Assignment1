#!/usr/bin/python
import gzip
import subprocess
import zlib

__author__ = 'saipc'

import socket
import sys
import re
from urlparse import unquote

# set this to the port specified on command line
# or default to 8080
HOST = ''
PORT = sys.argv[1] if len(sys.argv) > 1 else 8080
# create a socket connection to listen on specified port
# set up the socket
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

# the regexes to extract the command passed
r = re.compile("(GET|POST)(.*)(HTTP/1.1)", re.IGNORECASE)
exec_r = re.compile("(/exec/)(.*)", re.IGNORECASE)
while True:
    # Multiline string yay!
    http_response_headers = """\
HTTP/1.1 200 OK
"""
    http_response = ""
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)
    headers = request.split("\r\n")
    print headers[0]
    if "/exec" in request:
        is_send_404 = False
        parts = r.search(headers[0]).groups()
        print parts[1]
        if exec_r.search(parts[1]):
            command = unquote(exec_r.search(parts[1]).groups()[1])
            print command
            # execute as a linux command
            retVal = subprocess.call(command, shell=True)
            if retVal == 0:
                response = subprocess.check_output(command, shell=True)
                # print response
                http_response = str(response)
    else:
        is_send_404 = True

    if "gzip" in request:
        # encode with gzip, do nothing for now
        http_response_headers = http_response_headers + "Content-Encoding: gzip\r\n"
        http_response = zlib.compress(http_response)

    http_response = http_response_headers + "\r\n" + http_response
    print http_response

    if is_send_404:
        client_connection.sendall(http_404_response)
    else:
        client_connection.sendall(http_response)
    client_connection.close()

