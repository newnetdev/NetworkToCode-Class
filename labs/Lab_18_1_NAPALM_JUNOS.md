## Lab 18.1 - NAPALM

### Task 1 - Basic Configuration Merge with NAPALM

In this task, you will explore working with the NAPALM Python library to perform a configuration **merge** on an JUNOS vMX device.

##### Step 1

Create a new file called `snmp.conf` in your home directory and open the file in Sublime Text or the editor of your choice.

##### Step 2

Take the config snippet below and save it in the file just created (`snmp.conf`). These commands will be used to directly configure the switches. 

```
set snmp community networktocode authorization read-only
set snmp community public authorization read-only
set snmp community private authorization read-write
set snmp community supersecret authorization read-write
set snmp location SYDNEY
set snmp contact JOHN_SMITH

```


##### Step 3

Enter the Python shell **from your home directory**.

```python
ntc@ntc:~$ python

Python 2.7.6 (default, Jun 22 2015, 17:58:13) 
[GCC 4.8.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.

>>> 
>>> 
```

##### Step 4

Load the correct NAPALM driver.  Since we're using the Arista switch in this lab, load the **eos** driver.

```python
>>> from napalm import get_network_driver
>>>
>>> driver = get_network_driver('junos')
>>> 
```

##### Step 5

Create an **junos** device object for **vmx7** using the previously loaded driver.  Use the variable name `device`.

```python
>>> device = driver('vmx7', 'ntc', 'ntc123')
>>> 
```

##### Step 6

Use `help` on `device`.  You will be able to see all of supported properties and methods of this object.

```python
>>> help(device)

```

```
Help on JunOSDriver in module napalm_junos.junos object:

class JunOSDriver(napalm_base.base.NetworkDriver)
 |  JunOSDriver class - inherits NetworkDriver from napalm_base.
 |  
 |  Method resolution order:
 |      JunOSDriver
 |      napalm_base.base.NetworkDriver
 |      __builtin__.object
 |  
 |  Methods defined here:
 |  
 |  __init__(self, hostname, username, password, timeout=60, optional_args=None)
 |      Initialise JunOS driver.
 |      
 |      Optional args:
 |          * config_lock (True/False): lock configuration DB after the connection is established.
 |          * port (int): custom port
 |          * key_file (string): SSH key file path
 |          * keepalive (int): Keepalive interval
 |          * ignore_warning (boolean): not generate warning exceptions
 |  
 |  cli(self, commands)
 |      Execute raw CLI commands and returns their output.
 |  
 |  close(self)

```

Just like you've seen with built-in data types, you can use `help()` and `dir()` on 3rd party object types too.

There are two primary methods of the device class you'd work with to apply configurations.  They are `load_merge_candidate` and `load_replace_candidate`.

These are used to load a partial configuration (and merge with the device) and load a *full* configuration that will replace the full running configuration, respectively.  You'll see these if you look at the full help documentation (the above is just a snippet from the help output).


For this lab, we are  using `load_merge_candidate`.

> Note: we will use `load_replace_candidate` indirectly in an upcoming Ansible lab.

##### Step 7

Open a connection to the device.  This is done using the `open()` method.

```python
>>> device.open()
>>> 
```

##### Step 8

Load the configuration you created in Step 2 onto the device.

This is done by using the `load_merge_candiate` method of the device object.

```python
>>> device.load_merge_candidate(filename='snmp.conf')
>>> 
```

As soon as you hit enter in this step, NAPALM is loading this configuration onto the device, but NOT committing it to the running configuration.  **How** this happens is different for every OS.  For JUNOS, NAPALM depends on the candidate configuration feature, prior to committing the configuration.

At this step you can verify the changes manually by going to the device to view the preview of configs to be pushed too. As already stated, in the NAPALM implementation for JUNOS, the candidate configuration database is being used.

```
ntc@vmx7> configure    
Entering configuration mode
Users currently editing the configuration:
  ntc (pid 8788) on since 2017-10-16 22:42:11 UTC, idle 00:01:53
      exclusive
The configuration has been changed but not committed

[edit]

```

You can then generate a diff on the EOS CLI, if desired, using the command:


```
ntc@vmx7# show | compare 
[edit snmp]
+  location SYDNEY;
+  contact JOHN_SMITH;
[edit snmp]
    community networktocode { ... }
+   community private {
+       authorization read-write;
+   }
+   community supersecret {
+       authorization read-write;
+   }

[edit]

```



##### Step 9

Commit the config to the device while back at the Python shell. 

This is when the configuration will be activated and _committed_ to the running configuration.

```python
>>> device.commit_config()
>>> 
```

> If you wanted to discard this change rather than commit, alternatively you **could** have ran the following:

```python
>>> device.discard_config()
>>> 
```


##### Step 10


To rollback, you use the rollback method.

Feel free to view the config on the CLI of the device before and after you issue the next command.

```python
>>> device.rollback()
>>> 
```

##### Step 11

We now want to see how to view diffs directly from Python and not using the JUNOS CLI.

Re-load the configuration on the device.


```python
>>> device.load_merge_candidate(filename='snmp.conf')
>>> 
```

After it's loaded, view the diffs with the `compare_config` method.

```python
>>> diffs = device.compare_config()
>>> 
>>> print(diffs)
[edit snmp]
+  location SYDNEY;
+  contact JOHN_SMITH;
[edit snmp]
    community networktocode { ... }
+   community private {
+       authorization read-write;
+   }
+   community supersecret {
+       authorization read-write;
+   }
>>> 

```

Now NAPALM is generating the diffs using the same CLI command you just tried in Step 8.

##### Step 12

Load the new SNMP configuration on the two other JUNOS vMX routers.  

Use a for loop to build the proper NAPALM device object as well as load and commit the configuration for each JUNOS switch.


### Task 2 - Declarative Network Configuration with NAPALM for a Configuration Section

In this task, you will use NAPALM to declaratively configure BGP on an Arista switch.  Normally, NAPALM is known for declaratively managing _full_ configuration files, but we'll show you can still use NAPALM to declaratively manage a single section.

> Note: this is 100% dependent on the OS being used. 

##### Step 1

Use SSH to manully log to eos-spine1 switch.

Load the following BGP configuration onto the device:

```bash
eos-spine1#show run section bgp
router bgp 65512
   neighbor 10.0.0.0 remote-as 65500
   neighbor 10.0.0.0 maximum-routes 12000
   neighbor 10.0.0.1 remote-as 65512
   neighbor 10.0.0.1 maximum-routes 12000
   network 20.20.20.0/24
```

##### Step 2

Create a new file called `bgp.conf` in your home directory and open the file in Sublime Text or the text editor of your choice.

##### Step 3

We now want to declaratively manage just BGP.  This means we DO NOT CARE what's there.  What's in our new `bgp.conf` should be the only BGP config that ends up on the device.

Take the config below and save it as `bgp.conf`.

```
no router bgp 65512
router bgp 65512
   neighbor 10.0.0.2 remote-as 65500
   neighbor 10.0.0.2 maximum-routes 12000
   neighbor 10.0.0.1 remote-as 65512
   neighbor 10.0.0.1 maximum-routes 12000
   neighbor 10.0.0.10 remote-as 65512
   network 100.0.100.0/24
```

> Take note of the first line `no router bgp 65512`.  Watch what's going to happen next.

##### Step 4

Enter the Python shell from your home directory, import the *eos* napalm driver and create an *eos* device object for *eos-spine1* just like you already did on Task 1.

```python
ntc@ntc:~$ python

Python 2.7.6 (default, Jun 22 2015, 17:58:13) 
[GCC 4.8.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.

>>> from napalm import get_network_driver
>>> driver = get_network_driver('eos')
>>> device = driver('eos-spine1', 'ntc', 'ntc123')
>>>
```

##### Step 5

Open a connection to the device.

```python
>>> device.open()
>>> 
```

##### Step 6

Load the configuration you created in Step 3 onto the device.

All of these steps are no different than Task 1.

```python
>>> device.load_merge_candidate(filename='bgp.conf')
>>> 
```

##### Step 7

Use the `compare_config` method to show the configuration diffs.

This is where you get to see the real power of EOS and NAPALM working together.

```python
>>> print device.compare_config()
@@ -44,11 +44,13 @@
 ip routing vrf MANAGEMENT
 !
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
 management api http-commands
    protocol http
```

Notice how the commands aren't just getting pushed.  BGP is NOT getting un-configured and re-configured.  Simply, the commands required to get BGP into its final are the only commands actually being used EOS.

##### Step 8

Finally, commit the config to the device.

```python
>>> device.commit_config()
>>> 
```

Feel free to log back to the device and verify the configuration has been applied correctly.

### Task 3 - NAPALM Getters

In this task you will make practice with NAPALM getters on several platforms.

##### Step 1

Enter into the Python shell from your home directory.

```python
ntc@ntc:~$ python
Python 2.7.12 (default, Nov 19 2016, 06:48:10)
[GCC 5.4.0 20160609] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

##### Step 2

Import `get_network_driver` from `napalm` and load the drivers for IOS, NXOS, Junos and EOS.

```python
>>> from napalm import get_network_driver
>>>
>>> ios_driver = get_network_driver('ios')
>>> nxos_driver = get_network_driver('nxos')
>>> eos_driver = get_network_driver('eos')
>>>
```

##### Step 3

Create 4 devices, one for each NAPALM driver you have loaded.

```python
>>> ios_device = ios_driver ('csr1', 'ntc', 'ntc123')
>>> nxos_device = nxos_driver ('nxos-spine1', 'ntc', 'ntc123')
>>> eos_device = eos_driver ('eos-spine1', 'ntc', 'ntc123')
>>>
```

##### Step 4

Open a NAPALM session for all the devices you have just created.

```python
>>> ios_device.open()
>>> nxos_device.open()
>>> eos_device.open()
>>>
```

##### Step 5

Import `json` library and pretty print facts for all devices.

```python
>>> import json
>>>
>>> print json.dumps(ios_device.get_facts(), indent=4)
{
    "os_version": "CSR1000V Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.3.1, RELEASE SOFTWARE (fc3)",
    "uptime": 56880,
    "interface_list": [
        "GigabitEthernet1",
        "GigabitEthernet2",
        "GigabitEthernet3",
        "GigabitEthernet4",
        "Loopback100",
        "Loopback200"
    ],
    "vendor": "Cisco",
    "serial_number": "9KXI0D7TVFI",
    "model": "CSR1000V",
    "hostname": "csr1",
    "fqdn": "csr1.ntc.com"
}
>>>
```


```python
>>> print json.dumps(nxos_device.get_facts(), indent=4)
{
    "uptime": 57153,
    "vendor": "Cisco",
    "hostname": "nxos-spine1",
    "fqdn": "nxos-spine1",
    "os_version": "7.3(1)D1(1) [build 7.3(1)D1(0.10)]",
    "serial_number": "TM602622D6B",
    "model": "NX-OSv Chassis",
    "interface_list": [
        "mgmt0",
        "Ethernet2/1",
        "Ethernet2/2",
        "Ethernet2/3",
        "Ethernet2/4",
        "Ethernet2/5",
        "Ethernet2/6",
        "Ethernet2/7",
        "Ethernet2/8",
        "Ethernet2/9",
        "Ethernet2/10",
        "Ethernet2/11",
        "Ethernet2/12",
        "Ethernet2/13",
        "Ethernet2/14",
        "Ethernet2/15",
        "Ethernet2/16",
        "Ethernet2/17",
        "Ethernet2/18",
        "Ethernet2/19",
        "Ethernet2/20",
        "Ethernet2/21",
        "Ethernet2/22",
        "Ethernet2/23",
        "Ethernet2/24",
        "Ethernet2/25",
        "Ethernet2/26",
        "Ethernet2/27",
        "Ethernet2/28",
        "Ethernet2/29",
        "Ethernet2/30",
        "Ethernet2/31",
        "Ethernet2/32",
        "Ethernet2/33",
        "Ethernet2/34",
        "Ethernet2/35",
        "Ethernet2/36",
        "Ethernet2/37",
        "Ethernet2/38",
        "Ethernet2/39",
        "Ethernet2/40",
        "Ethernet2/41",
        "Ethernet2/42",
        "Ethernet2/43",
        "Ethernet2/44",
        "Ethernet2/45",
        "Ethernet2/46",
        "Ethernet2/47",
        "Ethernet2/48",
        "Ethernet3/1",
        "Ethernet3/2",
        "Ethernet3/3",
        "Ethernet3/4",
        "Ethernet3/5",
        "Ethernet3/6",
        "Ethernet3/7",
        "Ethernet3/8",
        "Ethernet3/9",
        "Ethernet3/10",
        "Ethernet3/11",
        "Ethernet3/12",
        "Ethernet3/13",
        "Ethernet3/14",
        "Ethernet3/15",
        "Ethernet3/16",
        "Ethernet3/17",
        "Ethernet3/18",
        "Ethernet3/19",
        "Ethernet3/20",
        "Ethernet3/21",
        "Ethernet3/22",
        "Ethernet3/23",
        "Ethernet3/24",
        "Ethernet3/25",
        "Ethernet3/26",
        "Ethernet3/27",
        "Ethernet3/28",
        "Ethernet3/29",
        "Ethernet3/30",
        "Ethernet3/31",
        "Ethernet3/32",
        "Ethernet3/33",
        "Ethernet3/34",
        "Ethernet3/35",
        "Ethernet3/36",
        "Ethernet3/37",
        "Ethernet3/38",
        "Ethernet3/39",
        "Ethernet3/40",
        "Ethernet3/41",
        "Ethernet3/42",
        "Ethernet3/43",
        "Ethernet3/44",
        "Ethernet3/45",
        "Ethernet3/46",
        "Ethernet3/47",
        "Ethernet3/48",
        "Ethernet4/1",
        "Ethernet4/2",
        "Ethernet4/3",
        "Ethernet4/4",
        "Ethernet4/5",
        "Ethernet4/6",
        "Ethernet4/7",
        "Ethernet4/8",
        "Ethernet4/9",
        "Ethernet4/10",
        "Ethernet4/11",
        "Ethernet4/12",
        "Ethernet4/13",
        "Ethernet4/14",
        "Ethernet4/15",
        "Ethernet4/16",
        "Ethernet4/17",
        "Ethernet4/18",
        "Ethernet4/19",
        "Ethernet4/20",
        "Ethernet4/21",
        "Ethernet4/22",
        "Ethernet4/23",
        "Ethernet4/24",
        "Ethernet4/25",
        "Ethernet4/26",
        "Ethernet4/27",
        "Ethernet4/28",
        "Ethernet4/29",
        "Ethernet4/30",
        "Ethernet4/31",
        "Ethernet4/32",
        "Ethernet4/33",
        "Ethernet4/34",
        "Ethernet4/35",
        "Ethernet4/36",
        "Ethernet4/37",
        "Ethernet4/38",
        "Ethernet4/39",
        "Ethernet4/40",
        "Ethernet4/41",
        "Ethernet4/42",
        "Ethernet4/43",
        "Ethernet4/44",
        "Ethernet4/45",
        "Ethernet4/46",
        "Ethernet4/47",
        "Ethernet4/48",
        "Vlan1"
    ]
}
>>>
```


```python
>>> print json.dumps(eos_device.get_facts(), indent=4)
{
    "os_version": "4.15.2F-2663444.4152F",
    "uptime": 57154,
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

##### Step 6

Print all interfaces for all devices.

```python
>>> print json.dumps(ios_device.get_interfaces(), indent=4)
{
    "GigabitEthernet4": {
        "is_enabled": false,
        "description": "N/A",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:5B:75:4F",
        "speed": 1000
    },
    "GigabitEthernet1": {
        "is_enabled": true,
        "description": "N/A",
        "last_flapped": -1.0,
        "is_up": true,
        "mac_address": "2C:C2:60:09:D3:A8",
        "speed": 1000
    },
    "GigabitEthernet2": {
        "is_enabled": false,
        "description": "N/A",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:49:C8:53",
        "speed": 1000
    },
    "GigabitEthernet3": {
        "is_enabled": false,
        "description": "N/A",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:1B:84:EF",
        "speed": 1000
    },
    "Loopback100": {
        "is_enabled": true,
        "description": "N/A",
        "last_flapped": -1.0,
        "is_up": true,
        "mac_address": "N/A",
        "speed": 8000
    },
    "Loopback200": {
        "is_enabled": true,
        "description": "testt",
        "last_flapped": -1.0,
        "is_up": true,
        "mac_address": "N/A",
        "speed": 8000
    }
}
>>> 
```


```python
>>> print json.dumps(nxos_device.get_interfaces(), indent=4)
{
    "Ethernet3/21": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/20": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/23": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/22": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/25": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/24": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/27": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/26": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/29": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/28": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet2/39": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/38": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/31": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/30": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/33": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/32": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/35": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/34": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/37": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/36": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/48": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/44": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/45": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/46": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/47": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/40": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/41": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/42": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/43": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Vlan1": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "",
        "speed": 0
    },
    "Ethernet3/47": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/46": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/45": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/44": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/43": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/42": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/41": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/40": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/48": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/42": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/43": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/40": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/41": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/46": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/47": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/44": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/45": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/48": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet2/8": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/1": {
        "is_enabled": true,
        "description": "",
        "last_flapped": 1488279568.424748,
        "is_up": true,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet4/28": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/29": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/20": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/21": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/22": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/23": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/24": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/25": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/26": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/27": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/18": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/19": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/10": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/11": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/12": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/13": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/14": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/15": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/16": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/17": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/5": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/4": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/7": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/6": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/1": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/3": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/2": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/9": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/8": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/39": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/38": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/33": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/32": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/31": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/30": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/37": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/36": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/35": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/34": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/6": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/7": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/4": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/5": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/2": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/3": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet2/9": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet3/1": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet2/7": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/6": {
        "is_enabled": true,
        "description": "",
        "last_flapped": 1488279568.424975,
        "is_up": true,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/5": {
        "is_enabled": true,
        "description": "",
        "last_flapped": 1488279568.424934,
        "is_up": true,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/4": {
        "is_enabled": true,
        "description": "",
        "last_flapped": 1488279568.424893,
        "is_up": true,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/3": {
        "is_enabled": true,
        "description": "",
        "last_flapped": 1488279568.42485,
        "is_up": true,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/2": {
        "is_enabled": true,
        "description": "",
        "last_flapped": 1488279568.424805,
        "is_up": true,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet3/8": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/9": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "mgmt0": {
        "is_enabled": true,
        "description": "",
        "last_flapped": -1.0,
        "is_up": true,
        "mac_address": "2C:C2:60:26:22:D6",
        "speed": 1000
    },
    "Ethernet2/13": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/12": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/11": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/10": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/17": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/16": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/15": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/14": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/19": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/18": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet3/36": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/37": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/34": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/35": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/32": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/33": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/30": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/31": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/38": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet3/39": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet2/28": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/29": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/26": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/27": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/24": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/25": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/22": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/23": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/20": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet2/21": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "2C:C2:60:4F:FE:B2",
        "speed": 1000
    },
    "Ethernet4/11": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/10": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/13": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/12": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/15": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/14": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/17": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/16": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/19": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    },
    "Ethernet4/18": {
        "is_enabled": false,
        "description": "",
        "last_flapped": -1.0,
        "is_up": false,
        "mac_address": "00:0C:29:D1:D5:6B",
        "speed": 1000
    }
}
>>> 
>>> 
```

```python
>>> 
>>> print json.dumps(eos_device.get_interfaces(), indent=4)
{
    "Management1": {
        "is_enabled": true,
        "description": "",
        "last_flapped": 1488222407.1041465,
        "is_up": true,
        "mac_address": "2C:C2:60:B3:DE:84",
        "speed": 1000
    },
    "Ethernet2": {
        "is_enabled": true,
        "description": "",
        "last_flapped": 1488222411.414313,
        "is_up": true,
        "mac_address": "2C:C2:60:43:F7:37",
        "speed": 0
    },
    "Ethernet3": {
        "is_enabled": true,
        "description": "",
        "last_flapped": 1488222411.4145062,
        "is_up": true,
        "mac_address": "2C:C2:60:24:D1:3D",
        "speed": 0
    },
    "Ethernet1": {
        "is_enabled": true,
        "description": "",
        "last_flapped": 1488222411.4140322,
        "is_up": true,
        "mac_address": "2C:C2:60:49:18:51",
        "speed": 0
    },
    "Ethernet6": {
        "is_enabled": true,
        "description": "",
        "last_flapped": 1488222411.4151587,
        "is_up": true,
        "mac_address": "2C:C2:60:47:5F:56",
        "speed": 0
    },
    "Ethernet7": {
        "is_enabled": true,
        "description": "",
        "last_flapped": 1488222411.4153645,
        "is_up": true,
        "mac_address": "2C:C2:60:5F:55:B3",
        "speed": 0
    },
    "Ethernet4": {
        "is_enabled": true,
        "description": "",
        "last_flapped": 1488222411.41475,
        "is_up": true,
        "mac_address": "2C:C2:60:05:B0:EA",
        "speed": 0
    },
    "Ethernet5": {
        "is_enabled": true,
        "description": "",
        "last_flapped": 1488222411.4149394,
        "is_up": true,
        "mac_address": "2C:C2:60:72:A4:5D",
        "speed": 0
    }
}
>>>
```

As you can see, outputs structure is the same regardless of the device platform.
