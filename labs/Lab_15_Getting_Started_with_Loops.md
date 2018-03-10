## Lab 15 - Getting Started with For Loops

This lab walks you through an introduction of using for loops iterating over a list of strings, a dictionaries, and finally, a list of dictionaries.

### Task 1 - Printing in a For Loop

The first task you will do is to loop through a list and print each element to the terminal.

##### Step 1

Create the following list of commands:

```python
>>> commands = ['interface Eth2/1', 'description Configured by Python', 'speed 100', 'duplex full']
>>> 
```

##### Step 2

Loop through `commands` and simply print each element out.

```python
>>> for command in commands:
...      print(command)
...
interface Eth2/1
description Configured by Python
speed 100
duplex full
>>>
```

##### Step 3

Now try this again using a different variable than `command`.  Use `for item in commands:` instead:

```python
>>> for item in commands:
...     print(item)
... 
interface Eth2/1
description Configured by Python
speed 100
duplex full
>>> 
```

Remember the variable that comes after the `for` keyword is arbitrary.

##### Step 4

Create a list of routers and loop through them printing the following status message for each device:

```
Connecting to device | csr1
```

But replace "csr1" with the correct hostname as your looping through.

```python
>>> routers = ['csr1', 'csr2', 'csr3']
>>> 
>>> for router in routers:
...     print("Connecting to device | {}".format(router))
... 
Connecting to device | csr1
Connecting to device | csr2
Connecting to device | csr3
>>> 
```

##### Step 5

Update the previous loop to ensure each hostname is "uppercase":

```python
>>> for router in routers:                               
...     print("Connecting to device | {}".format(router.upper()))
... 
Connecting to device | CSR1
Connecting to device | CSR2
Connecting to device | CSR3
>>> 
```


### Task 2 - Looping Over a Dictionary

##### Step 1

Create a dictionary that stores information about a network interface that will be configured.  The keys will be parameters/features and the values will be the specific commands to send to the device.

Create this dictionary:

```python
>>> interface = {}
>>> interface['duplex'] = 'full'
>>> interface['speed'] = '100'
>>> interface['description'] = 'Configured by Python'
>>>
>>> print(interface)
{'duplex': 'full', 'speed': '100', 'description': 'Configured by Python'}
>>>
```

##### Step 2

Loop through `interface`, print the keys, values, and then the keys and values together.

Print the Keys:

```python
>>> for key in interface.keys():
...      print(key)
...
duplex
speed
description
>>>
```

##### Step 3

Print the Values:

```python
>>> for value in interface.values():
...     print(value)
...
full
100
Configured by Python
>>>

```

##### Step 4

Print the Keys & Values:

```python
>>> for key, value in interface.items():
...     print key, value)
...
duplex full
speed 100)
description Configured by Python)
>>>
```

Note that using `items` gives you each to each `item` and remember that `items` returns a list of tuples (you can also think of this as a list of lists from a usability perspective). Here `key` maps to the first element in each tuple and `value` maps to the second in element in each tuple.

Remember `key` and `value` are user defined:

This also works just fine:

```python
>>> for feature, configured_value in interface.items():
...     print feature, configured_value
...
duplex full
speed 100)
description Configured by Python)
>>>
```

##### Step 5

Let's make this a little more challenging.  Let's loop through a nested dictionary.

We will re-use an object we used in an earlier lab.

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

Copy this into the Python shell.

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

##### Step 6

Loop through first by just printing each key on one line, the value on the next, followed by `-----` as an "item" delimiter.

```python
>>> for hostname, config in INTERFACE_MAP.items():
...     print hostname                            
...     print config                              
...     print '-----'                             
... 
csr1
{'interface': 'GigabitEthernet4', 'mask': '255.255.255.0', 'ipaddr': '10.100.12.1', 'description': 'Connect to csr2'}
-----
csr2
{'interface': 'GigabitEthernet4', 'mask': '255.255.255.0', 'ipaddr': '10.100.12.2', 'description': 'Connect to csr1'}
-----
>>> 
```

You can see that `hostname` is printing "csr1" and "csr2", e.g. they are they keys and then you can see that `config` is printing the whole value, which happens to be a dictionary itself.

##### Step 7

Looping over `INTERFACES_MAP`, only print the hostname and IP address for each device using the following print messages:

```
The IP address of csr1 is 10.100.12.1.
The IP address of csr2 is 10.100.12.2.
```


```python
>>> for hostname, config in INTERFACE_MAP.items():                            
...     print("The IP address of {} is {}.".format(hostname, config['ipaddr']))
... 
The IP address of csr1 is 10.100.12.1.
The IP address of csr2 is 10.100.12.2.
>>> 
```



### Task 3 - Looping over a List of Dictionaries

In this task, we will build a list of elements. Each element will represent a VLAN configuration, that consists of the `vlan id` and `vlan name`. 

##### Step 1
Create the vlan dictionaries:

``` python
>>> vlan10 = {'name': 'web', 'id': '10'}
>>> vlan20 = {'name': 'app', 'id': '20'}
>>> vlan30 = {'name': 'db', 'id': '30'}

```

##### Step 2

Create the list of VLANs.  Remember, this will be a list of dictionaries.

``` python
>>> vlans = [vlan10, vlan20, vlan30]
>>>
```

##### Step 3

Print the `vlans` variable to see what you just created:

```python
>>> print vlans
[{'name': 'web', 'id': '10'}, {'name': 'app', 'id': '20'}, {'name': 'db', 'id': '30'}]
>>>
```

##### Step 4

Pretty print the `vlans` list:

```python
>>> import json
>>> 
>>> print json.dumps(vlans, indent=4)
[
    {
        "name": "web", 
        "id": "10"
    }, 
    {
        "name": "app", 
        "id": "20"
    }, 
    {
        "name": "db", 
        "id": "30"
    }
]
>>> 
```

##### Step 5

Loop over `vlans` and simply print each element.

```python
>>> for vlan in vlans:
...     print(vlan)
... 
{'name': 'web', 'id': '10'}
{'name': 'app', 'id': '20'}
{'name': 'db', 'id': '30'}
>>> 
```

You can see that each element is a dictionary.

##### Step 6

You can verify it by using the `type()` statement in the for loop.

```python
>>> for vlan in vlans:   
...     print(vlan)
...     print(type(vlan))
... 
{'name': 'web', 'id': '10'}
<type 'dict'>
{'name': 'app', 'id': '20'}
<type 'dict'>
{'name': 'db', 'id': '30'}
<type 'dict'>
>>> 
```

##### Step 7

Since you understand the data type of this object now, print the following by using a for loop:

```
vlan 10
 name web
vlan 20
 name app
vlan 30
 name db
```

``` python
>>> for vlan in vlans:
...     print("vlan {}".format(vlan['id']))
...     print(" name {}".format(vlan['name']))
... 
vlan 10
 name web
vlan 20
 name app
vlan 30
 name db
>>> 
```

