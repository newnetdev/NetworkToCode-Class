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
    template = ENV.get_template("./templates/interfaces.j2")
    file_handler = open('./files/interfaces.yml')

    # config_data is a dictionary that is the YAML file with 
    # three keys, i.e  csr1, csr2, and csr3
    config_data = yaml.load(file_handler)

    devices = ['csr1', 'csr2', 'csr3']

    for device in devices:
        # basic variable that is where we want to create 
        # the config file per device 
        device_file = "./configs/{}".format(device)

        # creating a config string per device
        # notice how it's config_data[device]
        # device is csr1, then csr2 and then csr3
        # so we're sending in the interfaces dict from the yaml
        # file per device as we loop over them
        config = template.render(interfaces=config_data[device])
        
        # dumping the newly created config into a file per device
        with open(device_file, "w") as config_file:
            config_file.write(config)

        # netmiko actions
        conn_device = connect_to_device(device)
        print("Sending config from file | {}".format(device))
        conn_device.send_config_from_file(device_file)
        print("Disconnecting from device | {}".format(device))
        conn_device.disconnect()



