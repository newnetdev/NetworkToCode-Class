## Lab 2 - Using the debug module

This lab highlights the use of the `debug` modules.  It offers you the ability to "print" variables to the terminal often very helpful for verifying what a variable is set to.

##### Step 1

Navigate to the `ansible` directory.

```
ntc@ntc:~$ cd ansible/
ntc@ntc:ansible$ 
```

##### Step 2

Create a new inventory file called `netdevices`.

```
ntc@ntc:ansible$ touch netdevices
ntc@ntc:ansible$ 
```

##### Step 3

Create one group in the inventory file.  It should be called "datacenter"

Include 5 devices in the "datacenter" group called *sw1*, *sw2*, *router1*, *fw1usa*, and *fw2ie*.


```

[datacenter]
sw1
sw2
router1
fw1usa
fw2ie

```

##### Step 4

In the same directory, create a file called `debug.yml`.  

Open the file in your text editor.

The playbook will consist of a single play and a single task.  

  - The task will use the "debug" module.  The goal for this task is use "debug" to print a variable to the terminal when you run the playbook.
  - The variable called `inventory_hostname` will be used in this playbook.  As you already know, it is an Ansible built-in variable that is equal to name of the host as it's defined in the inventory file.  

This play should be limited to the `datacenter` group in the inventory file; use the `hosts: datacenter` in the play declaration.

By using the debug module and setting the parameter `var` equal to "inventory_hostname", we should expect to see each device's name as it is in `inventory`, printed to the terminal when the playbook is executed.

> Note: as in all of our labs for this course, always include `connection: local` and `gather_facts: no` because we aren't using the default connection mechanism Ansible offers, i.e. SSH.  And in this case, we are only running a local operation for debugging. 

```yaml
---

  - name: USING THE DEBUG MODULE
    hosts: datacenter
    connection: local
    gather_facts: no


    tasks:
      - name: DEBUG AND PRINT TO TERMINAL
        debug: var=inventory_hostname

```

##### Step 5

Save the playbook.

##### Step 6

Execute the playbook from the Linux terminal.

Use the `-i` flag to specific the inventory file you want to use for this playbook, which should be `netdevices`

```
ntc@ntc:ansible$ ansible-playbook -i netdevices debug.yml 
```


```
ntc@ntc:ansible$ ansible-playbook -i netdevices debug.yml 

PLAY [USING THE DEBUG MODULE] *********************************************************************************

TASK [DEBUG AND PRINT TO TERMINAL] ****************************************************************************
ok: [sw1] => {
    "inventory_hostname": "sw1"
}
ok: [sw2] => {
    "inventory_hostname": "sw2"
}
ok: [router1] => {
    "inventory_hostname": "router1"
}
ok: [fw1usa] => {
    "inventory_hostname": "fw1usa"
}
ok: [fw2ie] => {
    "inventory_hostname": "fw2ie"
}

PLAY RECAP ****************************************************************************************************
fw1usa                     : ok=1    changed=0    unreachable=0    failed=0   
fw2ie                      : ok=1    changed=0    unreachable=0    failed=0   
router1                    : ok=1    changed=0    unreachable=0    failed=0   
sw1                        : ok=1    changed=0    unreachable=0    failed=0   
sw2                        : ok=1    changed=0    unreachable=0    failed=0   

ntc@ntc:ansible$  
```

##### Step 7

Update the inventory file so it includes a host based variable called `device_type` for each device: 

```
[datacenter]
sw1  device_type=switch
sw2  device_type=switch
router1  device_type=router
fw1usa  device_type=fw
fw2ie  device_type=fw

```

You just created host specific variables within the inventory file.  This will be covered in greater detail in upcoming labs, but you will see that you can define "host vars" in either the inventory file or in separate files that exist in a directory called `host_vars` (covered in the next section).

##### Step 8

Add a new task to the playbook to debug the `device_type` variable.

```yaml
---

  - name: USING THE DEBUG MODULE
    hosts: datacenter
    connection: local
    gather_facts: no

    tasks:
      - name: DEBUG AND PRINT TO TERMINAL
        debug: var=inventory_hostname

      - name: PRINT THE DEVICE TYPE TO THE TERMINAL
        debug:
          var: device_type  

```


> Note: the other syntax being used in the second task.  In all tasks with Ansible, you can use parameter=value as shown with `var=inventory_hostname` or parameter: value as shown with `var: device_type`.

##### Step 9

Save and re-run the playbook.

```
ntc@ntc:ansible$ ansible-playbook -i netdevices debug.yml 

```


```

ntc@ntc:ansible$ ansible-playbook -i netdevices debug.yml 

PLAY [USING THE DEBUG MODULE] *********************************************************************************

TASK [DEBUG AND PRINT TO TERMINAL] ****************************************************************************
ok: [sw1] => {
    "inventory_hostname": "sw1"
}
ok: [sw2] => {
    "inventory_hostname": "sw2"
}
ok: [router1] => {
    "inventory_hostname": "router1"
}
ok: [fw1usa] => {
    "inventory_hostname": "fw1usa"
}
ok: [fw2ie] => {
    "inventory_hostname": "fw2ie"
}

TASK [PRINT THE DEVICE TYPE TO THE TERMINAL] ******************************************************************
ok: [sw1] => {
    "device_type": "switch"
}
ok: [sw2] => {
    "device_type": "switch"
}
ok: [router1] => {
    "device_type": "router"
}
ok: [fw1usa] => {
    "device_type": "fw"
}
ok: [fw2ie] => {
    "device_type": "fw"
}

PLAY RECAP ****************************************************************************************************
fw1usa                     : ok=2    changed=0    unreachable=0    failed=0   
fw2ie                      : ok=2    changed=0    unreachable=0    failed=0   
router1                    : ok=2    changed=0    unreachable=0    failed=0   
sw1                        : ok=2    changed=0    unreachable=0    failed=0   
sw2                        : ok=2    changed=0    unreachable=0    failed=0   

ntc@ntc:ansible$ 

```


##### Step 10

In order to show the power of the **debug** module for variable checks, add a group variable into the inventory file like this:

```
[datacenter:vars]
device_type=unknown

```

This group variable will serve as a default value for `device_type` just in case there isn't a more specific value set as a host variable.

##### Step 11

Add two more devices (sw3 and router4) without host variables set like this:

```
[datacenter]
sw1  device_type=switch
sw2  device_type=switch
router1  device_type=router
fw1usa  device_type=fw
fw2ie  device_type=fw
sw3
router4

```


##### Step 12

Save and re-run the playbook.

```
ntc@ntc:ansible$ ansible-playbook -i netdevices debug.yml 

```

Pay close attention to each value of `device_type` that is shown.

```

ntc@ntc:ansible$ ansible-playbook -i netdevices debug.yml 

PLAY [USING THE DEBUG MODULE] *********************************************************************************

TASK [DEBUG AND PRINT TO TERMINAL] ****************************************************************************
ok: [sw1] => {
    "inventory_hostname": "sw1"
}
ok: [sw2] => {
    "inventory_hostname": "sw2"
}
ok: [router1] => {
    "inventory_hostname": "router1"
}
ok: [fw1usa] => {
    "inventory_hostname": "fw1usa"
}
ok: [fw2ie] => {
    "inventory_hostname": "fw2ie"
}
ok: [sw3] => {
    "inventory_hostname": "sw3"
}
ok: [router4] => {
    "inventory_hostname": "router4"
}

TASK [PRINT THE DEVICE TYPE TO THE TERMINAL] ******************************************************************
ok: [sw1] => {
    "device_type": "switch"
}
ok: [sw2] => {
    "device_type": "switch"
}
ok: [router1] => {
    "device_type": "router"
}
ok: [fw1usa] => {
    "device_type": "fw"
}
ok: [fw2ie] => {
    "device_type": "fw"
}
ok: [sw3] => {
    "device_type": "unknown"
}
ok: [router4] => {
    "device_type": "unknown"
}

PLAY RECAP ****************************************************************************************************
fw1usa                     : ok=2    changed=0    unreachable=0    failed=0   
fw2ie                      : ok=2    changed=0    unreachable=0    failed=0   
router1                    : ok=2    changed=0    unreachable=0    failed=0   
router4                    : ok=2    changed=0    unreachable=0    failed=0   
sw1                        : ok=2    changed=0    unreachable=0    failed=0   
sw2                        : ok=2    changed=0    unreachable=0    failed=0   
sw3                        : ok=2    changed=0    unreachable=0    failed=0   

ntc@ntc:ansible$
```

Using the **debug** module allows you to easily see what a given variable is set to at a given point in a playbook.





