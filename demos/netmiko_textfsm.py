# make sure templates are present and netmiko knows about them
# git clone https://github.com/networktocode/ntc-templates
# export NET_TEXTFSM=/home/ntc/ntc-templates/templates/

# see https://github.com/networktocode/ntc-templates/tree/master/templates
# for list of templates

from netmiko import ConnectHandler
import json

user = 'ntc'
pwd = 'ntc123'
d_type = 'cisco_ios'

csr1 = ConnectHandler(ip='csr1', username=user, password=pwd, device_type=d_type)

sh_ip_int_br = csr1.send_command("show ip int brief", use_textfsm=True)
# [{'status': 'up', 'intf': 'GigabitEthernet1', 'ipaddr': '10.0.0.51', 'proto': 'up'}, {'status': 'up', 'intf': 'GigabitEthernet2', 'ipaddr': 'unassigned', 'proto': 'up'}, {'status': 'up', 'intf': 'GigabitEthernet3', 'ipaddr': 'unassigned', 'proto': 'up'}, {'status': 'up', 'intf': 'GigabitEthernet4', 'ipaddr': '5.12.1.1', 'proto': 'up'}, {'status': 'up', 'intf': 'Loopback100', 'ipaddr': '10.200.1.20', 'proto': 'up'}]

# is type list
print (type(sh_ip_int_br))
# list of dicts
print (type(sh_ip_int_br[0]))

for each_dict in sh_ip_int_br:
    print "\n"
    for key in each_dict.keys():
        print key

for each_dict in sh_ip_int_br:
    print "\n"
    for key, value in each_dict.items():
        print key + " is " + value

sh_ver_ios = csr1.send_command("show version", use_textfsm=True)
# [{'running_image': 'packages.conf', 'hostname': 'csr1', 'uptime': '6 hours, 59 minutes', 'config_register': '0x2102', 'hardware': ['CSR1000V'], 'version': '16.6.2', 'serial': ['9KIBQAQ3OPE'], 'rommon': 'IOS-XE'}]

# print the json nicely
print (json.dumps(sh_ver_ios, indent=4))
print sh_ver_ios

# list
print type(sh_ver_ios)
# each item is a dict
print type(sh_ver_ios[0])

# list of dicts with some nested lists with the dicts
for each_dict in sh_ver_ios:
    print "\n"
    for key, value in each_dict.items():
        if type(value) is list:
            print key + " is "
            for list_entry in value:
                print list_entry
        if type(value) is str:
            print key + " is " + value
