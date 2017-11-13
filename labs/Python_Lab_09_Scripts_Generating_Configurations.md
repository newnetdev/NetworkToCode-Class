## Lab 9 - Writing Scripts To Generate Interface Configuration

In Lab 8, we learned how to write basic scripts.  In this lab, we will write a script that prints out interface configurations for an IOS device based on configuration parameters that will also be defined in the script.

### Task 1 - Printing interface configuration

##### Step 1

Navigate to the `scripts` directory you created in the previous lab within your home directory:

```
ntc@ntc:~$ cd scripts
ntc@ntc:~/scripts$
```

##### Step 2

Create a new file called `generate_config.py`:

```
ntc@ntc:~/scripts$ touch generate_config.py
ntc@ntc:~/scripts$
```

##### Step 3

Open the file in the text editor of your choice.

  * If you've RDP'd into the jump host, you can use Sublime Text on the desktop.
  * If you've SSH'd into the jump host, you can use nano, vi/vim, gedit, or any other text-based editor of your choosing.

> Note: An alternative option is to use a program called Cyberduck (or equivalent) that allows you to connect to the jump host via SFTP and edit files locally on your laptop.  As soon as you save them, they are SFTP'd back to the jump host.  This could improve latency for particular labs.

##### Step 4

In this new file, create a nested dictionary object called `interfaces`. This dictionary contains data we need to properly generate interface configurations. You will see that physical interfaces define speed and duplex while logical interface just define description.

``` python
#!/usr/bin/env python

if __name__ == "__main__":

    interfaces = {
        "GigabitEthernet1":
        {
            "speed": 1000,
            "duplex": "full",
            "description": "Configured_by_Python_GigabitEthernet1"
        },
        "GigabitEthernet2":
        {
            "speed": 100,
            "duplex": "half",
            "description": "Configured_by_Python_GigabitEthernet2"
        },
        "Loopback100":
        {
            "description": "Configured_by_Python_Loopback100"
        },
        "Loopback101":
        {
            "description": "Configured_by_Python_Looback101"
        }
    }

```

##### Step 5

Using a for loop, iterate over all of the items in the dictionary that  contains configuration data of the interfaces.  Print each item as you loop over the dictionary.

> Rememer, an "item" is a complete key-value pair.

This code snippet gets placed below the dictionary.

``` python
    for interface, config_params in interfaces.items():
        print(interface, config_params)

```

Save the file and execute it from the command line:

```
ntc@ntc:~/scripts$ python generate_config.py
Loopback101 {'description': 'Configured_by_Python_Looback101'}
GigabitEthernet2 {'duplex': 'half', 'speed': 100, 'description': 'Configured_by_Python_GigabitEthernet2'}
GigabitEthernet1 {'duplex': 'full', 'speed': 1000, 'description': 'Configured_by_Python_GigabitEthernet1'}
Loopback100 {'description': 'Configured_by_Python_Loopback100'}

```

As you can see from the output, we are able to print the interface name and the attributes to be configured for that interface. Notice also that the `key` for the nested `config_params` dictionary is the command that is used to configure that particular attribute.

#### Step 6

Now that we have visualized the dictionary object, let's use a list to contain all the interfaces and associated commands to send to the device. Now, our for loop will look as follows:

``` python
    commands_list = []

    for interface, config_params in interfaces.items():
        interface_command = "interface {}".format(interface)
        commands_list.append(interface_command)

```

Add the above snippet to the script.

#### Step 7

Pay careful attention to the dictionary object -  not every interface has all attributes. For instance, the logical interfaces do not contain speed and duplex attributes. In this step, write conditional logic, to append the attributes for an interface if, and only if the attribute key is defined.

``` python
    commands_list = []

    for interface, config_params in interfaces.items():

        interface_command = "interface {}".format(interface)
        commands_list.append(interface_command)
        description = config_params.get('description')
        if description:
            description_command = " description {}".format(description)
            commands_list.append(description_command)
        speed = config_params.get('speed')
        if speed:
            speed_command = " speed {}".format(speed)
            commands_list.append(speed_command)
        duplex = config_params.get('duplex')
        if duplex:
            duplex_command = " duplex {}".format(duplex)
            commands_list.append(duplex_command)

    print("Commands as a List:")
    print(commands_list)
            
            
```

Go ahead and save this file and execute it.

``` shell
ntc@ntc:~/scripts$ python generate_config.py
Commands as a List:
['interface Loopback101', ' description Configured_by_Python_Looback101', 'interface GigabitEthernet1',
' description Configured_by_Python_GigabitEthernet1', ' speed 1000', ' duplex full', 'interface GigabitEthernet2',
' description Configured_by_Python_GigabitEthernet2', ' speed 100', ' duplex half', 'interface Loopback100',
' description Configured_by_Python_Loopback100']
ntc@ntc:~/scripts$ 
```

#### Step 8

Finally, we can now loops over this list and generate the device specific configuration for it's interfaces

``` python
    print("--------------------")
    print("Commands Simulating Config File:")
    for command in commands_list:
        print(command)

```

The final complete script should look like this:

``` python
#!/usr/bin/env python

if __name__ == "__main__":

    """ Given a dictionary of interfaces, generate and print the configurations
    """

    interfaces = {
        "GigabitEthernet1":
        {
            "speed": 1000,
            "duplex": "full",
            "description": "Configured_by_Python_GigabitEthernet1"
        },
        "GigabitEthernet2":
        {
            "speed": 100,
            "duplex": "half",
            "description": "Configured_by_Python_GigabitEthernet2"
        },
        "Loopback100":
        {
            "description": "Configured_by_Python_Loopback100"
        },
        "Loopback101":
        {
            "description": "Configured_by_Python_Looback101"
        }
    }

    # Iterate over the dictionary and commands list.
    commands_list = []

    for interface, config_params in interfaces.items():
        interface_command = "interface {}".format(interface)
        commands_list.append(interface_command)
        description = config_params.get('description')
        if description:
            description_command = " description {}".format(description)
            commands_list.append(description_command)
        speed = config_params.get('speed')
        if speed:
            speed_command = " speed {}".format(speed)
            commands_list.append(speed_command)
        duplex = config_params.get('duplex')
        if duplex:
            duplex_command = " duplex {}".format(duplex)
            commands_list.append(duplex_command)

    print("Commands as a List:")
    print(commands_list)
    print("--------------------")
    print("Commands Simulating Config File:")
    for command in commands_list:
        print(command)

```


Save and execute this script:


``` shell
ntc@ntc:~/scripts$ python generate_config.py
Commands as a List:
['interface Loopback101', ' description Configured_by_Python_Looback101', 'interface GigabitEthernet1',
' description Configured_by_Python_GigabitEthernet1', ' speed 1000', ' duplex full', 'interface GigabitEthernet2',
' description Configured_by_Python_GigabitEthernet2', ' speed 100', ' duplex half', 'interface Loopback100',
' description Configured_by_Python_Loopback100']
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
