## Lab 6 - Conditionals

### Task 1 - if

##### Step 1

Given a device name, test whether it complies with naming standards:

``` python
>>> device_name = 'switch1'
# naming standard requires device name to be all upper case

>>> if device_name != device_name.upper():
...   print("Device {} is NOT compliant".format(device_name)
... else:
...   print("Device {} is compliant".format(device_name))
... 
Device switch1 is NOT compliant

```

### Task 2 - if-elif

You may have realized that when you checked `state` there are two `if` statements, but they should never be executed one after the other because the **state** is EITHER up **or** down.  It makes much more sense to use `elif` and replace the second `if` statement.

##### Step 1

Create a dictionary object that represents switches in the datacenter

``` python

>>> dc = { 'switch1': { 'type': 'distribution'}, 'switch100': {'type': 'access'}, 'switch99': { 'type': 'campus_core'} }

```

##### Step 2

Given the datcenter switch data-model, print the device type

``` python
>>> for switch in dc.keys():
...   if dc[switch]['type'].upper() == "ACCESS":
...     print("Device {} is an access layer switch".format(switch))
...   elif dc[switch]['type'].upper() == "DISTRIBUTION":
...     print("Device {} is a distribution layer switch".format(switch))
... 
Device switch1 is a distribution layer switch
Device switch100 is an access layer switch
>>> 

```

### Task 3 - if-elif-else


##### Step 1

If `type` is neither "access" or "distribution", print that there is an erroneous entry.

``` python
>>> for switch in dc.keys():
...   if dc[switch]['type'].upper() == "ACCESS":
...     print("Device {} is an access layer switch".format(switch))
...   elif dc[switch]['type'].upper() == "DISTRIBUTION":
...     print("Device {} is a distribution layer switch".format(switch))
...   else:
...     print("Device {} is of type {}. This is an invalid DC device".format(switch, dc[switch]['type']))
... 
Device switch1 is a distribution layer switch
Device switch100 is an access layer switch
Device switch99 is of type campus_core. This is an invalid DC device
>>> 

```


### Task 4 - Containment

When there are specific values that you want to check, you can usually check them within your first conditional statement.  For example, we know that `type` should be "access" or "distribution", for datcenter switches.  We can use containment, using the `in` keyword to do this.  Let's examine how.

##### Step 1

Update the first conditional `if` with an expression that checks to make sure `type` is `in ['access', 'didstribution']`.  Otherwise, continue to print "INVALID INPUT!!!"

Notice the new indentation level for the `else` statement.

``` python
>>> valid_types = ['access', 'distribution']
>>> for switch in dc.keys():
...   if dc[switch]['type'] in valid_types:
...     if dc[switch]['type'].upper() == "ACCESS":
...       print("Device {} is an access layer switch".format(switch))
...     elif dc[switch]['type'].upper() == "DISTRIBUTION":
...       print("Device {} is a distribution layer switch".format(switch))
...   else:
...     print("Device {} is of type {}. This is an invalid DC device".format(switch, dc[switch]['type']))
... 
Device switch1 is a distribution layer switch
Device switch100 is an access layer switch
Device switch99 is of type campus_core. This is an invalid DC device
>>> 

```


You can also perform the same operation without pre-creating the list:

```python
>>> for switch in dc.keys():
...   if dc[switch]['type'] in ['access', 'distribution']:
...     if dc[switch]['type'].upper() == "ACCESS":
...       print("Device {} is an access layer switch".format(switch))
...     elif dc[switch]['type'].upper() == "DISTRIBUTION":
...       print("Device {} is a distribution layer switch".format(switch))
...   else:
...     print("Device {} is of type {}. This is an invalid DC device".format(switch, dc[switch]['type']))
... 
Device switch1 is a distribution layer switch
Device switch100 is an access layer switch
Device switch99 is of type campus_core. This is an invalid DC device
>>> 

```





