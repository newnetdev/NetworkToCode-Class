## Lab 24.2 - Cisco NX-API

### Task 1 - Getting Started with the Python Requests Module

In this task, you will explore working with the Python requests module built to simplify working with HTTP-based (REST) APIs.

For this lab, you will use two Cisco Nexus switches.

##### Step 1

Verify you can ping the Cisco switches by name.  They have been pre-configured in your `/etc/hosts` file.

```
$ ping nxos-spine1
$ ping nxos-spine2
```

##### Step 2

Enter the Python shell.

```python
$ python

Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
[GCC 5.4.0 20160609] on linux2
Type "help", "copyright", "credits" or "license" for more information.

>>>
```

##### Step 3

Import the `requests` module while on the Python shell.  In addition, import the object that simplified using authentication for REST APIs as well as the `json` module.

```python
>>> import requests
>>> from requests.auth import HTTPBasicAuth
>>> import json
>>>
```

##### Step 4

Use `help` on `requests`.  You will see a description of this Python package.

```python
>>> help(requests)

```

```
Help on package requests:

NAME
    requests

FILE
    /usr/local/lib/python2.7/dist-packages/requests/__init__.py

DESCRIPTION
    Requests HTTP library
    ~~~~~~~~~~~~~~~~~~~~~

    Requests is an HTTP library, written in Python, for human beings. Basic GET
    usage:

       >>> import requests
       >>> r = requests.get('https://www.python.org')
       >>> r.status_code
       200
       >>> 'Python is a programming language' in r.content
       True

    ... or POST:

       >>> payload = dict(key1='value1', key2='value2')
       >>> r = requests.post('http://httpbin.org/post', data=payload)
       >>> print(r.text)
       {
         ...
         "form": {
           "key2": "value2",
           "key1": "value1"

# output omitted

```


You can also do a `dir(requests)` to see available attributes and built-in methods.


##### Step 5

Navigate to the NX-API Sandbox.  

Set the message format to `json` and command type is `cli_show`.  Enter the command `show version` into the text box.

You should see the following Request object in the bottom left:

```python
{
  "ins_api": {
    "version": "1.0",
    "type": "cli_show",
    "chunk": "0",
    "sid": "1",
    "input": "show version",
    "output_format": "json"
  }
}
```

This is the object we need to send to the device.  We'll use this in an upcoming step, so don't close the browser.

> You could also Press the "Python" button in the NX-API sandbox to give you a jump start, but we are doing things slightly different in this lab, so we won't use that code directly from the sandbox.


##### Step 6

Create four new variables while on the Python shell: `auth`, `headers`, `payload`, and `url`.

`auth` should be equal to `auth = HTTPBasicAuth('ntc', 'ntc123')`

`headers` should be equal to `headers = { 'Content-Type': 'application/json' }`

`payload` should be equal to the Request object you copied above as a dictionary.

`url` should be equal to `url = 'http://nxos-spine1/ins'` - this needs the `ins` appended to the switch name or IP to work.  

The summary up until this point is the following:

> Note: there is no need to format the dictionaries as shown below.  It is done for readability.  

```python
>>> import requests
>>> import json
>>> from requests.auth import HTTPBasicAuth
>>>
>>> auth = HTTPBasicAuth('ntc', 'ntc123')
>>> headers = {
...     'Content-Type': 'application/json'
... }
>>>
>>> payload = {
...     "ins_api": {
...         "version": "1.0",
...         "type": "cli_show",
...         "chunk": "0",
...         "sid": "1",
...         "input": "show version",
...         "output_format": "json"
...     }
... }
>>>
>>> url = 'http://nxos-spine1/ins'
>>>
```

At this point, we are ready to make a HTTP API call to the Nexus switch.  Remember the Nexus switch only supports HTTP POSTs even though we are _getting_ data back. This is why it's non-RESTful HTTP API.

##### Step 7

Make the API call to the device using the `post` function of `requests` as shown below.

```python
>>> response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth)
>>>
```

This made the API call and returned data back stored as response.

You can verify the type of response and see it's still a Requests object:

```python
>>> type(response)
<class 'requests.models.Response'>
>>>
```

##### Step 8

Let's explore key attributes of `response`.

First, let's validate the API call was successful.  If it was we should see an HTTP status code of "200" as the value for the `status_code`.

```python
>>> response.status_code
200
>>>
```

Now, let's see the actual response from the switch using the `text` attribute.

```python
>>> rsp = response.text
>>>
>>> type(rsp)
<type 'unicode'>
>>>
```

> Whenever, you see `unicode`, you can think of it as a different type of encoding for a string.

Now print out the `rsp` variable:

> Note: if you use the print statement, you actually can't tell it's a string (unicode). This is critical to understand because you may think it's a dictionary.


```python
>>> rsp
u'{\n\t"ins_api":\t{\n\t\t"type":\t"cli_show",\n\t\t"version":\t"1.2",\n\t\
"sid":\t"eoc",\n\t\t"outputs":\t{\n\t\t\t"output":\t{\n\t\t\t\t"input":\t"show
version",\n\t\t\t\t"msg":\t"Success",\n\t\t\t\t"code":\t"200",\n\t\t\t\t"body"
\t{\n\t\t\t\t\t"header_str":\t"Cisco Nexus Operating System (NX-OS)
Software\\nTAC support: http://www.cisco.com/tac\\nDocuments: http://www.cisco
com/en/US/products/ps9372/tsd_products_support_series_home.html\\nCopyright
c) 2002-2016, Cisco Systems, Inc. All rights reserved.\\nThe copyrights to
certain works contained herein are owned by\\nother third parties and are used
and distributed under license.\\nSome parts of this software are covered under
the GNU Public\\nLicense. A copy of the license is available at\\nhttp://www
gnu.org/licenses/gpl.html.\\n\\nNX-OSv is a demo version of the Nexus
Operating System\\n",\n\t\t\t\t\t"loader_ver_str":\t"N
A",\n\t\t\t\t\t"kickstart_ver_str":\t"7.3(1)D1(1) [build 7.3(1)D1(0.10)]",\n\
\t\t\t\t"sys_ver_str":\t"7.3(1)D1(1) [build 7.3(1)D1(0.10)]",\n\t\t\t\t\t
kick_file_name":\t"bootflash:///titanium-d1-kickstart.7.3.1.D1.0.10.bin",\n\t\
\t\t\t"kick_cmpl_time":\t" 1/11/2016 16:00:00",\n\t\t\t\t\t"kick_tmstmp":\t"02
22/2016 23:39:33",\n\t\t\t\t\t"isan_file_name":\t"bootflash:///titanium-d
.7.3.1.D1.0.10.bin",\n\t\t\t\t\t"isan_cmpl_time":\t" 1/11/2016 16:00:00",\n\t\
\t\t\t"isan_tmstmp":\t"02/23/2016 01:43:36",\n\t\t\t\t\t"chassis_id":\t"NX-OSv
Chassis",\n\t\t\t\t\t"module_id":\t"NX-OSv Supervisor Module",\n\t\t\t\t\t
cpu_name":\t"Intel(R) Xeon(R) CPU @ 2.50G",\n\t\t\t\t\t"memory":\t4002312,\n\
\t\t\t\t"mem_type":\t"kB",\n\t\t\t\t\t"proc_board_id":\t"TM29D1D533B",\n\t\t\
\t\t"host_name":\t"nxos-spine1",\n\t\t\t\t\t"bootflash_size":\t1582402,\n\t\t\
\t\t"kern_uptm_days":\t0,\n\t\t\t\t\t"kern_uptm_hrs":\t2,\n\t\t\t\t\t
kern_uptm_mins":\t17,\n\t\t\t\t\t"kern_uptm_secs":\t42,\n\t\t\t\t\t
manufacturer":\t"Cisco Systems, Inc."\n\t\t\t\t}\n\t\t\t}\n\t\t}\n\t}\n}'
>>>

```

Try also printing it with the `print` statement.

##### Step 9

Load the response **JSON string** and convert it to a dictionary:

```python
>>> data = json.loads(response.text)
>>>
```

##### Step 10

Perform a type check:

```python
>>> type(data)
<type 'dict'>
>>>
```

##### Step 11

Print the dictionary using `json.dumps`:

```python
>>> print(json.dumps(data, indent=4))
{
    "ins_api": {
        "outputs": {
            "output": {
                "msg": "Success",
                "input": "show version",
                "code": "200",
                "body": {
                    "kern_uptm_secs": 42,
                    "kick_file_name": "bootflash:///titanium-d1-kickstart.7.3.1.D1.0.10.bin",
                    "loader_ver_str": "N/A",
                    "module_id": "NX-OSv Supervisor Module",
                    "kick_tmstmp": "02/22/2016 23:39:33",
                    "isan_file_name": "bootflash:///titanium-d1.7.3.1.D1.0.10.bin",
                    "sys_ver_str": "7.3(1)D1(1) [build 7.3(1)D1(0.10)]",
                    "bootflash_size": 1582402,
                    "kickstart_ver_str": "7.3(1)D1(1) [build 7.3(1)D1(0.10)]",
                    "kick_cmpl_time": " 1/11/2016 16:00:00",
                    "chassis_id": "NX-OSv Chassis",
                    "proc_board_id": "TM29D1D533B",
                    "memory": 4002312,
                    "kern_uptm_mins": 17,
                    "cpu_name": "Intel(R) Xeon(R) CPU @ 2.50G",
                    "kern_uptm_hrs": 2,
                    "isan_tmstmp": "02/23/2016 01:43:36",
                    "manufacturer": "Cisco Systems, Inc.",
                    "header_str": "Cisco Nexus Operating System (NX-OS) Software\nTAC support: http://www.cisco.com/tac\nDocuments: http://www.cisco.com/en/US/products/ps9372/tsd_products_support_series_home.html\nCopyright (c) 2002-2016, Cisco Systems, Inc. All rights reserved.\nThe copyrights to certain works contained herein are owned by\nother third parties and are used and distributed under license.\nSome parts of this software are covered under the GNU Public\nLicense. A copy of the license is available at\nhttp://www.gnu.org/licenses/gpl.html.\n\nNX-OSv is a demo version of the Nexus Operating System\n",
                    "isan_cmpl_time": " 1/11/2016 16:00:00",
                    "host_name": "nxos-spine1",
                    "mem_type": "kB",
                    "kern_uptm_days": 0
                }
            }
        },
        "version": "1.2",
        "type": "cli_show",
        "sid": "eoc"
    }
}
>>>
```

##### Step 12

Print the name of the kickstart image.

```python
>>> print(data['ins_api']['outputs']['output']['body']['kickstart_ver_str'])
7.3(1)D1(1) [build 7.3(1)D1(0.10)]
>>>
```

##### Step 13

Extract everything from `body` in a variable first and then print the kickstart image again.

```python
>>> body = data['ins_api']['outputs']['output']['body']
>>>
>>> print(body.get('kickstart_ver_str'))
7.3(1)D1(1) [build 7.3(1)D1(0.10)]
>>>
```

Saving everything under `body` as it's own variable streamlines accessing data if you need to extract multiple key-value pairs.


##### Step 14

Use the command `show vlan brief` to get all vlans back from the device.

Print the JSON object using `json.dumps` out when complete.

```python
>>> payload = {
...     "ins_api": {
...         "version": "1.0",
...         "type": "cli_show",
...         "chunk": "0",
...         "sid": "1",
...         "input": "show vlan brief",
...         "output_format": "json"
...     }
... }
>>>
>>> response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth)
>>>
>>> data = json.loads(response.text)
>>>
>>> print(json.dumps(data, indent=4))
{
    "ins_api": {
        "outputs": {
            "output": {
                "msg": "Success",
                "input": "show vlan brief",
                "code": "200",
                "body": {
                    "TABLE_vlanbriefxbrief": {
                        "ROW_vlanbriefxbrief": {
                            "vlanshowbr-vlanid": 16777216,
                            "vlanshowbr-vlanid-utf": 1,
                            "vlanshowbr-vlanname": "default",
                            "vlanshowbr-vlanstate": "active",
                            "vlanshowbr-shutstate": "noshutdown"
                        }
                    }
                }
            }
        },
        "version": "1.2",
        "type": "cli_show",
        "sid": "eoc"
    }
}
>>>

```

##### Step 15

Save the VLAN object (everything under body) as a new variable called `vlans`.

```python
>>> vlans = data['ins_api']['outputs']['output']['body']
>>>
>>> print(json.dumps(vlans, indent=4))
{
    "TABLE_vlanbriefxbrief": {
        "ROW_vlanbriefxbrief": {
            "vlanshowbr-vlanid": 16777216,
            "vlanshowbr-vlanid-utf": 1,
            "vlanshowbr-vlanname": "default",
            "vlanshowbr-vlanstate": "active",
            "vlanshowbr-shutstate": "noshutdown"
        }
    }
}
>>>
```

##### Step 16

**If you see more than VLAN 1 on the switch, manually SSH into nxos-spine1 and remove them.**

Print out the vlan name for VLAN 1.

```python
>>> print(vlans['TABLE_vlanbriefxbrief']['ROW_vlanbriefxbrief']['vlanshowbr-vlanname'])
default
```

You should see that this is quite the nested dictionary and the work from Module 1 is extremely helpful for working with REST APIs returning JSON data.

##### Step 17

SSH back into the switch and add VLAN 10.

##### Step 18

Re-issue the same API call and re-create the `vlans` variable.

```python
>>> response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth)
>>>
>>> data = json.loads(response.text)
>>>
>>> vlans = data['ins_api']['outputs']['output']['body']
>>>
```

The same steps worked so far.

##### Step 19

Now print the name for VLAN 1.

```python
>>> print(vlans['TABLE_vlanbriefxbrief']['ROW_vlanbriefxbrief']['vlanshowbr-vlanname'])
### output omitted
```

Did it work?  

Print out `vlans` on it's own:

```python
>>> print(json.dumps(vlans, indent=4))
{
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
                "vlanshowbr-vlanid": 167772160,
                "vlanshowbr-vlanid-utf": 10,
                "vlanshowbr-vlanname": "VLAN0010",
                "vlanshowbr-vlanstate": "active",
                "vlanshowbr-shutstate": "noshutdown"
            }
        ]
    }
}
>>>
```

Notice anything different about this object compared to the previous one?  You should see that this is a list of dictionaries and the previous was just a dictionary.  This often happens when using native JSON encoding with NX-API when there is ONE object being returned or MULTIPLE.  One VLAN == dictionary.  More than one VLAN is a list.  Same is true any other object such as interfaces, neighbors, and so on.  We'll see how to mitigate this later on.

##### Step 20

Print out the VLAN name for VLAN 1 correctly since we now it's a list.

```python
>>> print(vlans['TABLE_vlanbriefxbrief']['ROW_vlanbriefxbrief'][0]['vlanshowbr-vlanname'])
default
```

Because of this, it's common to use the following block of code when using NX-API:

```
>>> if isinstance(<your-variable>, dict):
...     <your-variable> = [<your-variable>]
...
>>>
```

This does a type check on `your-variable` and if it's a dictionary, creates a list of one so you can always through it and not need two ways of access the same sets of data, e.g. when there is one VLAN, and when there is multiple VLANs, when there is one neighbor, and when there is multiple neighbors, etc.

##### Step 21

Print the name for VLAN 10:

```python
>>> print(vlans['TABLE_vlanbriefxbrief']['ROW_vlanbriefxbrief'][1]['vlanshowbr-vlanname'])
VLAN0010
```

Remember, when only ONE element exists (not just for VLANs), a dictionary is returned.  When MORE THAN ONE exists, a list is returned.  


### Task 2 - Gather Neighbors Script

In this task, you will write a script that queries two Cisco Nexus switches for their CDP neighbors.

The final data structure should be a dictionary.  Each key will be the hostname of the device.  The value will be a list of dictionaries - each of these dictionaries should have the following keys:  `neighbor_interface`, `neighbor`, and `local_interface`.

Before you query both devices and create the final script, you will start with testing on the Python shell.


##### Step 1

Run the command `show cdp neighbors` for `nxos-spine1`.  Store the **"JSON"** results in a variable called `data` and print it using `json.dumps`.

You'll notice this process becomes repetitive, so you'd want to store a few of these statements in a re-usable object like a function if you wanted to use this for production.

```python
>>>
>>> payload = {
...     "ins_api": {
...         "version": "1.0",
...         "type": "cli_show",
...         "chunk": "0",
...         "sid": "1",
...         "input": "show cdp neighbors",
...         "output_format": "json"
...     }
... }
>>>
>>> response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth)
>>>
>>> data = json.loads(response.text)
>>>
>>> print(json.dumps(data, indent=4))
{
    "ins_api": {
        "outputs": {
            "output": {
                "msg": "Success",
                "input": "show cdp neighbors",
                "code": "200",
                "body": {
                    "neigh_count": 5,
                    "TABLE_cdp_neighbor_brief_info": {
                        "ROW_cdp_neighbor_brief_info": [
                            {
                                "platform_id": "N7K-C7018",
                                "intf_id": "mgmt0",
                                "capability": [
                                    "router",
                                    "switch",
                                    "Supports-STP-Dispute"
                                ],
                                "ttl": 150,
                                "ifindex": 83886080,
                                "port_id": "mgmt0",
                                "device_id": "nxos-spine2(TB601325DFB)"
                            },
                            {
                                "platform_id": "N7K-C7018",
                                "intf_id": "Ethernet2/1",
                                "capability": [
                                    "router",
                                    "switch",
                                    "Supports-STP-Dispute"
                                ],
                                "ttl": 120,
                                "ifindex": 436731904,
                                "port_id": "Ethernet2/1",
                                "device_id": "nxos-spine2(TB601325DFB)"
                            },
                            {
                                "platform_id": "N7K-C7018",
                                "intf_id": "Ethernet2/2",
                                "capability": [
                                    "router",
                                    "switch",
                                    "Supports-STP-Dispute"
                                ],
                                "ttl": 120,
                                "ifindex": 436736000,
                                "port_id": "Ethernet2/2",
                                "device_id": "nxos-spine2(TB601325DFB)"
                            },
                            {
                                "platform_id": "N7K-C7018",
                                "intf_id": "Ethernet2/3",
                                "capability": [
                                    "router",
                                    "switch",
                                    "Supports-STP-Dispute"
                                ],
                                "ttl": 120,
                                "ifindex": 436740096,
                                "port_id": "Ethernet2/3",
                                "device_id": "nxos-spine2(TB601325DFB)"
                            },
                            {
                                "platform_id": "N7K-C7018",
                                "intf_id": "Ethernet2/4",
                                "capability": [
                                    "router",
                                    "switch",
                                    "Supports-STP-Dispute"
                                ],
                                "ttl": 120,
                                "ifindex": 436744192,
                                "port_id": "Ethernet2/4",
                                "device_id": "nxos-spine2(TB601325DFB)"
                            }
                        ]
                    }
                }
            }
        },
        "version": "1.2",
        "type": "cli_show",
        "sid": "eoc"
    }
}
>>>



```

We can see that **nxos-spine1** has 4+ neighbor entries pointing to the same device, **nxos-spine2**. That's because **nxos-spine1** and **nxos-spine2** are connected with 4 links.

We can also see the keys returned from the device do not match the keys we want for this lab.  We need to map `device_id` to `neighbor`, `port_id` to `neighbor_interface`, and `intf_id` to `local_interface`.

##### Step 2

Extract the neighbors object from `data` and save it as `cdp_neighbors`.

```python
>>> cdp_neighbors = data['ins_api']['outputs']['output']['body']['TABLE_cdp_neighbor_brief_info']['ROW_cdp_neighbor_brief_info']
>>>
```

There are two ways we can go about mapping the current dictionary keys to the desired keys.  We can use conditional if statements for each key or create a dictionary that maps them for us that provides a bit more scale.  Let's use the first option.

##### Step 3

As previously stated, Cisco returns a dictionary when there is a single element like when returning a single neighbor. We will introduce and use isinstance to check the data type of cdp_neighbors. If it is a dictionary, we'll make it a list of 1. If it's a list, it'll stay as-is.

>>> if isinstance(cdp_neighbors, dict):
...     cdp_neighbors = [cdp_neighbors]


##### Step 4

Now create a new list that will store the **new** dictionary with the new values.

This list will be called `neighbors_list`.

```python
>>> neighbors_list = []
>>>
```

##### Step 5

Loop through each neighbor in `cdp_neighbors` (from the Cisco Nexus switch).  For each iteration, you will create a dictionary that will be appended to `neighbors_list`.

While building this dictionary, you will also convert keys as described above.

```python
>>> for neighbor in cdp_neighbors:
...      neighbor = {
...              "neighbor_interface": neighbor["port_id"],
...              "local_interface": neighbor["intf_id"],
...              "neighbor": neighbor["device_id"]
...      }
...      neighbors_list.append(neighbor)
...
>>>
```

##### Step 6

Pretty print `neighbors_list`.

```python
>>> print(json.dumps(neighbors_list, indent=4))
[
    {
        "neighbor_interface": "mgmt0",
        "local_interface": "mgmt0",
        "neighbor": "nxos-spine2(TB601325DFB)"
    },
    {
        "neighbor_interface": "Ethernet2/1",
        "local_interface": "Ethernet2/1",
        "neighbor": "nxos-spine2(TB601325DFB)"
    },
    {
        "neighbor_interface": "Ethernet2/2",
        "local_interface": "Ethernet2/2",
        "neighbor": "nxos-spine2(TB601325DFB)"
    },
    {
        "neighbor_interface": "Ethernet2/3",
        "local_interface": "Ethernet2/3",
        "neighbor": "nxos-spine2(TB601325DFB)"
    },
    {
        "neighbor_interface": "Ethernet2/4",
        "local_interface": "Ethernet2/4",
        "neighbor": "nxos-spine2(TB601325DFB)"
    }
]
```

##### Challenge Exercise

Use the previous steps to build a script that outputs neighbors for **nxos-spine1** and **nxos-spine2** as such:


```
$ python cisco2.py
{
    "nxos-spine1": [
        {
            "neighbor_interface": "mgmt0",
            "local_interface": "mgmt0",
            "neighbor": "nxos-spine2(TB601325DFB)"
        },
        {
            "neighbor_interface": "Ethernet2/1",
            "local_interface": "Ethernet2/1",
            "neighbor": "nxos-spine2(TB601325DFB)"
        },
        {
            "neighbor_interface": "Ethernet2/2",
            "local_interface": "Ethernet2/2",
            "neighbor": "nxos-spine2(TB601325DFB)"
        },
        {
            "neighbor_interface": "Ethernet2/3",
            "local_interface": "Ethernet2/3",
            "neighbor": "nxos-spine2(TB601325DFB)"
        },
        {
            "neighbor_interface": "Ethernet2/4",
            "local_interface": "Ethernet2/4",
            "neighbor": "nxos-spine2(TB601325DFB)"
        }
    ],
    "nxos-spine2": [
        {
            "neighbor_interface": "mgmt0",
            "local_interface": "mgmt0",
            "neighbor": "nxos-spine1(TB6017D760B)"
        },
        {
            "neighbor_interface": "Ethernet2/1",
            "local_interface": "Ethernet2/1",
            "neighbor": "nxos-spine1(TB6017D760B)"
        },
        {
            "neighbor_interface": "Ethernet2/2",
            "local_interface": "Ethernet2/2",
            "neighbor": "nxos-spine1(TB6017D760B)"
        },
        {
            "neighbor_interface": "Ethernet2/3",
            "local_interface": "Ethernet2/3",
            "neighbor": "nxos-spine1(TB6017D760B)"
        },
        {
            "neighbor_interface": "Ethernet2/4",
            "local_interface": "Ethernet2/4",
            "neighbor": "nxos-spine1(TB6017D760B)"
        }
    ]
}

```


**Scroll for the solution**

```
.
























.
```



### Solution












Here is an example of a working script:

> There is no need to parameterize the command being sent or use functions, but this should give you a good idea how to start coding, and adding modularity, as you re-factor and optimize.  Even the script below could be modularized more.  Remember, this is just for learning purposes.

```python
import requests
import json
from requests.auth import HTTPBasicAuth


def nxapi_request(device, command):
    auth = HTTPBasicAuth('ntc', 'ntc123')
    headers = {
        'Content-Type': 'application/json'
    }

    url = 'http://{}/ins'.format(device)

    payload = {
        "ins_api": {
            "version": "1.0",
            "type": "cli_show",
            "chunk": "0",
            "sid": "1",
            "input": command,
            "output_format": "json"
        }
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth)
    return response

def get_nxos_neighbors(response):

    data = json.loads(response.text)

    device_neighbors = data['ins_api']['outputs']['output']['body']['TABLE_cdp_neighbor_brief_info']['ROW_cdp_neighbor_brief_info']
    if isinstance(device_neighbors, dict):
        device_neighbors = [device_neighbors]

    neighbors_list = []
    for neighbor in device_neighbors:
        neighbor = {
             "neighbor_interface": neighbor["port_id"],
             "local_interface": neighbor["intf_id"],
             "neighbor": neighbor["device_id"]
        }
        neighbors_list.append(neighbor)

    return neighbors_list

def main():

    neighbors = {}

    devices = ['nxos-spine1', 'nxos-spine2']
    command = 'show cdp neighbors'
    for dev in devices:
        response = nxapi_request(dev, command)
        neighbors[dev] = get_nxos_neighbors(response)

    print(json.dumps(neighbors, indent=4))

if __name__ == "__main__":
    main()



```


And there you have it.  A complete script to go out and collect neighbor information from a Cisco DC network.

You can even combine this with a Jinja2 template if you'd like to create a CSV report of all your neighbors!
