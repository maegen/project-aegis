#!/usr/bin/env python

import socket, threading
from queue import Queue

#target IP --ill figure out how to make it scan an IP range in a bit
'''
loopback address will be a placeholder for now lol
'''
target = "127.0.0.1"

#creates a Queue instance to queue the jobs
queue = Queue()

#list of open ports so it's easier to log
open_ports = []

def scan_my_port(port):
    #error checking: attempt to connect first
    try:
        my_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_sock.connect((target, port))
        return True
    except:
        return False

'''
 # scan ports 1-1024 since 1024< is just semi-reserved ports
for port in range (1, 1024):
    result = scan_my_port(port)
    #if result returns True
    if result: 
        print("Port{} is open".format(port))
    else:
        return None
'''
def queue_fill(port_list):
    for port in port_list:
        #put every port in the queue list
        queue.put(port)

#this is to run thread
def threader_work():
    while not queue.empty():
        #grabs the next port in the list
        port = queue.get()
        #if scan_my_port returns True
        if scan_my_port(port):
            print("Port {} is open".format(port))
            #append the open port to list so it's easier to log later
            open_ports.append(port)
        else:
            return None

# scan ports 1-1024 since 1024< is just semi-reserved ports
port_list = range(1, 1024)
queue_fill(port_list)

#empty thread list
thread_list = []

#running 10 threads at a time, Thread will take threader_work as an arg
for t in range(10):
    thread = threading.Thread(target=threader_work)
    thread_list.append(thread)

for thread in thread_list:
    thread.start()

#join just waits for other threads to finish
for thread in thread_list:
    thread.join()

print("Open ports are ", open_ports)