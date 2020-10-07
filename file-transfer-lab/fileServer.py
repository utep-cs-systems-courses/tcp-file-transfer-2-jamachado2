#! /usr/bin/env python3

import sys
sys.path.append("../lib")       # for params
import re, socket, params, os
from framedSock import framedSend, framedReceive

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)
outputNames = sys.argv
store_files = []

#with open(outputNames, "wb") as out:
while True:
                sock, addr = lsock.accept()
                print("connection rec'd from", addr)
                try:
                    file = open(outputNames, "wb")
                    if not os.fork():
                        fileNames = framedReceive(sock, debug)
                        if debug: print("rec'd: ", out)  #outputNames

                        if fileNames == None:
                            print("Empty file!")

                        if fileNames in store_files:
                            framedSend(sock, b"File already exists on server", debug)
                        else:
                            store_files.append(fileNames) # add files

                            framedSend(sock, fileNames, debug)

                            print("Server received the following file")
                            print(fileNames)
                            print(store_files)
                    file.close()
                except:
                    print("Connection to the client lost")
                    sys.exit(0)
                lsock.close()
