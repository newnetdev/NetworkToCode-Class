## Lab 3 - Lists and Bools

### Task 1 - Working with Lists Part 1

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

```python
>>> mac_list.pop()
'44.00.00.00.44.44'
>>>
>>> mac_list
['00.00.00.00.11.11', '00.00.00.00.22.22', '33.00.00.00.33.33']
```

##### Step 6

Insert the mac address `22.22.00.00.00.22` as the 3rd element.

The list we want is: `['00.00.00.00.11.11', '00.00.00.00.22.22', '22.22.00.00.00.22, '33.00.00.00.33.33']`

```python
>>> mac_list.insert(2, '22.22.00.00.00.22')
>>>
>>> mac_list
['00.00.00.00.11.11', '00.00.00.00.22.22', '22.22.00.00.00.22', '33.00.00.00.33.33']
```

##### Step 7

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
```

##### Step 2

Convert the list of commands to a string and insert a semi-colon in between each command.  Use the `join` method.

```python
>>> cmd_string = ' ; '.join(commands)
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

### Task 3 - Working with Booleans

Every time a condition is evaluated, the result is a boolean, i.e. `True` or `False`. In this task you will learn how to use them using boolean operators.

##### Step 1

Enter the Python shell from your home directory.

```python
ntc@ntc:~$ python

Python 2.7.6 (default, Jun 22 2015, 17:58:13) 
[GCC 4.8.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.

>>> 
```

##### Step 2

Initialize 3 variables called `hostname`, `vendor` and `interfaces`. We will use these to make some practice with boolean operators.

```python
>>> hostname = 'nxos-spine1'
>>> vendor = 'cisco'
>>> interfaces = ['Ethernet2/1', 'Ethernet2/2', 'Ethernet2/3']
>>> 
```

##### Step 3

Use the `==` operator to evaluate `hostname` with the `nxos-spine2` string and `vendor` with the `cisco` string.

```python
>>> hostname == 'nxos-spine2'
False 
>>>
>>> vendor == 'cisco'
True
```

##### Step 4

Use the `>` and `!=` operators to evaluate `interfaces`'s length with the `3` number.

```python
>>> len(interfaces) > 3
False 
>>>
>>> len(interfaces) != 3
False 
```

##### Step 5

Use the `in` operator to evaluate if `Ethernet2/4` is a valid interface.

```python
>>> 'Ethernet2/4' in interfaces
False 
```

##### Step 6

Use the `and` logical operator to evaluate if `Ethernet2/2` is a valid interface and `vendor` is equals to `cisco`.

```python
>>> 'Ethernet2/2' in interfaces and vendor == 'cisco'
True
```
