## Lab 20 - Passing in User Input

### Task 1 - Update the Modularized Script

In this lab, you will still deploy the generated configuration for SNMP to an end device, but will now collect user input for the parameters that were hard-coded earlier.

##### Step 1

The following was the solution from Lab 19.  Use the following code and save it into a new script called `interactive.py` in your `scripts` directory:

> Ensure you have `/home/ntc/scripts/configs/snmp.cfg` as that will be deployed again in this lab.

```python
from netmiko import ConnectHandler


def connect_to_device(hostname):
    message = "Connecting to device"
    print_logger(message, hostname)
    net_d = ConnectHandler(host=hostname, username='ntc', password='ntc123', device_type='cisco_ios')

    return net_d

def deploy_commands(device, hostname, config_file):
    print("Sending commands from file | {}".format(hostname))
    device.send_config_from_file(config_file)
    
def print_logger(message, hostname):
    print("{} | {}".format(message, hostname))

def main():
    devices = ['csr1', 'csr2', 'csr3']

    config_file = './configs/snmp.cfg'
    
    for device in devices:
        net_device = connect_to_device(device)

        deploy_commands(net_device, device, config_file)

        print_logger("Disconnecting from device", device)
        net_device.disconnect()

if __name__ == "__main__":
    main()
```

##### Step 2

Make two main changes the script.  

* Remove the for loop
* Define the device to automate, credentials, and device type under `if __name__ == "__main__":` and pass them into `main()`.  Once you're passing them into `main()`, continue to pass them into `connect_to_device()` and use those parameter to connect to a device.

The updated script should look like this:

```python
from netmiko import ConnectHandler


def connect_to_device(hostname, username, password, device_type):
    message = "Connecting to device"
    print_logger(message, hostname)
    net_d = ConnectHandler(host=hostname, username=username, password=password, device_type=device_type)

    return net_d

def deploy_commands(device, hostname, config_file):
    print("Sending commands from file | {}".format(hostname))
    device.send_config_from_file(config_file)
    
def print_logger(message, hostname):
    print("{} | {}".format(message, hostname))

def main(device, username, password, device_type):
    config_file = './configs/snmp.cfg'
    
    net_device = connect_to_device(device, username, password, device_type)

    deploy_commands(net_device, device, config_file)

    print_logger("Disconnecting from device", device)
    net_device.disconnect()

if __name__ == "__main__":
    device = 'csr1'
    username = 'ntc'
    password = 'ntc123'
    device_type = 'cisco_ios'

    main(device, username, password, device_type)
```


##### Step 3

Replace the hard-coded variables you just created with interactive prompts:

```python
    device = raw_input("Please enter the hostname or IP: ")
    username = raw_input("Please enter the username: ")
    password = raw_input("Please enter the password: ")
    device_type = raw_input("Please enter the device type: ")
```

The bottom portion of the script should look like this:

```python
if __name__ == "__main__":
    device = raw_input("Please enter the hostname or IP: ")
    username = raw_input("Please enter the username: ")
    password = raw_input("Please enter the password: ")
    device_type = raw_input("Please enter the device type: ")

    main(device, username, password, device_type)
```

##### Step 4

Save and execute the script.

##### Step 5

Import `getpass` at the top of your script like this:

```
from getpass import getpass
```

Replace `raw_input` for `getpass` when entering the password.

```python
password = getpass("Please enter the password: ")
```

##### Step 6

Save and re-run the script.

### Task 2 - Collecting Input Using argparse

Prompting the user is one way to collect input interactively. In this task we will use the Python `argparse` module to collect input from the user, in a style that mimics most Unix commands.

Our goal here is to allow the script to help instruct the user on the usage/limitations and understand how to supply default values that users can potentially override.

##### Step 1

Perform a Save As on the file you just created in the previous lab.  Save it as `user-flags.py`.

##### Step 2

Open this new file in Sublime Text or any other text editor.

The new code needed to collect user input will use python's `argparse` library. Go ahead and import this at the top of your script.

``` python
import argparse

```

##### Step 3

Replace the following interactive prompts in your script:

```python
    device = raw_input("Please enter the hostname or IP: ")
    username = raw_input("Please enter the username: ")
    password = raw_input("Please enter the password: ")
    device_type = raw_input("Please enter the device type: ")
```

You will replace them with the following:

```python
    parser = argparse.ArgumentParser(description='Collect device and data'
                                     ' file information to configure a device')
    parser.add_argument('-i', '--ip',
                        help='Enter the IP address or hostname of the device',
                        required=True)
    parser.add_argument('-d', '--device_type', help='Enter the device type',
                        required=True)
    parser.add_argument('-u', '--username', help='Enter the username',
                        required=True)
    parser.add_argument('-p', '--password', help='Enter the password',
                        required=True)

    # parse all args and render 
    args = parser.parse_args()

    device = args.ip
    username = args.username
    password = args.password
    device_type = args.device_type
```

##### Step 4

Save and execute this script, first without any arguments:

``` shell
ntc@ntc:scripts$ python user-flags.py
usage: flags_user_input.py [-h]  -i IP -d DEVICE_TYPE -u
                             USERNAME -p PASSWORD
flags_user_input.py: error: argument -i/--ip is required

```

> Note the usage instructions and required flags.

##### Step 5

Next try and execute the script with the `-h` or `--help` flag:

``` shell
ntc@ntc:~/scripts$ python user-flags.py --help
usage: flags_user_input.py [-h] -i IP -d DEVICE_TYPE -u
                             USERNAME -p PASSWORD
Collect device and data file information to configure a device

optional arguments:
  -h, --help            show this help message and exit
  -i IP, --ip IP        Enter the IP address or hostname of the device
  -d DEVICE_TYPE, --device_type DEVICE_TYPE
                        Enter the device type
  -u USERNAME, --username USERNAME
                        Enter the username
  -p PASSWORD, --password PASSWORD
                        Enter the password

```

##### Step 6

Finally, execute the script with all required inputs.

```
ntc@ntc:scripts$ python user-flags.py -i csr1 -d cisco_ios -u ntc -p ntc123 
# output omitted
```

> Remember you can also pass in the long-form of the flags using `--username ntc` or `--username=ntc`.

In this lab you have successfully used 2 ways to create a modular python script to collect user input. Using the user input, the script then generated the desired interface configurations. Finally, based on the device, username and password supplied by the user, our script deployed configuration to the end device.

### Task 3 - Using sys.argv

This task shows the quickest way to get started working with command line arguments.  While `argparse` is recommended for more user-friendly scripts, you may want to use `sys.argv` for a quick and easy to pass in args into a script. 

This task shows how to get started with `sys.argv`

##### Step 1

Create a new script called `basic_args.py` in the `scripts` directory.

##### Step 2

In the script, `import sys`.  

Add a print statement that says "HERE ARE MY ARGUMENTS: "

Right under the print statement, add the following line:

```python
print sys.argv

```

It'll look like this:

```python
#! /usr/bin/env python

import sys

if __name__ == "__main__":

    print 'HERE ARE MY ARGUMENTS: '
    print sys.argv

```

##### Step 3

Save and execute the script.

```
ntc@ntc:~/scripts$ python basic_args.py
HERE ARE MY ARGUMENTS:
['my_args.py']
```

Can you tell that a list was printed out?  This is a list with one element.  We can see that the first and only element in the list is the name of the Python file being executed.

##### Step 4

Re-run the script like so:

```
ntc@ntc:~/scripts$ python basic_args.py cisco arista juniper
```

After running this script, you will see the following output:

```
HERE ARE MY ARGUMENTS:
['basic_args.py', 'cisco', 'arista', 'juniper']
```

Again, notice that the script name is always element 0 and then every other argument is another element in the list.

##### Step 5

Only print out the first *real* argument, i.e. "cisco".

Additionally, save `sys.argv` as `args`.  This will simplfy working with the objects going forward.

```python
if __name__ == "__main__":

    print 'HERE ARE MY ARGUMENTS: '

    args = sys.argv

    print args[1]
```

Run the script again.

```
ntc@ntc:~/scripts$ python basic_args.py cisco arista juniper
```

```
HERE ARE MY ARGUMENTS:
cisco
```

As you can see, using the `sys` module with the `argv` variable, it is quite fast and easy to pass in arguments from the command line.

One other trick is to use indexing with lists to only ever print everything BUT the first element.  

> You can use `[1:]` to access the list starting at index 1.  You can also do `[1:<ending index #>` too.
> 

Take a look:

```python
>>> args = ['basic_args.py', 'cisco', 'arista', 'juniper']
>>> 
>>> args[1:]
['cisco', 'arista', 'juniper']
>>> 
>>> 
>>> limited = args[1:]
>>> 
>>> if limited:
...   'args were passed in'
... 
'args were passed in'
>>> 
>>> 
>>> args = ['basic_args.py']
>>> 
>>> limited = args[1:]
>>> 
>>> if limited:
...   'args were passed in'
... 
>>> 
```


