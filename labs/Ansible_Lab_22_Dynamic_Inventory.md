## Lab 22 - Dynamic Inventory

### Using a Dynamic Inventory Script

When getting started with Ansible, it's quite common to use an inventory file like you've been using in the labs.

However, in larger or more dynamic environments, there may already be a single _source of truth_.  This is quite common in cloud environments.  For example, the number of VMs may change by the hour (maybe with AWS auto-scaling).  You could then use an AWS dynamic inventory script to always have required inventory information rather than trying to keep the inventory file up to date.  

If you already had a network management system or CMDB, then a dynamic inventory script could be used.  This way you aren't managing two inventories, one for the NMS/CMDB and one for Ansible.  

In this lab, you will explore and use a dynamic inventory script that simulates making an API to a NMS or CMDB.

##### Step 1

Navigate to the directory called `dynamic_inv` within your home directory.

##### Step 2

Open the file called `dynamo.py` in a text editor.

You'll see this script:

```python
#!/usr/bin/env python

import requests
import requests.packages.urllib3

import json

requests.packages.urllib3.disable_warnings()

def main():

    url = 'https://2z3oa80l2c.execute-api.us-east-1.amazonaws.com/prod/switch'

    inventory = requests.get(url, verify=False)

    return inventory.text

if __name__ == "__main__":

    rsp = main()

    print rsp


```

##### Step 3

Run this Python script using the `-i` flag from the Linux terminal, so you get dropped into the Python shell after it executes.

```
ntc@ntc:~/dynamic_inv$ python -i dynamo.py
```

The scripts executes, but you still have access to the variables in scope within `if __name__ == "__main__"`.  Here that's just `rsp`.

For example, you can print rsp:

```python
>>> print rsp
{
"cisco"   : {
    "hosts"   : [ "n9k1.ntc.com", "n9k2.ntc.com" ],
    "vars"    : {
        "platform"   : "nexus"
    }
},
"arista"  : [ "arista1.ntc.com", "arista2.ntc.com" ],
"hp"     : {
    "hosts"   : [ "hp1.ntc.com", "hp2.ntc.com", "hp3.ntc.com", "hp4.ntc.com" ],
    "vars"    : {
        "platform"   : "comware7"
    }
},
"juniper"    : [ "jnprfw.ntc.com" ],
"apic"     : [ "aci.ntc.com" ]
}

```

##### Step 4

Use `json.loads` to work with it as a Python dictionary.

```python
>>> import json
>>> 
>>> inv = json.loads(rsp)
>>> 
>>> inv
{u'hp': {u'hosts': [u'hp1.ntc.com', u'hp2.ntc.com', u'hp3.ntc.com', u'hp4.ntc.com'], u'vars': {u'platform': u'comware7'}}, u'cisco': {u'hosts': [u'n9k1.ntc.com', u'n9k2.ntc.com'], u'vars': {u'platform': u'nexus'}}, u'juniper': [u'jnprfw.ntc.com'], u'arista': [u'arista1.ntc.com', u'arista2.ntc.com'], u'apic': [u'aci.ntc.com']}
>>> 
>>> inv.get('hp')
{u'hosts': [u'hp1.ntc.com', u'hp2.ntc.com', u'hp3.ntc.com', u'hp4.ntc.com'], u'vars': {u'platform': u'comware7'}}
>>> 
>>> inv.get('arista')
[u'arista1.ntc.com', u'arista2.ntc.com']
```

The goal is to understand what key-values you need to return if you are building your own dynamic inventory script.

You can see here the keys are group names.  It's values has a key called hosts and there is a list of hosts inside there.

##### Step 5

Exit from the Python shell.

In this directory there is also a sample playbook called `site.yml`  

```yaml

---

  - name: test playbook for dynamic inventory
    connection: local
    gather_facts: no
    hosts: all


    tasks:

      - debug: var=inventory_hostname
```

##### Step 6

Run the playbook using the dynamic inventory script.

```
ntc@ntc:~/dynamic_inv$ ansible-playbook -i dynamo.py site.yml 
```

```

PLAY [test playbook for dynamic inventory] ************************************ 

TASK: [debug var=inventory_hostname] ****************************************** 
ok: [n9k1.ntc.com] => {
    "var": {
        "inventory_hostname": "n9k1.ntc.com"
    }
}
ok: [n9k2.ntc.com] => {
    "var": {
        "inventory_hostname": "n9k2.ntc.com"
    }
}
ok: [jnprfw.ntc.com] => {
    "var": {
        "inventory_hostname": "jnprfw.ntc.com"
    }
}
ok: [hp1.ntc.com] => {
    "var": {
        "inventory_hostname": "hp1.ntc.com"
    }
}
ok: [hp3.ntc.com] => {
    "var": {
        "inventory_hostname": "hp3.ntc.com"
    }
}
ok: [hp4.ntc.com] => {
    "var": {
        "inventory_hostname": "hp4.ntc.com"
    }
}
ok: [arista2.ntc.com] => {
    "var": {
        "inventory_hostname": "arista2.ntc.com"
    }
}
ok: [hp2.ntc.com] => {
    "var": {
        "inventory_hostname": "hp2.ntc.com"
    }
}
ok: [arista1.ntc.com] => {
    "var": {
        "inventory_hostname": "arista1.ntc.com"
    }
}
ok: [aci.ntc.com] => {
    "var": {
        "inventory_hostname": "aci.ntc.com"
    }
}

PLAY RECAP ******************************************************************** 
aci.ntc.com                : ok=1    changed=0    unreachable=0    failed=0   
arista1.ntc.com            : ok=1    changed=0    unreachable=0    failed=0   
arista2.ntc.com            : ok=1    changed=0    unreachable=0    failed=0   
hp1.ntc.com                : ok=1    changed=0    unreachable=0    failed=0   
hp2.ntc.com                : ok=1    changed=0    unreachable=0    failed=0   
hp3.ntc.com                : ok=1    changed=0    unreachable=0    failed=0   
hp4.ntc.com                : ok=1    changed=0    unreachable=0    failed=0   
jnprfw.ntc.com             : ok=1    changed=0    unreachable=0    failed=0   
n9k1.ntc.com               : ok=1    changed=0    unreachable=0    failed=0   
n9k2.ntc.com               : ok=1    changed=0    unreachable=0    failed=0   
```

See what happened?  You specified the script instead of using a static inventory file.
