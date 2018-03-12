## Lab 10 - Performing Basic File Operations

This lab introduces how to perform basic file operations such as opening a file for reading or writing.  We'll examine each of these in this lab.

### Task 1 - Reading Network Configuration Files

In this task, you'll explore working with raw text (configuration) files.  You will read configuration files, parse raw text, and create a Python dictionary from the data stored in the files.

##### Step 1

From the home directory, navigate to the `files` directory:

```
ntc@ntc:~$ cd files/
ntc@ntc:~/files$
```

##### Step 2

Enter into the Python shell while you're in the `files` directory.

```python
ntc@ntc:~/files$ python
Python 2.7.6 (default, Jun 22 2015, 17:58:13)
[GCC 4.8.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

##### Step 3

Either by using `cat` on the terminal (in a different terminal session) or your text editor take a look at the `vlan_ids.conf` file that is located in the `files` directory.  You'll see that the file looks like this:

```
ntc@ntc:~/files$ cat vlan_ids.conf

vlan 1
vlan 2
vlan 10
vlan 20
vlan 50
```

##### Step 4

Open the `vlan_ids.conf` file for reading and use the variable name `vlan_file` as the file object.

```python
>>> vlan_file = open('vlan_ids.conf', 'r')
>>> 
```

##### Step 5

View the type of the newly created object.

```python
>>> type(vlan_file)
<type 'file'>
>>>
```

You will notice this is an object of type `file`.

##### Step 6

Just like you've seen with string, lists, dictionaries, and other common data types, you can also view built-in methods for `file` objects.

```python
>>> dir(vlan_file)
['__class__', '__delattr__', '__doc__', '__enter__', '__exit__', '__format__', '__getattribute__',
'__hash__', '__init__', '__iter__', '__new__', '__reduce__', '__reduce_ex__', '__repr__',
'__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'close', 'closed', 'encoding',
'errors', 'fileno', 'flush', 'isatty', 'mode', 'name', 'newlines', 'next', 'read',
'readinto', 'readline', 'readlines', 'seek', 'softspace', 'tell', 'truncate', 'write',
'writelines', 'xreadlines']
>>>
```

##### Step 7

Since the file is still open, read in all data as a list using the built-in method called `read`.  Use the variable name `data`.

```python
>>> data = vlan_file.read()
>>> 
```

This reads the file as one big string.

##### Step 8

Print the variable called `data`:

```python
>>> print data
vlan 1
vlan 2
vlan 10
vlan 20
vlan 50
>>> 

```

The `read()` method is a basic way to simply read the file as one big string.

##### Step 9

Close the file properly using the `close` method.

```python
>>> vlan_file.close()
>>> 
```


### Task 2 - Writing to a Configuration File

In the last task, we saw how to read a text file.  This task shows how to create a text-based configuration file by writing to a file.

##### Step 1

Open a file for writing using the "w" value instead "r" for reading:

```python
>>> out_file = open('interface.cfg', 'w')
>>> 
```

##### Step 2

The last task used the `read` method.  This task uses the `write` method.

Take note that you need to explicitly tell Python to go to the next line using `\n` after each command (or line) added.

Add 3 interface commands and write them to the file:

```python
>>> out_file.write("interface Eth1\n")
>>> out_file.write(" speed 100\n")    
>>> out_file.write(" duplex full\n")
>>> 
```

##### Step 3

Close the file for writing:

```python
>>> out_file.close()
>>> 
```

##### Step 4

In another terminal windows, use `cat` to view the file just created:

```bash
ntc@ntc:~$ cat interface.cfg 
interface Eth1
 speed 100
 duplex full
ntc@ntc:~$
```

### Task 3 - Using a Context Manager

This task introduces the `with` statement to manage the file open and closing process should something happen to your running program.  This is the recommended way for working with files.

> Note: when you use `open('filename', 'w')`, the file gets written to only when the file is closed.  If you happen to forget to close the file, it could be an interesting time troubleshooting that!

When you use the `with` statement, all file closes happen automatically as soon as you un-indent from the `with` block. 

The following is the same example as above showing it using the `with` statement:

``` python
>>> with open("interfaces_2.cfg", "w") as out_file:
...     out_file.write("interface Eth2\n")
...     out_file.write(" speed 10\n")    
...     out_file.write(" duplex half\n")
...
>>>
```

Here is also another example to try for reading the file using the context manager:

```python
>>> with open("vlan_ids.conf", "r") as vlan_file:
...     data = vlan_file.read()
...
>>> print data
vlan 1
vlan 2
vlan 10
vlan 20
vlan 50
>>> 
```


This lab focused on very basic file operations. We'll continue to build on these in future labs as we start to deploy configurations from file to network devices.