## Lab 17 - Re-factoring Code Using Loops

In the last lab, you learned how to use a for loop and looped over a list of strings, list of dictionaries, and even a dictionary.  You'll use that knowledge now to re-factor your last two challenge labs.

The solution for **Challenge Lab 13** looked like this:

```python
#! /usr/bin/env python

from netmiko import ConnectHandler

print("Connecting to device | CSR1")

csr1 = ConnectHandler(host='csr1', username='ntc', password='ntc123', device_type='cisco_ios')

print("Saving configuration | CSR1")

csr1.send_command("wr mem")

print("Backing up configuration | CSR1")

csr1.send_command("term len 0")
csr1_config = csr1.send_command("show run")

print("Writing config to file | CSR1\n")

with open("/home/ntc/scripts/configs/csr1.cfg", "w") as config_file:
    config_file.write(csr1_config)

print("Connecting to device | CSR2")

csr2 = ConnectHandler(host='csr2', username='ntc', password='ntc123', device_type='cisco_ios')

print("Saving configuration | CSR2")

csr2.send_command("wr mem")

print("Backing up configuration | CSR2")

csr2.send_command("term len 0")
csr2_config = csr1.send_command("show run")

print("Writing config to file | CSR2\n")

with open("/home/ntc/scripts/configs/csr1.cfg", "w") as config_file:
    config_file.write(csr2_config)

```


### Task 1 - Re-factor Challenge Lab 13

The goal is to update this script eliminating all of the duplicate code introducing a for loop that iterates over **csr1** and **csr2**.


##### Step 1

Perform a save-as on this file and save it as `backupv2.py`.

##### Step 2

Without changing anything for CSR2, create a list of one device (for testing) just after importing `ConnectHandler`:

```python
#! /usr/bin/env python

from netmiko import ConnectHandler

devices = ['csr1']

```

##### Step 3

Add a for loop that loops over `devices` and update all lines that have a "csr1" string in replacing it with the variable called `device` that will be in the for loop, e.g. `for device in devices:`

The updated script should look like this with all "csr1" strings removed:

```python
#! /usr/bin/env python

from netmiko import ConnectHandler

devices = ['csr1']

for device in devices:
    print("Connecting to device | {}".format(device))

    csr1 = ConnectHandler(host=device, username='ntc', password='ntc123', device_type='cisco_ios')

    print("Saving configuration | {}".format(device))

    csr1.send_command("wr mem")

    print("Backing up configuration | {}".format(device))

    csr1.send_command("term len 0")
    csr1_config = csr1.send_command("show run")

    print("Writing config to file | {}\n".format(device))

    with open("/home/ntc/scripts/configs/{}.cfg".format(device), "w") as config_file:
        config_file.write(csr1_config)

print("Connecting to device | CSR2")

csr2 = ConnectHandler(host='csr2', username='ntc', password='ntc123', device_type='cisco_ios')

print("Saving configuration | CSR2")

csr2.send_command("wr mem")

print("Backing up configuration | CSR2")

csr2.send_command("term len 0")
csr2_config = csr1.send_command("show run")

print("Writing config to file | CSR2\n")

with open("/home/ntc/scripts/configs/csr1.cfg", "w") as config_file:
    config_file.write(csr2_config)


```

##### Step 4

Execute the script ensuring it still works as expected:

```
ntc@ntc:scripts$ python backupv2.py
Connecting to device | csr1
Saving configuration | csr1
Backing up configuration | csr1
Writing config to file | csr1

Connecting to device | CSR2
Saving configuration | CSR2
Backing up configuration | CSR2
Writing config to file | CSR2
```

##### Step 5

Add "csr2" to the `devices` list created in Step 2 and repeat Steps 3 and 4 for "csr2".

Hopepfully you realize, you can delete all of the code for CSR2!

This is what what updated script should look like:

```python
#! /usr/bin/env python

from netmiko import ConnectHandler

devices = ['csr1', 'csr2']

for device in devices:
    print("Connecting to device | {}".format(device))

    csr1 = ConnectHandler(host=device, username='ntc', password='ntc123', device_type='cisco_ios')

    print("Saving configuration | {}".format(device))

    csr1.send_command("wr mem")

    print("Backing up configuration | {}".format(device))

    csr1.send_command("term len 0")
    csr1_config = csr1.send_command("show run")

    print("Writing config to file | {}\n".format(device))

    with open("/home/ntc/scripts/configs/{}.cfg".format(device), "w") as config_file:
        config_file.write(csr1_config)
```

##### Step 6

Since you're using a for loop now, you should clean up variable names so they don't refernce a particular device.  Change `csr1` to `net_device` and change `csr1_config` to `config`.

The updated script should look like this:

```python
#! /usr/bin/env python

from netmiko import ConnectHandler

devices = ['csr1', 'csr2']

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
```

##### Step 7

Save and backup the config for CSR3.

The only change you have to make is update the `devices` list to:

```python
devices = ['csr1', 'csr2' ,'csr3']
```

**Final Script:**

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
