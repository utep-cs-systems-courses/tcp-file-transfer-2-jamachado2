#! /usr/bin/env python3

# Echo client program
import socket, sys, re, os
sys.path.append("../lib")       # for params
import params

from framedSock import framedSend, framedReceive


switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = (serverHost, serverPort)

s = socket.socket(addrFamily, socktype)

if s is None:
    print('could not open socket')
    sys.exit(1)

s.connect(addrPort)

fileNames = sys.argv

#with open(fileNames, "rb") as fn:

for f in fileNames:
    if os.path.isfile(f) == False:
        print("%s file does not exist" % f)
    elif os.path.getsize(f) <= 0:
        print("File is empty")
    else:
        print("\n Sending file %s to Server:" % f)

        file = open(f, "rb")
        for content in file.read():
            framedSend(s, str.encode(content))
            rec = framedReceive(s)
            print("Server : ", rec)
        file.close()
    s.close()

    """
    print("sending hello world")
    framedSend(s, b"hello world", debug)
    print("received:", framedReceive(s, debug))
    
    print("sending hello world")
    framedSend(s, b"hello world", debug)
    print("received:", framedReceive(s, debug))
    """
