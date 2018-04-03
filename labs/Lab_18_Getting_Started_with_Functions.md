## Lab 18 - Getting Started with Functions

This lab walks you through an introduction of using functions so you can start writing more modular code and eliminate any duplicate code in your scripts.

### Task 1 - Introduction to Functions

##### Step 1

In `scripts` directory, create a script called `functions.py`.

##### Step 2

Open the script in your text editor.

##### Step 3

Create a function that returns a hard-coded list of VLANs.  

* The function should be called  `get_vlans`
* The function should return the list that has VLANs 1, 5, 10, and 20.
* You should then call the function, save the list into a new variable called `vlans`, and print it out.

The script should look like this:

```python
#! /usr/bin/env python

def get_vlans():
    return [1, 5, 10, 20]

vlans = get_vlans()

print(vlans)
```

Save the script.

##### Step 4

Execute the script.  You'll see a basic output:

```
ntc@ntc:scripts$ python functions.py
[1, 5, 10, 20]
ntc@ntc:scripts$
```

##### Step 5

Add _another_ function called `vlan_exists`.  It should return `True` or `False` if the VLAN ID you pass into the function exists.

It should look like this:

```python
#! /usr/bin/env python

def get_vlans():
    return [1, 5, 10, 20]

vlans = get_vlans()

print(vlans)

def vlan_exists(vlan_id):
    return vlan_id in [1, 5, 10, 20]

print(vlan_exists(10))
print(vlan_exists(12))
```


Note you could have also broken it down in multiple statements like this:

```python
def vlan_exists(vlan_id):
    vlans = [1, 5, 10, 20]
    is_vlan_valid = vlan_id in vlans
    return is_vlan_valid
```


##### Step 6

Create a function that connects to a Cisco IOS device and call it `ez_cisco`.

`ez_cisco` should accept five parameters:
  * hostname of the device to connect to
  * username of the device
  * password of the device
  * show command to execute on the device

The function header and layout should look like this while just printing all parameter passed to the function:

```python
def ez_cisco(hostname, username, password, show_command):
    print(hostname)
    print(username)
    print(password)
    print(show_command)
```


You can test it by using the following statement:

```python
ez_cisco('csr1', 'ntc', 'ntc123', 'show version')
```

The updated script should look like this:

```python

#! /usr/bin/env python

def get_vlans():
    return [1, 5, 10, 20]

vlans = get_vlans()

print(vlans)

def vlan_exists(vlan_id):
    return vlan_id in [1, 5, 10, 20]

print(vlan_exists(10))
print(vlan_exists(12))

def ez_cisco(hostname, username, password, show_command):
    print(hostname)
    print(username)
    print(password)
    print(show_command)

ez_cisco('csr1', 'ntc', 'ntc123', 'show version')

```

##### Step 7

Save and Execute the script.  You should see the following:

```
ntc@ntc:scripts$ python functions.py
[1, 5, 10, 20]
True
False
csr1
ntc
ntc123
show version
ntc@ntc:scripts$
```

##### Step 8

Remove the latest function called `ez_cisco` and put it into a new script called `cisco-connect.py`.  The only code in that file should be the following:

```python
#! /usr/bin/env python

def ez_cisco(hostname, username, password, show_command):
    print(hostname)
    print(username)
    print(password)
    print(show_command)

ez_cisco('csr1', 'ntc', 'ntc123', 'show version')
```

##### Step 9

Make the following changes to the script:

* Import the `ConnectHandler` netmiko object
* Perform the desired action
* The function should return show command as a string
* Test the script by issuing the `show version` to **csr1**

```python
#! /usr/bin/env python

from netmiko import ConnectHandler

def ez_cisco(hostname, username, password, show_command):
    platform = "cisco_ios"
    device = ConnectHandler(ip=hostname, username=username, password=password, device_type=platform)

    output = device.send_command(show_command)
    device.disconnect()

    return output

response = ez_cisco('csr1', 'ntc', 'ntc123', 'show version')

print(response)
```


##### Step 10

Since the credentials are the same for all of our devices, we can treat them as "optional" arguments.  Let's update the function header so they are optional, but provide defaults of "ntc" and "ntc123" that the user can over-ride.

```python
#! /usr/bin/env python

from netmiko import ConnectHandler

def ez_cisco(hostname, show_command, username='ntc', password='ntc123'):
    platform = "cisco_ios"
    device = ConnectHandler(ip=hostname, username=username, password=password, device_type=platform)

    output = device.send_command(show_command)
    device.disconnect()

    return output

response = ez_cisco('csr1', 'show version')

print response
```

When you don't use "keyword" arguments, the arguments are positional and are required.  In order to accomplish this, we also needed to re-locate `show_command` as the second argument.

Now you only need to pass the hostname of the device and desired show command to run.

##### Step 11

Execute the following function calls in your script:

```python
response = ez_cisco('csr1', 'show version')
print response

response = ez_cisco('csr2', 'show ip int brief')
print response

response = ez_cisco('csr3', 'show run | inc snmp')
print response
```

The final script looks like this:

```python
#! /usr/bin/env python

from netmiko import ConnectHandler

def ez_cisco(hostname, show_command, username='ntc', password='ntc123'):
    platform = "cisco_ios"
    device = ConnectHandler(ip=hostname, username=username, password=password, device_type=platform)

    output = device.send_command(show_command)
    return output

response = ez_cisco('csr1', 'show version')
print response

response = ez_cisco('csr2', 'show ip int brief')
print response

response = ez_cisco('csr3', 'show run | inc snmp')
print response
```
