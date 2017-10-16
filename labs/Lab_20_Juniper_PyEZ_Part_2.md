## Lab 20 - Junos XML API

### Task 1 - Getting Started with Junos PyEZ

In this task, you will learn how to work with the Juniper PyEZ library while using the Python dynamic interpreter.

For this lab, you will use Juniper vMX devices.

##### Step 1

Verify you can ping the devices by name.  They have been pre-configured in your `/etc/hosts` file.

```
$ ping vmx1
$ ping vmx2
$ ping vmx3
```

##### Step 2

Enter the Python shell.

```python
$ python

Python 2.7.6 (default, Jun 22 2015, 17:58:13) 
[GCC 4.8.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.

>>> 
```

##### Step 3

Import the Juniper `Device` object from `jnpr.junos.device` and rename it to `JUNIPER`.

```python
>>> from jnpr.junos.device import Device as JUNIPER
>>> 
```

##### Step 4

Use `help` on `JUNIPER`.  You will be able to see what properties and methods this object supports.

```python
>>> help(JUNIPER)
```

```
Help on class Device in module jnpr.junos.device:

class Device(__builtin__.object)
 |  Junos Device class.
 |  
 |  :attr:`ON_JUNOS`:
 |      **READ-ONLY** -
 |      Auto-set to ``True`` when this code is running on a Junos device,
 |      vs. running on a local-server remotely connecting to a device.
 |  
 |  :attr:`auto_probe`:
 |      When non-zero the call to :meth:`open` will probe for NETCONF
 |      reachability before proceeding with the NETCONF session establishment.
 |      If you want to enable this behavior by default, you could do the
 |      following in your code::
 |  
 |          from jnpr.junos import Device
 |  
 |          # set all device open to auto-probe with timeout of 10 sec
 |          Device.auto_probe = 10
 |  
 |          dev = Device( ... )
 |          dev.open()   # this will probe before attempting NETCONF connect
:
<shortened for brevity>
```

Make sure you to scroll through the full help menu while on the Python shell.

> Note: you are also able to use SSH keys while using PyEZ.

##### Step 5

Create a Juniper device object for **vmx1**.

```python
>>> vmx1 = JUNIPER(host='vmx1', user='ntc', password='ntc123')
```

##### Step 6

Create two more device objects, but this time for **vmx2** and **vmx3**.

This time we'll use a different syntax that unpacks a dictionary into multiple key value pairs.

```python
>>> args = dict(host='vmx2', user='ntc', password='ntc123')
>>> 
>>> vmx2 = JUNIPER(**args)
>>> 
```


```python
>>> args = dict(host='vmx3', user='ntc', password='ntc123')
>>> 
>>> vmx3 = JUNIPER(**args)
>>> 
```


##### Step 7

We now have three device objects, but connections to each device still need to be opened.  This is in contrast to other APIs that are stateless and connections don't need to be opened at all.

Use the open method for each device.


```python
>>> vmx1.open()
Device(vmx1)
>>> 
>>> vmx2.open()
Device(vmx2)
>>> 
>>> vmx3.open()
Device(vmx2)
>>> 
```

Three NETCONF sessions have now been established to the network devices.

##### Step 8

Use the `connected` property of the device objects to perform a status check and ensure there is an active NETCONF session open to each device.

```python
>>> vmx1.connected
True
>>>
>>> vmx2.connected
True
>>>
>>> vmx3.connected
True
>>>
```

##### Step 9

View the _facts_ for each device using the `facts` property.

Print facts for **vmx1**.

For *vmx1*, save the facts in a new variable called `vmx1_facts` and pretty print the results.

Note: `pprint` is another Python module that can be used to pretty print objects.

```python
>>> vmx1_facts = vmx1.facts
>>>
>>> from pprint import pprint as pp
>>> 
>>> pp(vmx1_facts)
{'2RE': False,
 'HOME': '/var/home/ntc',
 'RE0': {'last_reboot_reason': '0x200:normal shutdown ',
         'mastership_state': 'master',
         'model': 'RE-VMX',
         'status': 'OK',
         'up_time': '34 minutes, 47 seconds'},
 'domain': 'ntc.com',
 'fqdn': 'vmx1.ntc.com',
 'hostname': 'vmx1',
 'ifd_style': 'CLASSIC',
 'master': 'RE0',
 'model': 'VMX',
 'personality': 'MX',
 'serialnumber': 'VMXf9',
 'switch_style': 'BRIDGE_DOMAIN',
 'vc_capable': False,
 'version': '15.1F4.15',
 'version_RE0': '15.1F4.15',
 'version_info': junos.version_info(major=(15, 1), type=F, minor=4, build=15),
 'virtual': True}
>>> 

```

Print the facts for the other two devices.

##### Step 10

Print the software version of *vmx3*.

Use the `version` key.

```python
>>> print vmx3.facts['version']
15.1X49-D15.4
>>> 
```

##### Step 11

Print the last reboot reason of **vmx3**.

```python
>>> print vmx3.facts['RE0']['last_reboot_reason']
0x200:normal shutdown 
>>> 
```


##### Step 12

You can also use the `hostname` property to view the hostname of the device.

Print the hostname for the vmx device.

```python
>>> vmx1.hostname
'vmx1'
>>> 
```


##### Step 13

There may be times when you want to issue CLI commands on a device in a program or while on the Python shell.  While this is not recommended because Juniper provides a robust API, you can use the `cli` method for this.

Issue the command `show version` and save the data being returned in a variable called `output`.

```python
>>> output = vmx1.cli('show version')
/usr/local/lib/python2.7/dist-packages/jnpr/junos/device.py:652: RuntimeWarning: CLI command is for debug use only!
  warnings.warn("CLI command is for debug use only!", RuntimeWarning)
>>> 
```

> You can see Juniper returns warnings as they highly recommend not using the `cli` method. 

Print the output.

```python
>>> print output

Hostname: vmx1
Model: vmx
Junos: 15.1F4.15
JUNOS Base OS boot [15.1F4.15]
JUNOS Base OS Software Suite [15.1F4.15]
JUNOS Crypto Software Suite [15.1F4.15]
JUNOS Online Documentation [15.1F4.15]
JUNOS 64-bit Kernel Software Suite [15.1F4.15]
JUNOS Routing Software Suite [15.1F4.15]
JUNOS Runtime Software Suite [15.1F4.15]
<shortened for brevity>
```

> You can disable the warning by setting `warning=False` when you call the `cli` method:

```python
>>> output = vmx1.cli('show version', warning=False)

>>> 
>>> print output

Hostname: vmx1
Model: vmx
Junos: 15.1F4.15
JUNOS Base OS boot [15.1F4.15]
JUNOS Base OS Software Suite [15.1F4.15]
JUNOS Crypto Software Suite [15.1F4.15]
```


### Task 2 - Performing a Configuration Merge

In this task you will use the `Config` object that exists within the `config` module within the Junos PyEZ library to load, rollback, and commit configurations on Junos devices.

##### Step 1

Import the `Config` object.  We use instances of this object to work with Juniper configurations.

```python
>>> from jnpr.junos.utils.config import Config
>>> 
```

##### Step 2

Explore the different methods of the `Config` object.

Use `dir()`:

```python
>>> dir(Config)
['commit', 'commit_check', 'dev', 'diff', 'load', 'lock', 'mode', 'pdiff', 'rescue', 'rollback', 'rpc', 'unlock']
>>> # shortened for clarity
```

Use `help()`:

```python
>>> help(Config)
>>>
```

```python
Help on Config in module jnpr.junos.utils.config object:

class Config(jnpr.junos.utils.util.Util)
 |  Overivew of Configuration Utilities:
 |  
 |  * :meth:`commit`: commit changes
 |  * :meth:`commit_check`: perform the commit check operation
 |  * :meth:`diff`: return the diff string between running and candidate config
 |  * :meth:`load`: load changes into the candidate config
 |  * :meth:`lock`: take an exclusive lock on the candidate config
 |  * :meth:`pdiff`: prints the diff string (debug/helper)
 |  * :meth:`rescue`: controls "rescue configuration"
 |  * :meth:`rollback`: perform the load rollback command
 |  * :meth:`unlock`: release the exclusive lock
 |  
```

Continue to use the `help` function on some of the methods of the `Config` object.

```python
>>> help(Config.load)
>>>
```


```python
Help on method load in module jnpr.junos.utils.config:

load(self, *vargs, **kvargs) unbound jnpr.junos.utils.config.Config method
    Loads changes into the candidate configuration.  Changes can be
    in the form of strings (text,set,xml), XML objects, and files.
    Files can be either static snippets of configuration or Jinja2
    templates.  When using Jinja2 Templates, this method will render
    variables into the templates and then load the resulting change;
    i.e. "template building".
    
    :param object vargs[0]:
        The content to load.  If the contents is a string, the framework
        will attempt to automatically determine the format.  If it is
        unable to determine the format then you must specify the
        **format** parameter.  If the content is an XML object, then
        this method assumes you have structured it correctly:
        and if not an Exception will be raised.
```

##### Step 3

In a new terminal window, SSH to *vmx1* and look at its current interface configuration.

```
ntc@ntc:~$ ssh ntc@vmx1
```

You should see this output:

```
ntc@vmx1> show configuration interfaces 
ge-0/0/0 {
    unit 0 {
        family inet;
    }
}
ge-0/0/1 {
    unit 0 {
        family inet;
    }
}
ge-0/0/2 {
    unit 0 {
        family inet;
    }
}
ge-0/0/3 {
    unit 0 {
        family inet;
    }
}
fxp0 {
    unit 0 {
        family inet {
            address 10.0.0.31/24;
        }
    }
} 
```


Our goal in this step is to simply update the the interface descriptions and IP addresses for interfaces ge-0/0/1 and ge-0/0/3 and the description for fxp0.

While in a Linux terminal window, and in the home directory, create sub-directory called `jnpr`, and in this new directory, create a file called `interface-descriptions.conf`.

Open the file and insert the following configuration stanza.

> Note: you need the parent object called *interfaces* which is not shown in the SSH output above.
> 
> The easiest way to get the format right is to take it from a show config.

```
interfaces {
    ge-0/0/1 {
        unit 0 {
            description UNUSED_INTERFACE;
            family inet {
                address 172.16.32.1/24;
            }
        }
    }
    ge-0/0/3 {
        unit 0 {
            description UNUSED_INTERFACE;
            family inet {
                address 10.100.100.1/24;
            }
        }
    }
    fxp0 {                              
        unit 0 {
            description MANAGEMENT_INTERFACE;
            family inet {
                address 10.0.0.31/24;
            }
        }
    }
}
```


##### Step 4

Load the new configuration file onto the device and treat it as a *configuration merge*.

First, you need to create a new configuration object.

```python
>>> config = Config(vmx1)
>>> 
```

Then as good practice, lock the configuration.

```python
>>> config.lock()
True
>>> 
```


Load the configuration onto the device.

> You can use a relative path if you so choose.

```python
>>> config.load(path='/home/ntc/jnpr/interface-descriptions.conf', format='text', merge=True)
<Element load-configuration-results at 0x7f913d45ddd0>
>>>
```

The configuration has been copied onto the device and is now the candidate configuration.


##### Step 5

Perform a commit check.  This will tell you if the commit will succeed.

```python
>>> config.commit_check()
True
>>> 

```


##### Step 6

View and access the diffs to see what _will_ be applied when the next commit takes place.

Simply print the diffs:

```python
>>> config.pdiff()

[edit interfaces ge-0/0/1 unit 0]
+    description UNUSED_INTERFACE;
[edit interfaces ge-0/0/1 unit 0 family inet]
+       address 172.16.32.1/24;
[edit interfaces ge-0/0/3 unit 0]
+    description UNUSED_INTERFACE;
[edit interfaces ge-0/0/3 unit 0 family inet]
+       address 10.100.100.1/24;
[edit interfaces fxp0 unit 0]
+    description MANAGEMENT_INTERFACE;


>>> 
```

Now save the diffs as a string.

```python
>>> diffs = config.diff()
>>> print diffs

[edit interfaces ge-0/0/1 unit 0]
+    description UNUSED_INTERFACE;
[edit interfaces ge-0/0/1 unit 0 family inet]
+       address 172.16.32.1/24;
[edit interfaces ge-0/0/3 unit 0]
+    description UNUSED_INTERFACE;
[edit interfaces ge-0/0/3 unit 0 family inet]
+       address 10.100.100.1/24;
[edit interfaces fxp0 unit 0]
+    description MANAGEMENT_INTERFACE;


>>>

```

##### Step 7

Perform a configuration rollback.

```python
>>> config.rollback()
True
>>> 
```

View the diffs again.

```python
>>> config.pdiff()
None
>>>
```

Notice how the candidate configuration has been rolled back.


##### Step 8

Since we do want to commit these changes, re-load the new configuration onto the device.

```python
>>> config.load(path='/home/ntc/jnpr/interface-descriptions.conf', format='text', merge=True)
<Element load-configuration-results at 0x7f913d45ddd0>
>>>
```

##### Step 9

Commit the changes.

```python
>>> config.commit()
True
>>>
```

Feel free to SSH to the vmx and view the updates that were implemented. You could have also compared the candidate to the running configuration before you committed the changes while on the CLI.

##### Step 10

Unlock the configuration.

```python
>>> config.unlock()
True
>>> 
```

### Task 3 - Performing a Configuration Replace

This task is very similar to the previous task, but instead of doing a configuration merge, you will do a configuration replace on a specific configuration stanza of vmx1.

##### Step 1

SSH to *vmx1*.  

```
ntc@ntc:~$ ssh ntc@vmx1
```

View the currently configured static routes.

You should see a single route:

```
routing-options {
    static {
        route 0.0.0.0/0 next-hop 10.0.0.2;
    }
}
```

##### Step 2

**Manually** add the following static routes to **vmx1** via the CLI and commit the changes.

```
set routing-options static route 20.0.0.0/8 next-hop 10.0.0.2
set routing-options static route 30.0.0.0/8 next-hop 10.0.0.2
set routing-options static route 40.0.0.0/8 next-hop 10.0.0.2
set routing-options static route 50.0.0.0/8 next-hop 10.0.0.2
set routing-options static route 60.0.0.0/8 next-hop 10.0.0.2
commit
```

You should see the updated routes on *vmx1*:

```
ntc@vmx1# show routing-options 
static {
    route 0.0.0.0/0 next-hop 10.0.0.2;
    route 20.0.0.0/8 next-hop 10.0.0.2;
    route 30.0.0.0/8 next-hop 10.0.0.2;
    route 40.0.0.0/8 next-hop 10.0.0.2;
    route 50.0.0.0/8 next-hop 10.0.0.2;
    route 60.0.0.0/8 next-hop 10.0.0.2;
}

[edit]
```


##### Step 3

Since our goal is to do a replace, create a new configuration file that has a single route, which happens to be the original route that was configured on the device.  

We want to replace all routes with the config stanza being sent to the device.

In the `jnpr` directory you created in the last task, create a new file called `vmx-routes.conf`.

It should look like this:

```
routing-options {
    static {
        route 0.0.0.0/0 next-hop 10.0.0.2;
    }
}
```

##### Step 4

Now, add "**replace:**" to the file right above the word *static* as shown below and save the file:

```
routing-options {
    replace:
    static {
        route 0.0.0.0/0 next-hop 10.0.0.2;
    }
}
```

This is required when you want to do a *replace* operation on a specific configuration stanza.


##### Step 5

Check and ensure you have a connection established to *vmx1*.

```python
>>> vmx1.connected
False
>>> 
```

If you see `False`, re-establish a connection:

```python
>>> vmx1.open()
Device(vmx1)
>>>
```


##### Step 6

Create a new config object for the vmx.

```python
>>> vmx_config = Config(vmx1)
>>> 
```

##### Step 7

Using the load method, load the configuration onto the device.  

**Use the proper flags (merge=False) to ensure the replace operation happens.**

`merge=False` is the default, but it's good to be explicit so we know exactly what operation is getting performed.

```python
>>> vmx_config.load(path='/home/ntc/jnpr/vmx-routes.conf', format='text', merge=False)
<Element load-configuration-results at 0x7f18a7310290>
>>> 
```

##### Step 8

View the diffs.

```python
>>> vmx_config.pdiff()

[edit routing-options static]
-    route 20.0.0.0/8 next-hop 10.0.0.2;
-    route 30.0.0.0/8 next-hop 10.0.0.2;
-    route 40.0.0.0/8 next-hop 10.0.0.2;
-    route 50.0.0.0/8 next-hop 10.0.0.2;
-    route 60.0.0.0/8 next-hop 10.0.0.2;

```

Notice how nothing is being added, but 5 routes are being removed ensuring the the configuration stanza is being *replaced*.

##### Step 9

Commit the changes.

```python
>>> vmx_config.commit()
True
>>> 

```

If you SSH back into the vmx, all you will see is a single route.

### Task 4 - Tables/Views

In this task, you will use Juniper PyEZ Tables and Views to simplify getting data out of Junos devices.

##### Step 1

Navigate to the Juniper PyEZ Github page and look at the Tables/Views that have been already built by others.  

[https://github.com/Juniper/py-junos-eznc/tree/master/lib/jnpr/junos/op](https://github.com/Juniper/py-junos-eznc/tree/master/lib/jnpr/junos/op)

You can see that there is a Python file and YAML file for every table.

> Note: it is possible to put multiple tables in a single YAML file.

The Python file is the meta Python module that is used to load the associated tables that are found in the YAML file.

##### Step 2

Use the native LLDP table/view to extract neighbor information from *vmx1*.

As can be found on Juniper's GitHub site, this is the LLDP table and view (`lldp.yml`):

```
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


> Note: the Python module is the name of the python file such as `lldp.py` and the object you import is the table name, which can be found in the `lldp.yml` file.

```python
>>> from jnpr.junos.op.lldp import LLDPNeighborTable
>>> 
>>> neighbors = LLDPNeighborTable(vmx1)
>>> 
>>> neighbors.get()
LLDPNeighborTable:vmx1: 4 items
>>> 

```


Loop through neighbors and print out the local interface and neighbor's hostname for each item.

Remember that:

* The `key` from the Table can be accessed using the `name` attribute.
* Each `field` from the View is also an attribute.

```python
>>> for neighbor in neighbors:
...   print 'Neighbor {} found on interface {}'.format(neighbor.remote_sysname, neighbor.name)
... 
Neighbor vmx2 found on interface fxp0
Neighbor vmx2 found on interface ge-0/0/2
Neighbor vmx3 found on interface fxp0
Neighbor vmx3 found on interface ge-0/0/0
>>>

```

Since the **key** happens to also be a **field**, i.e. `local_int`, you don't technically need to use `name`:


```python
>>> for neighbor in neighbors:
...   print 'Neighbor {} found on interface {}'.format(neighbor.remote_sysname, neighbor.local_int)
... 
Neighbor vmx2 found on interface fxp0
Neighbor vmx2 found on interface ge-0/0/2
Neighbor vmx3 found on interface fxp0
Neighbor vmx3 found on interface ge-0/0/0
>>> 
```


##### Step 3

Use the `PhyPortTable` in `phyport.yml` to extract information about the physical interfaces of the vmx.

Take a look at the Table/View here: [https://github.com/Juniper/py-junos-eznc/blob/master/lib/jnpr/junos/op/phyport.yml](https://github.com/Juniper/py-junos-eznc/blob/master/lib/jnpr/junos/op/phyport.yml)


```python
>>> from jnpr.junos.op.phyport import PhyPortTable
>>> 
>>> interfaces = PhyPortTable(vmx1)
>>> interfaces.get()
PhyPortTable:vmx1: 10 items
>>>

```

Loop through `interfaces` and print out the interface name and operational state for each interface.  Remember to check and see what the fields and key are in the `PhyPortTable` found in the YAML file.

```python
>>> for item in interfaces:
...     print 'interface: ', item.name
...     print 'status: ', item.oper
...     print '=' * 30
... 
interface:  ge-0/0/0
status:  up
==============================
interface:  ge-0/0/1
status:  up
==============================
interface:  ge-0/0/2
status:  up
==============================
interface:  ge-0/0/3
status:  up
==============================
interface:  ge-0/0/4
status:  up
==============================
interface:  ge-0/0/5
status:  up
==============================
interface:  ge-0/0/6
status:  down
==============================
interface:  ge-0/0/7
status:  down
==============================
interface:  ge-0/0/8
status:  down
==============================
interface:  ge-0/0/9
status:  down
==============================
>>>
```


If you noticed, there are other [tables](https://github.com/Juniper/py-junos-eznc/blob/master/lib/jnpr/junos/op/phyport.yml) in `phyport.yml` besides PhyPortTable.  

Experiment with using one or more of those other tables.

##### Step 4

This step shows how to create a custom Table/View without creating new files.  Rather, you can create a table/view inline as a multi-line string.

Create a new string variable called `ntc_neighbors` that will be the string representation of a new custom Table/View.

> Note: triple quotes is used to create a multi-line string (or comment).

```python
>>> ntc_neighbors = """
... ---
... NTCNeighborTable:
...   rpc: get-lldp-neighbors-information
...   item: lldp-neighbor-information
...   key: lldp-local-interface | lldp-local-port-id
...   view: LLDPNeighborView
... 
... LLDPNeighborView:
...   fields:
...     local_interface: lldp-local-interface | lldp-local-port-id
...     neighbor_interface: lldp-remote-port-id
...     neighbor: lldp-remote-system-name
... """
>>> 
```

Print out `ntc_neighbors`.

```python
>>> print ntc_neighbors

---
NTCNeighborTable:
  rpc: get-lldp-neighbors-information
  item: lldp-neighbor-information
  key: lldp-local-interface | lldp-local-port-id
  view: NTCNeighborView

NTCNeighborView:
  fields:
    local_interface: lldp-local-interface | lldp-local-port-id
    neighbor_interface: lldp-remote-port-id
    neighbor: lldp-remote-system-name

>>> 
```

>> Note that `ntc_neighbors` is only a string presentation of a YAML object.


##### Step 5

When using inline tables, you need to import two other objects.  Import these objects as shown below.

```python
>>> 
>>> from jnpr.junos.factory.factory_loader import FactoryLoader
>>> import yaml
>>> 
```

##### Step 6

There is a command that needs to be executed to load the table into the active namespace.  This means it will make the table from the `ntc_neighbors` string a callable object.

> This is an advanced concept and part of the PyEZ library to simplify working with inline tables.  All you need to do is pass in the name of your string to use it --- in our case, it's `ntc_neighbors`.

```python
>>> globals().update(FactoryLoader().load(yaml.load(ntc_neighbors)))
>>>
```

Call the `dir()` function and you can see the `NTCNeighborTable` is now part of your global namespace.

```python
>>> dir()
['FactoryLoader', 'J', 'LLDPNeighborTable', 'LLDPNeighborView', 'NTCNeighborTable', 'PhyPortTable', '__builtins__', '__doc__', '__name__', '__package__', 'interfaces', 'item', 'neighbor', 'neighbors', 'ntc_neighbors', 'vmx1', 'yaml']
>>> 
>>> 
```

You can now use it just like you would a normal table that was imported from a Python module!

##### Step 7

Use your custom table and retrieve all items.

```python
>>> neighbors = NTCNeighborTable(vmx1)
>>> 
>>> neighbors.get()
NTCNeighborTable:vmx1: 4 items
>>> 

```

Loop through and print each `field` for each item.

```python
>>> for item in neighbors:
...     print 'local_interface: {}, neighbor: {}, neighbor_interface {}'.format(item.local_interface, item.neighbor, item.neighbor_interface)
... 
local_interface: fxp0, neighbor: vmx2, neighbor_interface fxp0
local_interface: ge-0/0/2, neighbor: vmx2, neighbor_interface ge-0/0/2
local_interface: fxp0, neighbor: vmx3, neighbor_interface fxp0
local_interface: ge-0/0/0, neighbor: vmx3, neighbor_interface ge-0/0/0
>>>

```

##### Step 8

Print out neighbors.items()

```python
>>> print neighbors.items()
[('fxp0', [('neighbor_interface', 'fxp0'), ('local_interface', 'fxp0'), ('neighbor', 'vmx2')]), ('ge-0/0/2', [('neighbor_interface', 'ge-0/0/2'), ('local_interface', 'ge-0/0/2'), ('neighbor', 'vmx2')]), ('fxp0', [('neighbor_interface', 'fxp0'), ('local_interface', 'fxp0'), ('neighbor', 'vmx3')]), ('ge-0/0/0', [('neighbor_interface', 'ge-0/0/0'), ('local_interface', 'ge-0/0/0'), ('neighbor', 'vmx3')])]
>>> 

```

Do not close out the Python shell.


### Task 5 - Gather Neighbors Script

In this task, you will write a script that queries three Juniper vMX routers for their LLDP neighbors.

The final data structure should be a dictionary.  Each key will be the hostname of the device.  The value will be a list of dictionaries - each of these dictionaries should have the following keys:  `neighbor_interface`, `neighbor`, and `local_interface` --- this models what you did in the previous task with the custom NTCNeighborTable.

Before you query all three devices and create the final script, you will start with testing on the Python shell.

Before starting make sure you can ping *vmx2* and *vmx3*.

```
$ ping vmx2
$ ping vmx3
```

##### Step 1

This first step is a summary of what you did in the previous task.  Please review it and ensure you still have access to these objects on the Python shell.

```python
>>> from jnpr.junos.device import Device as JUNIPER
>>> from jnpr.junos.factory.factory_loader import FactoryLoader
>>> import yaml
>>> 
>>> vmx1 = JUNIPER(host='vmx1', user='ntc', password='ntc123')
>>> vmx1.open()
>>> 
>>> ntc_neighbors = """
>>> ---
>>> NTCNeighborTable:
>>>   rpc: get-lldp-neighbors-information
>>>   item: lldp-neighbor-information
>>>   key: lldp-local-interface | lldp-local-port-id
>>>   view: LLDPNeighborView
>>> 
>>> LLDPNeighborView:
>>>   fields:
>>>     local_interface: lldp-local-interface | lldp-local-port-id
>>>     neighbor_interface: lldp-remote-port-id
>>>     neighbor: lldp-remote-system-name
>>> """
>>> 
>>> globals().update(FactoryLoader().load(yaml.load(ntc_neighbors)))
>>> 
>>> neighbors = NTCNeighborTable(vmx1)
>>> 
>>> neighbors.get()
>>> 
>>> print neighbors.items()
[('fxp0', [('neighbor_interface', 'fxp0'), ('local_interface', 'fxp0'), ('neighbor', 'vmx2')]), ('ge-0/0/2', [('neighbor_interface', 'ge-0/0/2'), ('local_interface', 'ge-0/0/2'), ('neighbor', 'vmx2')]), ('fxp0', [('neighbor_interface', 'fxp0'), ('local_interface', 'fxp0'), ('neighbor', 'vmx3')]), ('ge-0/0/0', [('neighbor_interface', 'ge-0/0/0'), ('local_interface', 'ge-0/0/0'), ('neighbor', 'vmx3')])]
>>> 
>>> 
>>> 
>>> len(neighbors.items())
4
>>> 

```

We can see that *vmx1* has 4 neighbors.

##### Step 2

As discussed in the lesson/lecture and as you can see above, `neighbors.items()` is a list of tuples.  

We now need to convert the list of tuples to a list of dictionaries.

Loop through `neighbors.items()` and make a new a list of dictionaries instead of a list of tuples

Here is sample code that is commented that walks through the code required:

```python
list_of_neighbors = []

# neighbors.items() is a list of tuples
for table_key, table_fields in neighbors.items():
    # sample resource:
    # ('fxp0', [('neighbor_interface', '1'), ('local_interface', 'fxp0'),
    # ('neighbor', 'vmx2')]
    # table_key - element 0 is the key from the Table
    # table_fields element 1 is also a list of uples

    temp = {}
    for normalized_key, normalized_value in table_fields:
        # calling it normalized value because
        # YOU/WE created the keys
        temp[normalized_key] = normalized_value
    list_of_neighbors.append(temp)

```

Now enter it on the Python shell:

```python
>>> list_of_neighbors = []
>>> 
>>> for table_key, table_fields in neighbors.items():
...     temp = {}
...     for normalized_key, normalized_value in table_fields:
...         temp[normalized_key] = normalized_value
...     list_of_neighbors.append(temp)
... 
>>> 
```

Print `list_of_neighbors`:

```python
>>> print list_of_neighbors
[{'neighbor_interface': 'fxp0', 'local_interface': 'fxp0', 'neighbor': 'vmx2'}, {'neighbor_interface': 'ge-0/0/2', 'local_interface': 'ge-0/0/2', 'neighbor': 'vmx2'}, {'neighbor_interface': 'fxp0', 'local_interface': 'fxp0', 'neighbor': 'vmx3'}, {'neighbor_interface': 'ge-0/0/0', 'local_interface': 'ge-0/0/0', 'neighbor': 'vmx3'}]
>>> 
```

And now pretty print so it's more readable.

```python
>>> import json
>>> 
>>> print json.dumps(list_of_neighbors, indent=4)
[
    {
        "neighbor_interface": "fxp0", 
        "local_interface": "fxp0", 
        "neighbor": "vmx2"
    }, 
    {
        "neighbor_interface": "ge-0/0/2", 
        "local_interface": "ge-0/0/2", 
        "neighbor": "vmx2"
    }, 
    {
        "neighbor_interface": "fxp0", 
        "local_interface": "fxp0", 
        "neighbor": "vmx3"
    }, 
    {
        "neighbor_interface": "ge-0/0/0", 
        "local_interface": "ge-0/0/0", 
        "neighbor": "vmx3"
    }
]
>>> 
```

This process isn't technically required, but these are the 3 keys we use in this course to define a neighbor, and normalize neighbors across the variety of vendors we work with such as Arista and Cisco  devices.


##### Step 3

Now you will take this and build the script, which should print the final dictionary that should have three key value pairs.  The first key will be `vmx1`, the second key will be `vmx2`, and the final key will be `vmx3`.

The values will be equal to `list_of_neighbors` from the previous step, which is a list of dictionaries.

In the `scripts` directory, create a new file called `juniper_neighbors.py`

if __name__ == "__main__" should only call a main() function

- main() should call a function called get_neighbors()
- get_neighbors() should accept one parameter, which will be the Juniper device object.
- get_neighbors() will do everything that you just performed on the Python shell
- Instead of printing the resulting list, return it to main().
- Don't forget to import the proper objects!

The final script to retrieve *vmx1* neighbors should like this:

```python
from jnpr.junos.device import Device as JUNIPER
from jnpr.junos.factory.factory_loader import FactoryLoader
import json
import yaml


def get_neighbors(device):

    ntc_neighbors = """
---
NTCNeighborTable:
  rpc: get-lldp-neighbors-information
  item: lldp-neighbor-information
  key: lldp-local-interface | lldp-local-port-id
  view: LLDPNeighborView

LLDPNeighborView:
  fields:
    local_interface: lldp-local-interface | lldp-local-port-id
    neighbor_interface: lldp-remote-port-id
    neighbor: lldp-remote-system-name
"""

    globals().update(FactoryLoader().load(yaml.load(ntc_neighbors)))

    neighbors = NTCNeighborTable(device)

    neighbors.get()

    list_of_neighbors = []

    # neighbors.items() is a list of tuples
    for table_key, table_fields in neighbors.items():
        temp = {}
        for normalized_key, normalized_value in table_fields:
            temp[normalized_key] = normalized_value
        list_of_neighbors.append(temp)

    return list_of_neighbors

def main():

    vmx1 = JUNIPER(host='vmx1', user='ntc', password='ntc123')
    vmx1.open()

    vmx1_neighbors = get_neighbors(vmx1)
    vmx1.close()
    print json.dumps(vmx1_neighbors, indent=4)


if __name__ =="__main__":
    main()

```


However, this still only returns a list of neighbors for *vmx1*.

##### Step 8

Now update `main()` so it prints the final dictionary that has neighbors for *vmx1, vmx2, and vmx3*.

You can do this manually, but why not create a loop, and minimize the amount of code you need?

```python
def main():

    neighbors = {}

    devices = ['vmx1', 'vmx2', 'vmx3']

    for dev in devices:
        device = JUNIPER(host=dev, username='ntc', password='ntc123')
        device.open()
        neighbors[dev] = get_neighbors(device)
        device.close()

    print json.dumps(neighbors, indent=4)


```

##### Step 9

Save and re-run the script.

And there you have it.  A complete script to go out and collect neighbor information from a Juniper network.

For completeness, here is the full script:

```python
from jnpr.junos.device import Device as JUNIPER
from jnpr.junos.factory.factory_loader import FactoryLoader
import json
import yaml


def get_neighbors(device):

    ntc_neighbors = """
---
NTCNeighborTable:
  rpc: get-lldp-neighbors-information
  item: lldp-neighbor-information
  key: lldp-local-interface | lldp-local-port-id
  view: LLDPNeighborView

LLDPNeighborView:
  fields:
    local_interface: lldp-local-interface | lldp-local-port-id
    neighbor_interface: lldp-remote-port-id
    neighbor: lldp-remote-system-name
"""

    globals().update(FactoryLoader().load(yaml.load(ntc_neighbors)))

    neighbors = NTCNeighborTable(device)

    neighbors.get()

    list_of_neighbors = []

    # neighbors.items() is a list of tuples
    for table_key, table_fields in neighbors.items():
        temp = {}
        for normalized_key, normalized_value in table_fields:
            temp[normalized_key] = normalized_value
        list_of_neighbors.append(temp)

    return list_of_neighbors

def main():

    neighbors = {}

    devices = ['vmx1', 'vmx2', 'vmx3']

    for dev in devices:
        device = JUNIPER(host=dev, username='ntc', password='ntc123')
        device.open()
        neighbors[dev] = get_neighbors(device)
        device.close()

    print json.dumps(neighbors, indent=4)


if __name__ =="__main__":
    main()


```


