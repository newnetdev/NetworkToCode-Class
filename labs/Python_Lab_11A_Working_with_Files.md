## Lab 11A - Working with Files

### Task 1 - Raw Configuration Files

In this task, you'll explore working with raw text (configuration) files.  You will read configuration files, parse raw text, and create a Python dictionary from the data stored in the files.

##### Step 1

Navigate back to the home directory.

```
ntc@ntc:~/scripts$ cd
ntc@ntc:~$
```

##### Step 2

Navigate to the `files` directory:

```
ntc@ntc:~$ cd files/
ntc@ntc:~/files$
```

##### Step 3

Enter into the Python shell from the `files` directory.

```python
ntc@ntc:~/files$ python
Python 2.7.6 (default, Jun 22 2015, 17:58:13)
[GCC 4.8.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>>
>>>
```

##### Step 4

Either by using `cat` on the terminal (in a different terminal session) or your text editor take a look at the `vlan_ids.conf` file that is located in the `files` directory.  You'll the file looks like this:

```
ntc@ntc:~/files$ cat vlan_ids.conf

vlan 1
vlan 2
vlan 10
vlan 20
vlan 50
```

##### Step 5

Open the `vlan_ids.conf` file for reading and use the variable name `vlan_file` as the file object.

```python
>>> vlan_file = open('vlan_ids.conf', 'r')
>>> 
```

##### Step 6

View the type of the newly created object.

```python
>>> type(vlan_file)
<type 'file'>
```

You will notice this is an object of type "file".

##### Step 7

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

##### Step 8

Since the file is still open, read in all data as a list using the built-in method called `read`.  Use the variable name `data`.

```python
>>> data = vlan_file.read()
>>> 
```

This reads the file as one big string.

##### Step 9

To see what just happened, print the object out.

```python
>>> print data
vlan 1
vlan 2
vlan 10
vlan 20
vlan 50
>>> 

```

Again, using `.read()` reads the file as one string.

##### Step 10

Now use the `splitlines` method to covert each line from the file into a list element.

```python
>>> data_list = data.splitlines()
>>> 
>>> data_list
['vlan 1', 'vlan 2', 'vlan 10', 'vlan 20', 'vlan 50']
>>> 
```

Loop through the list and print each element.

```python
>>> for item in data_list:
...   print item
... 
vlan 1
vlan 2
vlan 10
vlan 20
vlan 50
>>>

```

##### Step 11 (Challenge)

Normalize the data into a list of dictionaries such that each dictionary represents a VLAN and each dictionary has two keys: `id` and `name`.  For each name, simply using "vlan_<id>".  For example, the VLAN name for VLAN 10 will be vlan_10.

Perform these steps to create the required code:
  * Use the same for loop from the previous step
  * Remember to create an empty list before you start the for loop
  * Create a temporary dictionary that is only valid for each iteration of the loop. 
  * Add the two key value pairs to the dictionary
  * In the last statement in the for loop, append this dictionary to the empty list you required.

Your final object should look like this:

```python
[
    {
        "id": "1", 
        "name": "vlan_1"
    }, 
    {
        "id": "2", 
        "name": "vlan_2"
    }, 
    {
        "id": "10", 
        "name": "vlan_10"
    }, 
    {
        "id": "20", 
        "name": "vlan_20"
    }, 
    {
        "id": "50", 
        "name": "vlan_50"
    }
]
```




```
Solution is below.






































.
```


## Solution


```python
>>> vlans_list = []
>>> 
>>> for item in data_list:
...     temp_dict = {}
...     temp_dict['id'] = item.strip('vlan ')
...     temp_dict['name'] = 'vlan_{}'.format(item.strip('vlan '))
...     vlans_list.append(temp_dict)
... 
>>> 
```

##### Step 12

Pretty print the final object.

```python
>>> import json
>>> 
>>> print json.dumps(vlans_list, indent=4)
[
    {
        "id": "1", 
        "name": "vlan_1"
    }, 
    {
        "id": "2", 
        "name": "vlan_2"
    }, 
    {
        "id": "10", 
        "name": "vlan_10"
    }, 
    {
        "id": "20", 
        "name": "vlan_20"
    }, 
    {
        "id": "50", 
        "name": "vlan_50"
    }
]
>>> 
```


### Task 2 - Generating & Creating a Configuration File

In the last lab, we created a modular python script that prints interface configurations.  In this lab, we will continue to build on that and write a script that extends that script to generate the interface configurations and write them to a file.

##### Step 1

Navigate to the `scripts` directory within your home directory:

```
ntc@ntc:~$ cd scripts
ntc@ntc:~/scripts$
```

##### Step 2

Copy the `modular_generate_config.py` file as  `generate_config_file.py`

```
ntc@ntc:~/scripts$ cp modular_generate_config.py  generate_config_file.py
ntc@ntc:~/scripts$
```

##### Step 3

Open the file in the text editor of your choice.


##### Step 4



Go ahead and add this new function, calling it `generate_config_file`

``` python
def generate_config_file(commands_list, config_file_name):
    """Write interface configs to a file"""
    print("Opening file {} to write...".format(config_file_name))

    with open(config_file_name, "w") as file_handler:
        for command in commands_list:
            file_handler.write("{}\n".format(command))

    # Output the file details
    print("File {} has been generated...".format(config_file_name))

```

Notice how this time we're using the `with` statement, a context manager, rather than using the method shown in the last task.  Using `with` is preferred and also automatically closes the file for you as soon as you "un-indent" from the `with` block.

##### Step 5

The first task the main function should do is collect the data needed to configure the interfaces.  This is no different than what was already there.

However, after the commands list is generated, we need to define the filename of where we want to store the config file being generated and then finally generate the config file.

``` python

def main():
    """Generate and write interface configurations to a file
    """

    interfaces_dict = get_interfaces()
    # Call a function that returns the configuration
    commands_list = get_commands_list(interfaces_dict)

    # Call a function that writes configs to a file
    config_file_name = '/tmp/device.cfg'
    generate_config_file(commands_list, config_file_name)

```

Save the file and execute it from the command line:

```
ntc@ntc:~/scripts$ python generate_config_file.py
{'GigabitEthernet1': {'duplex': 'full', 'description': 'Configured_by_Python_GigabitEthernet1', 'speed': 1000}, 'GigabitEthernet2': {'duplex': 'half', 'description': 'Configured_by_Python_GigabitEthernet2', 'speed': 100}, 'Loopback101': {'description': 'Configured_by_Python_Looback101'}, 'Loopback100': {'description': 'Configured_by_Python_Loopback100'}}

```


##### Step 6

The final, complete script should look like below:

``` python
#!/usr/bin/env python
""" Code for Lab 11"""


def generate_commands(config_params):
    """Generate specific feature commands using feature name & value.
    """

    cmd_list = []
    for feature, value in config_params.items():
        command = " {} {}".format(feature, value)
        cmd_list.append(command)
    return cmd_list


def get_commands_list(interfaces):
    """Return a list of interface configuration commands."""

    # Iterate over the dictionary and generate configuration.

    commands_list = []
    for interface, config_params in interfaces.items():
        interface_command = "interface {}".format(interface)
        commands_list.append(interface_command)
        feature_commands = generate_commands(config_params)
        commands_list.extend(feature_commands)

    return commands_list


def print_config(commands_list):
    """Print the commands as a list and config."""
    # Print the results as a list
    print("Commands as a List:")
    print(commands_list)
    print("--------------------")
    # Print the results as config
    print("Commands Simulating Config File:")
    for command in commands_list:
        print(command)


def generate_config_file(commands_list, config_file_name):
    """Write interface configs to a file"""
    print("Opening file {} to write...".format(config_file_name))

    with open(config_file_name, "w") as file_handler:
        for command in commands_list:
            file_handler.write("{}\n".format(command))
    # Output the file details
    print("File {} has been generated...".format(config_file_name))


def get_interfaces():
    """ Return a dictionary of interfaces containing attributes"""
    interfaces = {
        "GigabitEthernet1": {
            "duplex": "full",
            "speed": 1000,
            "description": "Configured_by_Python_GigabitEthernet1"
        },
        "GigabitEthernet2": {
            "duplex": "half",
            "speed": 100,
            "description": "Configured_by_Python_GigabitEthernet2"
        },
        "Loopback101": {
            "description": "Configured_by_Python_Looback101"
        },
        "Loopback100": {
            "description": "Configured_by_Python_Loopback100"
        }
    }

    return interfaces


def main():
    """Generate and write interface configurations to a file
    """

    interfaces_dict = get_interfaces()
    # Call a function that returns the configuration
    commands_list = get_commands_list(interfaces_dict)

    # Call a function that writes configs to a file
    config_file_name = '/tmp/device.cfg'
    generate_config_file(commands_list, config_file_name)

if __name__ == "__main__":
    main()

```


##### Step 7

Save and execute the final script:


``` shell
ntc@ntc:~/scripts$ python generate_config_file.py
Opening file /tmp/device.cfg to write...
File /tmp/device.cfg has been generated...

```

##### Step 8

Now open the file `/tmp/device.cfg` using Sublime Text or any other text editor.

``` shell
interface Loopback101
 description Configured_by_Python_Looback101
interface Loopback100
 description Configured_by_Python_Loopback100
interface GigabitEthernet2
 speed 100
 duplex half
 description Configured_by_Python_GigabitEthernet2
interface GigabitEthernet1
 speed 1000
 duplex full
 description Configured_by_Python_GigabitEthernet1

```


You have now successfully created a modular python script that generates device interface configurations that are saved as a file locally.

