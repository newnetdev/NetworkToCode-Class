layout: true

.footer-picture[![Network to Code Logo](slides/media/Footer2.PNG)]
.footnote-left[(C) 2015 Network to Code, LLC. All Rights Reserved. ]
.footnote-con[CONFIDENTIAL]

---

class: center, middle, title
.footer-picture[<img src="slides/media/Footer1.PNG" alt="Blue Logo" style="alight:middle;width:350px;height:60px;">]

# Python Network Libraries

---

# Module Overview

- Python Libraries
- netmiko
- argparse
- Regular Expressions 101
- TextFSM
- NAPALM

---




class: middle, segue

# Python Libraries
### Introduction to Python for Network Engineers

---

class: ubuntu

# Python Libraries 

* Python modules
  * Standalone Python file used to share code between programs
* Python packages
  * Collection of Python modules

Examples:

```
import json
import sys

```

---


# Example Script

Filename: `common.py`

```python
#! /usr/bin/env python

def show(command):
    print "Sending 'show' command..."
    print 'Command sent: ', command

def config(command):
    print "Sending 'config' command..."
    print 'Commands sent: ', command

if __name__ == "__main__":
    command = 'show version'
    show(command)
    command = 'interface Eth1/1 ; shutdown'
    config(command)

```

---

# Example Script Output

Running `common.py` as a standalone program:

.ubuntu[
```
netdev@networktocode:~$ python common.py 

Sending 'show' command...
Command sent:  show version

Sending 'config' command...
Commands sent:  interface Eth1/1 ; shutdown 
```
]

Remember, the code under the entry point conditional is only executed when the file is run as a standalone program

What if you just wanted to use a function from within `common.py`?


---

class: ubuntu 

# Re-Usable Python Objects

What if we wanted to re-use objects (function, variables) from this file in another program?

Remember the filename is called `common.py`

```
def show(command):
    print "Sending 'show' command..."
    print 'Command sent: ', command

def config(command):
    print "Sending 'config' command..."
    print 'Commands sent: ', command

if __name__ == "__main__":
    # Code only executed when ran as a a program
    # More flexibility than not using the entry point when
    # you're re-suing objects in other programs
```

--

.left-column[
```
>>> import common
>>> 
>>> common.show('show version')
Sending 'show' command...
Command sent:  show version
>>> 
```
]
--
.right-column[
```
>>> import common
>>> 
>>> common.config('no router ospf 1')
Sending 'config' command...
Commands sent:  no router ospf 1
>>>  
```
]




---

class: ubuntu 

# Using from/import and re-naming objects


.left-column[
```
>>> from common import show
>>> 
>>> show('show ip int brief')
Sending 'show' command...
Command sent:  show ip int brief
>>>
```
]
--
.right-column[
```
>>> from common import config
>>> 
>>> config('interface Ethernet2/1 ; no shut')
Sending 'config' command...
Commands sent:  interface Ethernet2/1 ; no shut
>>>  
```
]

--

- Use `as` to rename objects as you import them
- Helpful to reduce length of long object names and eliminate naming conflicts


.left-column[
```
>>> from common import show as sh
>>> 
>>> sh('show ip int brief')
Sending 'show' command...
Command sent:  show ip int brief
>>>
```
]

.right-column[
```
>>> from common import config as cfg
>>> 
>>> cfg('interface Ethernet2/1 ; no shut')
Sending 'config' command...
Commands sent:  interface Ethernet2/1 ; no shut
>>>  
```
]

---

class: ubuntu

# The PYTHONPATH

* For testing, as we are doing in the course, you need to use your Python module from within the same directory where it exists
  * Enter the Python shell where the module exists
  * Write a new program and place in same directory where the module exists

OR...update your PYTHONPATH

```
ntc@ntc:~$ env | grep "PYTHON"
PYTHONPATH=/home/ntc/python/libraries/
```

One option is to update the PYTHONPATH in `.bashrc` so changes are persistent :

```
export PYTHONPATH=$PYTHONPATH:/home/ntc/new/path
```


---

# Summary

- Functions are a great way to re-use code within a program
- Modules are a great way to re-used between programs
- Packages are a collection of modules

---

class: middle, segue

# netmiko
### Python Network Libraries

---

# Netmiko Overview

- Python library that simplifies SSH management to network devices
- Based on the Paramiko SSH library

**The purposes of the library are the following:**

- Successfully establish an SSH connection to the device
- Simplify the execution of show commands and the retrieval of output data
- Simplify execution of configuration commands including possibly commit actions
- Do the above across a broad set of networking vendors and platforms

---

# Supported Platforms

.left-column[
* Arista vEOS
* Cisco ASA
* Cisco IOS
* Cisco IOS-XR
* Cisco SG300
* HP Comware7
* HP ProCurve
* Juniper Junos
* Linux 
* Brocade VDX (limited)
* Brocade ICX/FastIron (limited)
* Brocade MLX/NetIron (limited)
]
.right-column[
* Avaya ERS (limited)
* Avaya VSP (limited)
* Cisco IOS-XE (limited)
* Cisco NX-OS (limited)
* Cisco WLC (limited)
* Dell-Force10 DNOS9 (limited)
* Huawei (limited)
* Palo Alto PAN-OS (limited)
* Vyatta VyOS  (limited)
]

---

# Supported Platforms (experimental)

.left-column[
* A10
* Alcatel-Lucent SR-OS
* Enterasys
* Extreme
* F5 LTM
* Fortinet 
]

---

# Getting Started with Netmiko


```python
>>> from netmiko import ConnectHandler
>>> 
>>> device = ConnectHandler(device_type='cisco_nxos', ip='n9k1', username='cisco', password='cisco')`
>>>

```

--

We could have also done: 

```python
>>> args = dict(device_type='cisco_nxos', ip='n9k2', username='cisco', password='cisco')
>>> 
>>> device = ConnectHandler(**args)
>>> 
```

Note: `**` as in `**args` is used to treat a dictionary (single object) as multiple key-value pairs.

---

# Using Netmiko

Send a command to the device 

```python
>>> device.send_command_timing('show hostname')
u'N9K1.cisconxapi.com '
>>>
```

Send a command to the device and wait for a string (prompt).

Default waits for the previous prompt string to return.

```python
>>> device.send_command('copy run start')
# output omitted
>>>
```


---

# Using netmiko (cont'd)

Enter config mode

```python
>>> device.config_mode()
u'config term\nEnter configuration commands, one per line. End with CNTL/Z.\nN9K1(config)# '
```


Send configuration mode command (must using timing here)

```python
>>> device.send_command_timing('hostname NEW_HOSTNAME')
u'NEW_HOSTNAME(config)# '
>>> 
```

Same result can be achieved specifying `expect_string` within `send_command`

```python
>>> device.send_command('hostname NEWER_HOSTNAME', expect_string='NEWER_HOSTNAME')
u'NEWER_HOSTNAME(config)# '
>>> 
```

Exit configuration mode

```python
device.exit_config_mode()
```

---

# Using netmiko (cont'd)

Storing & Printing a command response

```python
>>> vlans = device.send_command_expect('show vlan')
>>> 
>>> print vlans

VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Eth1/2, Eth1/3, Eth1/8, Eth1/9
                                                Eth1/11, Eth1/12, Eth1/13, Eth2/9
                                                Eth2/10, Eth2/11, Eth2/12
2    VLAN0002                         active    Po10, Po11, Po12, Eth1/4
                                                Eth1/5, Eth1/6, Eth1/7, Eth2/5
                                                Eth2/6
3    VLAN0003                         active    Po10, Po11, Po12, Eth1/4
                                                Eth1/5, Eth1/6, Eth1/7, Eth2/5
                                                Eth2/6
4    VLAN0004                         active    Po10, Po11, Po12, Eth1/4
                                                Eth1/5, Eth1/6, Eth1/7, Eth2/5
                                                Eth2/6
5    VLAN0005                         active    Po10, Po11, Po12, Eth1/4
                                                Eth1/5, Eth1/6, Eth1/7, Eth2/5
                                                Eth2/6

# shortened for brevity
```

---

# Using netmiko (cont'd)

Check your current prompt

```python
>>> device.find_prompt()
u'NEW_HOSTNAME#'
>>> 
```

---

### Primary List of Methods

* config_mode() -- Enter into config mode
* enable() -- Enter enable mode
* establish_connection() -- Establish SSH connection to device
* exit_enable_mode() -- Exit enable mode
* find_prompt() -- Return the current router prompt
* commit() -- Execute a commit action on Juniper and IOS-XR
* disconnect() -- Close the SSH connection
* send_command_timing() - Send command down the SSH channel, return output back (uses timer to wait for device)
* send_command_expect() -- Send command to device; retrieve output until router_prompt or expect_string
* send_config_set() -- Send a set of configuration commands to remote device
* send_config_from_file() -- Send a set of configuration commands loaded from a file


---

# Summary

- Legacy devices are here to stay (for awhile)
- Great way to bridge the gap between legacy and modern devices that return structured data

- Netmiko is a great library to integrate with TextFSM to create a psuedo-API
    -  CLI commands gets sent to the device and you get returned structured data
    -  We cover how to do this with Ansible

---

# Lab Time

- Lab 12 - Introduction to Netmiko
    - Choose either IOS or JUNOS

- Lab 13 -  Use Netmiko to interactively communicate with a network switch
 

---


class: middle, segue

# Command Line Arguments
### Introduction to Python for Network Engineers

---
class: ubuntu

# User interaction - Prompting users for input

- The `raw_input` (Python 2.x) or `input` (Python 3.x) built-in function is used to collect user input, interactively

- Prompt the user for data that can then be stored as a variable and used in the script


``` python

number_of_routers = raw_input('Enter the number of routers in the mesh:')

num_routers = int(number_of_routers)

number_of_connections = ( num_routers * (num_routers - 1) )/2

print("For a full mesh of {} routers, you will need {} connections".format(num_routers, number_of_connections))

```

---

# Passing in Arguments

- Using the `sys` module
  - `argv` is a attribute (variable) within the `sys` module that makes it fast and easy to pass variables in from the command line
+ Using `argparse` module
  - Built-in module that allows for more functionality such as defining a help menu and using user-friendly flags

---

# sys.argv 

- It's a variable that is of type `list`

  ```python
  #! /usr/bin/env python

  import sys

  if __name__ == "__main__":

      print sys.argv

  ```

--
- Script name is `argv[0]`

.ubuntu[```
ntc@ntc:~$ python args_test.py hello world 10.1.1.1 NYCR1
['args_test.py', 'hello', 'world', '10.1.1.1', 'NYCR1']
```
]

---

# Example - sys.argv

Objective:

- Pass in the "fact" you want to see the value for and the proper key-value pair will be printed from the `facts` dictionary.

Dictionary: 

```python
facts = {'vendor': 'cisco', 'mgmt_ip': '10.1.1.1', 'model': 'nexus', 'hostname': 'NYC301', 'os': '6.1.2'}
```

User experience:
.ubuntu[```
ntc@ntc:~$ python print_facts.py model
model: nexus
```
]
---

# Examining the Code

```python
#! /usr/bin/env python

import sys

if __name__ == "__main__":

    facts = {'vendor': 'cisco', 'mgmt_ip': '10.1.1.1', 'model': 'nexus', 'hostname': 'NYC301', 'os': '6.1.2'}

    args = sys.argv        # assign argv to args (optional; cleans up the code)

    fact_to_print = args[1]      # assign the second element to my_fact

    print fact_to_print + ': ' + facts[fact_to_print]

    print args             # added for example below
```

.ubuntu[
```
ntc@ntc:~$ python print_facts.py model
model: nexus
['print_facts.py', 'model']
```
]
---

# argparse

- Python module that simplifies defining a help menu, using user-friendly flags, and much more

.ubuntu[
```
ntc@ntc:~$ python get_facts.py -f model
model: nexus
ntc@ntc:~$ python get_facts.py -f=model
model: nexus
ntc@ntc:~$ python get_facts.py --f=model
model: nexus
ntc@ntc:~$ python get_facts.py --fact=model
model: nexus
ntc@ntc:~$ python get_facts.py --fact model
model: nexus
```
]
--

```python
import argparse

if __name__ == "__main__":

    facts = {'vendor': 'cisco', 'mgmt_ip': '10.1.1.1', 'model': 'nexus', 'hostname': 'NYC301', 'os': '6.1.2'}

    parser = argparse.ArgumentParser(description='Python Argparse Demo')
    parser.add_argument('-f', '--fact', help='enter a valid fact from the device facts dictionary')

    args = parser.parse_args()

    print args.fact + ': ' + facts[args.fact]

```

---

class: ubuntu 
# argparse - built-in help

- Leverage help menu natively built-in
- Can be disabled if needed when parser is instantiated 

```
ntc@ntc:~$ python get_facts.py --help
usage: get_facts.py [-h] [-f FACT]

Python Argparse demo.

optional arguments:
  -h, --help            show this help message and exit
  -f FACT, --fact FACT  enter a valid fact from the device facts dictionary
```

---


# arparse - choices

- Built-in error validation
- What if the user enters an invalid value for argument?

.ubuntu[
```
ntc@ntc:~$ python get_facts.py --f platform
Traceback (most recent call last):
  File "get_facts.py", line 14, in <module>
    print args.fact + ': ' + facts[args.fact]
KeyError: 'platform'
```
]
--

Use the `choices` parameter:

```python
parser.add_argument('-f', '--fact', choices=['vendor', 'mgmt_ip', 'model', 'hostname', 'os'], help='enter a valid fact from the device facts dictionary')
```

---

class: ubuntu

# argparse - Using choices

```
ntc@ntc:~$ python get_facts.py --f platform
usage: get_facts.py [-h] [-f {vendor,mgmt_ip,model,hostname,os}]
get_facts.py: error: argument -f/--fact: invalid choice: 'platform' (choose from 'vendor', 'mgmt_ip', 'model', 'hostname', 'os')
```
--
```
ntc@ntc:~$ python get_facts.py -h
usage: get_facts.py [-h] [-f {vendor,mgmt_ip,model,hostname,os}]

Python Argparse Demo

optional arguments:
  -h, --help            show this help message and exit
  -f {vendor,mgmt_ip,model,hostname,os}, --fact {vendor,mgmt_ip,model,hostname,os}
                        enter a valid fact from the device facts dictionary

```

---

class: ubuntu

# argparse - Multiple arguments

Objective:

- Pass in a fact you want to see the value for, but also include a description
- Code was modified to also print the description

```
ntc@ntc:~$ python get_facts.py -h
usage: get_facts.py [-h] [-f {vendor,mgmt_ip,model,hostname,os}] [-d DESCR]

Python Argparse Demo

optional arguments:
  -h, --help            show this help message and exit
  -f {vendor,mgmt_ip,model,hostname,os}, --fact {vendor,mgmt_ip,model,hostname,os}
                        enter a valid fact from the device facts dictionary
  -d DESCR, --descr DESCR
                        enter a description for this job

```

```
ntc@ntc:~$ python get_facts.py -f hostname -d "Test Job"
hostname: NYC301
Test Job
```

---

# argparse - Adding descr argument

```python
import argparse

if __name__ == "__main__":

    facts = {'vendor': 'cisco', 'mgmt_ip': '10.1.1.1', 'model': 'nexus', 'hostname': 'NYC301', 'os': '6.1.2'}

    parser = argparse.ArgumentParser(description='Python Argparse Demo')
    parser.add_argument('-f', '--fact', help='enter a valid fact from the device facts dictionary')
    parser.add_argument('-d', '--descr', help='enter a description for this job')

    args = parser.parse_args()

    print args.fact + ': ' + facts[args.fact]
    print args.descr

```




---

# Summary

- For quick testing `sys.argv` is a great option
- For a more robut script, you want others to use and to have a more defined help menu, `argparse` is the way to go
  - Supports more features, feel free to continue to digging!

---

# Lab Time

- Lab 14 - Gathering User input with Command Line Arguments
  - Prompt user input using `raw_input` and process the input
  - Continue to build on the neighbors script from previous labs and only print certain neighbor and device information based on the arguments being passed in
  - Write a basic script using `sys.argv` that prints arguments


---

class: middle, segue

# Regular Expressions
### Python Network Libraries

---


# RegEx Overview

- A Regular Expression (RegEx) is a special sequence of characters used to search patterns inside text.
- They are a powerful tool for:
  - Checking if a specific pattern is present inside a text.
  - Parsing unstructured output from a network device.

---

# Web Utilities for Testing

Online tools used for testing and learning regular expressions

- Regexr.com (picture below)
- Regex101.com



.center[
<img src="slides/media/regexr/regexr1.png" alt="Regexr.com Example" style="alight:middle;width:800px;height:325px;">
]

---

# Regex patterns

- **\d**: Matches any decimal digit
- **\D**: Matches any non-digit character
- **\w**: Matches any alphanumeric character
- **\W**: Matches any non-alphanumeric character
- **\s**: Matches any whitespace character
- **\S**: Matches any non-whitespace character
- **.**: Matches anything except a newline character
- **+**: Specifies that the previous character can be matched one or more times
- ** * **: Specifies that the previous character can be matched zero or more times
- ** ? **: Matches either once or zero times. Indicates something as being optional
    - Example: **ntc-?training** matches either **ntctraining** or **ntc-training**


---


# Demo

* Review Regular Expressions using Regexr.com


---
class: middle, segue

# TextFSM
### Python Network Libraries

---


# TextFSM Overview

- Python module for parsing semi-formatted text.
- Originally developed to allow programmatic access to information given by the output of CLI driven devices, such as network routers and switches
  - It can however be used for any such textual output.

---

# Using TextFSM

- The engine takes two inputs
  - Template file
  - Text input (such as command responses from the CLI of device)
- Returns a list of records that contains the data parsed from the text.
- Note: A template file is needed for each uniquely structured text input.

---

class: middle, segue

# TextFSM
### Network Examples

---

# Example 1: Text Input 

- show vlan (Arista EOS)
- Filename: `arista_eos_show_vlan.raw `

```bash
VLAN  Name                             Status    Ports
----- -------------------------------- --------- -------------------------------
1     default                          active    Et1
10    Test1                            active    Et1, Et2
20    Test2                            suspended
30    VLAN0030                         suspended
```

---

# Example 1: Template File

- show vlan (Arista EOS)
- Order is important
- Filename: `arista_eos_show_vlan.template`

```bash
Value VLAN_ID (\d+)
Value NAME (\w+)
Value STATUS (active|suspended)

Start
  ^${VLAN_ID}\s+${NAME}\s+${STATUS} -> Record
```

---

# Example 1: Executing textfsm

```bash
VLAN  Name                             Status    Ports
----- -------------------------------- --------- -------------------------------
1     default                          active    Et1
```

.ubuntu[
```
ntc@ntc$ python textfsm.py arista_eos_show_vlan.template arista_eos_show_vlan.raw 
FSM Template:
Value VLAN_ID (\d+)
Value NAME (\w+)
Value STATUS (active|suspended)

Start
  ^${VLAN_ID}\s+${NAME}\s+${STATUS} -> Record


FSM Table:
['VLAN_ID', 'NAME', 'STATUS']
['1', 'default', 'active']
['10', 'Test1', 'active']
['20', 'Test2', 'suspended']
['30', 'VLAN0030', 'suspended']
```
]

---

# Example 2: Text Input 

- show version (Cisco IOS)
- Filename: `cisco_ios_show_version.raw`

```bash
Cisco IOS XE Software, Version 16.03.01
Cisco IOS Software [Denali], CSR1000V Software (X86_64LINUX_IOSD-UNIVERSALK9-M), Version 16.3.1, RELEASE SOFTWARE (fc3)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2016 by Cisco Systems, Inc.
Compiled Tue 02-Aug-16 18:36 by mcpre

ROM: IOS-XE ROMMON

csr1 uptime is 2 minutes
Uptime for this control processor is 5 minutes
System returned to ROM by reload
System image file is "bootflash:packages.conf"
Last reload reason: reload

cisco CSR1000V (VXE) processor (revision VXE) with 2047392K/3075K bytes of memory.
Processor board ID 9KXI0D7TVFI
4 Gigabit Ethernet interfaces
32768K bytes of non-volatile configuration memory.
3984776K bytes of physical memory.
7774207K bytes of virtual hard disk at bootflash:.
0K bytes of  at webui:.

Configuration register is 0x2102
```

---

# Example 3: Template File

- show version (Cisco IOS)
- Filename: `cisco_ios_show_version.template`

```bash
Value VERSION (.+?)
Value HOSTNAME (\S+)
Value UPTIME (.+)
Value CONFIG_REGISTER (\S+)

Start
  ^.*Software\s.+\),\sVersion\s${VERSION},*\s+RELEASE.*
  ^\s*${HOSTNAME}\s+uptime\s+is\s+${UPTIME}
  ^[Cc]onfiguration\s+register\s+is\s+${CONFIG_REGISTER} -> Record

```

---

# Example 2: Executing textfsm

.ubuntu[
```
ntc@ntc$ python textfsm.py cisco_ios_show_version.template cisco_ios_show_version.raw 
FSM Template:
Value VERSION (.+?)
Value HOSTNAME (\S+)
Value UPTIME (.+)
Value CONFIG_REGISTER (\S+)

Start
  ^.*Software\s.+\),\sVersion\s${VERSION},*\s+RELEASE.*
  ^\s*${HOSTNAME}\s+uptime\s+is\s+${UPTIME}
  ^[Cc]onfiguration\s+register\s+is\s+${CONFIG_REGISTER}


FSM Table:
['VERSION', 'HOSTNAME', 'UPTIME', 'CONFIG_REGISTER']
['16.3.1', 'csr1', '2 minutes', '0x2102']
```
]

---

# Using TextFSM in Python

From Example 1:

```python
>>> import textfsm
>>>
>>> table = textfsm.TextFSM(open('arista_eos_show_vlan.template'))
>>> 
>>> data = table.ParseText(open('arista_eos_show_vlan.raw').read())
>>> 
>>> 
>>> data
[['1', 'default', 'active'], ['10', 'Test1', 'active'], ['20', 'Test2', 'suspended'], ['30', 'VLAN0030', 'suspended']]
>>> 
>>> table.header
['VLAN_ID', 'NAME', 'STATUS']
>>>
```

---

# Using TextFSM in Python (cont'd)

From Example 2:

```python
>>> import textfsm
>>> 
>>> table = textfsm.TextFSM(open('cisco_ios_show_version.template'))
>>> 
>>> data = table.ParseText(open('cisco_ios_show_version.raw').read())
>>> # data.table.ParseText(rawtext)
>>> 
>>> data
[['16.3.1', 'csr1', '2 minutes', '0x2102']]
>>> 
>>> table.header
['VERSION', 'HOSTNAME', 'UPTIME', 'CONFIG_REGISTER']
>>> 
```

---

# Summary

- Legacy devices are here to stay (for awhile)
- Even API-enabled device may return raw text
- Using TextFSM does not necessarily mean SSH/telnet as a transport mechanism
- Great way to bridge the gap between legacy and modern devices that return structured data

---



class: middle, segue

# Managing TextFSM Templates
### Python Network Libraries

---

# clitable (TextFSM object)

- Builds upon textfsm object
- Simplifies use of pre-created templates
- Maps CLI commands to the proper template
  - Uses an index file and a templates directory
- Provides a better abstraction for consumers of templates

---

class: ubuntu

# Templates Directory

- List of templates that `clitable` can use

```
cisco@ntc:~/projects/legacy/ntc_templates$ ls
arista_eos_show_clock.template                 cisco_ios_show_snmp_community.template
arista_eos_show_interfaces_status.template     cisco_ios_show_spanning-tree.template
arista_eos_show_ip_access-lists.template       cisco_ios_show_standby_brief.template
arista_eos_show_ip_arp.template                cisco_ios_show_vtp_status.template
arista_eos_show_ip_interface_brief.template    cisco_nxos_show_access-lists.template
arista_eos_show_lldp_neighbors.template        cisco_nxos_show_cdp_neighbors.template
arista_eos_show_mlag.template                  cisco_nxos_show_clock.template
arista_eos_show_snmp_community.template        cisco_nxos_show_feature.template
arista_eos_show_vlan.template                  cisco_nxos_show_flogi_database.template
cisco_ios_show_access-list.template            cisco_nxos_show_interface_brief.template
cisco_ios_show_cdp_neighbors.template          cisco_nxos_show_interface_status.template
cisco_ios_show_clock.template                  cisco_nxos_show_inventory.template
cisco_ios_show_interfaces_status.template      cisco_nxos_show_ip_arp_detail.template
cisco_ios_show_interfaces.template             cisco_nxos_show_ip_ospf_neighbor_vrf.template
cisco_ios_show_interface_transceiver.template  cisco_nxos_show_ip_route.template
cisco_ios_show_inventory.template              cisco_nxos_show_lldp_neighbors.template
cisco_ios_show_ip_arp.template                 cisco_nxos_show_mac_address-table.template
cisco_ios_show_ip_bgp_summary.template         cisco_nxos_show_port-channel_summary.template
cisco_ios_show_ip_bgp.template                 cisco_nxos_show_version.template
cisco_ios_show_ip_int_brief.template           cisco_nxos_show_vlan.template
cisco_ios_show_ip_ospf_neighbor.template       cisco_nxos_show_vpc.template
cisco_ios_show_ip_route.template               cisco_wlc_ssh_show_sysinfo.template
cisco_ios_show_lldp_neighbors.template         hp_comware_display_vlan_brief.template
cisco_ios_show_mac-address-table.template      index
```

---

class: ubuntu

# Index File

- Maps Template to **Platform** specific **Command** 
  - Can get more granular by specifying **Hostname** too

```
ntc@ntc:~/projects/legacy$ more ntc_templates/index 

# First line is the header fields for columns and is mandatory.
# Regular expressions are supported in all fields except the first.
# Last field supports variable length command completion.
# abc[[xyz]] is expanded to abc(x(y(z)?)?)?, regexp inside [[]] is not supported
#
Template, Hostname, Platform, Command
cisco_nxos_show_vlan.template, .*, cisco_nxos, sh[[ow]] vl[[an]]
cisco_ios_show_ip_int_brief.template, .*, cisco_ios, sh[[ow]] ip int[[erface]] br[[ief]]
cisco_nxos_show_ip_route.template, .*, cisco_nxos, sh[[ow]] ip route
hp_comware_display_vlan_brief.template, .*, hp_comware, di[[splay]] v[[lan]] b[[rief]]
cisco_nxos_show_version.template, .*, cisco_nxos, sh[[ow]] ver[[sion]]
cisco_wlc_ssh_show_sysinfo.template, .*, cisco_wlc_ssh, sh[[ow]] sysi[[nfo]]
cisco_ios_show_ip_ospf_neighbor.template, .*, cisco_ios, sh[[ow]] ip ospf nei[[ghbor]]
cisco_nxos_show_feature.template, .*, cisco_nxos, sh[[ow]] feat[[ure]]
arista_eos_show_vlan.template, .*, arista_eos, sh[[ow]] vl[[an]]
cisco_nxos_show_mac_address-table.template, .*, cisco_nxos, sh[[ow]] m[[ac]] addr[[ess-table]]
cisco_ios_show_snmp_community.template, .*, cisco_ios, sh[[ow]] sn[[mp]] com[[munity]]
cisco_ios_show_access-list.template, .*, cisco_ios, sh[[ow]] acc[[ess-list]]
arista_eos_show_clock.template, .*, arista_eos, sh[[ow]] cl[[ock]]

```

---


# Using clitable in Python

```python
import clitable

index_file = 'index'
template_dir = '/etc/ntc/ansible/library/ntc-ansible/ntc-templates/templates'

cli_table = clitable.CliTable(index_file, template_dir)

command = 'show vlan'
platform = 'cisco_nxos'

# keys map directly back to column headers in the index file (see previous slide)
attrs = {'Command': command, 'Platform': platform}

# rawtxt is the show output as a string; could be from a file or from device in real-time
cli_table.ParseCmd(rawtxt, attrs)

print cli_table 
```

--

```bash
>>> print cli_table
VLAN_ID, NAME, STATUS
1, default, active
10, Test1, active
20, Test2, suspended
30, VLAN0030, suspended

>>> type(cli_table)
<class 'clitable.CliTable'>

```


---

class: ubuntu

# Simplifying CliTable Objects

- `clitable_to_dict()`
- Creates list of dictionaries from a `CliTable` object
- For commands like `show version`, it still creates a list of one element

```
>>> from ntc_course import clitable_to_dict
>>> 
>>> help(clitable_to_dict)
>>>

Help on function clitable_to_dict in module ntc_course:

clitable_to_dict(cli_table)
    Converts TextFSM cli_table object to list of dictionaries
    Borrowed for this course from the ntc-ansible project at
    github.com/networktocode/ntc-ansible/library/ntc_show_command
(END)

```

---

class: ubuntu 

# Covert CliTable to List of Dictionaries

```
>>> print cli_table
VLAN_ID, NAME, STATUS
1, default, active
10, Test1, active
20, Test2, suspended
30, VLAN0030, suspended
>>>
>>> type(cli_table)
<class 'clitable.CliTable'>

```

```
>>> from ntc_course import clitable_to_dict
>>> 
>>> clitable_to_dict(cli_table)
[{'vlan_id': '1', 'name': 'default', 'status': 'active'}, 
{'vlan_id': '10', 'name': 'Test1', 'status': 'active'},
{'vlan_id': '20', 'name': 'Test2', 'status': 'suspended'},
{'vlan_id': '30', 'name': 'VLAN0030', 'status': 'suspended'}]
```

---

# Summary

- Level of abstraction above textfsm.py
- clitable makes it you don't have to know which template you need to call
- Rather, you know the command and Command and Platform

---
# Lab Time

- Lab 15 - TextFSM
  - Use TextFSM to parse `show ip interface brief` from a Cisco Nexus switch
  - Use `clitable` along with `netmiko` to generate structured data from unstructured device output

  - **Note: same workflow and process can be used for any other device.**

---

class: middle, segue

# NAPALM
### Network APIs

---


# NAPALM

_NAPALM (Network Automation and Programmability Abstraction Layer with Multivendor support) is a Python library that implements a set of functions to interact with different network device Operating Systems using a unified API._

_NAPALM supports several methods to connect to the devices, to manipulate configurations or to retrieve data._

https://napalm.readthedocs.io/en/latest/



---

# NAPALM Support Matrix

* Palo Alto PANOS
* Cisco IOS
* Cisco NX-OS
* Cisco IOS-XR
* Arista EOS
* Juniper Junos
* IBM
* Pluribus
* FortiOS
* Cumulus Linux
* Actively growing

---

# NAPALM

Three core functions:

* Retrieving Data
* Declarative Configuration Management
* Deployment Validation

All three are done in a uniform and vendor-neutral fashion

---

class: ubuntu

# Retrieving Data

**Uses a uniform and consistent data model across all device types supported by NAPALM**

.left-column[

- get_facts()
- get_arp_table()
- get_bgp_config()
- get_bgp_neighbors()
- get_bgp_neighbors_detail()
- get_interfaces()
- get_interfaces_counters()
- get_lldp_neighbors()
- get_lldp_neighbors_detail()
]

.right-column[
- get_ntp_peers()
- get_ntp_stats()
- get_ntp_servers()
- ... plus another dozen and growing...
]


---

class: ubuntu

# get_facts()

Network Device Facts

```
>>> device.get_facts()
{'os_version': u'4.15.2F-2663444.4152F', 'uptime': 5817, 'interface_list': [u'Ethernet1', u'Ethernet2', u'Ethernet3', u'Ethernet4', u'Ethernet5', u'Ethernet6', u'Ethernet7', u'Management1'], 'vendor': u'Arista', 'serial_number': u'', 'model': u'vEOS', 'hostname': u'eos-spine1', 'fqdn': u'eos-spine1.ntc.com'}
>>> 
>>> facts = device.get_facts()
>>> 
>>> import json
>>> 
>>> print json.dumps(facts, indent=4)
{
    "os_version": "4.15.2F-2663444.4152F", 
    "uptime": 5837, 
    "interface_list": [
        "Ethernet1", 
        "Ethernet2", 
        "Ethernet3", 
        "Ethernet4", 
        "Ethernet5", 
        "Ethernet6", 
        "Ethernet7", 
        "Management1"
    ], 
    "vendor": "Arista", 
    "serial_number": "", 
    "model": "vEOS", 
    "hostname": "eos-spine1", 
    "fqdn": "eos-spine1.ntc.com"
}
>>> 
```

---

class: ubuntu

# get_interfaces()

Gathering Interfaces Info


```
>>> device.get_interfaces()
{u'Management1': {'is_enabled': True, 'description': u'', 'last_flapped': 1467419703.021217, 'is_up': True, 'mac_address': u'2c:c2:60:0d:52:90', 'speed': 1000}, u'Ethernet2': {'is_enabled': True, 'description': u'', 'last_flapped': 1467419702.781202, 'is_up': True, 'mac_address': u'2c:c2:60:12:98:52', 'speed': 1000}, u'Ethernet3': {'is_enabled': True, 'description': u'', 'last_flapped': 1467419702.781203, 'is_up': True, 'mac_address': u'2c:c2:60:60:20:9b', 'speed': 1000}, u'Ethernet1': {'is_enabled': True, 'description': u'', 'last_flapped': 1467419703.1052225, 'is_up': True, 'mac_address': u'2c:c2:60:2d:45:d5', 'speed': 1000}, u'Ethernet6': {'is_enabled': True, 'description': u'', 'last_flapped': 1467419702.781202, 'is_up': True, 'mac_address': u'2c:c2:60:48:80:70', 'speed': 1000}, u'Ethernet7': {'is_enabled': True, 'description': u'', 'last_flapped': 1467419702.8092043, 'is_up': True, 'mac_address': u'2c:c2:60:40:8d:10', 'speed': 1000}, u'Ethernet4': {'is_enabled': True, 'description': u'', 'last_flapped': 1467419702.769202, 'is_up': True, 'mac_address': u'2c:c2:60:2e:c6:f8', 'speed': 1000}, u'Ethernet5': {'is_enabled': True, 'description': u'', 'last_flapped': 1467419703.105223, 'is_up': True, 'mac_address': u'2c:c2:60:60:7d:ba', 'speed': 1000}}
>>> 

```


---

class: ubuntu

# get_interfaces() (cont'd)


.left-column[

```
>>> interfaces = device.get_interfaces()
>>> 
>>> print json.dumps(interfaces, indent=4)
{
    "Management1": {
        "is_enabled": true, 
        "description": "", 
        "last_flapped": 1467419703.0212176, 
        "is_up": true, 
        "mac_address": "2c:c2:60:0d:52:90", 
        "speed": 1000
    }, 
    "Ethernet2": {
        "is_enabled": true, 
        "description": "", 
        "last_flapped": 1467419702.7812023, 
        "is_up": true, 
        "mac_address": "2c:c2:60:12:98:52", 
        "speed": 1000
    }, 
    "Ethernet3": {
        "is_enabled": true, 
        "description": "", 
        "last_flapped": 1467419702.7812028, 
        "is_up": true, 
        "mac_address": "2c:c2:60:60:20:9b", 
        "speed": 1000
    }, 
```
]

.right-column[

```
    "Ethernet1": {
        "is_enabled": true, 
        "description": "", 
        "last_flapped": 1467419702.781203, 
        "is_up": true, 
        "mac_address": "2c:c2:60:48:80:70", 
        "speed": 1000
    }, 
    "Ethernet5": {
        "is_enabled": true, 
        "description": "", 
        "last_flapped": 1467419702.8092043, 
        "is_up": true, 
        "mac_address": "2c:c2:60:40:8d:10", 
        "speed": 1000
    }, 
    "Ethernet4": {
        "is_enabled": true, 
        "description": "", 
        "last_flapped": 1467419702.7692015, 
        "is_up": true, 
        "mac_address": "2c:c2:60:2e:c6:f8", 
        "speed": 1000
    }
}


```
]

---

class: ubuntu

# get_interfaces_ip()

Get Interfaces IP Addresses

```
>>> {u'Management1': {u'ipv4': {u'10.0.0.11': {u'prefix_length': 24}}, u'ipv6': {}}}
{u'Management1': {u'ipv4': {u'10.0.0.11': {u'prefix_length': 24}}, u'ipv6': {}}}
>>>
```

---

class: ubuntu

# get_environment()

Device Environment Status

```
>>> device.get_environment()
{u'fans': {}, u'memory': {u'available_ram': 99060, u'used_ram': 1798476}, u'temperature': {}, u'power': {}, u'cpu': {0: {u'%usage': 5.4}}}
>>>
```

---

# NAPALM Configuration Management

Two main ways to manage device configurations with NAPALM

**Configuration Replace**

* Declarative configuration always pushing the full configuration
* Only commands required to get the device into its intended state are applied
* No "negation (no)" commands are sent to the device


**Configuration Merge**

* Send a set of commands or configuration stanza
* Only commands required to get the device into its intended state are applied
* You can use the merge for declarative management on a stanza based on OS

It does vary based on operating system.


---

class: ubuntu

# How NAPALM Works

* EOS
  - Creates and locks config sessions
  - Uses `rollback clean-config` to prepare for a config replace
  - Commit is performed issuing `copy startup-config flash:rollback-0`, `configure session #` and `commit`
  - Rollback is performed issuing `configure replace flash:rollback-0`
  - Diffs are generated on the device using the `show session-config named <file> diffs`

* IOS
  - Uses SCP or Netmiko (TCL) to transfer config files for config replace/merge
  - Uses `show archive config differences <base_file> <new_file>` to show diffs for config replace
  - Uses `show archive config incremental-diffs <file> ignorecase` to show incremental diffs
  - Replaces with `configure replace <file> force`. Merges with `copy <file> running-config`


---

class: ubuntu

# How NAPALM Works

* Junos
  - Uses junos-pyez API
  - Locks configurations while performing operations till first commit/rollback
  - Uses `rollback 0` to rollback configuration

* NXOS
  - Uses checkpoint files for config replacement. A checkpoint file can be obtained with `device._get_checkpoint_file()` which issues `checkpoint file temp_cp_file_from_napalm` on the device and then prints it
  - Diffs for config replacement are a list of commands that would be needed to take the device from its current state to the desired config state using `show diff rollback-patch file <source_of_truth_file> file <config_file>` command
  - Merges send config line by line. This doesn’t use the checkpoint/rollback functionality. As a result, merges are not atomic
  - Replaces uses `rollback running file <config_file>` command


---

# NAPALM Configuration Management

**Example Workflow**

Works slightly different than based on individual drivers and operating systems.

1. Connect to Device
2. Copy desired configuration to device (checkpoint file, candidate configuration, config session, bootflash as candidate_config.txt)
3. Use a vendor command to view diffs
4. Use a vendor command apply configuration changes
5. Optionally, rollback to a config that exists in the file system.

Note: you dictate if the supplised configuration is a full config file or partial configuration

---

# Performing a Full Configuration Replace

Focus on desired configuration commands.

There are no `no` commands used.  The underlying OS generates the diffs (for most NAPALM drivers).

```bash
$ more diffs/csr1.diffs 
+hostname csr1
-hostname csr_old_name
-interface Loopback100
 -ip address 1.1.1.1 255.255.255.255
```

---

# Configuration Merge (OSPF)

Performing a merge- ensuring a configuration exists.

.left-column[
Current OSPF Config
```bash
eos-spine1#show run section ospf
router ospf 100
   router-id 100.100.100.100
   network 10.0.0.10/32 area 0.0.0.0
   network 10.0.1.10/32 area 0.0.0.0
   network 10.0.2.10/32 area 0.0.0.0
   network 10.0.3.10/32 area 0.0.0.0
   network 10.0.4.10/32 area 0.0.0.0
   max-lsa 12000
eos-spine1#
```

Desired OSPF Config (file sent to device)
```bash
router ospf 100
   router-id 100.100.100.100
   network 10.0.4.10/32 area 0.0.0.0
   network 10.0.5.10/32 area 0.0.0.0
   max-lsa 12000
```

]

--

.right-column[

Diff Generated by NAPALM
```bash
@@ -54,6 +56,7 @@
    network 10.0.2.10/32 area 0.0.0.0
    network 10.0.3.10/32 area 0.0.0.0
    network 10.0.4.10/32 area 0.0.0.0
+   network 10.0.5.10/32 area 0.0.0.0
    max-lsa 12000
 !


```

]

---

# Configuration Merge (OSPF) 

You can use NAPALM for declarative management (replace) for a sectional config too. 

.left-column[
Current OSPF Config
```bash
eos-spine1#show run section ospf
router ospf 100
   router-id 100.100.100.100
   network 10.0.0.10/32 area 0.0.0.0
   network 10.0.1.10/32 area 0.0.0.0
   network 10.0.2.10/32 area 0.0.0.0
   network 10.0.3.10/32 area 0.0.0.0
   network 10.0.4.10/32 area 0.0.0.0
   max-lsa 12000
eos-spine1#
```

Desired OSPF Config (file sent to device)
```bash
no router ospf 100
router ospf 100
   router-id 100.100.100.100
   network 10.0.4.10/32 area 0.0.0.0
   network 10.0.5.10/32 area 0.0.0.0
   max-lsa 12000
```

]

--

.right-column[

Diff Generated by NAPALM
```bash
@@ -49,11 +51,8 @@
 !
 router ospf 100
    router-id 100.100.100.100
-   network 10.0.0.10/32 area 0.0.0.0
-   network 10.0.1.10/32 area 0.0.0.0
-   network 10.0.2.10/32 area 0.0.0.0
-   network 10.0.3.10/32 area 0.0.0.0
    network 10.0.4.10/32 area 0.0.0.0
+   network 10.0.5.10/32 area 0.0.0.0
    max-lsa 12000
 !


```
Be cautious of device support.  This is based on NAPALM driver implementation which is dictated by vendor OS support.  This example is EOS.
]




---

# Configuration Merge (BGP) 

You can use NAPALM for declarative management (replace) for a sectional config too
.left-column[
Current BGP Config
```bash
router bgp 65512
   neighbor 10.0.0.0 remote-as 65500
   neighbor 10.0.0.0 maximum-routes 12000 
   neighbor 10.0.0.1 remote-as 65512
   neighbor 10.0.0.1 maximum-routes 12000 
   network 20.20.20.0/24
!
```

Desired BGP Config (file sent to device)
```bash
no router bgp 65512
router bgp 65512
   neighbor 10.0.0.2 remote-as 65500
   neighbor 10.0.0.2 maximum-routes 12000
   neighbor 10.0.0.1 remote-as 65512
   neighbor 10.0.0.1 maximum-routes 12000
   neighbor 10.0.0.10 remote-as 65512
   network 100.0.100.0/24
!

```

]

--

.right-column[

Diff Generated by NAPALM
```bash
 router bgp 65512
-   neighbor 10.0.0.0 remote-as 65500
-   neighbor 10.0.0.0 maximum-routes 12000 
    neighbor 10.0.0.1 remote-as 65512
    neighbor 10.0.0.1 maximum-routes 12000 
-   network 20.20.20.0/24
+   neighbor 10.0.0.2 remote-as 65500
+   neighbor 10.0.0.2 maximum-routes 12000 
+   neighbor 10.0.0.10 remote-as 65512
+   neighbor 10.0.0.10 maximum-routes 12000 
+   network 100.0.100.0/24
 !


```
Be cautious of device support.  This is based on NAPALM driver implementation which is dictated by vendor OS support.  This example is EOS.
]

---

class: ubuntu

# Getting Started with NAPALM

Step 1. Import Network Driver

```
>>> from napalm import get_network_driver
>>>
>>> driver = get_network_driver('eos')
>>>

```

Step 2. Create Device Object

```
>>> hostname = 'eos-spine1'
>>> username = 'ntc'
>>> password = 'ntc123'
>>> 
>>> device = driver(hostname, username, password)
>>>
```

Step 3. Open connection

```
>>> device.open()
>>>
```

---

# Perform a Configuration Merge

Sample new config we want to send/merge with current configuration:

`snmp.conf`


```bash
snmp-server community networktocode ro
snmp-server community public ro
snmp-server community private rw
snmp-server community supersecret rw
snmp-server location SYDNEY
snmp-server contact JOHN_SMITH


```



---

class: ubuntu

# Perform a Configuration Merge


- `load_merge_candidate` method
- Support configuration files (`filename` parameter) and strings (`config` parameter)

```
>>> device.load_merge_candidate(filename='snmp.conf')
```

- Compare the running configuration and the new candidate configuration with `compare_config` 

```
>>> diffs = device.compare_config()
>>> 
>>> print diffs
@@ -7,7 +7,12 @@
 hostname eos-spine1
 ip domain-name ntc.com
 !
+snmp-server contact JOHN_SMITH
+snmp-server location SYDNEY
 snmp-server community networktocode ro
+snmp-server community private rw
+snmp-server community public ro
+snmp-server community supersecret rw
 !
 spanning-tree mode mstp
 !
```

---


class: ubuntu

# Perform a Configuration Replace

- Declarative network configuration management  
- Requires using a full configuration file 
- `load_replace_candidate` method
- Copies new config to the device, but does not commit it

```
>>> device.load_replace_candidate(filename='new_good.conf')
>>> 
```



---

class: ubuntu

# Other Methods

<html>
<head>
<style>
table, th, td {
    border: 1px solid black;
}
</style>
</head>
<body>

<table style="width:100%">
  <tr>
    <th>Method</th>
    <th>Description</th>
    <th>Example</th> 
  </tr>
  <tr>
    <td>discard_config</td>
    <td>Removes the loaded candidate configuration</td>
    <td>device.discard_config()</td>
  </tr>
  <tr>
    <td>commit_config</td>
    <td>Commit the loaded candidate configuration</td>
    <td>device.commit_config()</td>
  </tr>
  <tr>
    <td>rollback</td>
    <td>Restores a backup configuration saved before the last changes and commit</td>
    <td>device.rollback()</td>
  </tr>
</table>

</body>
</html>

```
>>> device.discard_config()
>>> 
>>> print device.compare_config()
u''
```

```
>>> device.commit_config()
>>> 
```

```
>>> device.rollback()
>>> 
```


---

# Lab Time - BONUS

- Lab 19 - NAPALM
 -   Using the NAPALM Python Library to do declarative config merge, full config merge and getters for Arista EOS
 -   Using the NAPALM Python Library to do basic config merge and getters for Cisco IOS
 -   Using the NAPALM Python Library to do declarative config merge, full config merge and getters for Juniper JUNOS


---


class: middle, segue

# pyntc
### Network APIs

---


# pyntc


- Open source multi-vendor Python library
- Freely provided to the open source community

**The purposes of the library are the following:**

- Simplify the execution of operational common tasks including
  - Copying files
  - Upgrading devices
  - Rebooting devices
  - Saving / Backing Up Configs
  - Executing arbitrary commands

---

# Supported Platforms

* Cisco IOS platforms
* Cisco NX-OS
* Arista EOS
* Juniper Junos

---

class: ubuntu

# Getting Started with pyntc

**Using the `ntc_device` object** and supplying all parameters within your code

Step 1. Import Device Object

```
>>> from pyntc import ntc_device as NTC
>>> 
```

Step 2. Create Device Object(s)
  * Key parameter is `device_type`

```
>>> # CREATE DEVICE OBJECT FOR AN IOS DEVICE
>>> 
>>> csr1 = NTC(host='csr1', username='ntc', password='ntc123', device_type='cisco_ios_ssh')
>>>
```

```
>>> # CREATE DEVICE OBJECT FOR A NEXUS DEVICE
>>> 
>>> nxs1 = NTC(host='nxos-spine1', username='ntc', password='ntc123', device_type='cisco_nxos_nxapi')
>>> 
```


---

class: ubuntu

# Viewing Running/Startup Configs

- Use `running_config` and `start_up` device properties
  - Only showing partial config (shortened for clarity)

```
>>> run = csr1.running_config
>>> 
>>> print run
Building configuration...

Current configuration : 2062 bytes
!
! Last configuration change at 18:26:59 UTC Wed Jan 6 2016 by ntc
!
version 15.5
service timestamps debug datetime msec

lldp run
cdp run
!
ip scp server enable
!
interface GigabitEthernet1
 ip address 10.0.0.50 255.255.255.0
 cdp enable
```


---

class: ubuntu

# Copying files

- `file_copy` method
- Copies file(s) from Python machine to target network devices

```
>>> devices = [csr1, nxs1]
>>> 
>>> for device in devices:
...   device.file_copy('newconfig.cfg')
...
>>>
```

---

class: ubuntu

# Save Configs

- `save` method
- Perform a save on the network device 

`copy run start` for Cisco/Arista and `commit` for Juniper

```
>>> csr1.save()
True
>>>
```

`copy running-config <filename>`

```
>>> csr1.save('mynewconfig.cfg')
True
>>>
```

---

class: ubuntu

# Backup Configs

- `backup_running_config` method
- Backup current running configuration and store it locally on Python machine

```
>>> csr1.backup_running_config('csr1.cfg')
>>> 
```

---

class: ubuntu
# Reboot

Reboot target device

Parameters:
  - `timer=0` by default
  - `confirm=False` by default

```
>>> csr1.reboot(confirm=True)
>>> 
```

---

class: ubuntu

# Installing Operating Systems

* Sets boot loader accordingly
* IOS still needs a reboot
* NXOS - reboot happens automatically

Note: not currently supported on Juniper

```
>>> device.install_os('nxos.7.0.3.I2.1.bin')
>>> 
```

---

class: ubuntu

# Upgrade Workflow 

**Sample Workflow**

```
>>> device.save('backup.cfg')
>>> device.backup_running_config('spine1.cfg')
>>> device.file_copy('nxos.7.0.3.I2.1.bin')
>>> device.install_os('nxos.7.0.3.I2.1.bin')
>>> device.reboot()          
>>> 
```

---

class: ubuntu

# Sending Show & Config Commands

- `show` and `show_list` methods
  - API enabled devices return JSON by default
- `config` and `config_list methods`

.left-column[

```
>>> nxs1.show('show hostname')
{'hostname': 'nxos-spine1'}
>>>
```

```
>>> nxs1.show('show hostname', raw_text=True)
'nxos-spine1 \n'
>>> 
```

```
>>> cmds = ['show hostname', 'show run int Eth2/1']
>>> data = nxs1.show_list(cmds, raw_text=True)
>>> 
```
]

.right-column[

```
>>> csr1.config('hostname testname')
>>> 
```

```
>>> csr1.config_list(['interface Gi3', 'shutdown'])
>>> 
```

]


---

# Summary

**NAPALM**
- Multi-vendor library that supports system level tasks
- Simplifies configuration management across a wide number of network and security devices.
  - Focus on desired state
- There are other getters that are part of NAPALM too
  + facts, interfaces, BGP neighbors, LLDP, NTP, etc.

**pyntc**

- Multi-vendor library that currently supports system level tasks
  - Backing up configs, copying files, upgrading images
  - Rebooting devices, issuing commands, saving configs


