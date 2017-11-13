## Lab 6 - Conditionals

### Task 1 - Using the if Statement

##### Step 1

Given a device name, test whether it complies with naming standards:

Note: the naming standard requires device name to be all upper case.

``` python
>>> device_name = 'switch1'
>>> 
```


```python
>>> if device_name != device_name.upper():
...   print("Device {} is NOT compliant".format(device_name))
... else:
...   print("Device {} is compliant".format(device_name))
... 
Device switch1 is NOT compliant

```

### Task 2 - Using if-elif

##### Step 1

Create a dictionary object that represents switches in the datacenter

```
{
    "switch1": {
        "type": "distribution"
    }, 
    "switch100": {
        "type": "access"
    }, 
    "switch99": {
        "type": "campus_core"
    }
}
```

You can copy from this object:

```python 
>>> dc_switches = { 'switch1': { 'type': 'distribution'}, 'switch100': {'type': 'acces
s'}, 'switch99': { 'type': 'campus_core'} }     
>>> 
```

##### Step 2

Given the datcenter switch data structure, print the device type for each device:

``` python
>>> for switch in dc.keys():
...   if dc_switches[switch]['type'].upper() == "ACCESS":
...     print("Device {} is an access layer switch".format(switch))
...   elif dc_switches[switch]['type'].upper() == "DISTRIBUTION":
...     print("Device {} is a distribution layer switch".format(switch))
... 
Device switch1 is a distribution layer switch
Device switch100 is an access layer switch
>>> 

```

##### Step 3

There is also a more Pythonic way to write the above iterating over `items` instead of just the keys.  Take and compare the following to the last Step:

```python
for switch, params in dc_switches.items():
  if params['type'].upper() == "ACCESS":
    print("Device {} is an access layer switch".format(switch))
  elif params['type'].upper() == "DISTRIBUTION":
    print("Device {} is a distribution layer switch".format(switch))
```


### Task 3 - if-elif-else


##### Step 1

If `type` is neither "access" or "distribution", print that there is an erroneous entry.

``` python
>>> for switch, params in dc_switches.items():
...   if params['type'].upper() == "ACCESS":
...     print("Device {} is an access layer switch".format(switch))
...   elif params['type'].upper() == "DISTRIBUTION":
...     print("Device {} is a distribution layer switch".format(switch))
...   else:
...     print("Device {} is of type {}. This is an invalid DC device".format(switch, params['type']))
... 
Device switch1 is a distribution layer switch
Device switch100 is an access layer switch
Device switch99 is of type campus_core. This is an invalid DC device
>>> 

```

### Task 4 - Containment

When there are specific values that you want to check, you can usually check them within your first conditional statement.  For example, we know that `type` should be "access" or "distribution", for datcenter switches.  We can use containment, using the `in` keyword to do this.  Let's examine how.

##### Step 1

Update the first conditional `if` with an expression that checks to make sure `type` is `in ['access', 'didstribution']`.  

Notice the new indentation level for the `else` statement.

``` python
>>> valid_types = ['access', 'distribution']
>>> for switch, params in dc_switches.items():
...   if params['type'] in valid_types:
...     if params['type'].upper() == "ACCESS":
...       print("Device {} is an access layer switch".format(switch))
...     elif params['type'].upper() == "DISTRIBUTION":
...       print("Device {} is a distribution layer switch".format(switch))
...   else:
...     print("Device {} is of type {}. This is an invalid DC device".format(switch, params['type']))
... 
Device switch1 is a distribution layer switch
Device switch100 is an access layer switch
Device switch99 is of type campus_core. This is an invalid DC device
>>> 

```

You can also perform the same operation without pre-creating the list that has `['access', 'distribution']`:

```python

>>> for switch, params in dc_switches.items():
...   if params['type'] in ['access', 'distribution']:
...     if params['type'].upper() == "ACCESS":
...       print("Device {} is an access layer switch".format(switch))
...     elif params['type'].upper() == "DISTRIBUTION":
...       print("Device {} is a distribution layer switch".format(switch))
...   else:
...     print("Device {} is of type {}. This is an invalid DC device".format(switch, params['type']))
... 
Device switch1 is a distribution layer switch
Device switch100 is an access layer switch
Device switch99 is of type campus_core. This is an invalid DC device
>>> 

```

The End.
