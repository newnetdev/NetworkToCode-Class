## Lab 18 - Re-factoring Code with Functions

In the last lab, you learned how to use functions and even created a small functions that connects to devices using Netmiko.  You'll use that knowledge now to re-factor and modularize the two scripts.

### Task 1 - Modularize the Backup Script

##### Step 1

We will begin with a backup script that looks like this:

```python
#! /usr/bin/env python

from netmiko import ConnectHandler

devices = ['csr1', 'csr2', 'csr3']

for device in devices:
    print("Connecting to device | {}".format(device))

    net_device = ConnectHandler(host=device, username='ntc', password='ntc123', device_type='cisco_ios')

    print("Saving configuration | {}".format(device))

    net_device.send_command("wr mem")

    print("Backing up configuration | {}".format(device))

    net_device.send_command("term len 0")
    config = net_device.send_command("show run")

    print("Writing config to file | {}\n".format(device))

    with open("/home/ntc/scripts/configs/{}.cfg".format(device), "w") as config_file:
        config_file.write(config)

    net_device.disconnect()


```

Open this script and save it as `backupv3.py`

##### Step 2

As you can see, there are logical distinctions to the actions actually being performed here.  They are Connecting to the device, Saving the configuration, Backing up the configuration, and writing the config to a file.  This is a good way to start to thinking about functions.  We'll also create a function called `main()` that'll act as the "beginning" of the program.

First let's start by creating `main()`.  Simply put everything into `main()` and then call the function at the bottom of the script.

It should look like this:

```python
#! /usr/bin/env python

from netmiko import ConnectHandler

def main():
    devices = ['csr1', 'csr2', 'csr3']

    for device in devices:
        print("Connecting to device | {}".format(device))

        net_device = ConnectHandler(host=device, username='ntc', password='ntc123', device_type='cisco_ios')

        print("Saving configuration | {}".format(device))

        net_device.send_command("wr mem")

        print("Backing up configuration | {}".format(device))

        net_device.send_command("term len 0")
        config = net_device.send_command("show run")

        print("Writing config to file | {}\n".format(device))

        with open("/home/ntc/scripts/configs/{}.cfg".format(device), "w") as config_file:
            config_file.write(config)

        net_device.disconnect()

main()
```

##### Step 3

Add a function called `connect_to_device` that looks like this:

```python
def connect_to_device(hostname):
    print("Connecting to device | {}".format(device))
    device = ConnectHandler(host=hostname, username='ntc', password='ntc123', device_type='cisco_ios')

    return device
```

Notice that we'll receive the hostname of the device, use that to connect witih netmiko, and return the actual "device object".

> Note: a few variable names changed to ensure you understand which variables can be accessed inside and outside of the functions.

The updated script looks like this:

```python
#! /usr/bin/env python

from netmiko import ConnectHandler

def connect_to_device(hostname):
    print("Connecting to device | {}".format(hostname))
    net_d = ConnectHandler(host=hostname, username='ntc', password='ntc123', device_type='cisco_ios')

    return net_d

def main():
    devices = ['csr1', 'csr2', 'csr3']

    for device in devices:

        net_device = connect_to_device(device)

        print("Saving configuration | {}".format(device))
        net_device.send_command("wr mem")

        print("Backing up configuration | {}".format(device))

        net_device.send_command("term len 0")
        config = net_device.send_command("show run")

        print("Writing config to file | {}\n".format(device))

        with open("/home/ntc/scripts/configs/{}.cfg".format(device), "w") as config_file:
            config_file.write(config)

        net_device.disconnect()

main()
```

##### Step 4

Add another three functions called `save_config`, `backup_config`, `write_to_file`.

In this step, we'll just perform the work for `save_config` and use a `pass` statement in Python to allow us to prep the ground work for the next two Steps beyond this one.


```python
#! /usr/bin/env python

from netmiko import ConnectHandler

def connect_to_device(hostname):
    print("Connecting to device | {}".format(hostname))
    net_d = ConnectHandler(host=hostname, username='ntc', password='ntc123', device_type='cisco_ios')

    return net_d

def save_config(device, hostname):
    print("Saving configuration | {}".format(hostname))
    device.send_command("wr mem")

def backup_config(device, hostname):
    pass

def write_to_file():
    pass

def main():
    devices = ['csr1', 'csr2', 'csr3']

    for device in devices:
        net_device = connect_to_device(device)

        save_config(net_device, device)

        print("Backing up configuration | {}".format(device))
        net_device.send_command("term len 0")
        config = net_device.send_command("show run")

        print("Writing config to file | {}\n".format(device))
        with open("/home/ntc/scripts/configs/{}.cfg".format(device), "w") as config_file:
            config_file.write(config)

        net_device.disconnect()

main()

```

##### Step 5

Next, we need to add the code for the `backup_config` function.

```python
def backup_config(device, hostname):
    print("Backing up configuration | {}".format(hostname))
    device.send_command("term len 0")
    config = device.send_command("show run")

    return config
```

The associated `main()` function would need to be changed to the following too:

```python
def main():
    devices = ['csr1', 'csr2', 'csr3']

    for device in devices:
        net_device = connect_to_device(device)
        save_config(net_device, device)

        config = backup_config(net_device, device)

        print("Writing config to file | {}\n".format(device))
        with open("/home/ntc/scripts/configs/{}.cfg".format(device), "w") as config_file:
            config_file.write(config)

        net_device.disconnect()
```

##### Step 6

Update the `write_to_file` function so it includes the following:

```python
def write_to_file(hostname, show_run):
    print("Writing config to file | {}\n".format(hostname))
    with open("/home/ntc/scripts/configs/{}.cfg".format(hostname), "w") as config_file:
        config_file.write(show_run)
```


The final script after updating `main()` should look like this:

```python
#! /usr/bin/env python

from netmiko import ConnectHandler

def connect_to_device(hostname):
    print("Connecting to device | {}".format(hostname))
    net_d = ConnectHandler(host=hostname, username='ntc', password='ntc123', device_type='cisco_ios')

    return net_d

def save_config(device, hostname):
    print("Saving configuration | {}".format(hostname))
    device.send_command("wr mem")

def backup_config(device, hostname):
    print("Backing up configuration | {}".format(hostname))
    device.send_command("term len 0")
    config = device.send_command("show run")

    return config

def write_to_file(hostname, show_run):
    print("Writing config to file | {}\n".format(hostname))
    with open("/home/ntc/scripts/configs/{}.cfg".format(hostname), "w") as config_file:
        config_file.write(show_run)

def main():
    devices = ['csr1', 'csr2', 'csr3']

    for device in devices:
        net_device = connect_to_device(device)

        save_config(net_device, device)

        config = backup_config(net_device, device)

        write_to_file(device, config)

        net_device.disconnect()

main()
```

As you can tell, this code is much more modular and you can now re-use these functions as you need too, for example, if you need to do another save or backup somewhere else in the script.


### Task 2 - Modularize the SNMP Deploy

##### Step 1

Now we will modularixe an SNMP Deploy script.  The starting script looks like this:

```python
from netmiko import ConnectHandler

devices = ['csr1', 'csr2', 'csr3']

for device in devices:
    print("Connecting to device | {}".format(device))
    net_device = ConnectHandler(host=device, username='ntc', password='ntc123', device_type='cisco_ios')

    print("Sending commands from file | {}".format(device))
    net_device.send_config_from_file("./configs/snmp.cfg")

    print("Disconnecting from device | {}".format(device))
    net_device.disconnect()
```

##### Step 2

Re-factor this script including the following functions:
  * `main()` - to act as the main program
  * `connect_to_device()` - same as last Task
  * `deploy_commands` - which will send the commands from the file

Scroll for the solution.

```
.













































```

##### Step 3

You would end up with something like this:

```python
from netmiko import ConnectHandler


def connect_to_device(hostname):
    print("Connecting to device | {}".format(hostname))
    net_d = ConnectHandler(host=hostname, username='ntc', password='ntc123', device_type='cisco_ios')

    return net_d

def deploy_commands(device, hostname):
    print("Sending commands from file | {}".format(hostname))
    device.send_config_from_file("./configs/snmp.cfg")

def main():
    devices = ['csr1', 'csr2', 'csr3']

    for device in devices:
        net_device = connect_to_device(device)

        deploy_commands(net_device, device)

        print("Disconnecting from device | {}".format(device))
        net_device.disconnect()

main()
```

##### Step 4

But note, you should also parameterize the filename you'd like to deploy from like this:

```python
from netmiko import ConnectHandler


def connect_to_device(hostname):
    print("Connecting to device | {}".format(hostname))
    net_d = ConnectHandler(host=hostname, username='ntc', password='ntc123', device_type='cisco_ios')

    return net_d

def deploy_commands(device, hostname, config_file):
    print("Sending commands from file | {}".format(hostname))
    device.send_config_from_file(config_file)

def main():
    devices = ['csr1', 'csr2', 'csr3']

    config_file = './configs/snmp.cfg'

    for device in devices:
        net_device = connect_to_device(device)

        deploy_commands(net_device, device, config_file)

        print("Disconnecting from device | {}".format(device))
        net_device.disconnect()

main()
```

##### Step 5

You could even create a function for the print messages since they are standard--the only difference is the actual message.  This even has a function calling a function (note inside `connect_to_device` is calling `print_logger`)

Let's take a look:

```python
from netmiko import ConnectHandler


def connect_to_device(hostname):
    message = "Connecting to device"
    print_logger(message, hostname)
    net_d = ConnectHandler(host=hostname, username='ntc', password='ntc123', device_type='cisco_ios')

    return net_d

def deploy_commands(device, hostname, config_file):
    print("Sending commands from file | {}".format(hostname))
    device.send_config_from_file(config_file)

def print_logger(message, hostname):
    print("{} | {}".format(message, hostname))

def main():
    devices = ['csr1', 'csr2', 'csr3']

    config_file = './configs/snmp.cfg'

    for device in devices:
        net_device = connect_to_device(device)

        deploy_commands(net_device, device, config_file)

        print_logger("Disconnecting from device", device)
        net_device.disconnect()

main()
```

