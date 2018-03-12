## Lab 21 - Parsing Show Commands with TextFSM

In this lab, we'll use TextFSM templates to simplify parsing unstructured text .  You can build TextFSM templates (parsers) without doing any Python which simplifies the parsing, and enables more people (that don't know Python) to help build parsers.

### Task 1 - Using TextFSM to Parse Raw Text

As you've learned, TextFSM requires two inputs: a template (parser) and raw text.  This task walks you through the process of building a TextFSM template for the `show ip interface brief` command on Cisco Nexus switches that can then be used as an input to `textfsm.py` to easily extract the required data.

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

```
INTERFACE = \S+

IP = `\d+\.\d+\.\d+\.\d+`   => or \S+

PROTOCOL = ?

STATUS = ?

ADMIN = ?
```

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
import textfsm
from netmiko import ConnectHandler

TEMPLATES_PATH = "/etc/ntc/ansible/library/ntc-ansible/ntc-templates/templates/"

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

    raw_text = device.send_command(command)
    print "RAW RESPONSE:"
    print raw_text
    print "-" * 10

    template = TEMPLATES_PATH + 'cisco_ios_show_ip_int_brief.template'
    table = textfsm.TextFSM(open(template))

    print "-" * 10
    print "ALL HEADER (KEYS) from TextFSM Values:"
    print table.header

    # this actually parses the data
    data = table.ParseText(raw_text)
    print "THIS IS HOW TEXTFSM PARSES DATA (LIST OF LISTS)"
    print json.dumps(data, indent=4)
    print "-" * 10


    # this step is optional, but it cleans up the final object from a list of lists to a list of dictionaries
    final_list = []
    for entry in data:
        temp_dict = {}
        for index, value in enumerate(entry):
            temp_dict[table.header[index].lower()] = value
        final_list.append(temp_dict)

    print "FINAL CONVERTED/PARSED OBJECT:"
    print json.dumps(final_list, indent=4)


```

##### Step 2

The previous step created a template for the Nexus `show ip int brief`.

Now simply review a template that parses `show ip int brief`.

```
Value INTF (\S+)
Value IPADDR (\S+)
Value STATUS (up|down|administratively down)
Value PROTO (up|down)

Start
  ^${INTF}\s+${IPADDR}\s+\w+\s+\w+\s+${STATUS}\s+${PROTO} -> Record
```

Which do you prefer?  TextFSM or using `re`?


##### Step 3

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
* View online for more templates

You can try any of the associated commands that start with "cisco_ios" on your router (assuming the device supports the command).  The commands supported map directly to the template name removing "cisco_ios" and substituting spaces for underscores.


**Once you see and understand the data coming back, you can use it in your own scripts.**

