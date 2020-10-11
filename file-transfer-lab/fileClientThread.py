#! /usr/bin/env python3

import socket, sys, re

sys.path.append("../lib")
import params
from os import path
from os.path import exists

from encapFramedSock import EncapFramedSock

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False),
    (('-?', '--usage'), "usage", False),
)

progname = "testClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Cant parse Server: port from '%s'" % server)
    sys.exit(1)

addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = (serverHost, serverPort)

sock = socket.socket(addrFamily, socktype)

if sock is None:
    print('could not open socket')
    sys.exit(1)
sock.connect(addrPort)

fsock = EncapFramedSock((sock, addrPort))
for _ in range(1):
    try:
        filename = input("Select the file to send: ")
        if exists(filename):
            file = open(filename, 'rb')
            payload = file.read()
            if len(payload) == 0:
                print("File is empty. Closing")
                sys.exit(0)
            else:
                fsock.send(filename.encode(), debug)  # send filename to check for existance
                file_exists = fsock.receive(debug).decode()
                if file_exists == 'True':
                    print("Selected file already exists.")
                    sys.exit(0)
                else:
                    fsock.send(payload, debug)
                    print("server ", fsock.receive(debug).decode())
        else:
            print("File '%s' doesn't exist." % filename)

    except:
        print("Connection to the server lost")
        sys.exit(0)

