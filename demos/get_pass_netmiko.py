from netmiko import ConnectHandler
from getpass import getpass

if __name__ == "__main__":

  # raw_input -> input in py3
  # ipaddr = input("Enter...")

  ipaddr = raw_input("Enter IP Address (or FQDN): ")
  username = raw_input("Enter Username: ")
  password = getpass("Enter Password: ")
  device_type = raw_input("Enter Device Type: ")
  command = raw_input("Command to send in enable mode: ")

  print 'ipaddr', ipaddr
  print 'username', username
  print 'password', password
  print 'device_type', device_type

  csr1 = ConnectHandler(ip=ipaddr, username=username, password=password, device_type=device_type)
  print("Connected to CSR1")
  csr1_device_check = csr1.is_alive()
  print "Connected to device is verified " + str(csr1_device_check)
  csr1.send_command("term len 0")
  print "sending command"
  print csr1.send_command(command)