#! /usr/bin/env python3

import sys
sys.path.append("../lib")
import re, socket, params, os
from os.path import exists

switchesVarDefaults = (
    (('-l', '--listenPort'), 'listenPort', 50001),
    (('-d', '--debug'), "debug", False),
    (('-?', '--usage'), "usage", False),
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

from threading import Thread, Lock
from encapFramedSock import EncapFramedSock

global lock
lock = Lock()


class Server(Thread):
    def __init__(self, sockAddr):
        Thread.__init__(self)
        self.sock, self.addr = sockAddr
        self.fsock = EncapFramedSock(sockAddr)
    def run(self):
        global lock
        print("new thread handling connection from", self.addr)
        while True:
            try:
                filename = self.fsock.receive(debug)
                print("checking server for : ", filename.decode())
                lock.acquire()
                sentfile = filename.decode()
                sentfile = "receive_"+sentfile
                print(sentfile)
                if exists(sentfile):
                    self.fsock.send(b"True",debug)
                    lock.release()

                else:
                    self.fsock.send(b"False", debug)
                    payload = self.fsock.receive(debug)
                    outfile = open(sentfile,"wb")
                    outfile.write(filename)
                    outfile.write(payload)
                    self.fsock.send(b"wrote new file",debug)
                    lock.release()
                    outfile.close()
            except:
                print("Connection to the client lost.")
                sys.exit(0)

while True:
    sockAddr = lsock.accept()
    server = Server(sockAddr)
    server.start()

