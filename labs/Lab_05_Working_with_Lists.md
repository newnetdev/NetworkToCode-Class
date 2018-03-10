## Lab 5 - Working with Lists

### Task 1 - Working with Lists Part 1

In this lab, you'll start to work with lists and explore their built-in methods.

##### Step 1

Create the following list of MAC addresses and assign them to the variable `mac_list`:

```python
>>> mac_list = ['00.00.00.00.11.11', '00.00.00.00.22.22',
'33.00.00.00.33.33', '44:00:00:00:44:44']
```

##### Step 2

Print the value of `mac_list`:

```python
>>> print(mac_list)
['00.00.00.00.11.11', '00.00.00.00.22.22', '33.00.00.00.33.33', '44:00:00:00:44:44']
>>>

```

##### Step 3

Using the `replace` method, update the fourth element in the list so that it uses periods instead of colons.

```python
>>> mac_list[3] = mac_list[3].replace(':', '.')
```

This is show you that you can update (over-write) a single element in a list while combining it with a concept you learned when working with strings.

##### Step 4

Print the new list.

> Note:  it's always a good idea to print after each change to see how the object was modified, especially when you're just getting started.

```python
>>> print(mac_list)
['00.00.00.00.11.11', '00.00.00.00.22.22', '33.00.00.00.33.33', '44.00.00.00.44.44']
>>>
```

##### Step 5

Remove the last element using the `pop` built-in method.

Remember that `pop`, by default, removes and returns the last element in the list.

```python
>>> mac_list.pop()
'44.00.00.00.44.44'
>>>
>>> mac_list
['00.00.00.00.11.11', '00.00.00.00.22.22', '33.00.00.00.33.33']
>>>
```

##### Step 6

Pop the MAC address "00.00.00.00.22.22".  Since this is NOT the last element, you must supply the index value of the value you're looking to pop.

```python
>>> mac_list.pop(1)
'00.00.00.00.22.22'
>>> 
>>> mac_list
['00.00.00.00.11.11', '33.00.00.00.33.33']
>>> 
```

You needed to use the index value of `1` because "00.00.00.00.22.22" was the second element in the list and the value that has the index of 1.

##### Step 7

Insert "00.00.00.00.22.22" back into the list in the same position it was.  Use the `insert` method:

```python
>>> mac_list.insert(1, '00.00.00.00.22.22')
>>> 
>>> mac_list
['00.00.00.00.11.11', '00.00.00.00.22.22', '33.00.00.00.33.33']
>>>
```


##### Step 8

Insert the mac address `22.22.00.00.00.22` as the 3rd element:

The list we want is: `['00.00.00.00.11.11', '00.00.00.00.22.22', '22.22.00.00.00.22, '33.00.00.00.33.33']`

```python
>>> mac_list.insert(2, '22.22.00.00.00.22')
>>>
>>> mac_list
['00.00.00.00.11.11', '00.00.00.00.22.22', '22.22.00.00.00.22', '33.00.00.00.33.33']
```

##### Step 9

Add two more mac addresses to the list in sequential order using the `append` method.  

The MAC addresses to add are: `55.55.55.55.55.55` and `66.66.66.66.66.66`.

```python
>>> mac_list.append('55.55.55.55.55.55')
>>>
>>> mac_list.append('66.66.66.66.66.66')
>>>
>>> print(mac_list)
['00.00.00.00.11.11', '00.00.00.00.22.22', '22.22.00.00.00.22', '33.00.00.00.33.33', '55.55.55.55.55.55', '66.66.66.66.66.66']
>>>
```


### Task 2 - Working with Lists Part 2

When working with APIs such as Cisco NX-API, commands are sent as a string to the device (for certain encoding types).  However, while you are writing code, it's common to want to build the command set as a list.  Lists are simply easier to work with and manipulate in terms of adding/removing certain elements/commands, etc.

##### Step 1

Create a list of commands like the following:

```python
>>> commands = ['interface Eth1/1', 'description configured by Python', 'shutdown']
>>> 
```

##### Step 2

Convert the list of commands to a string and insert a semi-colon in between each command.  Use the `join` method.

```python
>>> cmd_string = ' ; '.join(commands)
>>> 
```

##### Step 3

Print the new variable called `cmd_string`.

```python
>>> print(cmd_string)
interface Eth1/1 ; description configured by Python ; shutdown
>>>
```

Take note what happened here.  You can use `join` to insert any character(s) in between elements in a list yielding a string.


##### Step 4

Instead of inserting ";", now insert a "\n":

```python
>>> cmd_string_n = '\n'.join(commands)
>>> 
```

This inserted a new line in between each command.

##### Step 5

Print the new variable called `cmd_string_n`:

```python
>>> print(cmd_string_n)
interface Eth1/1
description configured by Python
shutdown
>>>
```

##### Step 6

Perform the same two steps, but this time add a space after the "\n":

```python
>>> cmd_string_n = '\n '.join(commands)
>>> 
>>> print(cmd_string_n)                
interface Eth1/1
 description configured by Python
 shutdown
>>> 
```

Notice the subtle difference?

##### Step 7

Continue to try the other built-in methods for lists.

```python
>>> dir(list)
['__add__', '__class__', '__contains__', '__delattr__', '__delitem__', '__delslice__',
'__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getslice__', '__gt__', '__hash__', '__iadd__', '__imul__', '__init__', '__iter__',
'__le__', '__len__', '__lt__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
'__repr__', '__reversed__', '__rmul__', '__setattr__', '__setitem__', '__setslice__',
'__sizeof__', '__str__', '__subclasshook__', 'append', 'count', 'extend', 'index',
'insert', 'pop', 'remove', 'reverse', 'sort']
>>>

```

Remember, you can use:

* `type()` - check the data type of a variable
* `dir()` - view built-in methods, e.g. `dir(list)` or `dir(commands`
* `help()` - view the help on how to use a given method, e.g. `help(list.append)` or `help(commands.append)`


### Task 3 - Working with Lists Part 3

##### Step 1

Create a list of Cisco Nexus linecards:

```python
>>> n7k_linecards = ['N7K-SUP1', 'N7K-M132XP-12', 'N7K-M148GS-11', 'N7K-M148GT-11', 'N7K-F132XP-15', 'N7K-SUP1', 'N7K-M132XP-12', 'N7K-M132XP-12', 'N7K-M148GT-11','N7K-M148GT-11']
>>> 
```

##### Step 2

Verify how many linecards there are either SUP2, SUP1, or M1-32 blades:

```python
>>> n7k_linecards.count("N7K-SUP2")
0
>>> 
>>> n7k_linecards.count("N7K-SUP1")
2
>>> 
>>> n7k_linecards.count("N7K-M132XP-12")
3
>>>
```

##### Step 3

You can do the same for verifying how many device types of a given vendor are in your environment:

```python
>>> vendors = ["cisco", "cisco", "juniper", "cisco", "arista", "juniper"]
>>> 
>>> vendors.count('cisco')
3
>>> 
```

##### Step 4

Sort the `vendors` list:

```python
>>> vendors.sort()
>>> 
>>> vendors
['arista', 'cisco', 'cisco', 'cisco', 'juniper', 'juniper']
>>> 
```

##### Step 5

Let's now reverse the list using the optional keyword `reverse`:

```python
>>> vendors.sort(reverse=True)
>>> 
>>> vendors
['juniper', 'juniper', 'cisco', 'cisco', 'cisco', 'arista']
>>> 
```

> Note: remember to use help(vendors.sort)


