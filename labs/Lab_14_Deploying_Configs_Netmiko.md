## Lab 14 - Deploying Configurations with Netmiko

In this lab, you will continue to build on what you learned in the Netmiko building more useful scripts.

### Task 1 - Deploying Interface Configurations

This task will introduce how to model data as a dictionary and use that to build the appropriate configuration command that'll then get sent to each device.

##### Step 1

**Make sure you can ping csr1, csr2, and csr3 from the Linux terminal.**

##### Step 2

Navigate to the `scripts` directory.

##### Step 3

Create a new script called `deploy-interfaces.py`.

##### Step 4

Open the script in your text editor of choice.

##### Step 5

In a separate window, open the Python shell.

##### Step 6

Paste the following dictionary into the shell:

```
INTERFACE_MAP = {
    "csr1":
        {
            "interface": "GigabitEthernet4",
            "ipaddr": "10.100.12.1",
            "mask": "255.255.255.0",
            "description": "Connect to csr2"
        },
    "csr2":
        {
            "interface": "GigabitEthernet4",
            "ipaddr": "10.100.12.2",
            "mask": "255.255.255.0",
            "description": "Connect to csr1"
        }
  }

```

Showing the result copied in successfully:

```python
>>> INTERFACE_MAP = {
...     "csr1":
...         {
...             "interface": "GigabitEthernet4",
...             "ipaddr": "10.100.12.1",
...             "mask": "255.255.255.0",
...             "description": "Connect to csr2"
...         },
...     "csr2":
...         {
...             "interface": "GigabitEthernet4",
...             "ipaddr": "10.100.12.2",
...             "mask": "255.255.255.0",
...             "description": "Connect to csr1"
...         }
...   }
>>>
```


We need to make sure you understand using an object like this.  Let's walk through a few more steps.

##### Step 7

Print all configuration parameters for **csr1** followed by it's IP Address and mask:

```python
>>> print(INTERFACE_MAP['csr1'])
{'interface': 'GigabitEthernet4', 'mask': '255.255.255.0', 'ipaddr': '10.100.12.1.1', 'description': 'Connect to csr2'}
>>>
>>>
>>> print(INTERFACE_MAP['csr1']['ipaddr'])
10.100.12.1.1
>>>
>>>
>>> print(INTERFACE_MAP['csr1']['mask'])
255.255.255.0
>>>
```

##### Step 8

Repeat Step 7 for **csr2**

```python
>>> print(INTERFACE_MAP['csr2'])
{'interface': 'GigabitEthernet4', 'mask': '255.255.255.0', 'ipaddr': '10.100.1.2', 'description': 'Connect to csr1'}
>>>
>>> print(INTERFACE_MAP['csr2']['ipaddr'])
10.100.1.2
>>>
>>> print(INTERFACE_MAP['csr2']['mask'])
255.255.255.0
>>>
```

Now that we've practiced with this object, let's move back to the Python `deploy-interfaces.py` script.

##### Step 9

In the `deploy-interfaces.py` script, do these three tasks:

  *  import the `ConnectHandler` object
  *  Create the `INTERFACE_MAP`
  *  Initiate the connection to **csr1** and **csr2**

```python
from netmiko import ConnectHandler

INTERFACE_MAP = {
    "csr1":
        {
            "interface": "GigabitEthernet4",
            "ipaddr": "10.100.12.1",
            "mask": "255.255.255.0",
            "description": "Connect to csr2"
        },
    "csr2":
        {
            "interface": "GigabitEthernet4",
            "ipaddr": "10.100.12.2",
            "mask": "255.255.255.0",
            "description": "Connect to csr1"
        }
  }

csr1 = ConnectHandler(host='csr1', username='ntc', password='ntc123', device_type='cisco_ios')
csr2 = ConnectHandler(host='csr2', username='ntc', password='ntc123', device_type='cisco_ios')

```

##### Step 10

Build three Cisco IOS commands for **csr1** that will enter interface configuration mode and send the two commands for configuring an IP address and description on the interface.  To do this, use the `format`  method while accessing data from the `INTERFACE_MAP`.

```python
csr1_interface_command = "interface {}".format(INTERFACE_MAP['csr1']['interface'])
csr1_ipaddr_command = "ip address {} {}".format(INTERFACE_MAP['csr1']['ipaddr'], INTERFACE_MAP["csr1"]["mask"])
csr1_descr_command = "description {}".format(INTERFACE_MAP['csr1']['description'])
```

##### Step 11

Create a list of the three commands you created in the last Step.

```python
csr1_commands = [csr1_interface_command, csr1_ipaddr_command, csr1_descr_command]
```

##### Step 12

Repeat Steps 10 and 11, but this time for **csr2**:

```python
csr2_interface_command = "interface {}".format(INTERFACE_MAP['csr2']['interface'])
csr2_ipaddr_command = "ip address {} {}".format(INTERFACE_MAP['csr2']['ipaddr'], INTERFACE_MAP["csr2"]["mask"])
csr2_descr_command = "description {}".format(INTERFACE_MAP['csr2']['description'])
csr2_commands = [csr2_interface_command, csr2_ipaddr_command, csr2_descr_command]
```

##### Step 13

Add necessary print statements to your script. You may want to print each command or the final commands list for each evice.

##### Step 14

Deploy the commands to each device using the `send_config_set` method:

```python
csr1.send_config_set(csr1_commands)
csr2.send_config_set(csr2_commands)
```

#### Step 15

Validate L2 reachability for these two interfaces.

```python
print(csr1.send_command("ping {}".format(INTERFACE_MAP['csr2']['ipaddr'])))
print(csr2.send_command("ping {}".format(INTERFACE_MAP['csr1']['ipaddr'])))
```


##### Step 16

Finally, disconnect from each device.

```python
csr1.disconnect()
csr2.disconnect()
```

##### Final Script

This should be the final script:

```python

from netmiko import ConnectHandler

INTERFACE_MAP = {
    "csr1":
        {
            "interface": "GigabitEthernet4",
            "ipaddr": "10.100.12.1",
            "mask": "255.255.255.0",
            "description": "Connect to csr2"
        },
    "csr2":
        {
            "interface": "GigabitEthernet4",
            "ipaddr": "10.100.12.2",
            "mask": "255.255.255.0",
            "description": "Connect to csr1"
        }
  }

csr1 = ConnectHandler(host='csr1', username='ntc', password='ntc123', device_type='cisco_ios')
csr2 = ConnectHandler(host='csr2', username='ntc', password='ntc123', device_type='cisco_ios')

csr1_interface_command = "interface {}".format(INTERFACE_MAP['csr1']['interface'])
csr1_ipaddr_command = "ip address {} {}".format(INTERFACE_MAP['csr1']['ipaddr'], INTERFACE_MAP["csr1"]["mask"])
csr1_descr_command = "description {}".format(INTERFACE_MAP['csr1']['description'])

csr1_commands = [csr1_interface_command, csr1_ipaddr_command, csr1_descr_command]

csr2_interface_command = "interface {}".format(INTERFACE_MAP['csr2']['interface'])
csr2_ipaddr_command = "ip address {} {}".format(INTERFACE_MAP['csr2']['ipaddr'], INTERFACE_MAP["csr2"]["mask"])
csr2_descr_command = "description {}".format(INTERFACE_MAP['csr2']['description'])
csr2_commands = [csr2_interface_command, csr2_ipaddr_command, csr2_descr_command]

csr1.send_config_set(csr1_commands)
csr2.send_config_set(csr2_commands)

print(csr1.send_command("ping {}".format(INTERFACE_MAP['csr2']['ipaddr'])))
print(csr2.send_command("ping {}".format(INTERFACE_MAP['csr1']['ipaddr'])))

csr1.disconnect()
csr2.disconnect()

```
