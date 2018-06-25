layout: true

.footer-picture[![Network to Code Logo](data/media/Footer2.PNG)]
.footnote-left[(C) 2018 Network to Code, LLC. All Rights Reserved. ]
.footnote-con[CONFIDENTIAL]

---

class: center, middle, title
.footer-picture[<img src="data/media/Footer1.PNG" alt="Blue Logo" style="alight:middle;width:350px;height:60px;">]

# Data Types, JSON, and YAML


---

# Module Overview

- Strings
- Integers
- Boolean
- Lists
- Dictionaries
- Nested Objects
- JSON
- YAML

---

# Data Types - Strings

- Sequence of characters enclosed by quotes
- Single or double quotes are accepted, but be consistent

Examples:

``` python
'router1'
"10.200.1.1./24"
'3'
"3.141"

```
---

# Data Types - Integers
- Integers
- Whole numbers such as 1, 2, 3, 4, 100.
- Those that do not have a decimal point

Examples:

``` python
1
10
25
```
---

# Data Types - Boolean

- Conditions are evaluated and evaluate to:
- `True`
- `False`
- Capital T and F


---
# Data Types - Lists

- Store multiple objects as an **ordered** list
- Indexed by an integer value starting at 0
- Sometimes referred to as arrays
- Elements can be of different data types
- Identified by the encapsulating '[ ]'

Examples:

``` python

['switch1', '10.1.100.1/24', '00:00:00:00:00:01', 'cisco']
['switch2', '10.1.100.2/24', '00:00:00:00:00:02', 'arista']

var1[1] will yield '10.1.100.1/24'
var2[0] will yield 'switch2'



```

---
# Data Types - Lists


- Lists can be used as stacks or queues
- Supports access over a subset/range
- Are used in loops for iteration, since there is a predictable length
and index number

Examples:

``` python
available_vlans = [ 100, 101, 102, 103, 104 ]

available_vlans[-1] will yield 104  #Collect the last element
and available_vlans[-2] will yield 103

available_vlans[1:3] will yield a subset list [ 101, 102 ]

```


---

# Data Types - Dictionaries


- Dictionaries are **unordered** lists
- Instead of being indexed by a number, they are indexed by a name, more commonly known as a key
- Also known as hashes and associative arrays
- Dicts vs. Lists
- Key Values vs. Indexed Elements
- Identified by the encapsulating '{ }'

**Instead of accessing an element by an index, you can use a word/string you define, i.e. a _key_**

Example:

``` python
{ 'hostname': 'switch1', 'ip_address': '10.1.100.1/24','mac': '00:00:00:00:00:01', 'vendor': 'cisco' }
{ 'hostname': 'switch2', 'ip_address': '10.1.100.2/24','mac': '00:00:00:00:00:02', 'vendor': 'arista' }

```
---

# Data Types - Dictionaries


``` python

{
    'hostname': 'switch1',
    'ip_address': '10.1.100.1/24',
    'mac': '00:00:00:00:00:01',
    'vendor': 'cisco'
}

```
``` python
{
    'hostname': 'switch2',
    'ip_address': '10.1.100.2/24',
    'mac': '00:00:00:00:00:02',
    'vendor': 'arista'
}

```

Accessing values

If the dictionaries were stored as `sw1` and `sw2`, you can access the
values as follows:


``` python
sw1['hostname'] will yield 'switch1'
sw2['vendor'] will yield 'arista'

```
---

# Nested Objects


**When you're just starting it much more important to be able to extract data from a complex object.  Common for working with device APIs.**

Basic objects include:
* Lists of strings
* Dictionaries with strings as values
* Need to understand more complex objects
* One of the most important topics regardless of programming language or tool used

A list of lists

``` python
[
    ['switch1', '10.1.100.1/24', '00:00:00:00:00:01', 'cisco'],
    ['switch2', '10.1.100.2/24', '00:00:00:00:00:02', 'arista']
]

var[0] = ['switch1', '10.1.100.1/24', '00:00:00:00:00:01', 'cisco']
var[1][2] = '00:00:00:00:00:02'

```


---
# Nested Objects

List of dictionaries

.left-column[
``` python
[

    {
    'hostname': 'switch1',
    'ip_address': '10.1.100.1/24',
    'mac': '00:00:00:00:00:01',
    'vendor': 'cisco'
    },
    {
    'hostname': 'switch2',
    'ip_address': '10.1.100.2/24',
    'mac': '00:00:00:00:00:02',
    'vendor': 'arista'
    }

]
..............

var[0] = {'vendor': 'cisco', 'mac': '00:00:00:00:00:01', 'hostname': 'switch1', 'ip_address': '10.1.100.1/24'}

var[1]['mac'] = '00:00:00:00:00:02'

```
]

.right-column[

``` python
[
    {
    'vlan_name': 'web',
    'vlan_id': '10',
    'vlan_state': 'active'
    },
    {
    'vlan_name': 'app',
    'vlan_id': '20',
    'vlan_state': 'active'
    },
    {
    'vlan_name': 'DB',
    'vlan_id': '30',
    'vlan_state': 'active'
    }

]
...........

var[-1]['vlan_name'] = 'DB'
```
]

---

# Nested Objects

A nested dictionary

``` python
{
    'switches': {
        'hostname': 'switch1',
        'ip_address': '10.1.100.1/24',
        'mac': '00:00:00:00:00:01',
        'vendor': 'cisco',
        'vlans': [ 100, 101, 102, 103, 104 ],
        'snmp': {
            'ro': 'public',
            'rw': 'private',
            'info': {
                'location': 'nyc',
                'contact': 'bob'
                    }
                }
            }

}
=======================y
var['switches']['hostname'] = 'switch1'
var['switches']['vlans'][1] = 101
var['switches']['snmp']['ro'] = 'private'
var['switches']['snmp']['info']['location'] = 'nyc'

```

---
# Data Encoding

- Humans interface with network devices using SSH
- CLI commands are sent over SSH
- Device respond with un-structured, but formatted text
- Machines do not understand formatted text
- They need structured data
- APIs use encoding formats for a means to structure data between networked systems
- JSON & XML are the two most common data encoding formats



---

# JSON

.left-column[
- JavaScript Object Notation (JSON)
- Open Standard for data communication
- Uses *name*:*value* pairs (key-value)
- Maps directly to Python dictionaries
- Key-value pairs wrapped within curly braces
- Objects can be nested

```json
{
    "hostname": "switch1"
}
```

```json

{
    'snmp_ro': 'public',
    'snmp_rw': 'private',
    'location': 'nyc',
    'contact': 'bob'
}


```

]

.right-column[


```json
{
    "hostname": "switch1",
    "snmp": {
        "ro": "public",
        "rw": "private",
        "location": "nyc",
        "contact": "bob"
        },
}
```

```json
{
    "hostname": "switch1",
    "snmp": {
        "ro": "public",
        "rw": "private",
        "location": "nyc",
        "contact": "bob
        },
    "vlans": [100, 101, 102, 103, 104]
}
```


]


---


# Cisco Nexus NX-API JSON Objects


**NX-API JSON Response**

...For an API call to `show vlan brief`

.small-code[
```json
{
    "ins_api": {
        "type": "cli_show",
        "version": "1.2",
        "sid": "eoc",
        "outputs": {
            "output": {
                "input": "show vlan brief",
                "msg": "Success",
                "code": "200",
                "body": {
                    "TABLE_vlanbriefxbrief": {
                    "ROW_vlanbriefxbrief": [
                        {
                            "vlanshowbr-vlanid": 16777216,
                            "vlanshowbr-vlanid-utf": 1,
                            "vlanshowbr-vlanname": "default",
                            "vlanshowbr-vlanstate": "active",
                            "vlanshowbr-shutstate": "noshutdown"
                        },
                        {
                            "vlanshowbr-vlanid": 335544320,
                            "vlanshowbr-vlanid-utf": 20,
                            "vlanshowbr-vlanname": "app",
                            "vlanshowbr-vlanstate": "active",
                            "vlanshowbr-shutstate": "noshutdown"
                        }
                        ]
                    }
                }
            }
        }
    }
}
```
]


---


# Cisco IOS-XE REST JSON Objects

**RESTCONF JSON Response**

...For an API call to list the IP addresses for an interface
```json
{
    "ned:address": {
        "primary": {
            "address": "10.0.0.51",
            "mask": "255.255.255.0"
            },
        "secondary": [
            {
            "address": "10.89.1.1"
            }
        ]
    }
}
```

---

class: center, middle, title
.footer-picture[<img src="data/media/Footer1.PNG" alt="Blue Logo" style="alight:middle;width:350px;height:60px;">]

# YAML Basics


---

# YAML

- Human readable data serialization language
- Heavily used for configuration files
- Relies heavily on indentation
- 2 space indent is common
- Superset of JSON


---

# YAML Basics

**YAML documents start with 3 hyphens (`---`)**

Basic Key-Value Pairs
.left-column[
YAML

```yaml
---
  hostname: switch1
  snmp_ro: public
  snmp_rw: private
  snmp_location: "nyc"

  # integer
  vlan_id: 100

  # string
  vlan_id: "101"

```
]

.right-column[
JSON

``` json
{
  hostname: switch1,
  snmp_ro: public,
  snmp_rw: private,
  snmp_location: "nyc",
  vlan_id: 100,
  vlan_id: "101"
}


Note: You can comment YAML but not JSON

```
]



---

# YAML Basics

List of Strings / Numbers

.left-column[
YAML

```yaml
---
  snmp_ro_communities:
    - public
    - public123

  vlans:
    - 100
    - 101
    - 102
    - 103
    - 104

```
]

.right-column[
JSON

``` json
{
    "snmp_ro_communities": [
        "public",
        "public123"
    ],
    "vlans": [
        100,
        101,
        102,
        103,
        104
    ]
}


```

]


---

# YAML Basics

List of dictionaries

.left-column[
YAML

``` yaml
---
  - vlan_name: web
    vlan_id: '10'
    vlan_state: active
  - vlan_name: app
    vlan_id: '20'
    vlan_state: active
  - vlan_name: DB
    vlan_id: '30'
    vlan_state: active

```
]

.right-column[
JSON

``` json
[
    {
    "vlan_name": "web",
    "vlan_id": "10",
    "vlan_state": "active"
    },
    {
    "vlan_name": "app",
    "vlan_id": "20",
    "vlan_state": "active"
    },
    {
    "vlan_name": "DB",
    "vlan_id": "30",
    "vlan_state": "active"
    }

]

```
]


---

# YAML Advanced Data Types

Dictionaries

.left-column[
YAML

```yaml
---

snmp:
  ro: public
  rw: private
  info:
    location: nyc
    contact: bob

vlans:
  10:
    name: web
  20:
    name: app


```

]

.right-column[
JSON

``` json
{
  "snmp": {
    "ro": "public",
    "rw": "private",
    "info": {
      "location": "nyc",
      "contact": "bob"
    }
  },
  "vlans": {
    "10": {
      "name": "web"
    },
    "20": {
      "name": "app"
    }
  }
}
```

]


---
# YAML Advanced Data Types
Dictionaries that are lists of dictionaries

.left-column[
YAML

```yaml
---
vlans:
  - id: 10
    name: web
  - id: 20
    name: app

snmp_community_strings:
  - type: ro
    community: public
  - type: ro
    community: networktocode
  - type: rw
    community: private

```

]

.right-column[
JSON

.small-code[
``` json
{
  "vlans": [
    {
      "id": 10,
      "name": "web"
    },
    {
      "id": 20,
      "name": "app"
    }
  ],
  "snmp_community_strings": [
    {
      "type": "ro",
      "community": "public"
    },
    {
      "type": "ro",
      "community": "networktocode"
    },
    {
      "type": "rw",
      "community": "private"
    }
  ]
}

```
]
]

---

# YAML Advanced Data Types

YAML is a superset of JSON

.left-column[
YAML

``` yaml
---
ned:Loopback:
  #YAML supports comments
  name: 200
  ip:
    address:
      primary:
        address: 100.200.2.2
        mask: 255.255.255.0
      secondary:
      - address: 100.200.20.20
      - address: 100.200.200.200

```


]

.right-column[
JSON

``` json
{
  "ned:Loopback": {
    "name": 200,
      "ip": {
      "address": {
        "primary": {
          "address": "100.200.2.2",
          "mask": "255.255.255.0"
        },
        "secondary": [
          {
            "address": "100.200.20.20"
          },
          {
            "address": "100.200.200.200"
          }
        ]
      }
      }
  }
}

```

]

---

# YAML Abbreviated Syntax

Reduces number of lines, but not as readable

```yaml
---

# list of strings
snmp_ro_communities: [public, public123]

# dictionary
snmp: { ro: public, rw: private }

# list of dictionaries
snmp_communities:
- { type: ro, community: public }
- { type: rw, community: private }

```

---

# Data Types - Summary

- For most automation tasks YAML and JSON have 1-1 mapping
- They both tie back to dictionaries
- A lot of initial automation tasks revolve around parsing return
  data, therefore it is important to understand:
      - Lists of lists
      - Lists of dictionaries
      - Dictionaries with lists
      - Complex nested objects
- Always remember to traverse a complex object from left to right
---


# Demo

- Validate YAML
- http://yamllint.com/
- YAML to JSON Conversion
- JSON to YAML Conversion
- https://www.json2yaml.com
- Understand how to model network configuration data in YAML (for use in Ansible)
- Compare/Contrast Data Models on different platforms

