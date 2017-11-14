
### Lab 13 - Deploying a Network Configuration file with Netmiko

##### Step 1

Navigate to the `scripts` directory within your home directory.:

```
ntc@ntc:~$ cd scripts
ntc@ntc:~/scripts$
```

##### Step 2

We can start off by making a copy the file you created in the last lab.

```
ntc@ntc:~/scripts$ cp read_yaml_file.py deploy_csr1_config.py
```

##### Step 3

Open this new file in a text editor of your choice.

##### Step 4

We will need the `ConnectHandler` object from the `netmiko` library to achieve the goal of this lab. Go ahead and add the following import statement, to the top of the new script `deploy_csr1_config.py`:

``` python
from netmiko import ConnectHandler

```

The functions that we already created in the previous lab can be reused. The new function needed to deploy the configuration, will use the `netmiko` library to connect to the device and push the generated configuration file to it.

##### Step 5

Add a new function calling it `deploy_config`

``` python
def deploy_config(config_file_name, device_details):
    """Connects to the device and deploys the configuration"""

    print("Connecting to the remote device {}...\n".format(device_details['ip']))

    # Invoke netmiko ConnectHandler and pass it the device details
    # Using the "**" syntax, device_details must be a dictionary
    # that maps to keyword arguments that Netmiko supports
    device = ConnectHandler(**device_details)
    # Send the config file
    print("Sending the configuration from file {}...".format(config_file_name))
    # nemtiko supports a method called send_config_from_file so you don't 
    # have to open the file and loop through in your script
    device.send_config_from_file(config_file=config_file_name)
    print("Changes sent to device. Please log in and verify...")

```

> Passing a variable with `**` in Python has significance. It expects the variable to be a set of key,value pairs that will be unpacked as keyword arguments to the function.
> 
> For example, the following two are identical:
> 
> Example 1:
> ```
> platform = 'cisco_ios'
> host = 'csr1'
> username = 'ntc'
> password = 'ntc123'
> device_details = dict(device_type=platform, ip=host, username=username, password=password)
> 
> device = ConnectHandler(**device_details)
> ```

> Example 2:
> ```
> device = ConnectHandler(device_type=platform, ip=host, username=username, password=password)
> ```

This function takes the configuration file and device login/platform information as input arguments. It uses the `send_config_from_file` method to push configuration to the device. This method takes the name of the file containing the configuration commands as its input.


##### Step 6

Call this new function from `main()`. The `device_details` dictionary will be used to store the login details and the device type, needed by `netmiko` to connect to `csr1`.

```python

def main():
    """Generate and write interface configurations to a file
    """

    interfaces_dict = get_interfaces_from_file()
    # Call a function that returns the configuration
    commands_list = get_commands_list(interfaces_dict)

    # Call a function that writes configs to a file
    config_file_name = '/tmp/device.cfg'
    generate_config_file(commands_list, config_file_name)

    # Device details

    device_type = 'cisco_ios'
    ip = 'csr1'
    username = 'ntc'
    password = 'ntc123'

    device_details = dict(device_type=device_type, ip=ip,
                          username=username, password=password)

    # Deploy the configurations
    deploy_config(config_file_name, device_details)

```

##### Step 7

The final, complete script should look like this:

``` python
#!/usr/bin/env python
""" Code for Netmiko Lab"""
import yaml
from netmiko import ConnectHandler


def generate_commands(config_params):
    """Generate specific feature commands using feature name & value."""
    cmd_list = []
    for feature, value in config_params.items():
        command = " {} {}".format(feature, value)
        cmd_list.append(command)
    return cmd_list


def get_commands_list(interfaces):
    """Return a list of interface configuration commands."""
    # Iterate over the dictionary and generate configuration.

    commands_list = []
    for interface, config_params in interfaces.items():
        interface_command = "interface {}".format(interface)
        commands_list.append(interface_command)
        feature_commands = generate_commands(config_params)
        commands_list.extend(feature_commands)

    return commands_list


def print_config(commands_list):
    """Print the commands as a list and config."""
    # Print the results as a list
    print("Commands as a List:")
    print(commands_list)
    print("--------------------")
    # Print the results as config
    print("Commands Simulating Config File:")
    for command in commands_list:
        print(command)


def generate_config_file(commands_list, config_file_name):
    """Write interface configs to a file"""
    print("Opening file {} to write...".format(config_file_name))

    with open(config_file_name, "w") as file_handler:
        for command in commands_list:
            file_handler.write("{}\n".format(command))
    # Output the file details
    print("File {} has been generated...".format(config_file_name))


def get_interfaces_from_file():
    """Read in YAML data of the interfaces and generate the dictionary"""
    with open('csr1.yml') as yaml_file_handler:
        interfaces = yaml.load(yaml_file_handler)
    return interfaces


def get_interfaces():
    """ Return a dictionary of interfaces containing attributes"""
    interfaces = {
        "GigabitEthernet1": {
            "duplex": "full",
            "speed": 1000,
            "description": "Configured_by_Python_GigabitEthernet1"
        },
        "GigabitEthernet2": {
            "duplex": "half",
            "speed": 100,
            "description": "Configured_by_Python_GigabitEthernet2"
        },
        "Loopback101": {
            "description": "Configured_by_Python_Looback101"
        },
        "Loopback100": {
            "description": "Configured_by_Python_Loopback100"
        }
    }

    return interfaces


def deploy_config(config_file_name, device_details):
    """Connects to the device and deploys the configuration"""

    print("Connecting to the remote device {}...\n".format(device_details['ip']))
    # Invoke netmiko ConnectHandler and pass it the device details
    device = ConnectHandler(**device_details)
    # Send the config file
    print("Sending the configuration from file {}...".format(config_file_name))
    device.send_config_from_file(config_file=config_file_name)
    print("Changes sent to device. Please log in and verify...")


def main():
    """Generate and write interface configurations to a file
    """

    interfaces_dict = get_interfaces_from_file()
    # Call a function that returns the configuration
    commands_list = get_commands_list(interfaces_dict)

    # Call a function that writes configs to a file
    config_file_name = '/tmp/device.cfg'
    generate_config_file(commands_list, config_file_name)

    # Device details

    device_type = 'cisco_ios'
    ip = 'csr1'
    username = 'ntc'
    password = 'ntc123'

    device_details = dict(device_type=device_type, ip=ip,
                          username=username, password=password)

    # Deploy the configurations
    deploy_config(config_file_name, device_details)


if __name__ == "__main__":
    main()

```

##### Step 8

Save and execute this script:


``` shell
ntc@ntc:~/scripts$ python deploy_csr1_config.py
Opening file /tmp/device.cfg to write...
File /tmp/device.cfg has been generated...
Connecting to the remote device csr1...

Sending the configuration from file /tmp/device.cfg...
Changes sent to device. Please log in and verify...

```

##### Step 9

Finally, log into device `csr1` and ensure that the changes were pushed to the device.


``` shell
csr1#show interfaces description 
Interface                      Status         Protocol Description
Gi1                            up             up       Configured_by_Python_GigabitEthernet1
Gi2                            admin down     down     Configured_by_Python_GigabitEthernet2
Gi3                            admin down     down     
Gi4                            admin down     down     
Lo100                          up             up       Configured_by_Python_Loopback100
Lo101                          up             up       Configured_by_Python_Loopback101
csr1#
```

You have now successfully created a modular python script that reads in configration data from a YAML encoded file, generates device interface configurations and deploys the configurations to the end device!
