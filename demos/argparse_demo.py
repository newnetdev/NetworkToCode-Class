from netmiko import ConnectHandler
import argparse

if __name__ == "__main__":

    facts = {'vendor': 'cisco', 'mgmt_ip': '10.1.1.1', 'model': 'nexus', 'hostname': 'NYC301', 'os': '6.1.2'}


    parser = argparse.ArgumentParser(description='Python Argparse Demo for Training Course.')
    parser.add_argument('-f', '--fact', choices=facts.keys(), help='enter a valid fact from the device facts dictionary')
    parser.add_argument('-u', '--user', help='enter username to login to the device')
    parser.add_argument('-p', '--password', required=True, help='enter password to login to the device')
    parser.add_argument('-d', '--device_type', help='enter device type for netmiko')
    parser.add_argument('-i', '--ipaddr', choices=['csr1', 'csr2'], help='enter ipaddress for netmiko')
    parser.add_argument('-c', '--cmd', choices=['show version', 'show run'], help='enter command to execute for netmiko')
    args = parser.parse_args()

    print "the key to look up is "
    print args.fact
    print "fact looked up is"
    print facts[args.fact]
    print args.user
    password = args.password

    csr1 = ConnectHandler(ip=args.ipaddr, username=args.user, password=args.password, device_type=args.device_type)
    print("Connected to CSR1")
    csr1_device_check = csr1.is_alive()
    print "Connected to device is verified " + str(csr1_device_check)
    csr1.send_command("term len 0")
    print "sending command"
    print csr1.send_command(args.cmd)




