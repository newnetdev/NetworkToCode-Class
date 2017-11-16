
### TextFSM Part 2 - Parsing show version command output

##### Step 1

Navigate to the `scripts` directory within your home directory.:

```
ntc@ntc:~$ cd scripts
```

##### Step 2


If the `templates` directory does not exist here, create it and change directory to it.

```
ntc@ntc:~/scripts$ mkdir templates
ntc@ntc:~/scripts$ cd templates
```

##### Step 3

Download the pre-written TextFSM templates for the `cisco_ios_show_version` command.

```

ntc@ntc:~/templates$ wget https://raw.githubusercontent.com/networktocode/ntc-templates/master/templates/cisco_ios_show_version.template
--2017-10-12 00:22:14--  https://raw.githubusercontent.com/networktocode/ntc-templates/master/templates/cisco_ios_show_version.template
wget: /home/ajay/.netrc:4: unknown token "protocol"
wget: /home/ajay/.netrc:4: unknown token "https"
Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 151.101.0.133, 151.101.64.133, 151.101.128.133, ...
Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|151.101.0.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 682 [text/plain]
Saving to: ‘cisco_ios_show_version.template’

cisco_ios_show_version.template   100%[============================================================>]     682  --.-KB/s    in 0s      

2017-10-12 00:22:14 (214 MB/s) - ‘cisco_ios_show_version.template’ saved [682/682]

```
    
##### Step 4

Open this file in Sublime Text or any other text editor.


```
Value VERSION (.+?)
Value ROMMON (\S+)
Value HOSTNAME (\S+)
Value UPTIME (.+)
Value RUNNING_IMAGE (\S+)
Value List HARDWARE (\S+\d\S+)
Value List SERIAL (\S+)
Value CONFIG_REGISTER (\S+)

Start
  ^.*Software\s.+\),\sVersion\s${VERSION},*\s+RELEASE.*
  ^ROM: ${ROMMON}
  ^\s*${HOSTNAME}\s+uptime\s+is\s+${UPTIME}
  ^[sS]ystem\s+image\s+file\s+is\s+"(.*?):${RUNNING_IMAGE}"
  ^[Pp]rocessor\s+board\s+ID\s+${SERIAL}
  ^[Cc]isco\s+${HARDWARE}.+
  ^[Cc]onfiguration\s+register\s+is\s+${CONFIG_REGISTER}
  ^Switch Port -> Stack


Stack
  ^[Ss]ystem [Ss]erial [Nn]umber\s+:\s+${SERIAL}
  ^[Mm]odel\s+[Nn]umber\s+:\s+${HARDWARE}\s*
  ^[Cc]onfiguration\s+register\s+is\s+${CONFIG_REGISTER}

```

> Compare how the matches are done, with the final task in the regular expressions lab.

This pre-written TextFSM template captures the OS version, ROMMON info, device hostname, uptime, serial number etc based on the output from the show version command.

##### Step 5

Change back to the scripts directory and touch a new file here. Call it `textfsm_parse_command.py`.

```
ntc@ntc:~/templates$ cd ../scripts
ntc@ntc:~/scripts$ touch textfsm_parse_command.py

```

##### Step 6

The objective of this script is to collect the show command and template file details from the user - in addition to device details - use that to collect the raw output response from the device and glean the data matched by the template. The resulting output will be a structured text that we can potentially then use to create reports etc.


Create logical functions to gather the user input, collect the raw data from the device parse the response using a TextFSM template. Also create an empty `main()` function that will call these different functions. Leave these function definitions empty for now.


``` python
def user_input_parse():
    """Collect the device details using an unix-command-like menu"""
    pass

def command_output(device_details, command):
    """Collect and return command output from device"""
    pass
    
def textfsm_output(command_output, template):
    """Use template file to parse command_output"""
    pass
    
def main():
    pass
```



##### Step 6

Fill in the `user_input_parse` function. Write this function to collect user input using the `argparse` library. This should collect the following data from the users:
    - Name of the template file
    - Show command to execute
    - IP Address of remote device
    - Device type, username and password [ Set these with the following defaults - `cisco_ios`, `ntc` and `ntc123`]
    
``` python
import argparse  # Add this to the top of the file
```

``` python
def user_input_parse():
    """Collect the device details using an unix-command-like menu"""
    parser = argparse.ArgumentParser(description='Collect device details,'
                                     'template file and show command')
    parser.add_argument('-t', '--template',
                        help='Enter the full path to the template file',
                        required=True)
    parser.add_argument('-c', '--command',
                        help='Enter the show command',
                        required=True)
    parser.add_argument('-i', '--ip',
                        help='Enter the IP address or hostname of the device',
                        default='csr1')
    parser.add_argument('-d', '--device_type', help='Enter the device type',
                        default='cisco_ios')
    parser.add_argument('-u', '--username', help='Enter the username',
                        default='ntc')
    parser.add_argument('-p', '--password', help='Enter the password',
                        default='ntc123')
    input_data = parser.parse_args()
    host = input_data.ip
    username = input_data.username
    password = input_data.password
    device_type = input_data.device_type
    template = input_data.template
    command = input_data.command

    user_input = dict(device_type=device_type, ip=host,
                      username=username, password=password,
                      template=template, command=command)
    return(user_input)

```

##### Step 7 

Call this function from `main()`

``` python
def main():
    """Return structured data for show commands"""
    # Collect user input
    user_input = user_input_parse()
    

```

##### Step 8

`pop` the show command and template name from the `user_input` dictionary and save it as `device_details`


``` python
def main():
    """Return structured data for show commands"""
    # Collect user input
    user_input = user_input_parse()
    command = user_input.pop('command')
    template = user_input.pop('template')
    device_details = user_input

```

##### Step 9

Now fill out the `command_output` function. This takes the `device_details` and `command` variables as input and uses the `netmiko` library to connect to the device. It should then execute the user provided command on the remote system and collect the response back.

``` python
from netmiko import ConnectHandler  # Add this to the top of the file
```

``` python
def command_output(device_details, command):
    """Collect and return command output from device"""
    print("Connecting to device {}...\n".format(device_details['ip']))
    device = ConnectHandler(**device_details)
    return(device.send_command(command))

```
The function returns the response from the device as a blob of text.


##### Step 10

Call this function now from `main()`

``` python
def main():
    """Return structured data for show commands"""
    # Collect user input
    user_input = user_input_parse()
    command = user_input.pop('command')
    template = user_input.pop('template')
    device_details = user_input
    # Send command to the device and collect raw text response
    output = command_output(device_details, command)

```

##### Step 11

Fill out the `textfsm_output` function. This function, takes the raw text response from the device and the name of the template file as it's arguments.

First import the library

``` python
import textfsm  # Add this top the top of the file
```


``` python
def textfsm_output(command_output, template):
    """Use template file to parse command_output"""
    print("Converting raw output into structured data...")
    table = textfsm.TextFSM(open(template))
    data = table.ParseText(command_output)
    result = [table.header, data]
    return result

```

Here we are creating a variable called `table` that instantiates a `TextFSM` object. This object represents the template and uses the name of the template file as its argument.

Then we use the template object to parse the raw command output from the device. The result is stored in the `data` variable. 

> The table object will have a `header` attribute that corresponds to the `Value` items we defined in the template.


##### Step 12

Call this function from `main()`.

``` python
def main():
    """Return structured data for show commands"""
    # Collect user input
    user_input = user_input_parse()
    command = user_input.pop('command')
    template = user_input.pop('template')
    device_details = user_input
    # Send command to the device and collect raw text response
    output = command_output(device_details, command)
    # Send raw device output to textFSM and collect structured data response
    textfsm_result = textfsm_output(output, template)

```


##### Step 13

Finally, print the output to the screen


``` python
    print("Printing result.....")
    print(textfsm_result[0])  # Contains the header information
    print(json.dumps(textfsm_result[1], indent=4))

```

##### Step 14

The final, complete script should look as follows:

``` python
#!/usr/bin/env python
"""Code for Lab 18"""
from netmiko import ConnectHandler
import textfsm
import json
import argparse


def command_output(device_details, command):
    """Collect and return command output from device"""
    print("Connecting to device {}...\n".format(device_details['ip']))
    device = ConnectHandler(**device_details)
    return(device.send_command(command))


def textfsm_output(command_output, template):
    """Use template file to parse command_output"""
    print("Converting raw output into structured data...")
    table = textfsm.TextFSM(open(template))
    data = table.ParseText(command_output)
    result = [table.header, data]
    return result


def user_input_parse():
    """Collect the device details using an unix-command-like menu"""
    parser = argparse.ArgumentParser(description='Collect device details,'
                                     'template file and show command')
    parser.add_argument('-t', '--template',
                        help='Enter the full path to the template file',
                        required=True)
    parser.add_argument('-c', '--command',
                        help='Enter the show command',
                        required=True)
    parser.add_argument('-i', '--ip',
                        help='Enter the IP address or hostname of the device',
                        default='csr1')
    parser.add_argument('-d', '--device_type', help='Enter the device type',
                        default='cisco_ios')
    parser.add_argument('-u', '--username', help='Enter the username',
                        default='ntc')
    parser.add_argument('-p', '--password', help='Enter the password',
                        default='ntc123')
    input_data = parser.parse_args()
    host = input_data.ip
    username = input_data.username
    password = input_data.password
    device_type = input_data.device_type
    template = input_data.template
    command = input_data.command

    user_input = dict(device_type=device_type, ip=host,
                      username=username, password=password,
                      template=template, command=command)
    return(user_input)


def main():
    """Return structured data for show commands"""
    # Collect user input
    user_input = user_input_parse()
    command = user_input.pop('command')
    template = user_input.pop('template')
    device_details = user_input
    # Send command to the device and collect raw text response
    output = command_output(device_details, command)
    # Send raw device output to textFSM and collect structured data response
    textfsm_result = textfsm_output(output, template)
    print("Printing result.....")
    print(textfsm_result[0])
    print(json.dumps(textfsm_result[1], indent=4))


if __name__ == '__main__':
    main()

```


##### Step 15

Save and exit the file. Now execute the file

```
ntc@ntc:~/scripts$ textfsm_parse_command.py -t ./templates/cisco_ios_show_version.template -c show version -i csr1
Connecting to device csr1...

Converting raw output into structured data...
Printing result.....
['VERSION', 'ROMMON', 'HOSTNAME', 'UPTIME', 'RUNNING_IMAGE', 'HARDWARE', 'SERIAL', 'CONFIG_REGISTER']
[
    [
        "16.3.1", 
        "IOS-XE", 
        "csr1", 
        "1 minute", 
        "packages.conf", 
        [
            "CSR1000V"
        ], 
        [
            "9KXI0D7TVFI"
        ], 
        "0x2102"
    ]
]

```



### Task 4 - Parsing show ip interface command output

In this task, we will reuse the code we just wrote and use it to parse the output of the `show ip interfaces brief` command instead.

##### Step 1

Navigate back to the templates directory

``` 
ntc@ntc:~/scripts$ cd templates
```


##### Step 2

Download the pre-written TextFSM templates for the `cisco_ios_show_ip_interface_brief` commands.

```
ntc@ntc:~/templates$ wget https://raw.githubusercontent.com/networktocode/ntc-templates/master/templates/cisco_ios_show_ip_int_brief.template
--2017-10-12 08:45:45--  https://raw.githubusercontent.com/networktocode/ntc-templates/master/templates/cisco_ios_show_ip_int_brief.template
wget: /home/ajay/.netrc:4: unknown token "protocol"
wget: /home/ajay/.netrc:4: unknown token "https"
Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 151.101.0.133, 151.101.64.133, 151.101.128.133, ...
Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|151.101.0.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 178 [text/plain]
Saving to: ‘cisco_ios_show_ip_int_brief.template’

cisco_ios_show_ip_int_brief.templ 100%[============================================================>]     178  --.-KB/s    in 0s      

2017-10-12 08:45:45 (27.4 MB/s) - ‘cisco_ios_show_ip_int_brief.template’ saved [178/178]

```

##### Step 3

Open this file using Sublime Text or any other text editor.

```
Value INTF (\S+)
Value IPADDR (\S+)
Value STATUS (up|down|administratively down)
Value PROTO (up|down)

Start
  ^${INTF}\s+${IPADDR}\s+\w+\s+\w+\s+${STATUS}\s+${PROTO} -> Record

```

This template captures the name of the interface, IP address, admin and protocol status.



##### Step 4

Now switch back to the `scripts` directory and execute the `textfsm_parse_command.py` script, passing the new template and command file as inputs




``` 
ntc@ntc:~/scripts$ textfsm_parse_command.py -t ./templates/cisco_ios_show_ip_int_brief.template -c "show ip interface brief" -i csr1

Connecting to device csr1...

Converting raw output into structured data...
Printing result.....
['INTF', 'IPADDR', 'STATUS', 'PROTO']
[
    [
        "GigabitEthernet1", 
        "10.0.0.51", 
        "up", 
        "up"
    ], 
    [
        "GigabitEthernet2", 
        "unassigned", 
        "administratively down", 
        "down"
    ], 
    [
        "GigabitEthernet3", 
        "unassigned", 
        "administratively down", 
        "down"
    ], 
    [
        "GigabitEthernet4", 
        "unassigned", 
        "administratively down", 
        "down"
    ], 
    [
        "Loopback100", 
        "unassigned", 
        "up", 
        "up"
    ], 
    [
        "Loopback101", 
        "unassigned", 
        "up", 
        "up"
    ]
]

```
