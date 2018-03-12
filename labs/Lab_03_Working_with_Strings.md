## Lab 3 - Working with Strings

### Task 1 - Working with Strings Part 1

##### Step 1

Create the variable `hostname` and assign it the value of "CORESWITCH-A"

```python
>>>
>>> hostname = 'CORESWITCH-A'
>>>
```

##### Step 2

Verify the data type of the `hostname` variable and prove that it is a string:

```python
>>> type(hostname)
<type 'str'>
>>>
```

##### Step 3

Now convert the value of `hostname` to be lowercase using the `lower` built-in method.

```python
>>> hostname.lower()
'coreswitch-a'
>>>
```

Notice how the new value "coreswitch-a" is printed automatically.  This is because this is the value being *returned* from the `lower` method.

When you just type a _variable.method()_ in at the shell window, you see the data printed to the terminal. In this case, it's "coreswitch-a" -- this data is not saved (yet). In order to do that, we'll need to perform variable assignment.

##### Step 4

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

##### Step 5

Create a new variable called `interface_config` and assign it the value of "interface Eth1\n duplex full\n speed 100":

```python
>>> interface_config = "interface Eth1\n duplex full\n speed 100"
>>> 
```

##### Step 6

Print `interface_config` with and without using hte `print` statement:

Without the `print` statement:

```python
>>> interface_config
'interface Eth1\n duplex full\n speed 100'
>>> 
```

With the `print` statement:

```python
>>> print(interface_config)
interface Eth1
 duplex full
 speed 100
>>> 

```

##### Step 7

Let's now take a look at another method--this time we'll look at using `replace()`.

Create a new variable called `ip_addr` and assign it the value of "10.20.5.5".

```python
>>>
>>> ip_addr = '10.20.5.5'
>>>
```

##### Step 8

Once it's created use the built-in method `replace` to replace only the 3rd octet.  The new 3rd octet should be `100`.

```python
>>>
>>> ip_addr.replace('5', '100')
'10.20.100.100'
>>>
```

If you notice, this replaces the 3rd and 4th octets.  We only want to replace the 3rd octet though.  The `replace` built-in method supports an optional parameter which specifies how many occurrences to replace of the matching string.

##### Step 9

Use that parameter to replace only ONE occurrence of the number `5`.  

The format to use is `replace(old, new, count)`.

```python
>>>
>>> ip_addr.replace('5', '100', 1)
'10.20.100.5'
>>>
```

Remember you need to assign the value returned from the method into a variable should you want to use it further down in your code.

##### Step 10

Store the value of the new IP address in a variable called `ip_addr2`.

For this task, you can replace both the 3rd and 4th octets:

```python
>>> ip_addr2 = ip_addr.replace('5', '100')
>>>
>>> print(ip_addr2)
10.20.100.100
>>>
```

##### Step 11

Let's take a step back.  So far, you've used the `lower` and `replace` methods.  You can use the built-in function called `dir()` to print ALL built-in methods for a given datatype by doing either `dir(<datatype>)` or `dir(<variable>`.

Print the list of available built-in methods for strings.  To do this, you can use any string variable or `str` to see these methods.

Using a variable that is a string:

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

And now using `str` as the data type:

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


##### Step 12

The `type` function allows you to see the data type.  The `dir()` function allows you to see all built-in methods.  

And `help()` allows you to learn how to use a given method.

Use `help()` on a few different methods:

```python
>>> help(str.upper)

# Then press "q" to quit the help text.
```


```python
>>> help(str.replace)

# Then press "q" to quit the help text.
```

```python
>>> help(str.split)

# Then press "q" to quit the help text.
```

##### Step 13

In this Step, print each octet in `ipaddr` individually using the `split` built-in method.


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

##### Step 14

Verify the data type of `octets` by using the `type()` function.

```python
>>> type(octets)
<type 'list'>
>>> 
```

Don't worry, we're showing this now because `split` is a method for strings, but we'll cover lists in detail in an upcoming lab.


### Task 2 - Working with Strings Part 2

As a network engineer, you'll often work with numbers in the form of IP Addresses, MAC addresses, Interface Numbers, etc., and you may need to validate the correct syntax of a user input parameter.  As such, you may want to ensure the value entered is really a number.

Let's say you need to parse the interface "Ethernet1/10" and want to ensure the interface has a number followed by a "/" followed by another number.

There are a few ways to do this.  One way is to use the `isdigit` method combined with the `split` and `lstrip` methods.  Let's take a look.

##### Step 1

Create a new variable called `interface` that stores a value of "Ethernet1/10".

```python
>>> interface = 'Ethernet1/10'
>>> 
```

##### Step 2

Use `lstrip` or `strip` to strip off the word "Ethernet" from the interface object.

> Note: The strip methods can strip characters, or by default, white space.

```python
>>> interface.lstrip('Ethernet')
'1/10'
>>>
```

##### Step 3

Create a new variable that stores the resulting string after "Ethernet" is stripped.

```python
>>> int_id = interface.lstrip('Ethernet')
>>>
>>> int_id
'1/10'
>>>
```

##### Step 4

Create two new variables called `slot` and `intf` - each should store the slot/interface, respectively.

```python
>>> slot = int_id.split('/')[0]
>>>
>>> intf = int_id.split('/')[1]
```

Remember that `split` returns a list and you access elements in a list using an index value starting at zero.  Again, we'll cover lists in depth in an upcoming lab.

##### Step 5

You could also try this in two separate steps:

```python
>>> parsed_interface = int_id.split('/')
>>>
>>> parsed_interface
['1', '10']
>>>
>>> slot = parsed_interface[0]
>>> intf = parsed_interface[1]
>>> 
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

If you do another example, you'll need to re-run the "parsing" statements stripping "Ethernet"< splitting on `/`, and then checking each element to see if they are digits.

> Note: this is just one example of how this could be done to teach particular methods.  There are other ways this could be done that's more _"production" grade_. 

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

##### Step 4

Create a new variable called `default_gw` and assign it the value of "10.{}.10.1".

```python
>>> default_gw = "10.{}.10.1"
>>> 
```

##### Step 5

Create a new variable called `site_id` and assign it the value of "20":

```python
>>> site_id = "20"
>>> 
```

##### Step 6

Using the `format` method, insert `site_id` in the `default_gw` string:

```python
>>> default_gw.format(site_id)
'10.20.10.1'
>>> 
```

##### Step 7

Perform the same step again using "30" as `site_id`:

```python
>>> site_id = "30"
>>> 
>>> default_gw.format(site_id)
'10.30.10.1'
>>>
```

##### Step 8 

Create variables called `service_id`, `node_id`, and `mask`.  Assign them the values of "100", "1", and "24" respectively:

```python
>>> service_id = "100"
>>> 
>>> node_id = "1"
>>> 
>>> mask = "24"
>>> 
```

##### Step 9

Update the variable called `default_gw` and insert all 4 variables into their correct locations using the `format` method:

```python
>>> default_gw = "10.{}.{}.{}/{}"
>>> 
>>> default_gw.format(site_id, service_id, node_id, mask)
'10.30.100.1/24'
>>>
```

##### Step 10

You can also format the spacing of a string while using the `format` method.  For example, you may want a nicely formatted string that is spaced accordingly with a pre-defined amount of spaces between each "column".

If you use the syntax `:<integer>` in between the curly brackets, it'll ensure you have that many spaces before the variable is printed.  Let's take a look:

Standard printing with the `format` method:

```python
>>> "{} {} {}".format("Hostname", "Location", "Vendor")                
'Hostname Location Vendor'

>>> 
```

Allocating 12 spaces for each element:

```python
>>> "{:12} {:12} {:12}".format("Hostname", "Location", "Vendor")
'Hostname     Location     Vendor      '
>>>
```

If you're printing "rows" in each table, you may have devices as such:

```python
>>> "{:12} {:12} {:12}".format("nyc-rt01", "New York", "Cisco")                      
'nyc-rt01     New York     Cisco       '
>>>
```

And another:

```python
>>> "{:12} {:12} {:12}".format("nyc-rt02", "New York", "Juniper") 
'nyc-rt02     New York     Juniper     '
>>> 
```


This will be more handy as you start to do more with loops and have the desire to print text tables.  This is in contrast with manually adding spaces in your templated string.


**End of Lab**



