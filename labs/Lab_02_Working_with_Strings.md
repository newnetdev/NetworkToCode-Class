## Lab 2 - Working with Strings

### Task 1 - Working with Strings Part 1

##### Step 1

Create the variable `hostname` and assign it the value of "CORESWITCH-A"

```python
>>>
>>> hostname = 'CORESWITCH-A'
>>>
```

##### Step 2

Convert the value of `hostname` to be lowercase using the `lower` built-in method.

```python
>>> hostname.lower()
'coreswitch-a'
>>>
```

Notice how the new value `coreswitch-a` is printed automatically.  This is because this is the value being *returned* from the `lower` method.

##### Step 3

Re-run the previous statement assigning the new hostname to the variable `lower_hostname` and then print the new hostname.  This time print it using the `print` statement.

```python
>>> lower_hostname = hostname.lower()
>>>
>>> print(lower_hostname)
coreswitch-a
>>>
>>> lower_hostname
'coreswitch-a'
>>>

```

As you can see, you can print using the `print` statement, but also print by typing the variable name and pressing Enter.  Using the print statement in the Python _shell_ is not a requirement, but it is needed if you want to render escape characters such as `\n`.

##### Step 4

Create a new variable called `ip_addr` and assign it the value of "10.20.5.5".

```python
>>>
>>> ip_addr = '10.20.5.5'
>>>
```

##### Step 5

Once it's created use the built-in method `replace` to replace only the 3rd octet.  The new 3rd octet should be `100`.

```python
>>>
>>> ip_addr.replace('5', '100')
'10.20.100.100'

```

If you notice, this replaces the 3rd and 4th octets.  We only want to replace the 3rd octet though.  The `replace` built-in method supports an optional parameter which specifies how many occurrences to replace of the matching string.

##### Step 6

Use that parameter to replace only ONE occurrence of the number `5`.  The format to use is `replace(old, new, count)`.

```python
>>>
>>> ip_addr.replace('5', '100', 1)
'10.20.100.5'
```

##### Step 7

Store the value of the new IP address in a variable called `ip_addr2`.  For this, we'll just replace both the 3rd and 4th octets.

```python
>>> ip_addr2 = ip_addr.replace('5', '100')
>>>
>>> print(ip_addr2)
10.20.100.100
```

##### Step 8

Print each octet individually.

> Hint: Use the `split` built-in method.


```python
>>> octets = ip_addr2.split('.')
>>>
>>> print(octets)
['10', '20', '100', '100']
>>>
>>> print(octets[0])
10
>>>
>>> print(octets[1])
20
>>>
>>> print(octets[2])
100
>>>
>>> print(octets[3])
100

```

##### Step 9

Print the list of available built-in methods for strings.  This can be done by using the `dir()` command.  You can use any string variable or `str` to see these methods.

Using the variable name:

```python
>>> dir(ip_addr2)
['__add__', '__class__', '__contains__', '__delattr__', '__doc__', '__eq__', '__format__',
'__ge__', '__getattribute__', '__getitem__', '__getnewargs__', '__getslice__', '__gt__',
'__hash__', '__init__', '__le__', '__len__', '__lt__', '__mod__', '__mul__', '__ne__',
'__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmod__', '__rmul__', '__setattr__',
'__sizeof__', '__str__', '__subclasshook__', '_formatter_field_name_split', '_formatter_parser',
'capitalize', 'center', 'count', 'decode', 'encode', 'endswith', 'expandtabs', 'find',
'format', 'index', 'isalnum', 'isalpha', 'isdigit', 'islower', 'isspace', 'istitle',
'isupper', 'join', 'ljust', 'lower', 'lstrip', 'partition', 'replace', 'rfind', 'rindex',
'rjust', 'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 'strip',
'swapcase', 'title', 'translate', 'upper', 'zfill']
```

Using "str":

```python
>>> dir(str)
['__add__', '__class__', '__contains__', '__delattr__', '__doc__', '__eq__', '__format__',
'__ge__', '__getattribute__', '__getitem__', '__getnewargs__', '__getslice__', '__gt__',
'__hash__', '__init__', '__le__', '__len__', '__lt__', '__mod__', '__mul__', '__ne__',
'__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmod__', '__rmul__', '__setattr__',
'__sizeof__', '__str__', '__subclasshook__', '_formatter_field_name_split', '_formatter_parser',
'capitalize', 'center', 'count', 'decode', 'encode', 'endswith', 'expandtabs', 'find',
'format', 'index', 'isalnum', 'isalpha', 'isdigit', 'islower', 'isspace', 'istitle',
'isupper', 'join', 'ljust', 'lower', 'lstrip', 'partition', 'replace', 'rfind', 'rindex',
'rjust', 'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 'strip',
'swapcase', 'title', 'translate', 'upper', 'zfill']
>>>
```

As you can see, either the variable or `str` works just fine.

### Task 2 - Working with Strings Part 2

As a network engineer, you will often work with numbers in the form of IP Addresses, MAC addresses, Interface Numbers, etc., and you may need to validate the correct syntax of a user input parameter.  As such, you may want to ensure the value entered is really a number.

Let's say you need to parse the interface "Ethernet1/10" and want to ensure the interface has a number followed by a "/" followed by another number.

There are a few ways to do this.  One way is to use the `isdigit` method combined with the `split` and `lstrip` methods.  We will walk through this process.

##### Step 1

Create a new variable called `interface` that stores the string "Ethernet1/10".

```python
>>> interface = 'Ethernet1/10'
```

##### Step 2

Use `lstrip` or `strip` to strip off the word "Ethernet" from the interface object.

```python
>>> interface.lstrip('Ethernet')
'1/10'
```

##### Step 3

Create a new variable that stores the resulting string after "Ethernet" is stripped.

```python
>>> int_id = interface.lstrip('Ethernet')
>>>
>>> int_id
'1/10'
```

##### Step 4

Create two new variables called `slot` and `intf` - each should store the slot/interface, respectively.

```python
>>> slot = int_id.split('/')[0]
>>>
>>> intf = int_id.split('/')[1]
```

You could also try this in two separate steps:

```python
>>> mylist = int_id.split('/')
>>>
>>> mylist
['1', '10']
>>>
>>> slot = mylist[0]
>>> intf = mylist[1]
```


##### Step 5

Finally, use the `isdigit` method to see if the values are *digits*.

```python
>>> slot.isdigit()
True
>>> 
>>> intf.isdigit()
True
>>>
```

Feel free to run through this example again with a typo such as EthernetX/10, and see what happens.

> Note: this is just one example of this could be done to teach particular methods.  We could have also used reverse indexing to extract characters until one is not a digit or a "/".

### Task 3 - Working with Strings Part 3

When working with CLI commands, you usually know the command to enter, but just need the particular value to configure.  So, if you are configuring Ethernet1/10, you may need to configure it's speed, duplex, and description.

As a network engineer, you already know the interface commands for each of these are:

```
speed { auto | 100 | 1000}
duplex { auto | full }
description { user text }
```

When you're working in Python, you may store the values you want to *insert* in a variable (or take them in as user input).  Let's take a look.

##### Step 1

Configure the following variables that will be treated as simulated user inputs:

```python
>>> speed = '1000'
>>>
>>> duplex = 'full'
>>>
>>> description = 'Uplink Interface Configured by Python'
```

##### Step 2

Create three new command strings and insert the proper value into each command using the `format` built-in method.

```python
>>> speed_cmd = 'speed {}'.format(speed)
>>>
>>> duplex_cmd = 'duplex {}'.format(duplex)
>>>
>>> descr_cmd = 'description {}'.format(description)
```

> Note: the variable is being inserted where the curly braces are.  This is merely a templated string.

##### Step 3

Print each of variables you create in the previous step:

```python
>>> print(speed_cmd)
speed 1000
>>>
>>> print(duplex_cmd)
duplex full
>>>
>>> print(descr_cmd)
description Uplink Interface Configured by Python
```

You will be using `format` in future labs, so make sure you understand it.

