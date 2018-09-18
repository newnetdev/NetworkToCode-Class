from netmiko import ConnectHandler
import json


DEVICES = ["csr1", "csr2"]

for device in DEVICES:
    d = ConnectHandler(host=device, username='ntc', password='ntc123', device_type='cisco_ios')
    # save config
    d.send_command("term len 0")
    config = d.send_command("show run")
    # save config to file
    with open("{}.cfg".format(device), "w") as f:
        f.write(config)


# checking version in nxos
nxos_login = {
"ip":"nxos-spine1",
"device_type":"cisco_nxos",
"username":"ntc",
"password":"ntc123"
}
nxos = ConnectHandler(**nxos_login)

show_ver_nx = nxos.send_command("show version | json")
show_ver_nx_dict = json.loads(show_ver_nx)
show_ver_nx_dict.keys()


# verify keys present
print show_ver_nx_dict.keys()

compliant_devices = []

# check for sh ver string in dict and pull hostname from device to put in list
if "7.3(1)D1(1)" in show_ver_nx_dict['sys_ver_str']:
    compliant_devices.append(show_ver_nx_dict["host_name"])

print compliant_devices
