## Lab 15 -  Using TextFSM to parse device command output

In the previous lab, we used Python's `re` library to create match patterns against raw output from device show commands. In this lab, we will use the Open Source 3rd party library - TextFSM to achive the same result. 


### Task 1 - Using TextFSM to Parse Raw Text

As you've learned, TextFSM requires two inputs: a template and raw text.  This task walks you through the process of building a TextFSM template for the `show ip interface brief` command on Cisco Nexus switches that can then be used as an input to `textfsm.py` to easily extract the required data.

##### Step 1

Capture the text output that will be used for testing the template.  

> NOTE: these steps are exactly the same no matter what OS is running on the device from IOS to NXOS, EOS, JunOS, etc.

Normally, this is where you would connect to one of your devices and get the output for a specific show command, but for this task, we'll use the following output:

```bash
IP Interface Status for VRF "default"(1)
Interface            IP Address      Interface Status
Vlan10               10.20.10.1      protocol-down/link-down/admin-down
Vlan20               10.20.20.1      protocol-down/link-down/admin-down
Vlan30               10.20.30.1      protocol-down/link-down/admin-up
Lo0                  10.20.0.101     protocol-up/link-up/admin-up
Lo1                  10.20.1.101     protocol-up/link-up/admin-up
Lo2                  10.20.2.101     protocol-up/link-up/admin-up
Eth2/1               10.20.1.1       protocol-up/link-up/admin-up
Eth2/2               10.20.1.5       protocol-down/link-down/admin-down
Eth2/3               10.20.101.2     protocol-up/link-up/admin-up
Eth2/4               10.20.102.2     protocol-up/link-up/admin-up
```

Note: This file already exists as cisco_nxos_show_ip_interface_brief.raw in the following directory: `/home/ntc/textfsm/`on your jump host.


##### Step 2

For this lab, we will define the *needs*, i.e. which values are important to extract.  The requirement is to extract five different pieces of data from the `show ip interface brief` output:
  * interface
  * ip address
  * protocol status
  * link status
  * admin state

##### Step 3

Determine the regular expression specifically for each piece of data we want to extract. The information structure we want to extract is always the same regardless of the interface type. For example, considering the first interface we will want to parse the following values:  

INTERFACE = Vlan10
IP = 10.20.10.1  
PROTOCOL = down
STATUS = down
ADMIN = down

We will walk through two of these now and leave it as an exercise to complete the others.

Let's start with the interface name.

**Interface Regular Expression**

The interface name is a combination of letters and numbers, but as you can see, it also has forward slashes such as `/`.  One way to capture this easily is to use the `\S+` which says to match one or more characters that are non-whitespace.

Let's take a look at the IP address.

**Interface Regular Expression**


An IP is made up of four numbers separated from the others by a period.  Since a number is represented with `\d` using regular expressions, we can represent a full IP address using `\d+\.\d+\.\d+\.\d+`.  Note that since `.` is a special character in regular expressions, we need to escape it using `\` to match the actual period.

> Note: we already know Cisco will only accept valid IP addresses as inputs, so you can simplify this regex by just using `\S+`.


You can use [regexr.com](http://regexr.com) for further testing and validation.  Checkout their Regex cheatsheet too.


We still need to determine Regular Expressions for the other 4 pieces of data we want to extract, but hold off on that for now (you will do this as the last step in this lab):

INTERFACE = \S+

IP = `\d+\.\d+\.\d+\.\d+`   => or \S+

PROTOCOL = ?

STATUS = ?

ADMIN = ?


##### Step 4

Navigate to the `textfsm` sub-directory in your home directory.

Create a TextFSM template to extract ONLY the interface name and save it as `cisco_nxos_show_ip_interface_brief.template`.

This is what the template should look like:

```
Value INTERFACE (\S+)

Start
  ^${INTERFACE} -> Record
```

Few points to note about the template:

**It must begin with `Value` <value-name-that-you-define> (<regex for just the data being extracted>)**

The RegEx created in Step 3 gets enclosed in parentheses right next to what will become the "header" name for that specific column (and Python dictionary key for that specific value).  "Value" denotes the data that will be extracted from the raw text.  The Value lines must all appear before any state definitions and must be contiguous lines, separated only by comments. 

**You must include the "Start" state and it must use a capital "S"**

"Start" which is a reserved state (TextFSM is a finite state machine).  The FSM starts in state Start, so this label is mandatory and the template will not parse without it. This lab won't be using other states, but you can transition from one state to the next, which is helpful with command outputs that have several distinct sections.

**Parsing Rules**

Right below Start are rules, the full line(s) of text with the *Values* that we want to extract with the RegEx(es) inserted at its appropriate location.  The parsing happens one line at a time, so the rule must be able to identify the value you want to extract distinctly.

Once their is a match on the specific line/rule in the state machine, you *Record* the value, so we include `-> Record` to perform this operation.  You can also perform no operation (do nothing on match), or transition to another state.

In this one example, the full line was:

```
Vlan10               10.20.10.1      protocol-down/link-down/admin-down
```

And the rule to parse this line is:

```
  ^${INTERFACE} -> Record
```

This will parse and _Record_ the first grouping of non-white space characters on any line.  As you may expect, as it stands, it'll also capture the column headers.  As you add more variables to capture, they will not be caught anymore since that match will become more specific.


> Note: The FSM reads a line from the input buffer and tests it against each rule, in turn, starting from the top of the current state. If a rule matches the line, then the action is carried out and the process repeats (from the top of the state again) with the next line. Source: [TextFSM Wiki](https://code.google.com/p/textfsm/wiki/TextFSMHowto)


##### Step 5

Save the template.

##### Step 6

Return to the terminal within the `textfsm` directory.

Run the following command using `textfsm.py`:

```bash
ntc@ntc:~/textfsm$ python textfsm.py cisco_nxos_show_ip_interface_brief.template cisco_nxos_show_ip_interface_brief.raw
```

You will see the following output:
```bash
FSM Template:
Value INTERFACE (\S+)

Start
  ^${INTERFACE} -> Record


FSM Table:
['INTERFACE']
['IP']
['Interface']
['Vlan10']
['Vlan20']
['Vlan30']
['Lo0']
['Lo1']
['Lo2']
['Eth2/1']
['Eth2/2']
['Eth2/3']
['Eth2/4']

```

Now we know the state machine and parsing is working as we want it to.

##### Step 7

Now update the template to extract the IP Address.


```
Value INTERFACE (\S+)
Value IP (\d+\.\d+\.\d+\.\d+)

Start
  ^${INTERFACE}\s+${IP} -> Record
```

##### Step 8

Save the updated template.

##### Step 9

Re-run the textfsm.py script.

```bash
ntc@ntc:~/textfsm$ python textfsm.py cisco_nxos_show_ip_interface_brief.template cisco_nxos_show_ip_interface_brief.raw 
FSM Template:
Value INTERFACE (\S+)
Value IP (\d+\.\d+\.\d+\.\d+)

Start
  ^${INTERFACE}\s+${IP} -> Record


FSM Table:
['INTERFACE', 'IP']
['Vlan10', '10.20.10.1']
['Vlan20', '10.20.20.1']
['Vlan30', '10.20.30.1']
['Lo0', '10.20.0.101']
['Lo1', '10.20.1.101']
['Lo2', '10.20.2.101']
['Eth2/1', '10.20.1.1']
['Eth2/2', '10.20.1.5']
['Eth2/3', '10.20.101.2']
['Eth2/4', '10.20.102.2']

```

Now we've verified 2 of the 5 values are working as expected.

##### Step 10

Continue and finish the last 3 values, i.e. PROTOCOL, STATUS and ADMIN.

Here is a hint for what the rule looks like after adding the next value.

```
^${INTERFACE}\s+${IP}\s+protocol-${PROTOCOL} -> Record
```

Please do one a time.  This helps the testing process tremendously.



Additionally, we will collect as user input the location of the TextFSM template to be used, the show command to parse etc.

### Task 2 - Using Netmiko and TextFSM Together

##### Step 1

Navigate to the `textfsm` directory while on the Linux shell.

Copy and paste the following script into a new file called `netmiko-clitable-ios.py` in the `textfsm` directory.

```python
#! /usr/bin/env python

import json
import clitable
from netmiko import ConnectHandler
from ntc_course import clitable_to_dict

TEMPLATES_DIR = '/etc/ntc/ansible/library/ntc-ansible/ntc-templates/templates'
INDEX_FILE = '/etc/ntc/ansible/library/ntc-ansible/ntc-templates/templates/index'

if __name__ == "__main__":

    platform = 'cisco_ios'
    host = 'csr1'
    command = 'show ip int brief'

    device = ConnectHandler(
                device_type=platform,
                ip=host,
                username='ntc',
                password='ntc123'
                )

    rawtxt = device.send_command(command)

    # this script is using clitable objects that are part of textfsm
    # to help manage when you use a large qty of templates

    cli_table = clitable.CliTable(INDEX_FILE, TEMPLATES_DIR)

    attrs = {
        'Command': command,
        'Platform': platform
    }

    # based on the command and platform, the right template is used
    # based on an index file - see PATH above for index file

    cli_table.ParseCmd(rawtxt, attrs)

    # helper function used to convert native list of lists from textfsm
    # to a list of dictionaries

    structured_data = clitable_to_dict(cli_table)

    print json.dumps(structured_data, indent=4)

```

##### Step 2

Take a few minutes to understand the script.  Here is a brief overview:

- The `ConnectHandler` is the same as we've already used in the previous task - there is nothing new here.
- The netmiko device method `send_command` is used to capture output from the switch (again, nothing new here)
- The variable `attrs` is created which is a dictionary that has two key-value pairs.  The keys map directly to the column headers as defined in the TextFSM `index` file.  Feel free to look at the file.  It's located here: `/etc/ntc/ansible/library/ntc-ansible/ntc-templates/templates/index`
- Once `attrs` is created, it denotes the command we will be parsing using a TextFSM template
- Then we use the `ParseCmd` method of the `cli_table` object to perform the magic of using the right template to parse the raw text based on the parameters being used, i.e. `rawtxt` and `attrs`.  Internal to the `cli_table`, the right template is used based on the inputs of command and platform from the `attrs` object.  Then `textfsm` is used just as we learned in the previous lab.
- The final output is the "list" output just like the previous lab
- While out of scope at this point for further review, the `cli_table` object is then sent to a helper function to create a list of dictionaries for a more standardized output.
- Finally, the new object is printed to the terminal.

##### Step 3

Execute the script using the following command:

```bash
ntc@ntc:~/textfsm$ python netmiko-clitable-ios.py 
```


```bash
ntc@ntc:~/textfsm$ python netmiko-clitable-ios.py
[
    {
        "status": "up", 
        "intf": "GigabitEthernet1", 
        "ipaddr": "10.0.0.51", 
        "proto": "up"
    }, 
    {
        "status": "up", 
        "intf": "GigabitEthernet2", 
        "ipaddr": "10.254.13.1", 
        "proto": "up"
    }, 
    {
        "status": "up", 
        "intf": "GigabitEthernet3", 
        "ipaddr": "unassigned", 
        "proto": "up"
    }, 
    {
        "status": "up", 
        "intf": "GigabitEthernet4", 
        "ipaddr": "10.254.12.1", 
        "proto": "up"
    }
]

```

When you combine netmiko with TextFSM, you get a pseudo-API comparable to Cisco Nexus NX-API or Arista eAPI that takes a command in and returns structured data.


#### Step 4

Feel free to make changes as you desire and try other commands.

This is a list of commands / templates of common commands.

For an exact list of commands supported, navigate [here](https://github.com/networktocode/ntc-templates/templates)

* arista_eos_show_clock.template                 
* cisco_ios_show_ip_arp.template             
* cisco_nxos_show_flogi_database.template
* arista_eos_show_interfaces_status.template     
* cisco_ios_show_ip_bgp_summary.template     
* cisco_nxos_show_interface_brief.template
* arista_eos_show_ip_access-lists.template       
* cisco_ios_show_ip_bgp.template             
* cisco_nxos_show_interface_status.template
* arista_eos_show_ip_arp.template                
* cisco_ios_show_ip_int_brief.template       
* cisco_nxos_show_inventory.template
* arista_eos_show_ip_interface_brief.template    
* cisco_ios_show_ip_ospf_neighbor.template   
* cisco_nxos_show_ip_arp_detail.template
* arista_eos_show_lldp_neighbors.template        
* cisco_ios_show_ip_route.template           
* cisco_nxos_show_ip_ospf_neighbor_vrf.template
* arista_eos_show_mlag.template                  
* cisco_ios_show_lldp_neighbors.template     
* cisco_nxos_show_ip_route.template
* arista_eos_show_snmp_community.template        
* cisco_ios_show_mac-address-table.template  
* cisco_nxos_show_lldp_neighbors.template
* arista_eos_show_vlan.template                  
* cisco_ios_show_snmp_community.template     
* cisco_nxos_show_mac_address-table.template
* cisco_ios_show_access-list.template            
* cisco_ios_show_spanning-tree.template      
* cisco_nxos_show_port-channel_summary.template
* cisco_ios_show_cdp_neighbors.template          
* cisco_ios_show_standby_brief.template      
* cisco_nxos_show_version.template
* cisco_ios_show_clock.template                  
* cisco_ios_show_vtp_status.template         
* cisco_nxos_show_vlan.template
* cisco_ios_show_interfaces_status.template      
* cisco_nxos_show_access-lists.template      
* cisco_nxos_show_vpc.template
* cisco_ios_show_interfaces.template             
* cisco_nxos_show_cdp_neighbors.template     
* cisco_wlc_ssh_show_sysinfo.template
* cisco_ios_show_interface_transceiver.template  
* cisco_nxos_show_clock.template             
* hp_comware_display_vlan_brief.template
* cisco_ios_show_inventory.template              
* cisco_nxos_show_feature.template

You can try any of the associated commands that start with "cisco_ios" on your router (assuming the device supports the command).  The commands supported map directly to the template name removing "cisco_ios" and substituting spaces for underscores.


**Once you see and understand the data coming back, you can use it in your own scripts.**

# STOP!

# BONUS TASKS

You should only move forward with these tasks if you have extra time. They aren't meant to be performed in the course.  They are purely bonus and challenge labs.

### Task 3 - Parsing show version command output

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
