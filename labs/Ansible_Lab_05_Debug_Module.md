## Lab 5 - Using the debug module

### Task 1 - Debugging Variables

This lab highlights the use of the `debug` modules.  It offers you the ability to "print" variables to the terminal often very helpful for verifying what a variable is set to.  As you can see from the last lab, you can see variables can be defined in many locations in the inventory file, e.g. same variable for different groups.

Let's review a few ways the `debug` module helps with troubleshooting.

##### Step 1

Navigate to the `ansible` directory.

```
ntc@ntc:~$ cd ansible/
ntc@ntc:ansible$
```

##### Step 2

Create a playbook file called `debug.yml`.

```
ntc@ntc:ansible$ touch debug.yml
ntc@ntc:ansible$
```

Open the file in your text editor.

The playbook will consist of a single play and a single task.


##### Step 3

Use the following for the starting point of the playbook.  This will execute for all devices in the _iosxe_ group.
 The task will simply print the variable `ntc_vendor` for each device in the group.

```yaml
---

  - name: USING THE DEBUG MODULE
    hosts: iosxe
    gather_facts: no


    tasks:
      - name: DEBUG AND PRINT TO TERMINAL
        debug: var=ntc_vendor

```

##### Step 5

Save and execute the playbook.

You should see the following output.

```
ntc@ntc:ansible$ ansible-playbook -i inventory debug.yml

PLAY [USING THE DEBUG MODULE] ***************************************************

TASK [DEBUG AND PRINT TO TERMINAL] **********************************************
ok: [csr1] => {
    "ntc_vendor": "cisco"
}
ok: [csr2] => {
    "ntc_vendor": "cisco"
}
ok: [csr3] => {
    "ntc_vendor": "cisco"
}

PLAY RECAP **********************************************************************
csr1                       : ok=1    changed=0    unreachable=0    failed=0
csr2                       : ok=1    changed=0    unreachable=0    failed=0
csr3                       : ok=1    changed=0    unreachable=0    failed=0

ntc@ntc:ansible$
```

Note, this just printed the variable to the terminal.

##### Step 4

Change the `hosts:` in the play definition to automate "all" devices in the inventory file.

```yaml
    hosts: all
```

##### Step 6

Save and execute the playbook.

You should see the following output.

```
ntc@ntc:ansible$ ansible-playbook -i inventory debug.yml


PLAY [USING THE DEBUG MODULE] ***************************************************

TASK [DEBUG AND PRINT TO TERMINAL] **********************************************
ok: [eos-spine1] => {
    "ntc_vendor": "arista"
}
ok: [vmx7] => {
    "ntc_vendor": "juniper"
}
ok: [nxos-spine1] => {
    "ntc_vendor": "cisco"
}
ok: [nxos-spine2] => {
    "ntc_vendor": "cisco"
}
ok: [eos-spine2] => {
    "ntc_vendor": "arista"
}
ok: [vmx9] => {
    "ntc_vendor": "juniper"
}
ok: [csr1] => {
    "ntc_vendor": "cisco"
}
ok: [csr3] => {
    "ntc_vendor": "cisco"
}
ok: [csr2] => {
    "ntc_vendor": "cisco"
}
ok: [vmx8] => {
    "ntc_vendor": "juniper"
}
ok: [eos-leaf1] => {
    "ntc_vendor": "arista"
}
ok: [eos-leaf2] => {
    "ntc_vendor": "arista"
}

PLAY RECAP **********************************************************************
csr1                       : ok=1    changed=0    unreachable=0    failed=0
csr2                       : ok=1    changed=0    unreachable=0    failed=0
csr3                       : ok=1    changed=0    unreachable=0    failed=0
eos-leaf1                  : ok=1    changed=0    unreachable=0    failed=0
eos-leaf2                  : ok=1    changed=0    unreachable=0    failed=0
eos-spine1                 : ok=1    changed=0    unreachable=0    failed=0
eos-spine2                 : ok=1    changed=0    unreachable=0    failed=0
nxos-spine1                : ok=1    changed=0    unreachable=0    failed=0
nxos-spine2                : ok=1    changed=0    unreachable=0    failed=0
vmx7                       : ok=1    changed=0    unreachable=0    failed=0
vmx8                       : ok=1    changed=0    unreachable=0    failed=0
vmx9                       : ok=1    changed=0    unreachable=0    failed=0

ntc@ntc:ansible$
```

See how we can quickly view the same variable for all devices quite easily?

### Task 2 - Adding & Printing More Group Variables

##### Step 1

Add a variable called `ntc_device_type` to the `[all:vars]` section of the inventory file.

The updated section should look like this:

```
[all:vars]
ansible_user=ntc
ansible_ssh_pass=ntc123
ansible_connection=network_cli
ntc_device_type=unknown
```

##### Step 2

Add a task to the playbook to debug the `device_type` variable so the playbook reflects the following:

```yaml
---

  - name: USING THE DEBUG MODULE
    hosts: all
    connection: network_cli
    gather_facts: no


    tasks:
      - name: DEBUG AND PRINT TO TERMINAL
        debug: var=ntc_vendor

      - name: DEBUG AND PRINT DEVICE TYPE TO TERMINAL
        debug: var=ntc_device_type


```

##### Step 3

Save and execute the following:

```
ntc@ntc:ansible$ ansible-playbook -i inventory debug.yml

```

You should see the following output for the new task:

```
TASK [DEBUG AND PRINT DEVICE TYPE TO TERMINAL] **********************************
ok: [eos-spine1] => {
    "ntc_device_type": "unknown"
}
ok: [eos-spine2] => {
    "ntc_device_type": "unknown"
}
ok: [eos-leaf1] => {
    "ntc_device_type": "unknown"
}
ok: [eos-leaf2] => {
    "ntc_device_type": "unknown"
}
ok: [vmx7] => {
    "ntc_device_type": "unknown"
}
ok: [vmx8] => {
    "ntc_device_type": "unknown"
}
ok: [vmx9] => {
    "ntc_device_type": "unknown"
}
ok: [csr1] => {
    "ntc_device_type": "unknown"
}
ok: [csr2] => {
    "ntc_device_type": "unknown"
}
ok: [csr3] => {
    "ntc_device_type": "unknown"
}
ok: [nxos-spine1] => {
    "ntc_device_type": "unknown"
}
ok: [nxos-spine2] => {
    "ntc_device_type": "unknown"
}
```

##### Step 4

Update the inventory file so it includes a group-based variable called `ntc_device_type`
 for the `nxos` group and for the `iosxe` group.  Set them to be "n7kv" and "csr1000v" respectively.

Those two groups should now look like this:

```
[iosxe:vars]
ansible_network_os=ios
ntc_os=ios
ntc_api=ssh
ntc_vendor=cisco
ntc_device_type=csr1000v

[nxos:vars]
ansible_network_os=nxos
ntc_os=nxos
ntc_api=nxapi
ntc_vendor=cisco
ntc_device_type=n7kv


```

##### Step 5

Save and execute the following:

```
ntc@ntc:ansible$ ansible-playbook -i inventory debug.yml

```

You should see the following output for the new task:

```
TASK [DEBUG AND PRINT DEVICE TYPE TO TERMINAL] **********************************
ok: [eos-spine1] => {
    "ntc_device_type": "unknown"
}
ok: [eos-spine2] => {
    "ntc_device_type": "unknown"
}
ok: [eos-leaf1] => {
    "ntc_device_type": "unknown"
}
ok: [eos-leaf2] => {
    "ntc_device_type": "unknown"
}
ok: [vmx7] => {
    "ntc_device_type": "unknown"
}
ok: [vmx8] => {
    "ntc_device_type": "unknown"
}
ok: [vmx9] => {
    "ntc_device_type": "unknown"
}
ok: [csr1] => {
    "ntc_device_type": "csr1000v"
}
ok: [csr2] => {
    "ntc_device_type": "csr1000v"
}
ok: [csr3] => {
    "ntc_device_type": "csr1000v"
}
ok: [nxos-spine1] => {
    "ntc_device_type": "n7kv"
}
ok: [nxos-spine2] => {
    "ntc_device_type": "n7kv"
}


```

See how the more specific group variables are taking priority over the _all_ group?


### Task 3 - Adding & Printing Host Variables

In this task, you'll add "host based variables" to two hosts and print them to the terminal using the same playbook as the previous task.

##### Step 1

Add two host variables.  For **csr1**, set the value to "csr1000v-ng" and for **nxos-spine1**, set the value to "n9k":

```
[iosxe]
csr1    ntc_device_type=csr1000v-ng
csr2
csr3

[nxos-spines]
nxos-spine1  ntc_device_type=n9k
nxos-spine2
```

##### Step 2

Save the inventory file.

##### Step 3

Execute the playbook.  You should see the following relevant output:

```
TASK [DEBUG AND PRINT DEVICE TYPE TO TERMINAL] *****************************************************
ok: [eos-spine1] => {
    "ntc_device_type": "unknown"
}
ok: [eos-spine2] => {
    "ntc_device_type": "unknown"
}
ok: [eos-leaf1] => {
    "ntc_device_type": "unknown"
}
ok: [eos-leaf2] => {
    "ntc_device_type": "unknown"
}
ok: [vmx7] => {
    "ntc_device_type": "unknown"
}
ok: [vmx8] => {
    "ntc_device_type": "unknown"
}
ok: [vmx9] => {
    "ntc_device_type": "unknown"
}
ok: [csr1] => {
    "ntc_device_type": "csr1000v-ng"
}
ok: [csr2] => {
    "ntc_device_type": "csr1000v"
}
ok: [csr3] => {
    "ntc_device_type": "csr1000v"
}
ok: [nxos-spine1] => {
    "ntc_device_type": "n9k"
}
ok: [nxos-spine2] => {
    "ntc_device_type": "n7kv"
}
```

Take a minute to think about the variable priority occurring.  The **all** group is serving as the default, then specific group variables take priority over the **all** group, and then host variables take priority over the specific group variables.


### Task 4 - Using the msg Parameter

This task will introduce the `msg` parameter for the `debug` module.  Using `msg` is mutually exclusive with the `var` parameter.

When you just want to print a single variable, you use the `var` parameter.  If you want to add context (add a full sentence), you should use the `msg` parameter.

##### Step 1

Add a new task to the playbook to debug the `inventory_hostname` and `ntc_os` variables.

**The `inventory_hostname` variable is a built-in variable that's equal to the hostname of the device as you've defined it in the inventory file**.


```yaml
---

  - name: USING THE DEBUG MODULE
    hosts: all
    gather_facts: no


    tasks:
      - name: DEBUG AND PRINT TO TERMINAL
        debug: var=ntc_vendor

      - name: DEBUG AND PRINT DEVICE TYPE TO TERMINAL
        debug: var=ntc_device_type

      - name: DEBUG AND PRINT THE OS
        debug: msg="The OS for {{ inventory_hostname }} is {{ ntc_os }}."

```

##### Step 2

Save and execute the playbook.

You'll see the relevant output for the 3rd task in the playbook:

```
TASK [DEBUG AND PRINT THE OS] ***************************************************
ok: [eos-spine1] => {
    "msg": "The OS for eos-spine1 is eos."
}
ok: [eos-spine2] => {
    "msg": "The OS for eos-spine2 is eos."
}
ok: [eos-leaf1] => {
    "msg": "The OS for eos-leaf1 is eos."
}
ok: [eos-leaf2] => {
    "msg": "The OS for eos-leaf2 is eos."
}
ok: [vmx7] => {
    "msg": "The OS for vmx7 is junos."
}
ok: [vmx8] => {
    "msg": "The OS for vmx8 is junos."
}
ok: [vmx9] => {
    "msg": "The OS for vmx9 is junos."
}
ok: [csr1] => {
    "msg": "The OS for csr1 is ios."
}
ok: [csr2] => {
    "msg": "The OS for csr2 is ios."
}
ok: [csr3] => {
    "msg": "The OS for csr3 is ios."
}
ok: [nxos-spine1] => {
    "msg": "The OS for nxos-spine1 is nxos."
}
ok: [nxos-spine2] => {
    "msg": "The OS for nxos-spine2 is nxos."
}


```



### Task 5 - Using the YAML Syntax for Tasks

Your playbook should look like this:

```yaml
---

  - name: USING THE DEBUG MODULE
    hosts: all
    gather_facts: no


    tasks:
      - name: DEBUG AND PRINT TO TERMINAL
        debug: var=ntc_vendor

      - name: DEBUG AND PRINT DEVICE TYPE TO TERMINAL
        debug: var=ntc_device_type

      - name: DEBUG AND PRINT THE OS
        debug: msg="The OS for {{ inventory_hostname }} is {{ ntc_os }}."

```

This is using one type of syntax supported within the playbook in which it is `parameter=value`, e.g. `var=ntc_vendor` and `var=ntc_device_type`.

However, Ansible also supports a more native YAML syntax using colons in which it becomes `parameter: value` indented as a key under the module name. For example this is what the first task would look like:

```yaml
      - name: DEBUG AND PRINT TO TERMINAL
        debug:
          var: ntc_vendor
```


###### Step 1

Convert this playbook to using the YAML syntax.


```yaml
---

  - name: USING THE DEBUG MODULE
    hosts: all
    gather_facts: no


    tasks:
      - name: DEBUG AND PRINT TO TERMINAL
        debug:
          var: ntc_vendor

      - name: DEBUG AND PRINT DEVICE TYPE TO TERMINAL
        debug:
          var: ntc_device_type

      - name: DEBUG AND PRINT THE OS
        debug:
          msg: "The OS for {{ inventory_hostname }} is {{ ntc_os }}."
```

##### Step 2

Re-run the playbook ensuring there are no indentation issues.
