interfaces = ['Eth1/1', 'vlan20', 'Eth4/4', 'loop10']

for interface in interfaces:
    itype = ""
    interface = interface.lower()
    if interface.startswith('et'):
        itype = 'ethernet'
    elif interface.startswith('vl'):
        itype = 'svi'
    elif interface.startswith('lo'):
        itype = 'loopback'
    elif interface.startswith('po'):
        itype = 'portchannel'
    elif interface.startswith('mgmt'):
        itype = 'management'
    else:
        itype = "unknown"
    print(itype)

#####
#####
# demo nested dicts

INTERFACES = {
    'GigabitEthernet1': {
        'ipaddr': '10.1.1.1',
        'mask': '30',
        'admin': 'up'
    },
    'GigabitEthernet2': {
        'ipaddr': '10.2.1.1',
        'mask': '255.255.255.252',
        'admin': 'down'
    },
    'GigabitEthernet3': {
        'ipaddr': '10.3.1.1',
        'mask': '255.255.255.252',
        'admin': 'up'
    },
    'GigabitEthernet4': {
        'ipaddr': '10.4.1.1',
        'mask': '255.255.255.252',
        'admin': 'down'
    }
}

commands = []

for key, values in INTERFACES.items():
    commands.append("interface {0}".format(key))
    commands.append("ip address {0} {1}".format(values["ipaddr"], values["mask"]))
    if values["admin"]=="up":
        commands.append("no shut")
    elif values["admin"] == "down":
        commands.append("shut")
    else:
        print "Unknown admin state"

print commands
