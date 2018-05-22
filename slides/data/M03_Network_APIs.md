layout: true

.footer-picture[![Network to Code Logo](data/media/Footer2.PNG)]
.footnote-left[(C) 2018 Network to Code, LLC. All Rights Reserved. ]
.footnote-con[CONFIDENTIAL]

---

class: center, middle, title
.footer-picture[<img src="data/media/Footer1.PNG" alt="Blue Logo" style="alight:middle;width:350px;height:60px;">]

# Network APIs

---

# Agenda

* HTTP-Based APIs
* non-RESTful HTTP-Based APIs
  * Cisco Nexus NX-API
  * Arista eAPI
* RESTful HTTP-Based APIs
  * Cisco IOS-XE RESTCONF
  * Using Postman
* Consuming HTTP-Based APIs with Python requests
* Vendor Libraries
  * Juniper XML API (NETCONF) & PyEZ
  * Arista pyeapi
* Open Multi-Vendor Libraries
  * NAPALM
  * pyntc

---

class: middle, segue

# HTTP-Based APIs
### Network APIs

---

# HTTP-Based APIs

**There are two main types of HTTP-Based APIs:**

* RESTful HTTP-Based APIs
* non-RESTful HTP-Based APIs

In other words, those that adhere to the principles of REST and those that do not.

Both use HTTP(s) as transport.

---

# RESTful APIs

* The structure of modern web-based REST APIs came from a PhD called [Architectural Styles and the Design of Network-based Software Architectures](http://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm) by Roy Fielding in 2000.
* Goal to define the detail of working with networked systems on the Internet that use the architecture defined as REST
* REST architecture includes six (6) constraints that must be adhered to.  Three (3) of them that help understand REST for this course:
  * Client-Server
  * Stateless
  * Uniform interface

---

# REST Architecture

* **Client-Server** - Having a client-server architecture allows for portability and **changeability of client applications** without the server components being changed.  This could mean having different clients that consume the server resources (back-end API).

* **Stateless** - the communication between the client and server must be stateless.  **Clients** that use stateless forms of communications **must send all data required for the server to understand and perform the requested operation in a single request**.  This is in contrast to interfaces such as SSH where there is a persistent connection between a client and a server.

* **Uniform interface** - individual resources in scope within an API call are identified in HTTP request message. For example, in RESTful HTTP-based systems, **the URL used will reference a particular resource**.  In the context of networking, the resource maps to a network device construct such as a hostname, interface, routing protocol configuration, or any other _resource_ that exists on the device.  The uniform interface also states that the client should have enough information about a resource to create, modify, or delete a resource.

---

# HTTP Request Types

**RESTful and non-RESTful HTTP APIs use standard HTTP Request Types.**

.center[
<img src="data/media/apis/new/http_request_types.png" alt="HTTP Request Types" style="alight:middle;width:700px;height:270px;">
]


---

# HTTP Request Types

* In the context of networking, we can think of these request types as the following:

  * GET: obtaining configuration or operational data
  * PUT, POST, PATCH: making a configuration change
  * DELETE: removing a particular configuration



---

# Sample HTTP Requests

.left-column[

* Authentication Type
* HTTP Request Type
* URL
* Headers
  * Accept-Type
  * Content-Type
* Data (Body)

]

.right-column[

Example 1:

```bash
Basic Auth: ntc/ntc123
Request: GET
Accept-Type: application/json
URL: http://device/path/to/resource
```

Example 2:

```bash
Basic Auth: ntc/ntc123
Request: POST
Content-Type: application/json
URL: http://device/path/to/resource
Body: {'interface': "Eth1", "admin_state": "down"}
```

**Take note of the body**

]


---

# HTTP Response Codes

.center[
<img src="data/media/apis/new/http_response_codes.png" alt="HTTP Response  Codes" style="alight:middle;width:700px;height:200px;">
]

**Note: the response code types for HTTP-based APIs are no different than standard HTTP response codes.**

---

# Data Encoding

**Data is sent over the wire as XML or JSON**

.left-column[
- JavaScript Object Notation (JSON)
- Open Standard for data communication
- Uses *name*:*value* pairs
- Maps directly to Python dictionaries

]

.right-column[
```json
{
  "ins_api": {
    "type": "cli_show",
    "version": "1.2",
    "sid": "eoc",
    "outputs": {
      "output": {
        "input": "show hostname",
        "msg": "Success",
        "code": "200",
        "body": {
          "hostname": "nxos-spine1.ntc.com"
        }
      }
    }
  }
}

```

]


---

class: ubuntu

# Working with JSON in Python

* Remember `json.dumps(variable, indent=4)`
* We've been using it to pretty print a dictionary
  * It's also serializing the dictionary as a JSON string


```
>>> facts = {'vendor': 'cisco'}
>>>
>>> import json
>>>
>>> test = json.dumps(facts, indent=4)
>>>
>>> type(test)
<type 'str'>
>>>
```


**What about the reverse?**
  * Take a JSON string and consume as a Python dictionary.

---

# Working with JSON in Python

.left-column[

```python
#!/usr/bin/env python

import json

if __name__ == "__main__":
    facts = {
        'hostname': 'nxos-spine1',
        'os': '7.3',
        'location': 'New_York'
    }
    print(facts)
    print(json.dumps(facts, indent=4))
    print(facts['os'])
```
]

.right-column[
.ubuntu[```
$ python json_test.py
{'hostname': 'nxos-spine1', 'os': '7.3', 'location': 'New_York'}
{
    "hostname": "nxos-spine1",
    "os": "7.3",
    "location": "New_York"
}
7.3


```

]]

---


# Working with JSON in Python

.left-column[
- JSON strings are not dictionaries
- The **loads** function from **json** converts it into a dictionary

```python
facts = '{"hostname": "nxos-spine1", "os": "7.3", "location": "New_York"}'
print(facts)
print(type(facts))
print(facts['os'])

factsd = json.loads(facts)
print(factsd)
print(factsd['os'])
```
]

.right-column[
.ubuntu[
```
$ python json_test2.py
```

```
{"hostname": "nxos-spine1", "os": "7.3", "location": "New_York"}
```

```
<type 'str'>
```

```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: string indices must be integers, not str
```

```
{"hostname": "nxos-spine1", "os": "7.3", "location": "New_York"}
```

```
7.3
```

]]


---

# Getting Familiar with JSON Output

.left-column[
- Supported by many vendors who implement web based (REST) APIs
- Certain CLIs allow you to pipe commands to JSON

.ubuntu[```
nxos-spine1# show hostname
nxos-spine1.ntc.com
nxos-spine1#
```
]

.ubuntu[```
nxos-spine1# show vlan brief

VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Eth2/5, Eth2/6
100  web_vlan                         active

nxos-spine1#
```
]
]

.right-column[
.ubuntu[
```
nxos-spine1# show hostname | json
{
  "hostname": "nxos-spine1.ntc.com"
}
```

]

.ubuntu[
```
nxos-spine1# show vlan brief | json
{
  "TABLE_vlanbriefxbrief": {
    "ROW_vlanbriefxbrief": [
      {
        "vlanshowbr-vlanid": 16777216,
        "vlanshowbr-vlanid-utf": 1,
        "vlanshowbr-vlanname": "default",
        "vlanshowbr-vlanstate": "active",
      },
      {
        "vlanshowbr-vlanid": 1677721600,
        "vlanshowbr-vlanid-utf": 100,
        "vlanshowbr-vlanname": "web_vlan",
      }
    ]
output modified for brevity
```

]]


---

class: ubuntu


# Getting Familiar with JSON Output

**Take the output from the CLI and copy into the Python shell for testing**

```
>>> test_var = """
... {
...   "hostname": "nxos-spine1.ntc.com"
... }
... """
>>>
```

**Perform your tests**

```
>>> type(test_var)
<type 'str'>
>>>
>>> response = json.loads(test_var)
>>>
>>> type(response)
<type 'dict'>
>>>
>>> print(response['hostname'])
nxos-spine1.ntc.com
>>>
```




---

class: middle, segue

# non-RESTful HTTP APIs
### Network APIs

---

# What makes APIs non RESTful?

In the context of networking, pay attention to the following:

* The URL is always the same

* The HTTP Request Type (verb) is always the same
  * Are you simply collecting data using a HTTP POST?
  * Are you making a change using a HTTP GET?

---

# non-RESTful HTTP-Based APIs

We are going to look at two non-RESTful APIs:  **Cisco Nexus NX-API (CLI)** and **Arista eAPI**.

* All API requests are POSTs
* All API requests use the same URL


---

# Cisco Nexus NX-API

**Enable NX-API**:

```bash
feature nxapi
```

Configure ports as needed:

```bash
nxapi https port 8443
nxapi http port 8080
```

Certain platforms require a command to enable the **sandbox**:

```bash
nxapi sandbox
```

Certain platforms support VRF support:

```bash
n9k2(config)# nxapi ?
  certificate  Https certificate configuration
  http         Http configuration
  https        Https configuration
  use-vrf      Vrf to be used for nxapi communication
```

---

# Cisco NX-API Developer Sandbox

* On-box web utility that allows you to practice making API calls
* Visually see response objects before writing code
* Simply browse to the Nexus switch using a web browser


---

# Cisco NX-API Developer Sandbox

.center[
<img src="data/media/apis/cisco/01_auth.png" alt="NX-API Auth" style="alight:middle;width:900px;height:475px;">
]

---

# Cisco NX-API Developer Sandbox

.center[
<img src="data/media/apis/cisco/02_sandbox.png" alt="NX-API Sandbox" style="alight:middle;width:1000px;height:455px;">
]

---

# Arista eAPI

**Enable eAPI**

```bash
management api http-commands
   protocol http
   no shutdown
   vrf MANAGEMENT
      no shutdown
!
```

---

# Arista eAPI Command Explorer

* On-box web utility that allows you to practice making API calls
* Visually see response objects before writing code
* Simply browse to the Arista switch using a web browser



---

# eAPI Command Explorer

- Browser to http(s)://switch_ip_name

.center[
<img src="data/media/apis/arista/01a_auth.png" alt="Arista Explorer Auth" style="alight:middle;width:650px;height:175px;">
]

---

# eAPI Command Explorer

.center[
<img src="data/media/apis/arista/01_explorer.png" alt="Arista Explorer" style="alight:middle;width:700px;height:475px;">
]

---

# JSON Response

.left-column[
.center[
<img src="data/media/apis/arista/03_shver_req.png" alt="JSON Request" style="alight:middle;width:500px;height:475px;">
]]

.right-column[
.center[
<img src="data/media/apis/arista/04_shver_resp.png" alt="JSON Response" style="alight:middle;width:600px;height:450px;">
]]

---


# Text Response

.center[
<img src="data/media/apis/arista/05_shver_text.png" alt="JSON Text Response" style="alight:middle;width:1025px;height:500px;">
]

---

# Sending Multiple Show Commands

.center[
<img src="data/media/apis/arista/06_multi_show.png" alt="Sending Multiple Show commands" style="alight:middle;width:1025px;height:500px;">
]

---

# Sending Multiple Config Commands

.center[
<img src="data/media/apis/arista/06_multi_config.png" alt="Sending Multiple Config commands" style="alight:middle;width:1025px;height:500px;">
]

---

# Command Documentation

.center[
<img src="data/media/apis/arista/08_command_docs.png" alt="Docs" style="alight:middle;width:900px;height:475px;">
]


---

# Demo

* Cisco Nexus NX-API Sandbox
* Arista eAPI Command Explorer

Note: these are learning and testing tools.


---

# Lab Time

* Lab 22 - Exploring eAPI and NXAPI 
  * Choose either the eAPI Command Explorer or NX-API Developer Sandbox Lab


---

class: middle, segue

# RESTful HTTP APIs
### Network APIs

---

# RESTful APIs

* URL maps to a particular resource
* HTTP Request Type specifies requested operation

We are going to look at the IOS-XE RESTCONF API.

---

# What is RESTCONF?

* Functional sub-set of NETCONF
* Exposes YANG models via a REST API (URL)
* Uses HTTP(S) as transport
* Uses XML or JSON for encoding
* Uses standard HTTP verbs in REST APIs
* Content-Type & Accept Headers:
  * application/vnd.yang.data+json
  * application/vnd.yang.data+xml


**Note: Must exit configuration mode after making a change for it to be readable via RESTCONF**

---

# RESTCONF on IOS-XE

Enabling RESTCONF

```bash
restconf
!
username <username> privilege 15 password <password>
!
ip http server
ip http secure-server
!

```

Note:  not yet supported by TAC.

---

# Request Methods

GET - Retrieves data from the specified object

**PUT - Replaces full configuration object of tree specified**

POST- Creates the object with the supplied information

DELETE - Deletes the specified object

PATCH - Applies partial modifications to the specified object


---

# RESTCONF Example 1

Retrieve a full running configuration modeled as JSON.

.left-column[
```bash
Method: GET
URL: 'http://csr1/restconf/api/config/native'
Accept-Type: application/vnd.yang.data+json
```
]

.right-column[

```json
{
    "ned:native": {
         # output removed for example
        "interface": {
            "GigabitEthernet": [
                {
                    "name": "1"
                },
                {
                    "name": "2"
                },
                {
                    "name": "3"
                },
                {
                    "name": "4"
                }
            ]
        },
        # truncated for example
}
```
]

---

# RESTCONF Example 2

Adding `?deep` adds the full configuration including all children elements.

.left-column[

```bash
Method: GET
URL: 'http://csr1/restconf/api/config/native?deep'
Accept-Type: application/vnd.yang.data+json
```
]


.right-column[

```json
{
    "ned:native": {
        # output removed
        "interface": {
            "GigabitEthernet": [
                {
                    "negotiation": {
                        "auto": true
                    },
                    "ip": {
                        "access-group": {},
                        "arp": {
                            "inspection": {}
                        },
                        "nhrp": {
                            "attribute": {},
                            "nhs": {
                                "dynamic": {}
                        },
                        "address": {
                            "primary": {
                                "mask": "255.255.255.0",
                                "address": "10.0.0.51"
                            }
                        },] #output truncated
```
]

---

# RESTCONF Example 2

Narrowing the scope and examining the hierarchy

```json
{
    "ned:native": {
        "interface": {
            "GigabitEthernet": [
                    "name": "1",
                    "ip": {
                        "address": {
                            "primary": {
                                "mask": "255.255.255.0",
                                "address": "10.0.0.51"
                            }
                        }]
    # output removed
```

**Pattern**

interface (dict) -> GigabitEthernet (list) -> ip (dict) -> address (dict)


---

# RESTCONF Example 3


Request:

```bash
Method: GET
URL: 'http://csr1/restconf/api/config/native/interface/GigabitEthernet/1/ip/address'
Accept-Type: application/vnd.yang.data+json
```

Response:
```json
{
    "ned:address": {
        "primary": {
            "mask": "255.255.255.0",
            "address": "10.0.0.51"
        }
    }
}
```
---

# RESTCONF Example 4

**Understanding PUT, PATCH, POST by Updating an Interface**

Existing Configuration

```bash
interface Loopback100
 ip address 222.22.2.2 255.255.255.0 secondary
 ip address 100.2.2.2 255.255.255.0
```

BODY Used for POST, PATCH, PUT:

```json
{
   "ned:Loopback":{
      "name":100,
      "ip":{
         "address":{
            "primary":{
               "address":"100.2.2.2",
               "mask":"255.255.255.0"
            }
         }
      }
   }
}

```

---

# RESTCONF Example 4 - The Result


**Request 1**:

POST   http://csr1/restconf/api/config/native/interface/

**Response**: 409; Error: Object Already Exists; No change in config

--

**Request 2**:

PATCH http://csr1/restconf/api/config/native/interface/Loopback

**Response** 204; No change in config

--

**Request 3**:

PUT     http://csr1/restconf/api/config/native/interface/Loopback/100


**Response** 204;

---

# RESTCONF Example 4 - The Result

**RESULT FOR THE PUT**

Existing Configuration

```bash
interface Loopback100
 ip address 100.2.2.2 255.255.255.0
```


---

# Static Route Management

Using RESTCONF to manage static route configuration

Starting Configuration:

```bash
csr1kv# show run | inc route
 ip route 0.0.0.0 0.0.0.0 10.0.0.2
```



---

# RESTCONF Example 5 - PATCHing Routes

PATCH  http://csr1/restconf/api/config/native/ip/route

Body:
```json
{
   "ned:route":{
      "ip-route-interface-forwarding-list":[
         {
            "prefix":"172.16.0.0",
            "mask":"255.255.0.0",
            "fwd-list":[
               {
                  "fwd":"192.168.1.1"
               }
            ]
         },
         {
            "prefix":"10.0.100.0",
            "mask":"255.255.255.0",
            "fwd-list":[
               {
                  "fwd":"192.168.1.1"
               }
            ]
         }
      ]
   }
}
```

---

# RESTCONF Example 5 - PATCHing Routes (cont'd)


Resulting New Configuration:

```bash
csr1kv# show run | inc route
ip route 0.0.0.0 0.0.0.0 10.0.0.2
ip route 10.0.100.0 255.255.255.0 192.168.1.1
ip route 172.16.0.0 255.255.0.0 192.168.1.1
```

---

# RESTCONF Example 6 - PUTing Routes

Starting Configuration:

```bash

csr1kv#show run | inc route
ip route 0.0.0.0 0.0.0.0 10.0.0.51
ip route 10.0.100.0 255.255.255.0 192.168.1.1
ip route 172.16.0.0 255.255.0.0 192.168.1.1
```

---

# RESTCONF Example 6 - PUTing Routes (cont'd)


PUT http://csr1/restconf/api/config/native/ip/route

Body:

```json
{
   "ned:route":{
      "ip-route-interface-forwarding-list":[
         {
            "prefix":"0.0.0.0",
            "mask":"0.0.0.0",
            "fwd-list":[
               {
                  "fwd":"10.0.0.2"
               }
            ]
         }
      ]
   }
}
```

---

# RESTCONF Example 6 - PUTing Routes (cont'd)


Resulting New Configuration:

```bash
csr1kv# show run | inc route
ip route 0.0.0.0 0.0.0.0 10.0.0.2
```


---

# Summary

* True REST APIs are powerful
* Be careful using PUTs
* With great power comes great responsibility


---


class: middle, segue

# Learning how to use HTTP APIs with Postman
### Network APIs


---


# Postman

* Google Chrome application that provides a user intuitive GUI application to interact with HTTP-based APIs.
* Primarily Used for testing and learning
* You can create a job collection


---

# Postman (cont'd)

.center[
<img src="data/media/apis/new/postman_intro.png" alt="Postman 101" style="alight:middle;width:900px;height:500px;">
]


---

# Demo

* Postman 101

---

# Lab Time

* Lab 23 - Exploring the IOS-XE RESTCONF API
  * Exploring the IOS-XE RESTCONF API
 


Note: Feel free to test it with NX-API or eAPI.

---

class: middle, segue

# Bonus Material
## Consuming HTTP APIs with Python requests
#### Network APIs

---

# Python requests

- Python module to interact with HTTP based APIs (REST)
- Useful functions are **post** and **get**
  - Function per HTTP verb, i.e. **post** is used for POST requests and **get** is used for GET requests
- Optional, helper method for basic Authentication
- Headers used to dictate data encoding

```python
import requests
from requests.auth import HTTPBasicAuth

auth = HTTPBasicAuth('ntc', 'ntc123')

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
```

Sample GET:

```python
response = requests.get('http://<device>', headers=headers, auth=auth)
```


---

# Python requests

* `data` must be a JSON string - must use `json.dumps()`
* `data`, `headers`, and `auth` are defined parameters that must be used within the requests library
* `payload` is an arbitrary variable that maps back to device API requirements

```py
import requests
import json
from requests.auth import HTTPBasicAuth

auth = HTTPBasicAuth('ntc', 'ntc123')

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
payload = <# some dictionary #>

url = 'http://eos-spine1/command-api'

response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth)

```

---

# Python requests

.left-column[

```python
#!/usr/bin/env python
import requests
import json
from requests.auth import HTTPBasicAuth

if __name__ == "__main__":
    auth = HTTPBasicAuth('ntc', 'ntc123')
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        "jsonrpc": "2.0",
        "method": "runCmds",
        "params": {
            "version": 1,
            "cmds": [
                "show version"
            ],
            "format": "json",
            "timestamps": False
        },
        "id": "ntc"
    }
    url = 'http://eos-spine1/command-api'
    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth)
    rx_object = json.loads(response.text)
    print('Status Code: ' + str(response.status_code))

```
]

--

.right-column[
- Run *show version* on a Arista switch
- Print **status_code**, **text** and OS version.
- The **text** attribute contains the response of a request as a JSON string
- The **status_code** attribute contains the HTTP response code


```python
Status Code: 200
{
    "jsonrpc": "2.0",
    "result": [
        {
            "memTotal": 3895836,
            "version": "4.15.2F",
            "internalVersion": "4.15.2F-2663444.4152F",
            "serialNumber": "",
            "systemMacAddress": "2c:c2:60:28:54:dd",
            "bootupTimestamp": 1477365548.64,
            "memFree": 1621108,
            "modelName": "vEOS",
            "architecture": "i386",
            "internalBuildId": "0ebbad93-563f-4920-8ecb-731057802b9c",
            "hardwareRevision": ""
        }
    ],
    "id": "ntc"
}
```
]

---

# Python requests

.left-column[

```python
#!/usr/bin/env python
import requests
import json
from requests.auth import HTTPBasicAuth
if __name__ == "__main__":
    auth = HTTPBasicAuth('ntc', 'ntc123')
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        "jsonrpc": "2.0",
        "method": "runCmds",
        "params": {
            "version": 1,
            "cmds": [
                "show hostname",
                "show vlan"
            ],
            "format": "json",
            "timestamps": False
        },
        "id": "ntc"
    }
    url = 'http://eos-spine1/command-api'
    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth)
    rx_object = json.loads(response.text)
    print('Status Code: ' + str(response.status_code))
    result = rx_object['result']
    print("Hostname: ", json.dumps(result[0], indent=4))
    print("VLANs: ", json.dumps(result[1], indent=4))
```
]

--

.right-column[
- The **cmds** request parameter is a list.
- Run *show hostname* and *show vlan* at the same time.
- *result* is a list and can be used to print individual command output.



```python
Status Code: 200
Hostname:  {
    "hostname": "eos-spine1",
    "fqdn": "eos-spine1.ntc.com"
}
VLANs:  {
    "sourceDetail": "",
    "vlans": {
        "1": {
            "status": "active",
            "interfaces": {},
            "dynamic": false,
            "name": "default"
        }
    }
}
```
]


---

# Using requests with IOS-XE

.left-column[
```python
#!/usr/bin/env python
import requests
import json
from requests.auth import HTTPBasicAuth

if __name__ == "__main__":
    auth = HTTPBasicAuth('ntc', 'ntc123')
    headers = {
        'Accept-Type': 'application/vnd.yang.data+json',
        'Content-Type': 'application/vnd.yang.data+json'
    }

    url = 'http://csr1/restconf/api/config/native/interface'
    response = requests.get(url, headers=headers, auth=auth)
    print('Status Code: ' + str(response.status_code))
    print("\nInterfaces Object: ", response.text)
```
]

.right-column[
```shell
Status Code: 200

{
  "ned:interface": {
    "GigabitEthernet": [
      {
        "name": "1"
      },
      {
        "name": "2"
      },
      {
        "name": "3"
      },
      {
        "name": "4"
      }
    ]
  }
}

```
]

---

# Lab Time

* Lab 24 - Using Python requests
* Pick one of the following labs:
  * 24.1 - requests using eAPI
  * 24.2 - requests using NX-API

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
>>> print(json.dumps(facts, indent=4))
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
>>> print(json.dumps(interfaces, indent=4))
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



# NAPALM Configuration Management

**Example Workflow**

Works slightly different than based on individual drivers and operating systems.

1. Connect to Device
2. Copy desired configuration to device (checkpoint file, candidate configuration, config session, bootflash as candidate_config.txt)
3. Use a vendor command to view diffs
4. Use a vendor command to apply configuration changes
5. Optionally, rollback to a config that exists in the file system.

Note: you dictate if the supplied configuration is a full config file or partial configuration

---

# Configuration Replace

Focus on desired configuration commands.

**Scenario:** You need to remove two loopback interfaces and change the hostname.

**NAPALM Config Replace**:
  * Full configuration is sent to the device, but...
  * Only diffs are applied.
  * You do not need to worry about going from A to B - you just focus on B.




```bash
$ more diffs/csr1.diffs
+hostname csr1
-hostname csr_old_name
-interface Loopback100
 -ip address 1.1.1.1 255.255.255.255
-interface Loopback200
 -ip address 22.2.1.1 255.255.255.255
-ip route 10.1.1.0 255.255.255.0 192.0.1.1
```

**IMPORTANT**: There are no `no` commands used.  The underlying OS generates the diffs (for most NAPALM drivers).

---

# Configuration Merge

You can use NAPALM for declarative management for a sectional config too.

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
    neighbor 10.0.0.0 maximum-routes 12000
    neighbor 10.0.0.1 remote-as 65512
    neighbor 10.0.0.1 maximum-routes 12000
+   neighbor 10.0.0.2 remote-as 65500
+   neighbor 10.0.0.2 maximum-routes 12000
+   neighbor 10.0.0.10 remote-as 65512
+   neighbor 10.0.0.10 maximum-routes 12000
    network 20.20.20.0/24
+   network 100.0.100.0/24
 !
 management api http-commands
    protocol http

```


]

---

# Configuration Merge (Advanced)

You can use NAPALM for declarative management for a sectional config too.

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
>>> print(diffs)
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
>>> print(device.compare_config())
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
  - Uses junos-pyez API with NETCONF Junos candidate configurations
  - Locks configurations while performing operations till first commit/rollback
  - Uses `rollback 0` to rollback configuration

* NXOS
  - Uses checkpoint files for config replacement. A checkpoint file can be obtained with `device._get_checkpoint_file()` which issues `checkpoint file temp_cp_file_from_napalm` on the device and then prints it
  - Diffs for config replacement are a list of commands that would be needed to take the device from its current state to the desired config state using `show diff rollback-patch file <source_of_truth_file> file <config_file>` command
  - Merges send config line by line. This doesn’t use the checkpoint/rollback functionality. As a result, merges are not atomic
  - Replaces uses `rollback running file <config_file>` command



---

# Lab Time - BONUS

- Lab 25 - NAPALM
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
>>> print(run)
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
