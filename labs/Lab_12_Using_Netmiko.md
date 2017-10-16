## Lab 12 - Network Automation with Netmiko 

In this lab, we will explore using netmiko for network automation.  

### Task 1 - Using Netmiko

This task will show you how to establish an interactive SSH session to a Cisco router running IOS using Netmiko.  

> Note: More specifically, this lab uses the CSR 1000V running IOS XE.

##### Step 1

Enter the Python Dynamic Interactive Interpreter.

##### Step 2

Import the netmiko `ConnectHandler` object and establish an SSH session to the Cloud Services Router device switch with the following details:

* hostname: csr1
* Username: ntc
* Password: ntc123
* SSH port: 22

```python
>>> from netmiko import ConnectHandler
>>> 
>>> platform = 'cisco_ios'
>>> host = 'csr1'
>>> username = 'ntc'
>>> password = 'ntc123'
>>> 
>>> device = ConnectHandler(device_type=platform, ip=host, username=username, password=password)
>>>
>>> 
```

##### Step 3

Issue a `dir()` on `device` to see available methods that can be called.

```python
>>> dir(device)
['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_autodetect_fs', '_connect_params_dict', '_read_channel_expect', '_read_channel_timing', '_sanitize_output', '_use_ssh_config', 'alt_host_keys', 'alt_key_file', 'ansi_escape_codes', 'base_prompt', 'check_config_mode', 'check_enable_mode', 'cleanup', 'clear_buffer', 'commit', 'config_mode', 'device_type', 'disable_paging', 'disconnect', 'enable', 'establish_connection', 'exit_config_mode', 'exit_enable_mode', 'find_prompt', 'global_delay_factor', 'host', 'ip', 'key_file', 'key_policy', 'normalize_cmd', 'normalize_linefeeds', 'password', 'port', 'protocol', 'read_channel', 'read_until_pattern', 'read_until_prompt', 'read_until_prompt_or_pattern', 'remote_conn', 'remote_conn_pre', 'secret', 'select_delay_factor', 'send_command', 'send_command_expect', 'send_command_timing', 'send_config_from_file', 'send_config_set', 'session_preparation', 'set_base_prompt', 'set_terminal_width', 'special_login_handler', 'ssh_config_file', 'strip_ansi_escape_codes', 'strip_backspaces', 'strip_command', 'strip_prompt', 'system_host_keys', 'telnet_login', 'timeout', 'use_keys', 'username', 'verbose', 'write_channel']
>>> 
```

##### Step 4

Execute the command `show version` using netmiko:

```python
>>> output = device.send_command('show version')
>>> 
>>> print output
Cisco IOS XE Software, Version 03.14.01.S - Standard Support Release
Cisco IOS Software, CSR1000V Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 15.5(1)S1, RELEASE SOFTWARE (fc1)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2015 by Cisco Systems, Inc.
Compiled Sun 01-Mar-15 03:58 by mcpre


Cisco IOS-XE software, Copyright (c) 2005-2015 by cisco Systems, Inc.
All rights reserved.  Certain components of Cisco IOS-XE software are
licensed under the GNU General Public License ("GPL") Version 2.0.  The
software code licensed under GPL Version 2.0 is free software that comes
with ABSOLUTELY NO WARRANTY.  You can redistribute and/or modify such
GPL code under the terms of GPL Version 2.0.  For more details, see the
documentation or "License Notice" file accompanying the IOS-XE software,
or the applicable URL provided on the flyer accompanying the IOS-XE
software.


ROM: IOS-XE ROMMON

csr1 uptime is 2 hours, 55 minutes
Uptime for this control processor is 2 hours, 57 minutes
System returned to ROM by reload
System image file is "bootflash:packages.conf"
Last reload reason: <NULL>



This product contains cryptographic features and is subject to United
States and local country laws governing import, export, transfer and
use. Delivery of Cisco cryptographic products does not imply
third-party authority to import, export, distribute or use encryption.
Importers, exporters, distributors and users are responsible for
compliance with U.S. and local country laws. By using this product you
agree to comply with applicable laws and regulations. If you are unable
to comply with U.S. and local laws, return this product immediately.

A summary of U.S. laws governing Cisco cryptographic products may be found at:
http://www.cisco.com/wwl/export/crypto/tool/stqrg.html

If you require further assistance please contact us by sending email to
export@cisco.com.

License Level: ax
License Type: Default. No valid license found.
Next reload license Level: ax

cisco CSR1000V (VXE) processor (revision VXE) with 2152318K/6147K bytes of memory.
Processor board ID 9LT7GSJVCI8
4 Gigabit Ethernet interfaces
32768K bytes of non-volatile configuration memory.
3988508K bytes of physical memory.
7774207K bytes of virtual hard disk at bootflash:.

Configuration register is 0x2102

>>>
```


##### Step 5

Shutdown interface GigabitEthernet3 sending one command at a time.

```python
>>> device.config_mode()
u'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\ncsr1(config)#'
>>> 
>>> device.send_command_timing('interface Gigabit3')
u''
>>> device.send_command('shutdown')
u''
>>>
```

To absorb the output for each command and not see the returning prompts, you can simply do the following (or use different variables):

```python 
>>> data =  device.config_mode()
>>> data = device.send_command_timing('interface Gigabit3')
>>> data = device.send_command('shutdown')
>>>
```

Exit configuration mode:

```python
>>> device.exit_config_mode()
u'end\ncsr1#'
>>>
```


##### Step 6

Re-enable interface Gi3 *sending a list of commands*.

```python
>>> commands = ['interface Gi3', 'no shut']
>>> 
>>> device.send_config_set(commands)
u'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\ncsr1(config)#interface Gi3\ncsr1(config-if)#no shut\ncsr1(config-if)#end\ncsr1#'
>>>
```

If you save the output in a variable and use the print command, you will see a cleaner output:

```python
>>> response = device.send_config_set(commands)
>>> 
>>> print response
config term
Enter configuration commands, one per line.  End with CNTL/Z.
csr1(config)#interface Gi3
csr1(config-if)#no shut
csr1(config-if)#end
csr1#
>>>
```

You can also use `help()` to learn more about each method just like you saw with the built-in Python data types.

For example, here is the help on `send_config_set`:

```python
>>> help(device.send_config_set)

Help on method send_config_set in module netmiko.base_connection:

send_config_set(self, config_commands=None, exit_config_mode=True, **kwargs) method of netmiko.cisco.cisco_nxos_ssh.CiscoNxosSSH instance
    Send group of configuration commands down the SSH channel.
    
    config_commands is an iterable containing all of the configuration commands.
    The commands will be executed one after the other.
    
    Automatically exits/enters configuration mode.
    
    **kwargs will allow passing of all the arguments to send_command
    strip_prompt and strip_command will be set to False if not explicitly set in
    the method call.
(END)
```

##### Step 7

Continue to try other Netmiko methods as you saw in Step 3.

##### Step 8

Disconnect from the device

```python
>>> device.disconnect()
>>> 
```

Exit the Python shell.


### Task 2 - Deploying a Network Configuration file with Netmiko

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

    print("Connecting to the remote device {}...\n"
          .format(device_details['ip']))

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

    print("Connecting to the remote device {}...\n"
          .format(device_details['ip']))
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
