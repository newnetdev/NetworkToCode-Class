from netmiko import ConnectHandler

print("Connecting to device | CSR1")
csr1 = ConnectHandler(host='csr1', username='ntc', password='ntc123', device_type='cisco_ios')

print("Connecting to device | CSR2")
csr2 = ConnectHandler(host='csr2', username='ntc', password='ntc123', device_type='cisco_ios')

print("Connecting to device | CSR3")
csr3 = ConnectHandler(host='csr3', username='ntc', password='ntc123', device_type='cisco_ios')

print("Sending commands from file | CSR1")
csr1.send_config_from_file("./configs/snmp.cfg")

print("Sending commands from file | CSR2")
csr2.send_config_from_file("./configs/snmp.cfg")

print("Sending commands from file | CSR3")
csr3.send_config_from_file("./configs/snmp.cfg")

print("Disconnecting from device | CSR1")
csr1.disconnect()

print("Disconnecting from device | CSR2")
csr2.disconnect()

print("Disconnecting from device | CSR3")
csr3.disconnect()

