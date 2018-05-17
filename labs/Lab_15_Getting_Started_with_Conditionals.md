## Lab 15 - Getting Started with Conditionals

This lab walks you through an introduction of using conditionals allowing you to add more intelligence and business logic into your code.

### Task 1 - Introduction to the if Statement

We've already reviewed boolean expressions, so you already know how to build if statements.

Examples:

```python
>>> hostname = "nxos-spine10"
>>>
```

```python
>>> hostname != 'nxos-spine2'
True
>>>
```

```python
>>> "eth" in "Ethernet2/4"
False
>>>
```

```python
>>> hostname == "nxos-spine2" or hostname == "nxos-spine10"
True
>>>
```

```python
>>> vendor = ""
>>>
```

Perform the same boolean check:

```python
>>> bool(vendor)
False
>>>
```

```python
>>> vendors = ['cisco']
>>>
>>> bool(vendors)
True
>>>
```

##### Step 1

Each of the expressions can easily be used in an `if` statement.

Try the following examples that map what was done previously:

```python
>>> hostname = "nxos-spine1"
>>>
>>> if hostname == "nxos-spine1":
...     print("The hostname is correct.")
...
The hostname is correct.
>>>
```

Notice how the only changes were adding the `if` statement, the trailing `:` colon, and then the code to execute if the expression is true.

##### Step 2

```python
>>> platforms = ['nexus', 'catalyst', 'asa', 'csr', 'aci']
>>>
>>> if 'catalyst' in platforms:
...     print("Catalyst has been found in the network.")
...
Catalyst has been found in the network.
>>>
```

##### Step 3

Create a variable called `supported_platforms` and assign it the value of `['nexus', 'catalyst']`.

Determine which of the `platforms` are _supported platforms_ using a combination of conditional logic and a for loop.

```python
>>> supported_platforms = ['nexus', 'catalyst']
>>>
>>> for platform in platforms:
...     if platform in supported_platforms:
...         print("Platform {}  -- SUPPORTED".format(platform))
...
...
Platform nexus  -- SUPPORTED
Platform catalyst  -- SUPPORTED
>>>
```

##### Step 4

Add an `else` statement to the previous example printing an equivalent statement so we can see even the invalid platforms.

```python
>>> for platform in platforms:
...     if platform in supported_platforms:
...         print("Platform {}  -- SUPPORTED".format(platform))
...     else:
...         print("Platform {}  -- NOT SUPPORTED".format(platform))
...
Platform nexus  -- SUPPORTED
Platform catalyst  -- SUPPORTED
Platform asa  -- NOT SUPPORTED
Platform csr  -- NOT SUPPORTED
Platform aci  -- NOT SUPPORTED
>>>
```

##### Step 5

Create the following list of dictionaries:

```python
>>> vlans = [{'name': 'web', 'id': 10}, {'name': 'app', 'id': 20}, {'name': 'db', 'id': 30}]
>>>
```

Pretty print it to make sure you understand it's data type.



##### Step 6

Print ONLY the VLAN name for VLAN 20.  Assume there are 100s of VLANs in this list and you don't know the VLANs index value.

```python
>>> for item in vlans:
...     if item['id'] == 20:
...         print("VLAN NAME: {}".format(item['name']))
...
VLAN NAME: app
>>>
```


##### Step 7

Generate and print all required Cisco IOS commands to configure the list of desired VLANs:

```python
>>> for item in vlans:
...   vlan_id = item['id']
...   name = item['name']
...   print("vlan {}".format(vlan_id))
...   print(" name {}".format(name))
...
vlan 10
 name web
vlan 20
 name app
vlan 30
 name db
>>>
```

##### Step 8

Remove the VLAN name for VLAN 20.

```python
>>> vlans[1].pop('name')
'app'
>>>
```

##### Step 9

Repeat Step 6.

Does it work?

```
.




























```


##### Step 10

When you use the `[]` notation it assumes the key is going to be there and if it's not (like for VLAN 20), a `KeyError` is raised.

However, we did cover in the booleans section AND the dictionary section a method we can use to overcome this.

ALWAYS, if a dictionary key may not exist, do NOT use the notation like `dict['key']`.  Instead, you should use `dict.get('key')`

Once you extract a value using `get`, you can perform a conditional check on it to see if it has a value assigned.  For reference scroll up and look at the examples before Step 1.

```python
>>> for item in vlans:
...   vlan_id = item['id']
...   name = item.get('name')
...   print("vlan {}".format(vlan_id))
...   if name:
...     print(" name {}".format(name))
...
vlan 10
 name web
vlan 20
vlan 30
 name db
>>>
```

See what happened here?  Since `get` returns `None` if the key doesn't exist, it's easy to use in an `if` statement to see if a value was in fact returned.

##### Step 11

Create the variable called `devices` as such:

```python
>>> print(devices)
[{'platform': 'nexus', 'hostname': 'nycr01'}, {'platform': 'catalyst', 'hostname': 'nycsw02'}, {'platform': 'mx', 'hostname': 'nycr03'}, {'platform': 'srx', 'hostname': 'nycfw01'}, {'platform': 'asa', 'hostname': 'nycfw02'}]
>>>
```

Pretty print to better see the full object, but it's a list of dictionaries.  Each dictionary has two key-value pairs, e.g. a `platform` key and a `hostname` key.

##### Step 12

Loop through `devices` and print the vendor of each device.  Make sure the code also prints out "Unknown Vendor" if it is an unknown vendor--for this example, treat the ASA as "unknown".

Make sure to use the `elif` statement in this example.

```python
>>> for item in devices:
...     platform = item.get('platform')
...     if platform == "nexus":
...         print("Vendor is Cisco")
...     elif platform == "catalyst":
...         print("Vendor is Cisco")
...     elif platform == "aci":
...         print("Vendor is Cisco")
...     elif platform == "srx" or platform == "mx":
...         print("Vendor is Juniper")
...     else:
...         print("Unknown Vendor")
...
Vendor is Cisco
Vendor is Cisco
Vendor is Juniper
Vendor is Juniper
Unknown Vendor
>>>
```

There are a few ways to handle this and we're showing two in this example.  You can check each platform separately as shown with Cisco or check them on the same line as shown with Juniper using an _or_ statement.

##### Step 13

There is another way too if we pre-build a known platforms list per vendor.

```python
>>> cisco_platforms = ['catalyst', 'nexus', 'aci']
>>> juniper_platforms = ['mx', 'srx']
>>>
>>> for item in devices:
...     platform = item.get('platform')
...     if platform in cisco_platforms:
...         print("Vendor is Cisco")
...     elif platform in juniper_platforms:
...         print("Vendor is Juniper")
...     else:
...         print("Unknown Vendor")
...
Vendor is Cisco
Vendor is Cisco
Vendor is Juniper
Vendor is Juniper
Unknown Vendor
>>>
```
