#!/usr/bin/env python

import os, socket, multiprocessing, subprocess, os

# os.devnull is just used to redirect standard output to write mode
#this function uses subprocess to ping the IPs and pingsweep to check live nodes
def pinger(job, result):

    DEVNULL = open(os.devnull, 'w')
    while True:

        ip = job.get()

        if ip is None:
            break

        try:
            subprocess.check_call(['ping', '-c1', ip],
                                  stdout=DEVNULL)
            result.put(ip)
        except:
            pass


def get_my_ip():
    #grabs subnet of the network
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def map_network(pool_size=255):
    ip_list = list()

    #split IP into subnet sections
    ip_parts = get_my_ip().split('.')
    base_ip = ip_parts[0] + '.' + ip_parts[1] + '.' + ip_parts[2] + '.'

    #multithreading the process to make it faster
    jobs = multiprocessing.Queue()
    results = multiprocessing.Queue()

    pool = [multiprocessing.Process(target=pinger, args=(jobs, results)) for i in range(pool_size)]

    for p in pool:
        p.start()

    # cue the ping processes
    for i in range(1, 255):
        jobs.put(base_ip + '{0}'.format(i))

    for p in pool:
        jobs.put(None)

    for p in pool:
        p.join()

    # collect he results
    while not results.empty():
        ip = results.get()
        ip_list.append(ip)

    return ip_list

# the global variable __name__ is used to execute the whole code  
# citation: https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == '__main__':

    print('Mapping...')
    lst = map_network()
    print(lst)