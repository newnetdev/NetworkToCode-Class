layout: true

.footer-picture[![Network to Code Logo](slides/media/Footer2.PNG)]
.footnote-left[(C) 2015 Network to Code, LLC. All Rights Reserved. ]
.footnote-con[CONFIDENTIAL]

---

class: center, middle, title
.footer-picture[<img src="slides/media/Footer1.PNG" alt="Blue Logo" style="alight:middle;width:350px;height:60px;">]

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
<img src="slides/media/apis/new/http_request_types.png" alt="HTTP Request Types" style="alight:middle;width:700px;height:270px;">
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
Basic Auth:  ntc/ntc123
Request: GET
Accept-Type: application/json
URL:  http://device/path/to/resource
```

Example 2:

```bash
Basic Auth:  ntc/ntc123
Request: POST
Content-Type: application/json
URL:  http://device/path/to/resource
Body: {'interface': "Eth1", "admin_state": "down"}
```

**Take note of the body**

]


---

# HTTP Response Codes

.center[
<img src="slides/media/apis/new/http_response_codes.png" alt="HTTP Response  Codes" style="alight:middle;width:700px;height:200px;">
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
    print facts
    print json.dumps(facts, indent=4)
    print facts['os']
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
print facts
print type(facts)
print facts['os']

factsd = json.loads(facts)
print factsd
print factsd['os']
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
>>> print response['hostname']
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

**Enable NX-API**

```bash
feature nxapi
```

Configure ports as needed:

```bash
nxapi https port 8443
nxapi http port 8080
```

Certain platforms require a command to enable the **sandbox**

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
<img src="slides/media/apis/cisco/01_auth.png" alt="NX-API Auth" style="alight:middle;width:900px;height:475px;">
]

---

# Cisco NX-API Developer Sandbox

.center[
<img src="slides/media/apis/cisco/02_sandbox.png" alt="NX-API Sandbox" style="alight:middle;width:1000px;height:455px;">
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
<img src="slides/media/apis/arista/01a_auth.png" alt="Arista Explorer Auth" style="alight:middle;width:650px;height:175px;">
]

---

# eAPI Command Explorer

.center[
<img src="slides/media/apis/arista/01_explorer.png" alt="Arista Explorer" style="alight:middle;width:700px;height:475px;">
]

---

# JSON Response

.left-column[
.center[
<img src="slides/media/apis/arista/03_shver_req.png" alt="JSON Request" style="alight:middle;width:500px;height:475px;">
]]

.right-column[
.center[
<img src="slides/media/apis/arista/04_shver_resp.png" alt="JSON Response" style="alight:middle;width:600px;height:450px;">
]]

---


# Text Response

.center[
<img src="slides/media/apis/arista/05_shver_text.png" alt="JSON Text Response" style="alight:middle;width:1025px;height:500px;">
]

---

# Sending Multiple Show Commands

.center[
<img src="slides/media/apis/arista/06_multi_show.png" alt="Sending Multiple Show commands" style="alight:middle;width:1025px;height:500px;">
]

---

# Sending Multiple Config Commands

.center[
<img src="slides/media/apis/arista/06_multi_config.png" alt="Sending Multiple Config commands" style="alight:middle;width:1025px;height:500px;">
]

---

# Sending Multiple Config Commands

.center[
<img src="slides/media/apis/arista/06_multi_config.png" alt="Sending Multiple Config commands" style="alight:middle;width:1025px;height:500px;">
]

---

# Command Documentation

.center[
<img src="slides/media/apis/arista/08_command_docs.png" alt="Docs" style="alight:middle;width:900px;height:475px;">
]


---

# Demo

* Cisco Nexus NX-API Sandbox
* Arista eAPI Command Explorer

Note: these are learning and testing tools.


---

# Lab Time

* Lab 16 - Exploring Cisco Nexus and Arista APIs
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

# RESTCONF EXAMPLE 1

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

# RC Example 5 - PATCHing Routes

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

# RC Example 5 - PATCHing Routes (cont'd)


Resulting New Configuration:

```bash
csr1kv# show run | inc route 
ip route 0.0.0.0 0.0.0.0 10.0.0.2
ip route 10.0.100.0 255.255.255.0 192.168.1.1 
ip route 172.16.0.0 255.255.0.0 192.168.1.1
```

---

# RC Example 6 - PUTing Routes

Starting Configuration:

```bash

csr1kv#show run | inc route 
ip route 0.0.0.0 0.0.0.0 10.0.0.51
ip route 10.0.100.0 255.255.255.0 192.168.1.1 
ip route 172.16.0.0 255.255.0.0 192.168.1.1
```

---

# RC Example 6 - PUTing Routes (cont'd)


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

# RC Example 6 - PUTing Routes (cont'd)


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
--- 

# Postman (cont'd)

.center[
<img src="slides/media/apis/new/postman_intro.png" alt="Postman 101" style="alight:middle;width:900px;height:500px;">
]


---

# Demo

* Postman 101

---

# Lab Time

* Lab 17 - Using Postman 
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
    print 'Status Code: ' + str(response.status_code)

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
    print 'Status Code: ' + str(response.status_code)
    result = rx_object['result']
    print "Hostname: ", json.dumps(result[0], indent=4)
    print "VLANs: ", json.dumps(result[1], indent=4)
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
    print 'Status Code: ' + str(response.status_code)
    print "\nInterfaces Object: ", response.text
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

* Lab 18 - Consuming HTTP APIs with requests
* Pick one of the following labs:
  * 18.1 - requests using eAPI
  * 18.2 - requests using NX-API
* Lab 18.3 - requests using RESTCONF on XE


