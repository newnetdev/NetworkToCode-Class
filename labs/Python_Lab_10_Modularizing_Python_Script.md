## Lab 10 - Modularizing A Python Script

In the last lab, you built a script that prints interface configurations. In this lab, you will write a script that achieves the same end goal, however you will now use of Python functions creating more usable code. 

Writing code using a modular approach helps break down a monolithic, inflexible script into a flexible, easy to read and  manage one. 

### Task 1 - Printing interface configuration using functions

##### Step 1

Navigate to the `scripts` directory you created in the previous lab within your home directory.:

```
ntc@ntc:~$ cd scripts
ntc@ntc:~/scripts$
```

##### Step 2

Create a new file called `modular_generate_config.py`

```
ntc@ntc:~/scripts$ touch modular_generate_config.py
```

##### Step 3

Open the file in the text editor of your choice.

  * If you've RDP'd into the jump host, you can use Sublime Text on the desktop.
  * If you've SSH'd into the jump host, you can use nano, vi/vim, gedit, or any other text-based editor of your choosing.

> Note: An alternative option is to use a program called Cyberduck (or equivalent) that allows you to connect to the jump host via SFTP and edit files locally on your laptop.  As soon as you save them, they are SFTP'd back to the jump host.  This could improve latency for particular labs.


##### Step 4

Think about how to modularize the script we created in the previous lab. One way to think about it is by writing the script to do the following:

1. A function that provides the data (dictionary object) needed by our script.
2. A function that uses this data and generates the list of commands.
3. A function that uses the nested attributes (speed, duplex, description) to generate interface specific configurations.
4. A function that prints the results
5. Finally, a function that ties it all together

In the file we just created, let us use these as building blocks for our modular script.

``` python
#!/usr/bin/env python


def generate_commands(config_params):
    """Generate specific feature commands using feature name & value.
    """
    pass

def get_commands_list(interfaces):
    """Return a list of interface configuration commands."""
    pass

def print_config(commands_list):
    """Print the commands as a list and config."""
    pass
    
def get_interfaces():
    """ Return a dictionary of interfaces containing attributes"""
    pass

def main():
    """Generate and print the interface configurations
    """
    pass

if __name__ == "__main__":
    main()

```

What we have done here, is build a scaffolding for the code. 

##### Step 5

The first task the main function should do is collect the data needed to configure the interfaces. Write out the `get_interfaces` function that will "return" the dictionary object.

You will notice there is almost no new code in this script going forward.  You are simply re-writing the script from the last lab, but now using functions.


``` python
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

```

Now call this function within the `main()` function.

``` python

def main():
    """Generate and print the interface configurations
    """
    interfaces_dict = get_interfaces()
    print(interfaces_dict)
```


The full script should look like this:

```python

#!/usr/bin/env python


def generate_commands(config_params):
    """Generate specific feature commands using feature name & value.
    """
    pass

def get_commands_list(interfaces):
    """Return a list of interface configuration commands."""
    pass

def print_config(commands_list):
    """Print the commands as a list and config."""
    pass
    
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
    """Generate and print the interface configurations
    """
    interfaces_dict = get_interfaces()
    print(interfaces_dict)

if __name__ == "__main__":
    main()


```


Save the file and execute it from the command line:

```
ntc@ntc:~/scripts$ python modular_generate_config.py
{'GigabitEthernet1': {'duplex': 'full', 'description': 'Configured_by_Python_GigabitEthernet1', 'speed': 1000}, 'GigabitEthernet2': {'duplex': 'half', 'description': 'Configured_by_Python_GigabitEthernet2', 'speed': 100}, 'Loopback101': {'description': 'Configured_by_Python_Looback101'}, 'Loopback100': {'description': 'Configured_by_Python_Loopback100'}}

```


> You can optionally `import json` and pretty print the dictionary by using the `json.dumps()` function.

##### Step 6

Now you can pass this data (interfaces dictionary) to the `get_commands_list` function. 

``` python
def main():
    """Generate and print the interface configurations
    """

    interfaces_dict = get_interfaces()
    commands_list = get_commands_list(interfaces_dict)

```

The `get_commands_list` method takes in the dictionary object as an argument and returns the list of configuration commands. 

``` python
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

```


##### Step 7

Within the `get_commands_list` function, call the `generate_commands` function. This function is supplied with the `config_params` that contains the configuration attribute dictionary.


``` python
def generate_commands(config_params):
    """Generate specific feature commands using feature name & value.
    """

    cmd_list = []
    for feature, value in config_params.items():
        command = " {} {}".format(feature, value)
        cmd_list.append(command)
    return cmd_list

```

By containing each "function" or "task" within a Python function, the code maintenance and readability becomes a lot easier and now you have the ability to re-use functions as needed through the script.


##### Step 8

The `get_commands_list` function now returns a list of configuration commands back to  `main()`. In order to print this to screen, we pass the data as an argument to the `print_config` function. This function is called as a final step in the `main` function.

``` python
def main():
    """Generate and print the interface configurations
    """

    interfaces_dict = get_interfaces()
    # Call a function that returns the configuration
    commands_list = get_commands_list(interfaces_dict)

    print_config(commands_list)

```

Create the `print_config` function to print the final output to the screen:

``` python
def print_config(commands_list):
    """Print the commands as a list and config."""
    # Print the results
    print("Commands as a List:")
    print(commands_list)
    print("--------------------")
    print("Commands Simulating Config File:")
    for command in commands_list:
        print(command)

```

The final and complete script should look like this:


``` python
#!/usr/bin/env python
""" Code for Lab 10"""


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
    # Print the results
    print("Commands as a List:")
    print(commands_list)
    print("--------------------")
    print("Commands Simulating Config File:")
    for command in commands_list:
        print(command)


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
    """Generate and print the interface configurations
    """

    interfaces_dict = get_interfaces()
    # Call a function that returns the configuration
    commands_list = get_commands_list(interfaces_dict)

    print_config(commands_list)


if __name__ == "__main__":
    main()

```

##### Step 9

Save and execute the final script:

``` shell
ntc@ntc:~/scripts$ python modular_generate_config.py
Commands as a List:
['interface Loopback101', ' description Configured_by_Python_Looback101', 'interface GigabitEthernet1', ' description Configured_by_Python_GigabitEthernet1', ' speed 1000', ' duplex full', 'interface GigabitEthernet2', ' description Configured_by_Python_GigabitEthernet2', ' speed 100', ' duplex half', 'interface Loopback100', ' description Configured_by_Python_Loopback100']
--------------------
Commands Simulating Config File:
interface Loopback101
 description Configured_by_Python_Looback101
interface GigabitEthernet1
 description Configured_by_Python_GigabitEthernet1
 speed 1000
 duplex full
interface GigabitEthernet2
 description Configured_by_Python_GigabitEthernet2
 speed 100
 duplex half
interface Loopback100
 description Configured_by_Python_Loopback100

```
