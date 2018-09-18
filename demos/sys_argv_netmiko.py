#! /usr/bin/env python
from netmiko import ConnectHandler
import sys

if __name__ == "__main__":

    print "\n\n\ninput hostname, username, pwd, and device type\n\n"

    print sys.argv

    args = sys.argv

    if len(args) == 5:
        print "hostname", args[1]
        print "username", args[2]
        print "pwd", args[3]
        print "device type", args[4]
    else:
        print "invalid input with args - should have 4 inputs"

    ipaddr = args[1]
    device_type = args[4]
    username = args[2]
    password = args[3]
    cmd = "show version"

    csr1 = ConnectHandler(ip=ipaddr, username=username, password=password, device_type=device_type)
    print("Connected to CSR1")
    csr1_device_check = csr1.is_alive()
    print "Connected to device is verified " + str(csr1_device_check)
    csr1.send_command("term len 0")
    print "sending command"
    print csr1.send_command(cmd)