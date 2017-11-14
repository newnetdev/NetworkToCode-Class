## Lab 11B - Working with Files

### Task 1 - Reading Data from YAML Files

In this task, we're going to continue to extend the script we've been working witih.  Up until now, we've used an interfaces dictionary created in the `get_interfaces` function. In this task, we will read in the configuration data from a YAML file and use that to generate the configuration.

> Note: we will spend much more time on YAML later in the course.  This is just a light introduction to see how a YAML file maps to Python objects.

##### Step 1

Navigate to the `scripts` directory within your home directory.:

```
ntc@ntc:~$ cd scripts
ntc@ntc:~/scripts$
```

##### Step 2

Create a new file named `csr1.yml`. This will contain the interface configuration data.

```
ntc@ntc:~/scripts$ touch csr1.yml
ntc@ntc:~/scripts$
```

##### Step 3

Open the file in Sublime (or text editor of your choice).

##### Step 4

Copy and paste the following into `csr1.yml`.

``` yaml
---
GigabitEthernet1:
  description: Configured_by_Python_GigabitEthernet1
  duplex: full
  speed: 1000
GigabitEthernet2:
  description: Configured_by_Python_GigabitEthernet2
  duplex: half
  speed: 100
Loopback100:
  description: Configured_by_Python_Loopback100
Loopback101:
  description: Configured_by_Python_Loopback101

```


> You can also copy and paste this content to the [JSON2YAML](http://json2yaml.com) website. Compare the JSON output to the `interfaces` dictionary you created in the previous lab.

Here, you have effectively defined a set of nested dictionaries with the key being the interface name, and it's values being interface attributes. The name of the attributes are the nested keys, with values corresponding to the value of the attribute.


##### Step 5

To visualize how to work with a YAML file within our code, we can first explore it within the Python interpreter shell.

From the command prompt, enter the Python interpreter shell.

``` python
ntc@ntc:~/scripts$ python
Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
[GCC 5.4.0 20160609] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> 
>>> 
```

Import the `pyaml` module - this is needed to easily translate YAML encoded data to standard Python datatypes.

``` shell
>>> import yaml
>>> 

```

Next, read the YAML file, and load it's contents as a standard python dictionary variable.

``` shell
>>> with open('csr1.yml') as yaml_file_handler:
...   interfaces = yaml.load(yaml_file_handler)
... 
>>> 
>>> type(interfaces)
<type 'dict'>
>>>
```

Finally, pretty print this variable.

``` shell
>>> import json
>>> 
>>> print(json.dumps(interfaces, indent=4))
{
    "GigabitEthernet2": {
        "duplex": "half", 
        "speed": 100, 
        "description": "Configured_by_Python_GigabitEthernet2"
    }, 
    "GigabitEthernet1": {
        "duplex": "full", 
        "speed": 1000, 
        "description": "Configured_by_Python_GigabitEthernet1"
    }, 
    "Loopback101": {
        "description": "Configured_by_Python_Loopback101"
    }, 
    "Loopback100": {
        "description": "Configured_by_Python_Loopback100"
    }
}

```

Now, we need to implement the above as a function within our script and use this data to build the interface configurations.

Note this is the same exact object we had manually defined in the `get_interfaces` function.

##### Step 6

Start off by making a copy the file you created in the previous lab.

After copying it, open the file in a text editor.

``` shell
ntc@ntc:~/scripts$ cp generate_config_file.py  read_yaml_file.py
ntc@ntc:~/scripts$
```

The functions that we already created in the previous lab can be reused. The new function needed to achieve this lab's goal is to read the interface configuration data from a YAML file, rather than from a locally defined dictionary.

##### Step 7

Go ahead and add this new function, calling it `get_interfaces_from_file`

``` python
def get_interfaces_from_file():
    """Read in YAML data of the interfaces and generate the dictionary"""
    with open('csr1.yml') as yaml_file_handler:
        interfaces = yaml.load(yaml_file_handler)
    return interfaces

```

This function opens the file `csr1.yml` and loads the data within the file using Python's `pyaml` library. 

> In Step 5, we inspected the type of this variable (dictionary) and printed it. Our function returns this dictionary to the caller.

##### Step 8

For this lab, we will need to import the `pyaml` module. Add this to the top of file.

``` python
import yaml
```


##### Step 9

Call this new function from `main()`, replacing the call to  `get_interfaces` 

``` python
def main():
    """Generate and write interface configurations to a file
    """

    interfaces_dict = get_interfaces_from_file()
    # Call a function that returns the configuration
    commands_list = get_commands_list(interfaces_dict)

    # Call a function that writes configs to a file
    config_file_name = '/tmp/device.cfg'
    generate_config_file(commands_list, config_file_name)

```

> The rest of the logic remains the same.


##### Step 10

The final complete script should look like this:

``` python
#!/usr/bin/env python
""" Code for Lab 11"""
import yaml


def generate_commands(config_params):
    """Generate specific feature commands using feature name & value."""
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


def get_interfaces_from_file():
    """Read in YAML data of the interfaces and generate the dictionary"""
    with open('csr1.yml') as yaml_file_handler:
        interfaces = yaml.load(yaml_file_handler)
    return interfaces


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

    interfaces_dict = get_interfaces_from_file()
    # Call a function that returns the configuration
    commands_list = get_commands_list(interfaces_dict)

    # Call a function that writes configs to a file
    config_file_name = '/tmp/device.cfg'
    generate_config_file(commands_list, config_file_name)

if __name__ == "__main__":
    main()

```


##### Step 11

Save and execute this script:


``` shell
ntc@ntc:~/scripts$ python read_yaml_file.py
Opening file /tmp/device.cfg to write...
File /tmp/device.cfg has been generated...

```
    
##### Step 12

Now open the file `/tmp/device.cfg` using Sublime Text or any other text editor of your choice.

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


You have now successfully created a modular python script that reads in configration data from a YAML encoded file and  generates device interface configurations that are saved as a file locally.
