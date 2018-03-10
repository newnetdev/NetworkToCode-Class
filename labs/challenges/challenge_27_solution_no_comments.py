from jinja2 import Environment, FileSystemLoader
import json
import yaml
from netmiko import ConnectHandler

def connect_to_device(hostname):
    print("Connecting to device | {}".format(hostname))
    net_device = ConnectHandler(host=hostname, username='ntc',
                                password='ntc123', device_type='cisco_ios')

    return net_device

if __name__ == "__main__":
    
    ENV = Environment(loader=FileSystemLoader('./templates'))
    template = ENV.get_template("interfaces.j2")
    file_handler = open('./files/interfaces.yml')

    config_data = yaml.load(file_handler)

    devices = ['csr1', 'csr2', 'csr3']

    for device in devices:
        device_file = "./configs/{}".format(device)

        config = template.render(interfaces=config_data[device])
        
        with open(device_file, "w") as config_file:
            config_file.write(config)

        conn_device = connect_to_device(device)
        print("Sending config from file | {}".format(device))
        conn_device.send_config_from_file(device_file)
        print("Disconnecting from device | {}".format(device))
        conn_device.disconnect()



