## Lab 9 - Exploring Nested Objects

### Task 1 - Nested Dictionary Objects

##### Step 1

Create a variable called `facts_list` that has the following value:

```python
facts_list = [{'customer': 'acme', 'vendor': 'arista', 'hostname': 'APAC1', 'location': 'Sydney', 'device_type': 'switch', 'model': '7050', 'os': 'eos'}, {'customer': 'acme', 'vendor': 'juniper', 'hostname': 'EMEA1', 'location': 'London', 'device_type': 'switch', 'model': 'mx', 'os': 'junos'}, {'customer': 'acme', 'vendor': 'cisco', 'hostname': 'nycr01', 'location': 'new_york', 'device_type': 'switch', 'model': 'catalyst', 'os': 'ios'}]
```

##### Step 2

Pretty print `facts_list` by using `json.dumps`

```python
>>> import json
>>> 
>>> print json.dumps(facts_list, indent=4)
[
    {
        "customer": "acme", 
        "vendor": "arista", 
        "hostname": "APAC1", 
        "location": "Sydney", 
        "device_type": "switch", 
        "model": "7050", 
        "os": "eos"
    }, 
    {
        "customer": "acme", 
        "vendor": "juniper", 
        "hostname": "EMEA1", 
        "location": "London", 
        "device_type": "switch", 
        "model": "mx", 
        "os": "junos"
    }, 
    {
        "customer": "acme", 
        "vendor": "cisco", 
        "hostname": "nycr01", 
        "location": "new_york", 
        "device_type": "switch", 
        "model": "catalyst", 
        "os": "ios"
    }
]
>>> 
```


##### Step 3

Can you tell this is a list of dictionaries? 

* You can tell this visually by seeing the object start with square brackets
* You can also do a type check!

##### Step 4

Do a type check on `facts_list`:

```python
>>> type(facts_list)
<type 'list'>
>>> 
```

We now know it's a list, but what is it a list of?  Generally speaking, you _wouldn't_ have a list of different data types.  We'll make the assumption every element is of the same data type for now.

##### Step 5

First, do a length check of `facts_list`:

```python
>>> len(facts_list)
3
>>> 
```

You know there are 3 elements now.  Let's check the first one.

##### Step 6

In this step, we'll just check the data type of the first element in the list.

```python
>>> type(facts_list[0])
<type 'dict'>
>>> 
```

OR

```python
>>> first = facts_list[0]
>>> 
>>> type(first)
<type 'dict'>
>>> 
```

We can tell now that this object is a list of dictionaries.

##### Step 7

Our goal is to print out the "location" of the "APAC1" device. 

To do this, you will need to reference the visual print out and see that it's the _first_ element or the element that has an index value of zero.

First, print out the whole first element:

```python
>>> print(facts_list[0])
{'customer': 'acme', 'vendor': 'arista', 'hostname': 'APAC1', 'location': 'Sydney', 'device_type': 'switch', 'model': '7050', 'os': 'eos'}
>>> 
```

##### Step 8

You can see that a dictionary is returned since the element begins with curly brackets.  Let's print out the location.

```python
>>> print(facts_list[0]['location'])
Sydney
>>> 
```

Notice how we have `[0]` and `['location']` in the same print statement.  You need to be very careful and understand the data type for each element inside a nested object.

Let's continue to build onto this.

##### Step 9

Create two new dictionary objects that depict the attributes of neighbor devices and then print them out.

```python
>>> neighbor1 = {'neighbor_interface': 'Eth1/2', 'local_interface': 'Eth1/1', 'neighbor'
: 'R1'}
>>> 
>>> neighbor2 = {'neighbor_interface': 'Eth1/4', 'local_interface': 'Eth1/2', 'neighbor'
: 'R2'}
>>>
```

##### Step 10

Create a list that is comprised of these neighbors.

```python
>>> neighbors = [neighbor1, neighbor2]
>>> 
```

##### Step 11

Print `neighbors` to see the newly formed list:

```python
>>> print(neighbors)
[{'neighbor_interface': 'Eth1/2', 'local_interface': 'Eth1/1', 'neighbor': 'R1'}, {'neighbor_interface': 'Eth1/4', 'local_interface': 'Eth1/2', 'neighbor': 'R2'}]
>>> 
```

Now pretty print them:

```python
>>> print(json.dumps(neighbors, indent=4))
[
    {
        "neighbor_interface": "Eth1/2", 
        "local_interface": "Eth1/1", 
        "neighbor": "R1"
    }, 
    {
        "neighbor_interface": "Eth1/4", 
        "local_interface": "Eth1/2", 
        "neighbor": "R2"
    }
]
>>> 
```

Remember to always pretty print complex objects as it makes them much easier to read.

Nothing new yet--you just created an isolated list of two dictionaries that represent neighbors of a given device.



##### Step 12

These neighbors created are the simulated neighbors of "APAC1" which is the device in `facts_list[0]`, i.e. the first element of `facts_list`.

Now add the `neighbors` list as a key/value pair in the dictionary that APAC1 is currently part of.  Use the `neighbors` key.

```python
>>> facts_list[0]['neighbors'] = neighbors
>>> 
```

Think about this:
  * `facts_list` is a list of dictionaries
  * `facts_list[0]` is a dictionary
  * We know to add key-value pairs to a dictionary, we use:
    *  `dict[key] = "value"`
  *  Knowing this, we can add the new key called `neighbors` and assign it the value of the variable that just happen to also be called `neighbors`


##### Step 13

Pretty print the `facts_list` to see the newly updated dictionary.

```python
>>> print(json.dumps(facts_list, indent=4))
[
    {
        "customer": "acme", 
        "neighbors": [
            {
                "neighbor_interface": "Eth1/2", 
                "local_interface": "Eth1/1", 
                "neighbor": "R1"
            }, 
            {
                "neighbor_interface": "Eth1/4", 
                "local_interface": "Eth1/2", 
                "neighbor": "R2"
            }
        ], 
        "vendor": "arista", 
        "hostname": "APAC1", 
        "location": "Sydney", 
        "device_type": "switch", 
        "model": "7050", 
        "os": "eos"
    }, 
    {
        "customer": "acme", 
        "vendor": "juniper", 
        "hostname": "EMEA1", 
        "location": "London", 
        "device_type": "switch", 
        "model": "mx", 
        "os": "junos"
    }, 
    {
        "customer": "acme", 
        "vendor": "cisco", 
        "hostname": "nycr01", 
        "location": "new_york", 
        "device_type": "switch", 
        "model": "catalyst", 
        "os": "ios"
    }
]
>>> 

```

This gives a better look at the complete object.

Notice how nested this object became now?


##### Step 14

Now print just the hostname of the second neighbor of "APAC1".

```python
>>> print(facts_list[0]['neighbors'][1]['neighbor'])
R2
>>>
```

Take your time to ensure you understand how we are accessing "R2".  

Understanding nested lists and dictionary objects are very important to use network APIs as you'll often get back a list of dictionaries for interfaces and neighbors, as an example.

In the next Task, we'll walk through a more gradual process helpful with parsing complex nested objects.

### Task 2 - Working with a Nested Facts Dictionary Object

##### Step 1

Enter the Python shell and import the `json` module.

```python
$ python
Python 2.7.6 (default, Jun 22 2015, 17:58:13) 
[GCC 4.8.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>>
>>> import json
>>> 
```

##### Step 2

Create a new variable called `content` and assign the following object like so:

```python
content = {'output': {'ansible_facts': {'fan_info': [{'status': 'Ok', 'model': None, 'hw_ver': '0.0', 'name': 'ChassisFan1'}, {'status': 'None', 'model': None, 'hw_ver': '0.0', 'name': 'ChassisFan2'}, {'status': 'Ok', 'model': '--', 'hw_ver': '--', 'name': 'Fan_in_PS1'}, {'status': 'Failure', 'model': '--', 'hw_ver': '--', 'name': 'Fan_in_PS2'}], 'ansible_net_model': 'NX-OSv Chassis', 'ansible_net_interfaces': {'Ethernet2/13': {'macaddress': '2cc2.604f.feb2', 'state': 'down', 'mode': 'routed', 'duplex': 'auto', 'speed': 'auto-speed', 'type': 'Ethernet', 'bandwidth': 1000000, 'mtu': '1500'}, 'Ethernet2/12': {'macaddress': '2cc2.604f.feb2', 'state': 'down', 'mode': 'routed', 'duplex': 'auto', 'speed': 'auto-speed', 'type': 'Ethernet', 'bandwidth': 1000000, 'mtu': '1500'}, 'Ethernet2/11': {'macaddress': '2cc2.604f.feb2', 'state': 'down', 'mode': 'routed', 'duplex': 'auto', 'speed': 'auto-speed', 'type': 'Ethernet', 'bandwidth': 1000000, 'mtu': '1500'}, 'Ethernet2/10': {'macaddress': '2cc2.604f.feb2', 'state': 'down', 'mode': 'routed', 'duplex': 'auto', 'speed': 'auto-speed', 'type': 'Ethernet', 'bandwidth': 1000000, 'mtu': '1500'}, 'Ethernet2/15': {'macaddress': '2cc2.604f.feb2', 'state': 'down', 'mode': 'routed', 'duplex': 'auto', 'speed': 'auto-speed', 'type': 'Ethernet', 'bandwidth': 1000000, 'mtu': '1500'}, 'Ethernet2/14': {'macaddress': '2cc2.604f.feb2', 'state': 'down', 'mode': 'routed', 'duplex': 'auto', 'speed': 'auto-speed', 'type': 'Ethernet', 'bandwidth': 1000000, 'mtu': '1500'}, 'Ethernet2/1': {'macaddress': '2cc2.604f.feb2', 'state': 'up', 'mode': 'routed', 'duplex': 'full', 'speed': '1000 Mb/s', 'type': 'Ethernet', 'bandwidth': 1000000, 'mtu': '1500'}}, 'ansible_net_all_ipv4_addresses': ['10.0.0.71'], 'ansible_net_hostname': 'nxos-spine1', 'hostname': 'nxos-spine1', 'ansible_net_serialnum': 'TM6017D760B', 'interfaces_list': ['mgmt0', 'Ethernet2/1', 'Ethernet2/2', 'Ethernet2/3', 'Ethernet2/4', 'Ethernet2/5', 'Ethernet2/6', 'Ethernet2/7', 'Ethernet2/8', 'Ethernet2/9', 'Ethernet2/10', 'Ethernet2/11', 'Ethernet2/12', 'Ethernet2/13', 'Ethernet2/14', 'Ethernet2/15'], 'ansible_net_gather_subset': ['hardware', 'default', 'interfaces', 'legacy'], 'power_supply_info': [{'status': 'Ok', 'model': 'DS-CAC-845W', 'number': 1}, {'status': 'Absent', 'model': '------------', 'number': 2}], 'platform': 'NX-OSv Chassis', 'ansible_net_version': '7.3(1)D1(1) [build 7.3(1)D1(0.10)]', 'module': [{'status': 'active *', 'model': 'N7K-SUP1', 'type': 'NX-OSv Supervisor Module', 'ports': 0}, {'status': 'ok', 'model': 'N7K-F248XP-25', 'type': 'NX-OSv Ethernet Module', 'ports': 48}, {'status': 'ok', 'model': 'N7K-F248XP-25', 'type': 'NX-OSv Ethernet Module', 'ports': 48}, {'status': 'ok', 'model': 'N7K-F248XP-25', 'type': 'NX-OSv Ethernet Module', 'ports': 48}], 'ansible_net_all_ipv6_addresses': [], 'ansible_net_memtotal_mb': 3908, 'ansible_net_filesystems': ['bootflash:'], 'ansible_net_image': 'bootflash:///titanium-d1.7.3.1.D1.0.10.bin', 'os': '7.3(1)D1(1) [build 7.3(1)D1(0.10)]', 'vlan_list': [1]}}}
>>>
```

##### Step 3

As you can see it's a very long and what seems to be a complex object.  Let's simplify it and pretty print it.

```python
>>> print json.dumps(content, indent=4)
{
    "output": {
        "ansible_facts": {
            "fan_info": [
                {
                    "status": "Ok", 
                    "model": null, 
                    "hw_ver": "0.0", 
                    "name": "ChassisFan1"
                }, 
                {
                    "status": "None", 
                    "model": null, 
                    "hw_ver": "0.0", 
                    "name": "ChassisFan2"
                }, 
                {
                    "status": "Ok", 
                    "model": "--", 
                    "hw_ver": "--", 
                    "name": "Fan_in_PS1"
                }, 
                {
                    "status": "Failure", 
                    "model": "--", 
                    "hw_ver": "--", 
                    "name": "Fan_in_PS2"
                }
            ], 
            "hostname": "nxos-spine1", 
            "ansible_net_serialnum": "TM6017D760B", 
            "platform": "NX-OSv Chassis", 
            "ansible_net_all_ipv4_addresses": [
                "10.0.0.71"
            ], 
            "ansible_net_model": "NX-OSv Chassis", 
            "ansible_net_hostname": "nxos-spine1", 
            "interfaces_list": [
                "mgmt0", 
                "Ethernet2/1", 
                "Ethernet2/2", 
                "Ethernet2/3", 
                "Ethernet2/4", 
                "Ethernet2/5", 
                "Ethernet2/6", 
                "Ethernet2/7", 
                "Ethernet2/8", 
                "Ethernet2/9", 
                "Ethernet2/10", 
                "Ethernet2/11", 
                "Ethernet2/12", 
                "Ethernet2/13", 
                "Ethernet2/14", 
                "Ethernet2/15"
            ], 
            "ansible_net_gather_subset": [
                "hardware", 
                "default", 
                "interfaces", 
                "legacy"
            ], 
            "power_supply_info": [
                {
                    "status": "Ok", 
                    "model": "DS-CAC-845W", 
                    "number": 1
                }, 
                {
                    "status": "Absent", 
                    "model": "------------", 
                    "number": 2
                }
            ], 
            "ansible_net_interfaces": {
                "Ethernet2/13": {
                    "macaddress": "2cc2.604f.feb2", 
                    "state": "down", 
                    "mode": "routed", 
                    "duplex": "auto", 
                    "type": "Ethernet", 
                    "speed": "auto-speed", 
                    "bandwidth": 1000000, 
                    "mtu": "1500"
                }, 
                "Ethernet2/12": {
                    "macaddress": "2cc2.604f.feb2", 
                    "state": "down", 
                    "mode": "routed", 
                    "duplex": "auto", 
                    "type": "Ethernet", 
                    "speed": "auto-speed", 
                    "bandwidth": 1000000, 
                    "mtu": "1500"
                }, 
                "Ethernet2/11": {
                    "macaddress": "2cc2.604f.feb2", 
                    "state": "down", 
                    "mode": "routed", 
                    "duplex": "auto", 
                    "type": "Ethernet", 
                    "speed": "auto-speed", 
                    "bandwidth": 1000000, 
                    "mtu": "1500"
                }, 
                "Ethernet2/10": {
                    "macaddress": "2cc2.604f.feb2", 
                    "state": "down", 
                    "mode": "routed", 
                    "duplex": "auto", 
                    "type": "Ethernet", 
                    "speed": "auto-speed", 
                    "bandwidth": 1000000, 
                    "mtu": "1500"
                }, 
                "Ethernet2/15": {
                    "macaddress": "2cc2.604f.feb2", 
                    "state": "down", 
                    "mode": "routed", 
                    "duplex": "auto", 
                    "type": "Ethernet", 
                    "speed": "auto-speed", 
                    "bandwidth": 1000000, 
                    "mtu": "1500"
                }, 
                "Ethernet2/14": {
                    "macaddress": "2cc2.604f.feb2", 
                    "state": "down", 
                    "mode": "routed", 
                    "duplex": "auto", 
                    "type": "Ethernet", 
                    "speed": "auto-speed", 
                    "bandwidth": 1000000, 
                    "mtu": "1500"
                }, 
                "Ethernet2/1": {
                    "macaddress": "2cc2.604f.feb2", 
                    "state": "up", 
                    "mode": "routed", 
                    "duplex": "full", 
                    "type": "Ethernet", 
                    "speed": "1000 Mb/s", 
                    "bandwidth": 1000000, 
                    "mtu": "1500"
                }
            }, 
            "ansible_net_version": "7.3(1)D1(1) [build 7.3(1)D1(0.10)]", 
            "module": [
                {
                    "status": "active *", 
                    "model": "N7K-SUP1", 
                    "type": "NX-OSv Supervisor Module", 
                    "ports": 0
                }, 
                {
                    "status": "ok", 
                    "model": "N7K-F248XP-25", 
                    "type": "NX-OSv Ethernet Module", 
                    "ports": 48
                }, 
                {
                    "status": "ok", 
                    "model": "N7K-F248XP-25", 
                    "type": "NX-OSv Ethernet Module", 
                    "ports": 48
                }, 
                {
                    "status": "ok", 
                    "model": "N7K-F248XP-25", 
                    "type": "NX-OSv Ethernet Module", 
                    "ports": 48
                }
            ], 
            "ansible_net_all_ipv6_addresses": [], 
            "ansible_net_memtotal_mb": 3908, 
            "ansible_net_filesystems": [
                "bootflash:"
            ], 
            "ansible_net_image": "bootflash:///titanium-d1.7.3.1.D1.0.10.bin", 
            "os": "7.3(1)D1(1) [build 7.3(1)D1(0.10)]", 
            "vlan_list": [
                1
            ]
        }
    }
}
>>>
```


##### Step 4

You can see that `content` is a dictionary with a single key called `output`, and multiple levels of nested objects. Scroll back up and/or open this file in your text editor to visually see that.

##### Step 5

After visually seeing it, we'll prove it.

Print its length using the `len()` function.

```python
>>> len(content)
1
>>>
```

This confirms that the outer dictionary is composed of only one "root" key.  In other words, there is only ONE item--one item means, one key and one value.  The value just happens to be a very nested object.

##### Step 6

Verify the single key of the dictionary by using the `values` method.

```python
>>> print(content.keys())
['output']
>>>
```

This is exactly what we said in Step 4.

##### Step 7

Let's extract the value of the `output` key by now saving it into a new variable called `output`.

```python
>>> output = content['output']
>>> 
```

You can repeat the steps 5 - 7 for every element in this object.

Check the data type and check the length.  If it's a list, you'll need to extract the value using an index (integer) value.  If it's a dictionary, you'll need to supply a key to extract the value, and remember, you can see all available keys by using the `keys()` method.

**This workflow can be repeated until you get to the data you're looking for.**

Let's try it.

```python
>>> type(output)
<type 'dict'>
>>> 
```

Now that you  know it's a dictionary, print the keys.

```python
>>> print(output.keys())
['ansible_facts']
>>> 
```

Let's continue and print `output`.

##### Step 8

Pretty print the new variable called `output`.


```python
>>> print(json.dumps(output, indent=4))
{
    "ansible_facts": {
        "fan_info": [
            {
                "status": "Ok", 
                "model": null, 
                "hw_ver": "0.0", 
                "name": "ChassisFan1"
            }, 
            {
                "status": "None", 
                "model": null, 
                "hw_ver": "0.0", 
                "name": "ChassisFan2"
            }, 
            {
                "status": "Ok", 
                "model": "--", 
                "hw_ver": "--", 
                "name": "Fan_in_PS1"
            }, 
            {
                "status": "Failure", 
                "model": "--", 
                "hw_ver": "--", 
                "name": "Fan_in_PS2"
            }
        ], 
        "hostname": "nxos-spine1", 
        "ansible_net_serialnum": "TM6017D760B", 
        "platform": "NX-OSv Chassis", 
        "ansible_net_all_ipv4_addresses": [
            "10.0.0.71"
        ], 
        "ansible_net_model": "NX-OSv Chassis", 
        "ansible_net_hostname": "nxos-spine1", 
        "interfaces_list": [
            "mgmt0", 
            "Ethernet2/1", 
            "Ethernet2/2", 
            "Ethernet2/3", 
            "Ethernet2/4", 
            "Ethernet2/5", 
            "Ethernet2/6", 
            "Ethernet2/7", 
            "Ethernet2/8", 
            "Ethernet2/9", 
            "Ethernet2/10", 
            "Ethernet2/11", 
            "Ethernet2/12", 
            "Ethernet2/13", 
            "Ethernet2/14", 
            "Ethernet2/15"
        ], 
        "ansible_net_gather_subset": [
            "hardware", 
            "default", 
            "interfaces", 
            "legacy"
        ], 
        "power_supply_info": [
            {
                "status": "Ok", 
                "model": "DS-CAC-845W", 
                "number": 1
            }, 
            {
                "status": "Absent", 
                "model": "------------", 
                "number": 2
            }
        ], 
        "ansible_net_interfaces": {
            "Ethernet2/13": {
                "macaddress": "2cc2.604f.feb2", 
                "duplex": "auto", 
                "type": "Ethernet", 
                "state": "down", 
                "mtu": "1500", 
                "bandwidth": 1000000, 
                "mode": "routed", 
                "speed": "auto-speed"
            }, 
            "Ethernet2/12": {
                "macaddress": "2cc2.604f.feb2", 
                "duplex": "auto", 
                "type": "Ethernet", 
                "state": "down", 
                "mtu": "1500", 
                "bandwidth": 1000000, 
                "mode": "routed", 
                "speed": "auto-speed"
            }, 
            "Ethernet2/11": {
                "macaddress": "2cc2.604f.feb2", 
                "duplex": "auto", 
                "type": "Ethernet", 
                "state": "down", 
                "mtu": "1500", 
                "bandwidth": 1000000, 
                "mode": "routed", 
                "speed": "auto-speed"
            }, 
            "Ethernet2/10": {
                "macaddress": "2cc2.604f.feb2", 
                "duplex": "auto", 
                "type": "Ethernet", 
                "state": "down", 
                "mtu": "1500", 
                "bandwidth": 1000000, 
                "mode": "routed", 
                "speed": "auto-speed"
            }, 
            "Ethernet2/15": {
                "macaddress": "2cc2.604f.feb2", 
                "duplex": "auto", 
                "type": "Ethernet", 
                "state": "down", 
                "mtu": "1500", 
                "bandwidth": 1000000, 
                "mode": "routed", 
                "speed": "auto-speed"
            }, 
            "Ethernet2/14": {
                "macaddress": "2cc2.604f.feb2", 
                "duplex": "auto", 
                "type": "Ethernet", 
                "state": "down", 
                "mtu": "1500", 
                "bandwidth": 1000000, 
                "mode": "routed", 
                "speed": "auto-speed"
            }, 
            "Ethernet2/1": {
                "macaddress": "2cc2.604f.feb2", 
                "duplex": "full", 
                "type": "Ethernet", 
                "state": "up", 
                "mtu": "1500", 
                "bandwidth": 1000000, 
                "mode": "routed", 
                "speed": "1000 Mb/s"
            }
        }, 
        "ansible_net_version": "7.3(1)D1(1) [build 7.3(1)D1(0.10)]", 
        "module": [
            {
                "status": "active *", 
                "model": "N7K-SUP1", 
                "type": "NX-OSv Supervisor Module", 
                "ports": 0
            }, 
            {
                "status": "ok", 
                "model": "N7K-F248XP-25", 
                "type": "NX-OSv Ethernet Module", 
                "ports": 48
            }, 
            {
                "status": "ok", 
                "model": "N7K-F248XP-25", 
                "type": "NX-OSv Ethernet Module", 
                "ports": 48
            }, 
            {
                "status": "ok", 
                "model": "N7K-F248XP-25", 
                "type": "NX-OSv Ethernet Module", 
                "ports": 48
            }
        ], 
        "ansible_net_all_ipv6_addresses": [], 
        "ansible_net_memtotal_mb": 3908, 
        "ansible_net_filesystems": [
            "bootflash:"
        ], 
        "ansible_net_image": "bootflash:///titanium-d1.7.3.1.D1.0.10.bin", 
        "os": "7.3(1)D1(1) [build 7.3(1)D1(0.10)]", 
        "vlan_list": [
            1
        ]
    }
}
```

##### Step 9

This is again a dictionary of one _root_ key, `ansible_facts`, whose value is still a dictionary, which you saw in Step 10 by printing all keys of `output`.  You could verify it with `len()` too.

Repeat the step by step process as necessary in order to print just the value of the `fan_info` key.  


```python
>>> print(json.dumps(output['ansible_facts']['fan_info'], indent=4))
[
    {
        "status": "Ok", 
        "model": null, 
        "hw_ver": "0.0", 
        "name": "ChassisFan1"
    }, 
    {
        "status": "None", 
        "model": null, 
        "hw_ver": "0.0", 
        "name": "ChassisFan2"
    }, 
    {
        "status": "Ok", 
        "model": "--", 
        "hw_ver": "--", 
        "name": "Fan_in_PS1"
    }, 
    {
        "status": "Failure", 
        "model": "--", 
        "hw_ver": "--", 
        "name": "Fan_in_PS2"
    }
]

```

##### Step 10

This time the value is not a dictionary but a list of four dictionaries.

You can see that it's a list visually because the value starts with a `[` and ends with a `]`.

But you can also verify using the following type function statement.

```python
>>> print(type(output['ansible_facts']['fan_info']))
<type 'list'>
>>>
```

Since it's a list, we need to supply an index value.

##### Step 11

Print the second dictionary in this list.

```python
>>> print(json.dumps(output['ansible_facts']['fan_info'][1], indent=4))
{
    "status": "None", 
    "model": null, 
    "hw_ver": "0.0", 
    "name": "ChassisFan2"
}
>>>
```

##### Step 12

Store the `name` ("ChassisFan2") into a new variable called `fan_name`. 

Finally, print the variable called `fan_name`.

```python
>>> fan_name = output['ansible_facts']['fan_info'][1]['name']
>>> 
>>> print(fan_name)
ChassisFan2
>>> 
```

##### Step 13

Now print the list of all interfaces found under the `ansible_net_interfaces` key.  Only print the interface names - do not print their values.

Use a dictionary built-in method to accomplish this.

**Continue scrolling for the solution**

```python
.





























>>> interfaces = output['ansible_facts']['ansible_net_interfaces']
>>> print(interfaces.keys())
# output omitted
```


##### Step 14

Print `output` again. 

Take a deeper look at its format and focus on the `ansible_net_interfaces` key. This is another nested dictionary. 

Store the "Ethernet2/11" MAC address value in a variable called `mac` and print it.

**Continue scrolling for the solution**

```python
..



































```python
>>> mac = output['ansible_facts']['ansible_net_interfaces']['Ethernet2/11']['macaddress']
>>> print(mac)
2cc2.604f.feb2
>>> 
```

### Task 3 - Handle VLANs Objects

##### Step 1

Create a new variable called `vlans` that contains the following object:

```python
vlans = {
    "output": {
        "proposed": {
            "name": "NTC"
        }, 
        "existing_vlans_list": [
            "1"
        ], 
        "end_state_vlans_list": [
            "1", 
            "100"
        ], 
        "existing": {}, 
        "updates": [
            "vlan 100", 
            "name NTC", 
            "exit"
        ], 
        "end_state": {
            "vlan_state": "active", 
            "mapped_vni": "", 
            "admin_state": "up", 
            "name": "NTC", 
            "vlan_id": "100"
        }, 
        "proposed_vlans_list": [
            "100"
        ]
    }
}
```

This is a nested dictionary with just one outer key, `output`.

##### Step 3

Search for `existing_vlans_list` and `proposed_vlans_list` keys and store their values into `existing_vlans` and `proposed_vlans`.

```python
>>> existing_vlans = vlans['output']['existing_vlans_list']
>>> proposed_vlans = vlans['output']['proposed_vlans_list']
>>> 
```

##### Step 4

Print both `existing_vlans` and `proposed_vlans`.

```python
>>> print(existing_vlans)
['1']
>>> print(proposed_vlans)
['100']
>>> 
```

These are two lists of one element each.

##### Step 5

Create a new variable called `end_state_vlans` and assign it the sum of `existing_vlans` and `proposed_vlans` and print the result.

```python
>>> end_state_vlans = existing_vlans + proposed_vlans
>>> 
>>> print(end_state_vlans)
['1', '100']
>>> 
```

##### Step 6

Verify that `end_state_vlans` is equal to the `end_state_vlans_list` inner key from `vlans` dictionary. 

```python
>>> end_state_vlans == vlans['output']['end_state_vlans_list']
True
>>> 
```


##### Step 7

You'll also find a key called `updates` in this VLAN object.

Print exactly and only the last _command_ found in the `updates` list.

```python

>>> print(vlans['output']['updates'][2])
exit
>>>
```

You could have also done this based on a list of variable length:

```python

>>> print(vlans['output']['updates'][-1])
exit
>>>
```

Python supports negative indexing and `-1` is always the last element in the list.  `-2` is the second to last, and so on.



As you finish this lab, please take your take to go back and review it because understanding how to parse nested objects is critical to working with network APIs, Python, and also even in Ansible.  If something doesn't make sense, please don't hesitate to ask.
