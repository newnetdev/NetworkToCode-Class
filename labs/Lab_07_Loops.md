## Lab 7 - Loops

### Task 1 - Printing in a For Loop

The first task you will do is to loop through a dictionary and a list to print its key-value pairs and elements, respectively.

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


Now try this again using a different variable than `command`.  Try using `for item in commands:` instead.


##### Step 3

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

##### Step 4

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

##### Step 5

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

##### Step 6

Print the Keys & Values:

```python
>>> for key, value in interface.items():
...     print(key, value)
...
duplex full
speed 100
description Configured by Python
>>>
```

Note that using `items` gives you each to each `item` and remember that `items` returns a list of tuples (you can also think of this as a list of lists from a usability perspective). Here `key` maps to the first element in each tuple and `value` maps to the second in element in each tuple.

Remember `key` and `value` are user defined:

This would also work just fine:

```python
>>> for feature, configured_value in interface.items():
...     print(feature, configured_value)
...
# output omitted
```

### Task 2 - Loop Through List of Dictionaries

##### Step 1

Create the following three dictionaries:

```python
>>> facts1 = {'vendor': 'cisco', 'os': 'nxos', 'ipaddr': '10.1.1.1'}
>>> facts2 = {'vendor': 'cisco', 'os': 'ios', 'ipaddr': '10.2.1.1'}
>>> facts3 = {'vendor': 'arista', 'os': 'eos', 'ipaddr': '10.1.1.2'}
>>>
```

##### Step 2

Create a list of dictionaries using the three previously created facts dictionaries:

``` python
>>> devices = [facts1, facts2, facts3]
>>> 
```

##### Step 3

Loop through `devices` and ensure you end up with the following output:

```
VENDOR: cisco
OS: nxos
IP ADDRESS: 10.1.1.1
----------
VENDOR: cisco
OS: ios
IP ADDRESS: 10.2.1.1
----------
VENDOR: arista
OS: eos
IP ADDRESS: 10.1.1.2
----------
```

Scroll for the solution:
```





















































.
```

Solution:

```python
>>> for item in devices:
...     print("VENDOR:", item['vendor'])
...     print("OS:", item['os'])
...     print("IP ADDRESS:", item['ipaddr'])
...     print('-' * 10)
... 
VENDOR: cisco
OS: nxos
IP ADDRESS: 10.1.1.1
----------
VENDOR: cisco
OS: ios
IP ADDRESS: 10.2.1.1
----------
VENDOR: arista
OS: eos
IP ADDRESS: 10.1.1.2
----------
>>> 
```


##### Step 4

Loop through the list again, this time checking to see if the IP address is in the data center.  Data Center switches start with `10.1`.  If it is a data center switch, append just the IP address to a newly created list.  

The final list created for this exercise should look like this:

```
['10.1.1.1', '10.1.1.2']
```

Scroll for the solution.


```









































.
```

Solution:

```python
>>> dc_switches = []
>>> 
>>> for item in devices:
...     if item['ipaddr'].startswith('10.1'):
...         dc_switches.append(item['ipaddr'])
... 
>>> 
>>> print(dc_switches)
['10.1.1.1', '10.1.1.2']
>>> 
```

You could have also broken down extracting the IP address like this:

```python
>>> dc_switches = []
>>> 
>>> for item in devices:
...     ip = item['ipaddr']
...     if ip.startswith('10.1'):
...         dc_switches.append(ip)
... 
>>> 
>>> print(dc_switches)
['10.1.1.1', '10.1.1.2']
>>> 
```

