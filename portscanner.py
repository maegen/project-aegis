#!/usr/bin/env python

import socket, threading
from queue import Queue

#target IP --ill figure out how tom ake it scan an IP range in a bit
'''
loopback address will be a placeholder for now lol
'''
target = "127.0.0.1"



def scan_my_port(port):
    #error checking: attempt to connect first
    try:
        my_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_sock.connect((target, port))
        return True
    except:
        return False

 # scan ports 1-1024 since 1024< is just semi-reserved ports
for port in range (1, 1024):
    result = scan_my_port(port)
    #if result returns True
    if result: 
        print("Port{} is open".format(port))
    else:
        return None