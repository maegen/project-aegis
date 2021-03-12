#!/usr/bin/env python

import os, sys, time, subprocess, socket

#import ipaddress module to verify if input is a real ip address
import ipaddress

os.system("clear")

#function to verify if its a real address
def validate_ip(ip):
 while True:
  try:
   ipaddress.IPv4Network(ip)
   return True
  except ValueError:
   return False


#ask for subnet and verifies
def isSubnet():
 while True:
  try:
   subnet = input("\033[1;36;40mEnter your subnet:\033[0m ")
   if validate_ip(subnet):
    return subnet
    break
   print("\033[1;31;40mInvalid subnet entered\033[0m\n")
  except Exception as e:
   print(e) 


#grab user's subnet automatically
def grabSubnet():
 ni.ifaddresses('ens33')
 ip = ni.ifaddresses('ens33')[ni.AF_INET][0]['addr']
 arr = re.split('[,.]',ip)

 subnet = (arr[0] + '.' + arr[1] + '.' + arr[2] + '.0/24')
 return subnet

#asks for user input subnet, verifies then nmap scans
def scanMyNetwork():
 subnet = grabSubnet()
 print("\033[1;36;40mNmap Scan Results\033[0m\n")
 print("-"*70)
 subprocess.check_call(['nmap',subnet,'-sP','-oN','/var/www/html/nmap.html'])
 input("Hit ENTER to go back to main menu")
 print("-"*70)
 os.system("clear")

#uses netdiscovery to view the whole network
def viewMyNetwork():
 subnet = isSubnet()
 subnet = subnet + "/16"
 subprocess.check_call(['netdiscover','-r',subnet])
 #just ctrl+c after 10 seconds and re-run code

#scan target IP
def scanSomeone():
 while True:
  try:
   subnet = input("\033[1;36;40mEnter target IP:\033[0m ")
   if validate_ip(subnet):
    break
   print("\033[1;31;40mInvalid subnet entered\033[0m\n")
  except Exception as e:
   print(e) 
 print("\033[1;36;40mNmap Scan Results\033[0m\n")
 print("-"*70)
 subprocess.check_call(['nmap','-A','-T4',subnet])
 input("Hit ENTER to go back to main menu")
 print("-"*70)
 os.system("clear")

#output system info
def sysInfo():
 print("\033[1;36;40mSystem Info\0\033[0m\n")
 print("-"*70)
 ipaddr = socket.gethostbyname(socket.gethostname())
 if ipaddr == "127.0.0.1":
  print("Internet: \033[1;31;40mNot Connected\033[0m")
 else:
  print("Internet: \033[1;32;40mConnected\033[0m")
 os = subprocess.check_output(['uname','-o'])
 os.decode('utf-8')
 print("Operating System: %s" % os)
 hostname = subprocess.check_output(['hostname'])
 print("Hostname: %s" % hostname)

#main menu to select option (testing out menu through CLI) --ONLY for testing for Linux Console 
def mainMenu():
 foo = True
 os.system("clear")
 while foo:
  print("1: Nmap Scan my Network\n2: Network Discovery View Network\n3: System Info\n4: Scan Target \n5: Quit")
  answer = input("Select your input: ")
  if answer == "1":
   scanMyNetwork()
  elif answer == "2":
   viewMyNetwork()
  elif answer == "3":
   sysInfo()
  elif answer == "4":
   scanSomeone()
  elif answer == "5":
   print("\nProgram Quitting")
   time.sleep(2)
   exit()
  elif answer != "":
   print("\nInvalid Choice")

mainMenu()