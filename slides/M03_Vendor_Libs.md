layout: true

.footer-picture[![Network to Code Logo](slides/media/Footer2.PNG)]
.footnote-left[(C) 2015 Network to Code, LLC. All Rights Reserved. ]
.footnote-con[CONFIDENTIAL]

---

class: center, middle, title
.footer-picture[<img src="slides/media/Footer1.PNG" alt="Blue Logo" style="alight:middle;width:350px;height:60px;">]

# Vendor Libraries


---

# Vendor Libraries

* Juniper PyEZ
* Arista pyeapi

---


class: middle, segue

# Juniper XML API and PyEZ 
### Vendor Libraries


---

class: middle, segue

# Juniper XML API (NETCONF)
### Network APIs

---

# Overview

- CLI is an actual client that uses the XML API
- Junos converts commands to XML for processing, returns XML, and then converts back to raw text for visual output on the CLI
- The Junos XML API is an XML representation of Junos OS configuration statements and operational mode commands.
- Defines an XML equivalent for all statements in the Junos configuration hierarchy
  - Includes many of the commands that you issue in CLI operational mode

---

# Displaying XML on the CLI

Normal Command Line output:

```bash
ntc@vmx1> show arp 
MAC Address       Address         Name                      Interface               Flags
2c:c2:60:ff:00:43 10.0.0.2        10.0.0.2                  fxp0.0                  none
Total entries: 1
```

Viewing it as XML:
```bash
ntc@vmx1> show arp | display xml        
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1F4/junos">
    <arp-table-information xmlns="http://xml.juniper.net/junos/15.1F4/junos-arp" junos:style="normal">
        <arp-table-entry>
            <mac-address>2c:c2:60:ff:00:43</mac-address>
            <ip-address>10.0.0.2</ip-address>
            <hostname>10.0.0.2</hostname>
            <interface-name>fxp0.0</interface-name>
            <arp-table-entry-flags>
                <none/>
            </arp-table-entry-flags>
        </arp-table-entry>
        <arp-entry-count>1</arp-entry-count>
    </arp-table-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
```

---

# Displaying XML RPC on the CLI

Viewing just the XML RPC:

```bash
ntc@vmx1> show arp | display xml rpc    
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1F4/junos">
    <rpc>
        <get-arp-table-information>
        </get-arp-table-information>
    </rpc>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>

```



---


class: middle, segue

# py-junos-eznc (PyEZ)
### Juniper XML API (NETCONF)

---


# PyEZ

- Python library that enables you to remotely manage and automate devices running Junos
- Provide the capabilities that a user would have on the Junos OS command-line interface (CLI) in an environment built for automation tasks
- Does not require extensive knowledge of Junos OS or the Junos XML APIs.
- Focuses on:
  - System level tasks (copying files, image upgrades, push config files in various formats such as set/text/xml formats)
  - Execute any RPC
  - Retrieving configuration and operational data from devices
- Freely provided to the open source community
- Support is provided through Github issues and Juniper PyEZ google group

---


# Requirements

- Junos 
  - Multi-platform support
- Ensure NETCONF over SSH is enabled
- Switch command:
  - `set system services netconf ssh`


---

class: ubuntu

# Create Device Object

Import Library

```
>>> from jnpr.junos.device import Device as JUNIPER
>>> 
```

Create Device Object

```
>>> device = JUNIPER(host='vsrx1', user='ntc', password='ntc123')
>>> 
```

Open a NETCONF Session to the device

```
>>> device.open()
Device(vsrx1)
>>>
```


---

class: middle

### Device Object Properties & Methods


---

class: ubuntu

# Open/Close the Connection

- Open and Close the NETCONF connection (rides over SSH)
- default port number is 830

```
>>> device.open()
>>>
>>> # PERFORM SOME TASKS
>>>
>>> device.close()
>>> 
```

---

class: ubuntu

# Hostname

- Get the device hostname

```
>>> device.hostname
'vsrx1'
>>> 
```

---

class: ubuntu

# Facts

- Gather facts about a particular device.

```
>>> device.facts
{'domain': 'ntc.com', 'hostname': 'vsrx1', 'ifd_style': 'CLASSIC', 'version_info': junos.version_info(major=(15, 1), type=X, minor=(49, 'D', 15), build=4), '2RE': False, 'serialnumber': '05d1ca5e2cf2', 'fqdn': 'vsrx1.ntc.com', 'switch_style': 'NONE', 'version': '15.1X49-D15.4', 'HOME': '/var/home/ntc', 'srx_cluster': False, 'model': 'VSRX', 'RE0': {'status': 'Testing', 'last_reboot_reason': 'Router rebooted after a normal shutdown.', 'model': 'VSRX RE', 'up_time': '9 minutes, 2 seconds'}, 'vc_capable': False, 'personality': 'UNKNOWN'}
>>>
```

```
>>> from pprint import pprint as pp
>>> 
>>> pp(facts)   # removed a few facts for brevity
{'2RE': False,
 'HOME': '/var/home/ntc',
 'RE0': {'last_reboot_reason': 'Router rebooted after a normal shutdown.',
         'model': 'VSRX RE',
         'up_time': '9 minutes, 2 seconds'},
 'domain': 'ntc.com',
 'fqdn': 'vsrx1.ntc.com',
 'hostname': 'vsrx1',
 'model': 'VSRX',
 'serialnumber': '05d1ca5e2cf2',
 'srx_cluster': False,
 'version': '15.1X49-D15.4',
 'version_info': junos.version_info(major=(15, 1), type=X, minor=(49, 'D', 15), build=4)}
>>> 
```

---

class: ubuntu

# Connection Status

- View the connection status of the NETCONF session

```
>>> device.connected
True
>>>
```


---

class: ubuntu

# Issuing CLI Commands

- Sending raw CLI commands
  - Note the warning!
  - Warning can be disabled

```
>>> output = device.cli('show version')
/usr/local/lib/python2.7/dist-packages/jnpr/junos/device.py:652: RuntimeWarning: CLI command is for debug use only!
  warnings.warn("CLI command is for debug use only!", RuntimeWarning)
>>> 
>>> print output

Hostname: vsrx1
Model: vSRX
Junos: 15.1X49-D15.4
JUNOS Software Release [15.1X49-D15.4]
>>>
```


---

class: ubuntu

# Get Configs

- Retrieve the configuration or configuration stanzas from Junos devices

.left-column[
```
>>> from lxml.builder import E
>>> 
>>> filter = E('interfaces')
```

```
>>> filter
<Element interfaces at 0x7f18a7313f38>
>>>
```

```
>>> from lxml import etree
>>> print etree.tostring(filter)
<interfaces/>
>>>
```

```
>>> device.rpc.get_config(filter_xml=filter)
<Element configuration at 0x7f18a7313f38>
>>> 
>>> config = device.rpc.get_config(filter_xml=filter)
>>> 
```
]

.right-column[


```
>>> print etree.tostring(config)
<configuration changed-seconds="1455733666" changed-localtime="2016-02-17 18:27:46 UTC">
    <interfaces>
            <name>fxp0</name>
            <unit>
                <name>0</name>
                <family>
                    <inet>
                        <address>
                            <name>10.0.0.40/24</name>
                        </address>
                    </inet>
                </family>
            </unit>
        </interface>
    </interfaces>
</configuration>
>>>
```
]


---

class: ubuntu

# Deploying Configuration Changes

- Config object is used to manage configurations on Junos devices
- Includes pushing configs, commits, commit checks, generating diffs, performing locks on the configuration, and rollback the the configuration.

```
>>> from jnpr.junos.utils.config import Config
>>> 
>>> config = Config(device)
>>> 
```

```
>>> dir(config)
['commit', 'commit_check', 'dev', 'diff', 'load', 'lock', 'mode', 'pdiff', 'rescue', 'rollback', 'rpc', 'unlock']
>>> # shortened for clarity
```
---

class: ubuntu

# Config Load

- Load changes into the candidate config
- Flexibility in loading different style configs:
  - XML objects
  - XML strings
  - set commands
  - config stanzas with curly brace notation
  - Jinj2a templates and template variables


---

class: ubuntu

# Config Merge

.left-column[
Sample current interfaces:

```
interfaces {
    ge-0/0/0 {
        unit 0 {
            family inet;                
        }                               
    }                                   
    ge-0/0/2 {                          
        unit 0 {                        
            family inet;                
        }                               
    }                                   
    fxp0 {                              
        unit 0 {                        
            family inet {               
                address 10.0.0.70/24;   
            }                           
        }                               
    }                                   
}
```
]


New configuration file being merged:

.right-column[
```
interfaces {
    ge-0/0/1 {
        disable;
        description CONFIGURED_BY_PYEZ;
        unit 0 {
            family inet;
        }
    }
    fxp0 {
        description MANAGEMENT;
        unit 0 {
            family inet {
                address 10.0.0.70/24;
            }
        }
    }
}

```

]

---

class: ubuntu

# Performing the Load

- `load` method used to perform the _push_ to the device.  
- Config is loaded as part of the candidate configuration
- A commit still needs to be performed at this point

```
>>> config.load(path='interface.conf', format='text')
<Element load-configuration-results at 0x7f18a73165a8>
>>> 
```

---

class: ubuntu

# Viewing Diffs

- `diff` method returns diffs
- `pdiff` simply prints the diffs

```
>>> diffs = config.diff()
>>> 
>>> print diffs

[edit interfaces]
+   ge-0/0/1 {
+       description CONFIGURED_BY_PYEZ;
+       disable;
+       unit 0 {
+           family inet;
+       }
+   }
[edit interfaces fxp0]
+   description MANAGEMENT;

```

---

class: ubuntu

# Config Rollback

- Rollback to a given configuration using the rollback id
- Starts at 0 for the most recent

```
>>> config.rollback(0)
True
>>> 
>>> diffs = config.diff()
>>> print diffs
None
```

---

class: ubuntu

# Configuration Replace

- Replace performs a configuration replace of a full configuration or stanza


Sample Existing Conifguration

```
ntc@vmx1# show routing-options 
static {
    route 0.0.0.0/0 next-hop 10.0.0.2;
    route 100.0.0.0/8 next-hop 10.0.0.2;
}
```

New routing-options configuration stanza (note the `replace:`)

```
routing-options {
    replace:
    static {
        route 0.0.0.0/0 next-hop 10.0.0.2;
    }

}
```


---

class: ubuntu

# Perform a Load Replace

- Replace a full configuration / configuration stanza
- Set merge=False (the default) and call the `load` method

```
>>> config.load(path='routing.conf', format='text', merge=False)
<Element load-configuration-results at 0x7f18a7310290>
>>> 
>>> diffs = config.diff()
>>> print diffs

[edit routing-options static]
-    route 100.0.0.0/8 next-hop 10.0.0.2;

>>> 
>>> 
```



---

class: ubuntu

# Config Load with Jinja2 Templates 

- Ability to use Jinja2 templates and variables instead of pre-built configuration files
- Need to define template and variables (Python dictionary)

.left-column[
```
# filename: interfaces-template.conf

interfaces { 
    {% for interface in interfaces %}
    {{ interface }} {
        description {{ description }};
        unit 0 {
            family inet;
        }      
    } {% endfor %}    
}
```


```
>>> config = {
    'interfaces': ['ge-1/0/1', 'ge-1/0/2', 'ge-1/0/3'],
    'description': 'Access_Interface',
    'family': 'inet'
}
>>>
```
]

.right-column[
```
>>> conf_file = "interfaces-template.conf"
>>> config.load(template_path=conf_file, template_vars=config, merge=True)
```
]


---

class: ubuntu

# Full Deployment Workflow

- Sample workflow that includes building a device object, locking the configuration, load a new candidate configuration, commit it, unlocking the configuration, and closing down the NETCONF session.

```
device = Device(host='vmx1', user='ntc', password='ntc123')
device.open()

config = Config(device)

config.lock()

config.load(path=conf_file, format='text', merge=True)

config.commit()

config.unlock()

device.close()

```




---

# Config Load Summary

.center[
<img src="slides/media/apis/juniper/config-table.png" alt="Juniper" style="alight:middle;width:700px;height:465px;">
]
Source: http://www.juniper.net


---

# Lab Time

- Lab 19 - Juniper PyEZ 
  - Exploring PyEZ device objects
  - Performing Config Merge
  - Performing a Config Replace
  

---

class: middle

### PyEZ Tables & Views

---

# Overview

- Tables and Views provide a simple and efficient way to extract information from complex operational command output or configuration data
- Two types of tables: Op and Config 
  - Operational (op) Tables select items from the RPC reply of an operational command
  - Configuration Tables select data from specific hierarchies in the selected configuration database
- A Table also references a View, which maps tag names (XML) into user-defined Python variables
- Tables and Views are defined using YAML

---

# Neighbor Table/View

- A number of tables/views are included when PyEZ is installed
- Located in `./lib/junpr/junos/op` directory in `py-junos-eznc`

Example of an Operational (op) table:

```bash
---
LLDPNeighborTable:
  rpc: get-lldp-neighbors-information
  item: lldp-neighbor-information
  key: lldp-local-interface | lldp-local-port-id
  view: LLDPNeighborView

```

--

```bash
ntc@vmx1> show lldp neighbors | display xml rpc 
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1F4/junos">
    <rpc>
        <get-lldp-neighbors-information>
        </get-lldp-neighbors-information>
    </rpc>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
```

---

# Neighbor Table/View

```bash
ntc@vmx1> show lldp neighbors | display xml        
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1F4/junos">
    <lldp-neighbors-information junos:style="brief">
        <lldp-neighbor-information>
            <lldp-local-port-id>fxp0</lldp-local-port-id>
            <lldp-local-parent-interface-name>-</lldp-local-parent-interface-name>
            <lldp-remote-chassis-id-subtype>Mac address</lldp-remote-chassis-id-subtype>
            <lldp-remote-chassis-id>28:03:82:9a:13:57</lldp-remote-chassis-id>
            <lldp-remote-port-id-subtype>Interface name</lldp-remote-port-id-subtype>
            <lldp-remote-port-id>Management1</lldp-remote-port-id>
            <lldp-remote-system-name>eos-leaf1.ntc.com</lldp-remote-system-name>
        </lldp-neighbor-information>
        <lldp-neighbor-information>
            <lldp-local-port-id>fxp0</lldp-local-port-id>
            <lldp-local-parent-interface-name>-</lldp-local-parent-interface-name>
            <lldp-remote-chassis-id-subtype>Mac address</lldp-remote-chassis-id-subtype>
            <lldp-remote-chassis-id>28:03:82:9a:13:5b</lldp-remote-chassis-id>
            <lldp-remote-port-id-subtype>Interface name</lldp-remote-port-id-subtype>
            <lldp-remote-port-id>Management1</lldp-remote-port-id>
            <lldp-remote-system-name>eos-leaf2.ntc.com</lldp-remote-system-name>
        </lldp-neighbor-information>
    </lldp-neighbors-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
```

---

# Neighbor Table

.left-column[

```bash
ntc@vmx1> show lldp neighbors | display xml        
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1F4/junos">
    <lldp-neighbors-information junos:style="brief">
        <lldp-neighbor-information>
            <lldp-local-port-id>fxp0</lldp-local-port-id>
            <lldp-local-parent-interface-name>-</lldp-local-parent-interface-name>
            <lldp-remote-chassis-id-subtype>Mac address</lldp-remote-chassis-id-subtype>
            <lldp-remote-chassis-id>28:03:82:9a:13:57</lldp-remote-chassis-id>
            <lldp-remote-port-id-subtype>Interface name</lldp-remote-port-id-subtype>
            <lldp-remote-port-id>Management1</lldp-remote-port-id>
            <lldp-remote-system-name>eos-leaf1.ntc.com</lldp-remote-system-name>
        </lldp-neighbor-information>
        <lldp-neighbor-information>
            <lldp-local-port-id>fxp0</lldp-local-port-id>
            <lldp-local-parent-interface-name>-</lldp-local-parent-interface-name>
            <lldp-remote-chassis-id-subtype>Mac address</lldp-remote-chassis-id-subtype>
            <lldp-remote-chassis-id>28:03:82:9a:13:5b</lldp-remote-chassis-id>
            <lldp-remote-port-id-subtype>Interface name</lldp-remote-port-id-subtype>
            <lldp-remote-port-id>Management1</lldp-remote-port-id>
            <lldp-remote-system-name>eos-leaf2.ntc.com</lldp-remote-system-name>
        </lldp-neighbor-information>
    </lldp-neighbors-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
```
]
--

.right-column[
```bash
---
LLDPNeighborTable:
  rpc: get-lldp-neighbors-information
  item: lldp-neighbor-information
  key: lldp-local-interface | lldp-local-port-id
  view: LLDPNeighborView
```

- Obtain the RPC (`show abc | display xml rpc`)
- Identify each **item** - the recurring element that you want to record
- What do you want to **key** for each instance of your **item**?
- Define a **view** (coming up)
]

---

# Neighbor View

.left-column[

```bash
ntc@vmx1> show lldp neighbors | display xml        
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1F4/junos">
    <lldp-neighbors-information junos:style="brief">
        <lldp-neighbor-information>
            <lldp-local-port-id>fxp0</lldp-local-port-id>
            <lldp-local-parent-interface-name>-</lldp-local-parent-interface-name>
            <lldp-remote-chassis-id-subtype>Mac address</lldp-remote-chassis-id-subtype>
            <lldp-remote-chassis-id>28:03:82:9a:13:57</lldp-remote-chassis-id>
            <lldp-remote-port-id-subtype>Interface name</lldp-remote-port-id-subtype>
            <lldp-remote-port-id>Management1</lldp-remote-port-id>
            <lldp-remote-system-name>eos-leaf1.ntc.com</lldp-remote-system-name>
        </lldp-neighbor-information>
        <lldp-neighbor-information>
            <lldp-local-port-id>fxp0</lldp-local-port-id>
            <lldp-local-parent-interface-name>-</lldp-local-parent-interface-name>
            <lldp-remote-chassis-id-subtype>Mac address</lldp-remote-chassis-id-subtype>
            <lldp-remote-chassis-id>28:03:82:9a:13:5b</lldp-remote-chassis-id>
            <lldp-remote-port-id-subtype>Interface name</lldp-remote-port-id-subtype>
            <lldp-remote-port-id>Management1</lldp-remote-port-id>
            <lldp-remote-system-name>eos-leaf2.ntc.com</lldp-remote-system-name>
        </lldp-neighbor-information>
    </lldp-neighbors-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
```
]

.right-column[
```bash
---
LLDPNeighborTable:
  rpc: get-lldp-neighbors-information
  item: lldp-neighbor-information
  key: lldp-local-interface | lldp-local-port-id
  view: LLDPNeighborView

LLDPNeighborView:
  fields:
    local_int: lldp-local-interface | lldp-local-port-id
    local_parent: lldp-local-parent-interface-name
    remote_type: lldp-remote-chassis-id-subtype
    remote_chassis_id: lldp-remote-chassis-id
    remote_port_desc: lldp-remote-port-description
    remote_sysname: lldp-remote-system-name
```

- Define each **field** you want from each **item**
- Map Juniper XML tags into what will be user-defined Python variables
  - XPath expressions are relative to the Table item context. 
- `fields`, `groups`, and `fields_groups` can be used within a View

]

---

# Helper File

- The PyEZ Tables/Views infrastructure is an advanced concept, which is the reason it's simple to use!
- A helper file is required, and you don't have to touch it at all.
  - Give the file a name and place it in the `op` sub-directory.
  - Same file for every Table/View you add; just a different name

For example, this file has the name of `lldp.py` and matches the name of the YAML file that has the associated neighbor Table/View, which is `lldp.yml`

```bash
"""
Pythonifier for LLDP Table/View
"""
from jnpr.junos.factory import loadyaml
from os.path import splitext
_YAML_ = splitext(__file__)[0] + '.yml'
globals().update(loadyaml(_YAML_))
```

---

class: ubuntu

# Included Tables/Views Files

- `jnpr/junos/op/` directory after installing PyEZ
- Each Table file has an associated helper Python file

```
arp.py
arp.yml
bfd.py
bfd.yml
ccc.py
ccc.yml
ethernetswitchingtable.py
ethernetswitchingtable.yml
ethport.py
ethport.yml
lacp.py
lacp.yml
ldp.py
ldp.yml
lldp.py
lldp.yml
ospf.py
ospf.yml
phyport.py
phyport.yml
routes.py
routes.yml
```


---

# Using Tables in Python

.left-column[
```bash
# filename: lldp.yml
.---    
LLDPNeighborTable:
  rpc: get-lldp-neighbors-information
  item: lldp-neighbor-information
  key: lldp-local-interface | lldp-local-port-id
  view: LLDPNeighborView

LLDPNeighborView:
  fields:
    local_int: lldp-local-interface | lldp-local-port-id
    local_parent: lldp-local-parent-interface-name
    remote_type: lldp-remote-chassis-id-subtype
    remote_chassis_id: lldp-remote-chassis-id
    remote_port_desc: lldp-remote-port-description
    remote_sysname: lldp-remote-system-name
```


```bash
# filename: lldp.py
"""
Pythonifier for LLDP Table/View
"""
from jnpr.junos.factory import loadyaml
from os.path import splitext
_YAML_ = splitext(__file__)[0] + '.yml'
globals().update(loadyaml(_YAML_))
```


]

.ubuntu[
.right-column[
```
>>> from jnpr.junos.device import Device as J
>>> 
>>> device = J(host='vmx1', user='ntc', password='ntc123')
>>> device.open()
Device(vmx1)
>>> 
```

```
>>> from jnpr.junos.op.lldp import LLDPNeighborTable
```

```
>>> neighbors = LLDPNeighborTable(device)
>>> neighbors.get()
LLDPNeighborTable:vmx1: 8 items
```

]

]

---

class: ubuntu

# Accessing items

- You can access a View item as variable properties
- Each View item has a `name` property that references the key that uniquely identifies that item.

```
>>> for item in neighbors:
...     print item.name           # key
...     print item.local_int      # local_int field
...     print item.remote_sysname # neighbor name
...     print '---'
... 
fxp0
fxp0
vmx2
---
ge-0/0/2
ge-0/0/2
vmx2
---
fxp0
fxp0
vmx3
---
```


---

# Using PyEZ Tables/Views -- Inline

- You also have the ability to embed Tables and Views inline in your Python code

```bash
from jnpr.junos.factory.factory_loader import FactoryLoader
import yaml

YAML_STRING = """
.---     
CustomNeighborTable:
  rpc: get-lldp-neighbors-information
  item: lldp-neighbor-information
  key: lldp-local-interface | lldp-local-port-id
  view: LLDPNeighborView

CustomNeighborView:
  fields:
    local_int: lldp-local-interface | lldp-local-port-id
    remote_sysname: lldp-remote-system-name
"""


globals().update(FactoryLoader().load(yaml.load(YAML_STRING)))

neighbors = CustomNeighborTable(device)
neighbors.get()

```

---

# PyEZ (op) Tables (Advanced)

- XPath Expressions can be used above and beyond the XML tags used for fields, items, and keys
  - Relative to the item context
  - Can 
- By default, all data types are strings
  -   `mymtu: { mtu : int }`
- Other examples:
  - `dc1_route: { rt-destination: True=regex(^198\.51\.)  }`
  - `oper_status_down: { oper-status: True=regex(down)  }`
  - ` running: { if-device-flags/ifdf-running : flag }`

---


# PyEZ (Other Functions)

- SCP files to/from devices
- Installing Software
- Viewing/Executing XML RPCs


---

# Summary

- Invest time in XML, i.e. lxml library
- Methods / Properties:
  - Config Object, i.e.  `commit`, `commit_check`, `diff`,  `load`,  `lock`,`pdiff`, `rescue`, `rollback`, `unlock`
  - `open`, `close`
  - `facts`, `hostname`
- PyEZ Tables & Views
  - Operational Tables
  - Config Tables
  - XPath, XPath, XPath


---

# Lab Time

- Lab 20 - Juniper PyEZ  
  - Using PyEZ Operational Tables/Views
  - Writing a LLDP Neighbors Script


---

class: middle, segue

# Arista pyeapi
### Vendor Libraries

---


# pyeapi

- Python library for Arista's eAPI command API implementation
- The Python library can be used to communicate with EOS either locally (on-box) or remotely (off-box). 
- Uses a standard INI-style configuration file to specify one or more nodes and connection properties.
- Provides an API layer for building native Python objects to interact with the destination nodes. 
- Extensible for developing custom implementations.
- Freely provided to the open source community
- Support is provided as best effort through Github issues.


---


# Configuration File (pyeapi)

- Arista uses a configuration file to store connection information for each node you will be using with pyeapi (`.eapi.conf`)

.left-column[
- host - The IP address or FQDN of the remote device. If omitted, then the connection name is used
- username - eAPI username (http/s)
- password - eAPI password (http/s)
- enablepwd - enable mode pwd if required
- transport - Type of transport connection to use. The default value is https. Valid values are: socket (EOS 4.14.5+), http_local (EOS 4.14.5+), http, https
- port - port to use for eAPI connection. Default port is used if omitted, based on the transport setting using the following values: http (80), https (443), https_local (8080), socket (n/a)
]

.right-column[
```bash
[connection:spine1]
host: 10.0.0.11
username: ntc
password: ntc123
transport: https

[connection:spine2]
host: 10.0.0.12
username: ntc
password: ntc123
transport: https

[connection:tor1]
host: 10.0.0.13
username: ntc
password: ntc123
transport: https

[connection:tor2]
host: 10.0.0.14
username: ntc
password: ntc123
transport: https
```

]

---

class: ubuntu

# Create Device Object

Import Library

```
from pyeapi import connect_to as ARISTA
```

Create Device Object

```
device = ARISTA('spine1')
```

> Note: by default, pyeapi searches for the conf file in your home directory.  Can also set an environment variable.

---

class: ubuntu

# Sending Commands

.left-column[
- Send show commands with the `enable` method

```
>>> rsp = device.enable('show version')
>>> 
>>> print rsp
[{'command': 'show version', 'result': {u'memTotal': 2028860, u'version': u'4.14.7M', u'internalVersion': u'4.14.7M-2384414.4147M', u'serialNumber': u'', u'systemMacAddress': u'28:03:82:9a:13:4b', u'bootupTimestamp': 1445780326.94, u'memFree': 294552, u'modelName': u'vEOS', u'architecture': u'i386', u'internalBuildId': u'92a53fad-f853-42a5-9f57-c3c4ea3c26b3', u'hardwareRevision': u''}, 'encoding': 'json'}]
```
]

.right-column[
- Send configuration commands with the `config` method

```
>>> cmds = ['interface Ethernet2', 'description config by Python']
>>> 
>>> device.config(cmds)
[{}, {}]
```


]

---

class: ubuntu

# Device Properties & Methods

- Get running config

```
>>> running = device.running_config      # startup_config also supported
```

```
>>> print running[1:400]
 Command: show running-config all
! device: spine2 (vEOS, EOS-4.14.7M)
!
! boot system flash:EOS.swi
!
no deep-inspection payload l2 skip
no deep-inspection payload l4 skip
!
bfd slow-timer 2000
bfd interval 300 min_rx 300 multiplier 3 default
!
prompt %H%R%v%P
no terminal length
no terminal width
!
schedule tech-support interval 60 max-log-files 100 command show tech-support
!
```

---

class: ubuntu

# Section

- Get _sections_ of running configuration

.left-column[
```
>>> bgp_run = device.section('router bgp')
>>> 
>>> print bgp_run
router bgp 64512
   no shutdown
   no router-id
   bgp convergence time 300
   bgp convergence slow-peer time 90
   no bgp confederation identifier
   no update wait-for-convergence
   no update wait-install
   bgp log-neighbor-changes
   bgp default ipv4-unicast
   no bgp default ipv6-unicast
   timers bgp 60 180

# shortened for brevity
```
]

.right-column[

```
>>> interface = device.section('interface Ethernet1')
>>> 
>>> print interface[:400]
interface Ethernet1
   description [L1] (w->10.0.9.0)
   no shutdown
   default load-interval
   mtu 1500
   logging event link-status use-global
   no dcbx mode
   no mac-address
   no link-debounce
   no flowcontrol send
   no flowcontrol receive
   no mac timestamp
   no speed
   no l2 mtu
   default logging event congestion-drops
   default unidirectional
   no switchport
   default encapsulat
# shortened for brevity

```


]
---

class: ubuntu

# api

```
>>> help(device.api)

Help on method api in module pyeapi.client:

api(self, name, namespace='pyeapi.api') method of pyeapi.client.Node instance
    Loads the specified api module
    
    This method is the API autoload mechanism that will load the API
    module specified by the name argument.  The API module will be loaded
    and look first for an initialize() function and secondly for an
    instance() function.  In both cases, the node object is passed to
    the module.
    
    Args:
        name (str): The name of the module to load.  The name should be
            the name of the python file to import
        namespace (str): The namespace to use to load the module.  The
            default value is 'pyeapi.api'
    
    Returns:
        The API module loaded with the node instance.
(END)

```

---

class: ubuntu

# APIs Modules / Features

- Examine the `api` directory within `pyeapi`
- https://github.com/arista-eosplus/pyeapi/tree/develop/pyeapi/api

```
dev@ntc:~/pyeapi$ cd pyeapi/
dev@ntc:~/pyeapi/pyeapi$ tree
.
├── api
│   ├── abstract.py
│   ├── acl.py
│   ├── bgp.py
│   ├── __init__.py
│   ├── interfaces.py
│   ├── ipinterfaces.py
│   ├── mlag.py
│   ├── routemaps.py
│   ├── spanningtree.py
│   ├── stp.py
│   ├── switchports.py
│   ├── system.py
│   ├── users.py
│   ├── varp.py
│   └── vlans.py
# shortened for brevity
```


---

class: ubuntu

# VLANs Module

.left-column[

```
>>> vlans = device.api('vlans')
>>> 
>>> dir(vlans)
['add_trunk_group', 'command_builder', 'config', 'configure', 'configure_interface', 'configure_vlan', 'create', 'default', 'delete', 'error', 'get', 'get_block', 'getall', 'items', 'iteritems', 'iterkeys', 'itervalues', 'keys', 'node', 'remove_trunk_group', 'set_name', 'set_state', 'set_trunk_groups', 'values']
>>> 
>>> vlans.get('1')
{'state': 'active', 'name': 'default', 'vlan_id': '1', 'trunk_groups': []}
>>> 
>>> vlans.get('2')
```

```
>>> vlans.getall()
{'1': {'state': 'active', 'name': 'default', 'vlan_id': '1', 'trunk_groups': []}, '10': {'state': 'active', 'name': 'VLAN0010', 'vlan_id': '10', 'trunk_groups': []}, '30': {'state': 'active', 'name': 'VLAN0030', 'vlan_id': '30', 'trunk_groups': []}, '20': {'state': 'active', 'name': 'VLAN0020', 'vlan_id': '20', 'trunk_groups': []}}
```
]

.right-column[


```
>>> vlans.create(100)
True
```

```
>>> vlans.set_name(100, 'vlan_100')
True
```

```
>>> vlans.get(100)
{'state': 'active', 'name': 'vlan_100', 'vlan_id': 100, 'trunk_groups': []}
```

```
>>> vlans.set_name(100, default=True)
True
```

```
>>> vlans.get(100)
{'state': 'active', 'name': 'VLAN0100', 'vlan_id': 100, 'trunk_groups': []}
>>> 
```


]

---

class: ubuntu

# Switchport Module

.left-column[

```
>>> sp = device.api('switchports')
>>> 
>>> dir(sp)
<-shortened for brevity->
[add_trunk_group', 'command_builder', 'config', 'configure', 'configure_interface', 'create', 'default', 'delete', 'error', 'get', 'get_block', 'getall', 'items', 'iteritems', 'iterkeys', 'itervalues', 'keys', 'node', 'remove_trunk_group', 'set_access_vlan', 'set_mode', 'set_trunk_allowed_vlans', 'set_trunk_groups', 'set_trunk_native_vlan', 'values']
>>> 
>>> sp.getall()
{'Ethernet2': {'access_vlan': '1', 'trunk_allowed_vlans': '1-4094', 'trunk_native_vlan': '1', 'mode': 'access', 'trunk_groups': [], 'name': 'Ethernet2'}, 'Ethernet3': {'access_vlan': '1', 'trunk_allowed_vlans': '1-4094', 'trunk_native_vlan': '1', 'mode': 'access', 'trunk_groups': [], 'name': 'Ethernet3'}, 'Ethernet1': {'access_vlan': '1', 'trunk_allowed_vlans': '1-4094', 'trunk_native_vlan': '1', 'mode': 'access', 'trunk_groups': [], 'name': 'Ethernet1'}, 'Ethernet6': {'access_vlan': '1', 'trunk_allowed_vlans': '1-4094', 'trunk_native_vlan': '1', 'mode': 'access', 'trunk_groups': [], 'name': 'Ethernet6'}, 'Ethernet7': {'access_vlan': '1', 'trunk_allowed_vlans': '1-4094', 'trunk_native_vlan': '1', 'mode': 'access', 'trunk_groups': [], 'name': 'Ethernet7'}}
>>>
```

]

.right-column[


```
>>> sp.get('Ethernet2')
{'access_vlan': '1', 'trunk_allowed_vlans': '1-4094', 'trunk_native_vlan': '1', 'mode': 'access', 'trunk_groups': [], 'name': 'Ethernet2'}
>>> 
```

```
>>> sp.set_mode('Ethernet2', 'trunk')
True
>>> 
```

```
>>> sp.set_trunk_native_vlan('Ethernet2', '10')
True
>>>
```

```
>>> sp.set_trunk_allowed_vlans('Ethernet2', '10-20')
True
>>> 
```

```
>>> sp.get('Ethernet2')
{'access_vlan': '1', 'trunk_allowed_vlans': '10-20', 'trunk_native_vlan': '10', 'mode': 'trunk', 'trunk_groups': [], 'name': 'Ethernet2'}
>>> 
```

]


---

class: ubuntu

# Users Module

.left-column[
```
>>> users = device.api('users')
```
```
>>> users.getall()
{'admin': {'privilege': '15', 'nopassword': False, 'secret': '$1$2twlR9pP$3DRY8KlH9vBOVDv28HM6R/', 'role': 'network-admin', 'format': '5'}}
>>> 
```
```

>>> users.create('ntc', secret='arista', encryption='cleartext')
True
```

```
>>> users.getall()
{'admin': {'privilege': '15', 'nopassword': False, 'secret': '$1$2twlR9pP$3DRY8KlH9vBOVDv28HM6R/', 'role': 'network-admin', 'format': '5'}, 'ntc': {'privilege': '1', 'nopassword': False, 'secret': '$1$AaNydwlV$vMgZSJ48pseyBstYJUvlm.', 'role': '', 'format': '5'}}
```

]

.right-column[

```
>>> users.set_privilege('ntc', 15)
True
```

```
>>> users.set_role('ntc', 'network-admin')
True
```

```
>>> users.getall()
{'admin': {'privilege': '15', 'nopassword': False, 'secret': '$1$2twlR9pP$3DRY8KlH9vBOVDv28HM6R/', 'role': 'network-admin', 'format': '5'}, 'ntc': {'privilege': '15', 'nopassword': False, 'secret': '$1$AaNydwlV$vMgZSJ48pseyBstYJUvlm.', 'role': 'network-admin', 'format': '5'}}
```
]

---

class: ubuntu

# System Module


```
>>> sys = device.api('system')
>>> 
```

```
>>> sys.get()
{'hostname': 'spine1', 'iprouting': True}
```

```
>>> sys.set_hostname('spine001')
True
```

```
>>> sys.set_iprouting(True)
True
```

```
>>> sys.get()
{'hostname': 'spine001', 'iprouting': True}

```

---

# Summary

- Methods / Properties:
  - enable
  - config
  - api
  - running_config
- api
  - Use help() and dir() on the object
  - get() & getall()
  - set() for specific configurations

---

# Lab Time

- Lab 21 - Arista eAPI
  - Exploring pyeapi
  - Writing a LLDP Neighbors Script

