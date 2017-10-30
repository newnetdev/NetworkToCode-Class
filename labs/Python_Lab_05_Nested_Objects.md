## Lab 5 - Nested Objects

### Task 1 - Nested Dictionary Objects

##### Step 0

Build objects from previous lab again.

Paste this into the Python shell:

```python
facts_list = [
    {
        "customer": "acme", 
        "vendor": "arista", 
        "location": "Sydney", 
        "device_type": "switch", 
        "model": "7050", 
        "hostname": "APAC1", 
        "os": "eos"
    }, 
    {
        "customer": "acme", 
        "vendor": "juniper", 
        "location": "London", 
        "device_type": "switch", 
        "model": "mx", 
        "hostname": "EMEA1", 
        "os": "junos"
    }, 
    {
        "customer": "acme", 
        "vendor": "cisco", 
        "location": "new_york", 
        "device_type": "switch", 
        "model": "catalyst", 
        "hostname": "nycr01", 
        "os": "ios"
    }
]
```



##### Step 1

Create two new dictionary objects that depict the attributes of neighbor devices and then print them out.

```python
>>> neighbor1 = dict(local_interface='Eth1/1', neighbor_interface='Eth1/2', neighbor='R1')
>>>
>>> neighbor2 = dict(local_interface='Eth1/2', neighbor_interface='Eth1/4', neighbor='R2')
>>
```

##### Step 2

Create a list that is comprised of these neighbors.

```python
>>> neighbors = [neighbor1, neighbor2]
>>> 
```

##### Step 3

Print `neighbors` to see the newly formed list:

```python
>>> print(neighbors)
[{'neighbor_interface': 'Eth1/2', 'local_interface': 'Eth1/1', 'neighbor': 'R1'}, {'neighbor_interface': 'Eth1/4', 'local_interface': 'Eth1/2', 'neighbor': 'R2'}]
>>> 

```

Now pretty print them:

```python
>>> import json
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



##### Step 4

These neighbors created are the simulated neighbors of APAC1 which is the device in `facts_1`, i.e. the first element of `facts_list`.

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


##### Step 5

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

##### Step 6

Print just the hostname of the second neighbor of APAC1.

```python
>>> print(facts_list[0]['neighbors'][1]['neighbor'])
R2
>>>
```

Take your time to ensure you understand how we are accessing "R2".  Understanding nested lists and dictionary objects are very important to use network APIs as you'll often get back a list of dictionaries for interfaces and neighbors, as an example.

In the next Task, we'll walk through a more gradual process helpful with parsing complex nested objects.

### Task 2 - Working with a Nested Facts Dictionary Object

##### Step 1

Move to the `nested` sub-directory. Here you will find text files containing show command outputs. Use `ls` to verify you see two files: `facts.json` and `vlans.json`.


```bash
ntc@ntc:~$ cd nested
ntc@ntc:~/nested$ ls
facts.json vlans.json
```


##### Step 2

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

##### Step 3

Open the file `facts.json` and load its contents as one big string into a variable called **content**. 

> Note: we'll cover more file operations in an upcoming lesson.


```python
$ python
>>> facts_file = open('facts.json', 'r')
>>>
>>> content = facts_file.read()
>>> 
```

##### Step 4

Print `content`.

```python
>>> print(content)
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
}
>>>
```


##### Step 5

Check the data type of `content`. 

```
>>> type(content)
<type 'str'>
```

Although it looks like a dictionary, it is still a simple string.

##### Step 6

Being a JSON string, we need to convert it into an actual dictionary using the `json.loads` method. Assign the dictionary to a variable called `facts`. 

Use `type` again to verify `facts` type. 

```python
>>> facts = json.loads(content)
>>>
>>> type(facts)
<type 'dict'>
>>> 
```

Note: we cover `json.loads()` more when we get to working with JSON APIs.  For now, just know it's taking a string and converting it to a dictionary.

##### Step 7

`facts` is a dictionary with a main key, `output`, and multiple level of nested dictionaries and lists. Scroll back up and/or open this file in your text editor visually see that.

Print its length using the `len()` function.

```python
>>> len(facts)
1
>>>
```

This confirms that the outer dictionary is composed by only one root key.  In other words, there is only ONE item.

##### Step 8

Verify the single key of the dictionary by using the `values` method.

```python
>>> print(facts.keys())
['output']
>>>
```


##### Step 9

Let's extract the value of the `output` key by now saving it into a new variable called `output`.

```python
>>> output = facts['output']
```

You can repeat the steps 6 - 8.  

Check the data type and check the length.  If it's a list, you'll need to extract the value using an index (integer) value.  If it's a dictionary, you'll need to supply a key to extract the value, and remember, you can see all available keys by using the `keys()` method.

**This workflow can be repeated until you get to the data you're looking for.**

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

Let's move on and print `output`.

##### Step 10

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

##### Step 11

This is again a dictionary of one _root_ key, `ansible_facts`, whose value is still a dictionary, which you saw in Step 10 by printing all keys of `output`.

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

##### Step 12

This time the value is not a dictionary but a list of four dictionaries.

You can see that it's a list visually because the value starts with a `[` and ends with a `]`.

But you can also verify using the following type function statement.

```python
>>> print(type(output['ansible_facts']['fan_info']))
<type 'list'>
>>>
```

Since it's a list, we need to supply an index value.

##### Step 13

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

##### Step 14

Store the `name` ("ChassisFan2") into a new variable called `fan_name`. 

Finally, print the variable called `fan_name`.

```python
>>> fan_name = output['ansible_facts']['fan_info'][1]['name']
>>> 
>>> print(fan_name)
ChassisFan2
>>> 
```

##### Step 15

Print the list of all interfaces found under the `ansible_net_interfaces` key.  Only print the interface names - do not print their values.

Use a dictionary built-in method to accomplish this.

Do not use a loop.

**Continue scrolling for the solution**

```python
.
























>>> interfaces = output['ansible_facts']['ansible_net_interfaces']
>>> print(interfaces.keys())
# output omitted
```


##### Step 16

Print `output` again. Take a deeper look at its format and focus on the `ansible_net_interfaces` key. This is another nested dictionary. 

Store the Ethernet2/11 MAC address value in a variable called `mac` and print it.

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

Open the file `vlans.json` and load its content into a `vlans` variable, converting it into a dictionary.

```python
>>> vlans_file = open('vlans.json', 'r')
>>> 
>>> vlans = json.loads(vlans_file.read())
>>> 
```

##### Step 2

Print `vlans`.

```python
>>> print(json.dumps(vlans, indent=4))
{
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

Notice how you can use these expression for a boolean check.  You could have also done this:

```python
is_true = end_state_vlans == vlans['output']['end_state_vlans_list']
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

