## Lab 24.1 - Arista eAPI

### Task 1 - Using Python requests with eapi


In this task, you will explore working with the Python requests module built to simplify working with HTTP-based APIs.

For this lab, you will use four Arista switches.

##### Step 1

Verify you can ping the Arista switches by name.  They have been pre-configured in your `/etc/hosts` file.

```
$ ping eos-spine1
$ ping eos-spine2
$ ping eos-leaf1
$ ping eos-leaf2
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

Navigate to the EOS Command Explorer.

Set the format to `json` and enter the command "show version" into the `Commands` box.

You should see the following Request object in the Request Viewer:

```python
{
    "jsonrpc": "2.0",
    "method": "runCmds",
    "params": {
        "format": "json",
        "timestamps": False,
        "cmds": [
            "show version"
        ],
        "version": 1
    },
    "id": "EapiExplorer-1"
}
```

This is the object we need to send to the device.  We'll use this in an upcoming step.


##### Step 6

Create four new variables while on the Python shell: `auth`, `headers`, `payload`, and `url`.

`auth` should be equal to `HTTPBasicAuth('ntc', 'ntc123')`

`headers` should be equal to `headers = { 'Content-Type': 'application/json' }`

`payload` should be equal to the Request object you copied above.

`url` should be url = `'http://eos-spine1/command-api'`  - this needs the `command-api` appended to the switch name or IP to work.

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
...     "jsonrpc": "2.0",
...     "method": "runCmds",
...     "params": {
...         "format": "json",
...         "timestamps": False,
...         "cmds": [
...             "show version"
...         ],
...         "version": 1
...     },
...     "id": "EapiExplorer-1"
... }
>>>
>>> url = 'http://eos-spine1/command-api'
>>>
```

At this point, we are ready to make a web API call to the Arista switch.  Remember the Arista switch only supports HTTP POSTs even though we are _getting_ data back. This is why it's a REST-like API.


##### Step 7

Make the API call to the device using the `post` method of `requests` as shown below.

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

Let's now explore key attributes of `response`.

First, validate the API call was successful.  If it was we should see an HTTP status code of "200" as the value for the `status_code`.

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

Remember the response comes back as a unicode string.  Now Print it out:

> Note: if you use the print statement, you actually can't tell it's a string. This is critical to understand because you may think it's a dictionary.


```python
>>> rsp
u'{"jsonrpc": "2.0", "result": [{"modelName": "vEOS", "internalVersion": "4.15.2F-2663444.4152F", "systemMacAddress": "2c:c2:60:28:54:dd", "serialNumber": "", "memTotal": 3895836, "bootupTimestamp": 1477365548.64, "memFree": 1615940, "version": "4.15.2F", "architecture": "i386", "internalBuildId": "0ebbad93-563f-4920-8ecb-731057802b9c", "hardwareRevision": ""}], "id": "EapiExplorer-1"}'
>>>
```


##### Step 9

Load the response JSON string and convert it to a dictionary:

```python
>>> data = json.loads(response.text)
>>>
```

Perform a type check:

```python
>>> type(data)
<type 'dict'>
>>>
```

##### Step 10

Print the dictionary using `json.dumps`:

```python
>>> print(json.dumps(data, indent=4))
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
            "memFree": 1615940,
            "modelName": "vEOS",
            "architecture": "i386",
            "internalBuildId": "0ebbad93-563f-4920-8ecb-731057802b9c",
            "hardwareRevision": ""
        }
    ],
    "id": "EapiExplorer-1"
}
>>>
```

##### Step 11

Print the system MAC address.

```python
>>> print(data['result'][0]['systemMacAddress'])
2c:c2:60:28:54:dd
>>>
```

##### Step 12

Extract everything from the actual output in a variable first and then print the system MAC address again.

```python
>>> result = data['result'][0]
>>>
>>> print(result.get('systemMacAddress'))
2c:c2:60:28:54:dd
>>>
```

Saving everything under `result` as it's own variable streamlines accessing data if you need to extract multiple key-value pairs.


##### Step 13

Use the command `show vlan brief` to get all vlans back from the device.

Print the JSON object using `json.dumps` out when complete.

```python
>>> payload = {
...     "jsonrpc": "2.0",
...     "method": "runCmds",
...     "params": {
...         "format": "json",
...         "timestamps": False,
...         "cmds": [
...             "show vlan brief"
...         ],
...         "version": 1
...     },
...     "id": "EapiExplorer-1"
... }
>>>
>>> response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth)
>>>
>>> data = json.loads(response.text)
>>>
>>> print(json.dumps(data, indent=4))
{
    "jsonrpc": "2.0",
    "result": [
        {
            "sourceDetail": "",
            "vlans": {
                "1": {
                    "status": "active",
                    "interfaces": {},
                    "dynamic": false,
                    "name": "default"
                },
                "10": {
                    "status": "active",
                    "interfaces": {},
                    "dynamic": false,
                    "name": "ntc"
                },
                "20": {
                    "status": "active",
                    "interfaces": {},
                    "dynamic": false,
                    "name": "testing"
                }
            }
        }
    ],
    "id": "EapiExplorer-1"
}
>>>

```

##### Step 14

Save the VLAN object as a new variable called `vlans`.

```python
>>> vlans = data['result'][0]
>>>
>>> print(json.dumps(vlans, indent=4))
{
    "sourceDetail": "",
    "vlans": {
        "1": {
            "status": "active",
            "interfaces": {},
            "dynamic": false,
            "name": "default"
        },
        "10": {
            "status": "active",
            "interfaces": {},
            "dynamic": false,
            "name": "ntc"
        },
        "20": {
            "status": "active",
            "interfaces": {},
            "dynamic": false,
            "name": "testing"
        }
    }
}
>>>
```

##### Step 15

Print out the vlan name for VLAN 1.

```python
>>> print(vlans['vlans']['1']['name'])
default
```

You should see that this is quite the nested dictionary and the work from Module 1 is extremely helpful for working with REST APIs returning JSON data.


### Task 2 - Gather Neighbors Script

In this task, you will write a script that queries two Arista EOS switches for their LLDP neighbors.

The final data structure should be a dictionary.  Each key will be the hostname of the device.  The value will be a list of dictionaries - each of these dictionaries should have the following keys:  `neighbor_interface`, `neighbor`, and `local_interface`.

Before you query both devices and create the final script, you will start with testing on the Python shell.


##### Step 1

Run the command `show lldp neighbors` for `eos-spine1`.  Store the **"JSON"** results in a variable called `data` and print it using `json.dumps`.

You'll notice this process becomes repetitive, so you'd want to store a few of these statements in a re-usable object like a function if you wanted to use this for production.

```python
>>>
>>> payload = {
...      "jsonrpc": "2.0",
...      "method": "runCmds",
...      "params": {
...          "format": "json",
...          "timestamps": False,
...          "cmds": [
...              "show lldp neighbors"
...          ],
...          "version": 1
...      },
...      "id": "EapiExplorer-1"
... }
>>>
>>> response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth)
>>>
>>> data = json.loads(response.text)
>>>
>>> print(json.dumps(data, indent=4))
{
    "jsonrpc": "2.0",
    "result": [
        {
            "tablesDrops": 0,
            "tablesAgeOuts": 0,
            "tablesDeletes": 1,
            "tablesInserts": 13,
            "lldpNeighbors": [
                {
                    "neighborDevice": "eos-spine2.ntc.com",
                    "neighborPort": "Ethernet1",
                    "port": "Ethernet1",
                    "ttl": 120
                },
                {
                    "neighborDevice": "eos-spine2.ntc.com",
                    "neighborPort": "Ethernet2",
                    "port": "Ethernet2",
                    "ttl": 120
                },
                {
                    "neighborDevice": "eos-spine2.ntc.com",
                    "neighborPort": "Ethernet3",
                    "port": "Ethernet3",
                    "ttl": 120
                },
                {
                    "neighborDevice": "eos-spine2.ntc.com",
                    "neighborPort": "Ethernet4",
                    "port": "Ethernet4",
                    "ttl": 120
                },
                {
                    "neighborDevice": "eos-leaf1.ntc.com",
                    "neighborPort": "Ethernet1",
                    "port": "Ethernet5",
                    "ttl": 120
                },
                {
                    "neighborDevice": "csr1.ntc.com",
                    "neighborPort": "Gi1",
                    "port": "Management1",
                    "ttl": 120
                },
                {
                    "neighborDevice": "csr3.ntc.com",
                    "neighborPort": "Gi1",
                    "port": "Management1",
                    "ttl": 120
                },
                {
                    "neighborDevice": "vmx2",
                    "neighborPort": "fxp0",
                    "port": "Management1",
                    "ttl": 120
                },
                {
                    "neighborDevice": "testing.ntc.com",
                    "neighborPort": "Gi1",
                    "port": "Management1",
                    "ttl": 120
                },
                {
                    "neighborDevice": "vmx1",
                    "neighborPort": "fxp0",
                    "port": "Management1",
                    "ttl": 120
                },
                {
                    "neighborDevice": "eos-spine2.ntc.com",
                    "neighborPort": "Management1",
                    "port": "Management1",
                    "ttl": 120
                },
                {
                    "neighborDevice": "eos-leaf1.ntc.com",
                    "neighborPort": "Management1",
                    "port": "Management1",
                    "ttl": 120
                }
            ],
            "tablesLastChangeTime": 1488113813.6645398
        }
    ],
    "id": "EapiExplorer-1"
}
>>>
```

We can see that **eos-spine1** has 4+ neighbor entries pointing to the same device, **eos-spine2**. That's because **eos-spine1** and **eos-spine2** are connected with 4 links.

We can also see the keys returned from the device do not match the keys we want for this lab.  We need to map `neighborDevice` to `neighbor`, `neighborPort` to `neighbor_interface`, and `port` to `local_interface`.

##### Step 2

Extract the neighbors object from `data` and save it as `lldp_neighbors`.

```python
>>> lldp_neighbors = data['result'][0]['lldpNeighbors']
>>>
```

There are two ways we can go about mapping the current dictionary keys to the desired keys.  We can use conditional if statements for each key or create a dictionary that maps them for us that provides a bit more scale.  Let's use the first option.

##### Step 3

Now create a new list that will store the **new** dictionary with the new values.

This list will be called `neighbors_list`.

```python
>>> neighbors_list = []
```

##### Step 4

Loop through each neighbor in `lldp_neighbors`.  For each iteration, you will create a dictionary that will be appended to `neighbors_list`.

While building this dictionary, you will also convert keys as described above.

```python
>>> for neighbor in lldp_neighbors:
...       neighbor = {
...               "neighbor_interface": neighbor["neighborPort"],
...               "local_interface": neighbor["port"],
...               "neighbor": neighbor["neighborDevice"]
...       }
...      neighbors_list.append(neighbor)
...
>>>
```

##### Step 5

Pretty print neighbors_list.

```python
>>> print(json.dumps(neighbors_list, indent=4))
[
    {
        "neighbor_interface": "Ethernet1",
        "local_interface": "Ethernet1",
        "neighbor": "eos-spine2.ntc.com"
    },
    {
        "neighbor_interface": "Ethernet2",
        "local_interface": "Ethernet2",
        "neighbor": "eos-spine2.ntc.com"
    },
    {
        "neighbor_interface": "Ethernet3",
        "local_interface": "Ethernet3",
        "neighbor": "eos-spine2.ntc.com"
    },
    {
        "neighbor_interface": "Ethernet4",
        "local_interface": "Ethernet4",
        "neighbor": "eos-spine2.ntc.com"
    },
    {
        "neighbor_interface": "Ethernet1",
        "local_interface": "Ethernet5",
        "neighbor": "eos-leaf1.ntc.com"
    },
    {
        "neighbor_interface": "Gi1",
        "local_interface": "Management1",
        "neighbor": "csr1.ntc.com"
    },
    {
        "neighbor_interface": "Gi1",
        "local_interface": "Management1",
        "neighbor": "csr3.ntc.com"
    },
    {
        "neighbor_interface": "fxp0",
        "local_interface": "Management1",
        "neighbor": "vmx2"
    },
    {
        "neighbor_interface": "Gi1",
        "local_interface": "Management1",
        "neighbor": "testing.ntc.com"
    },
    {
        "neighbor_interface": "fxp0",
        "local_interface": "Management1",
        "neighbor": "vmx1"
    },
    {
        "neighbor_interface": "Management1",
        "local_interface": "Management1",
        "neighbor": "eos-spine2.ntc.com"
    },
    {
        "neighbor_interface": "Management1",
        "local_interface": "Management1",
        "neighbor": "eos-leaf1.ntc.com"
    }
]
```

##### Challenge Exercise

Use the previous steps to build a script that outputs neighbors for eos-spine1 and eos-spine2 as such:


```
$ python arista2.py
{
    "eos-spine1": [
        {
            "neighbor_interface": "Ethernet1",
            "local_interface": "Ethernet1",
            "neighbor": "eos-spine2.ntc.com"
        },
        {
            "neighbor_interface": "Ethernet2",
            "local_interface": "Ethernet2",
            "neighbor": "eos-spine2.ntc.com"
        },
        {
            "neighbor_interface": "Ethernet3",
            "local_interface": "Ethernet3",
            "neighbor": "eos-spine2.ntc.com"
        },
        {
            "neighbor_interface": "Ethernet4",
            "local_interface": "Ethernet4",
            "neighbor": "eos-spine2.ntc.com"
        },
        {
            "neighbor_interface": "Ethernet1",
            "local_interface": "Ethernet5",
            "neighbor": "eos-leaf1.ntc.com"
        },
        {
            "neighbor_interface": "Gi1",
            "local_interface": "Management1",
            "neighbor": "csr1.ntc.com"
        },
        {
            "neighbor_interface": "Gi1",
            "local_interface": "Management1",
            "neighbor": "csr3.ntc.com"
        },
        {
            "neighbor_interface": "fxp0",
            "local_interface": "Management1",
            "neighbor": "vmx2"
        },
        {
            "neighbor_interface": "Gi1",
            "local_interface": "Management1",
            "neighbor": "testing.ntc.com"
        },
        {
            "neighbor_interface": "fxp0",
            "local_interface": "Management1",
            "neighbor": "vmx1"
        },
        {
            "neighbor_interface": "Management1",
            "local_interface": "Management1",
            "neighbor": "eos-spine2.ntc.com"
        },
        {
            "neighbor_interface": "Management1",
            "local_interface": "Management1",
            "neighbor": "eos-leaf1.ntc.com"
        }
    ],
    "eos-spine2": [
        {
            "neighbor_interface": "Ethernet1",
            "local_interface": "Ethernet1",
            "neighbor": "eos-spine1.ntc.com"
        },
        {
            "neighbor_interface": "Ethernet2",
            "local_interface": "Ethernet2",
            "neighbor": "eos-spine1.ntc.com"
        },
        {
            "neighbor_interface": "Ethernet3",
            "local_interface": "Ethernet3",
            "neighbor": "eos-spine1.ntc.com"
        },
        {
            "neighbor_interface": "Ethernet4",
            "local_interface": "Ethernet4",
            "neighbor": "eos-spine1.ntc.com"
        },
        {
            "neighbor_interface": "Ethernet2",
            "local_interface": "Ethernet5",
            "neighbor": "eos-leaf1.ntc.com"
        },
        {
            "neighbor_interface": "fxp0",
            "local_interface": "Management1",
            "neighbor": "vmx1"
        },
        {
            "neighbor_interface": "fxp0",
            "local_interface": "Management1",
            "neighbor": "vmx2"
        },
        {
            "neighbor_interface": "Gi1",
            "local_interface": "Management1",
            "neighbor": "csr1.ntc.com"
        },
        {
            "neighbor_interface": "Gi1",
            "local_interface": "Management1",
            "neighbor": "csr3.ntc.com"
        },
        {
            "neighbor_interface": "Gi1",
            "local_interface": "Management1",
            "neighbor": "testing.ntc.com"
        },
        {
            "neighbor_interface": "Management1",
            "local_interface": "Management1",
            "neighbor": "eos-spine1.ntc.com"
        },
        {
            "neighbor_interface": "Management1",
            "local_interface": "Management1",
            "neighbor": "eos-leaf1.ntc.com"
        }
    ]
}
```


Stop scrolling if you don't want to see the solution.

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


def eapi_request(device, commands):
    auth = HTTPBasicAuth('ntc', 'ntc123')
    headers = {
        'Content-Type': 'application/json'
    }

    url = 'http://{}/command-api'.format(device)
    payload = {
        "jsonrpc": "2.0",
        "method": "runCmds",
        "params": {
            "format": "json",
            "timestamps": False,
            "cmds": commands,
            "version": 1
        },
        "id": "EapiExplorer-1"
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth)
    return response

def get_eos_neighbors(response):

    data = json.loads(response.text)

    device_neighbors = data['result'][0]['lldpNeighbors']

    neighbors_list = []
    for neighbor in device_neighbors:
        neighbor = {
             "neighbor_interface": neighbor["neighborPort"],
             "local_interface": neighbor["port"],
             "neighbor": neighbor["neighborDevice"]
        }
        neighbors_list.append(neighbor)

    return neighbors_list

def main():

    neighbors = {}

    devices = ['eos-spine1', 'eos-spine2']
    commands = ['show lldp neighbors']
    for dev in devices:
        response = eapi_request(dev, commands)
        neighbors[dev] = get_eos_neighbors(response)

    print(json.dumps(neighbors, indent=4))

if __name__ == "__main__":
    main()
```


And there you have it.  A complete script to go out and collect neighbor information from a Arista DC network.
