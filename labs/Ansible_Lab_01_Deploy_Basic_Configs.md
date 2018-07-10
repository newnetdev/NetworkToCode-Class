## Lab 1 - Deploying "Basic" Configurations with Ansible

### Task 1 - Managing SNMP Global Configuration Commands for IOS

This lab provides an introduction to using Ansible creating your first playbook to deploy basic configurations.

##### Step 1

While in your home directory, create a new directory called `ansible` and then navigate into this new directory.

```
ntc@ntc:~$ mkdir ansible

ntc@ntc:~$ cd ansible/
ntc@ntc:ansible$ 
```

##### Step 2

Create an Ansible inventory file.  The name of this file is arbitrary--we'll use the name `inventory`. 

```
ntc@ntc:ansible$ touch inventory
ntc@ntc:ansible$ 
```

##### Step 3

Open the file `inventory` in your text editor of choice.


##### Step 4

For now, this will just be a very basic inventory file.  It'll only have a handful devices.  We'll continue to build on this through the course.

Based on your topology, you can add either three IOS devices to your inventory file or three IOS and Junos devices to your inventory for this lab. 

> It is based on your course topology.

After adding these devices, your inventory file should look like this

**Inventory File**

```
[iosxe]
csr1
csr2
csr3

[vmx]
vmx7
vmx8
vmx9

```

This inventory file has **TWO** groups: **iosxe** and **vmx**.  Each group has THREE devices.  For the course, each of these devices are reachable by name, but you can also use an IP address if you didn't have devices in DNS or `/etc/hosts`.


> Note: you should be able to ping each device by name


We now have a basic inventory file that we can use to get started.

##### Step 5

Create a file called `snmp-config-01.yml`.  This will be your first playbook.

Once it's created, open the file in your text editor.

##### Step 6

Add the following to your playbook.

```yaml
---

  - name: PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS
    hosts: iosxe
    connection: network_cli
    gather_facts: no

    tasks:

      - name: TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES
        ios_config:
          commands:
            - snmp-server community ntc-course RO
            - snmp-server location NYC_HQ
            - snmp-server contact JOHN_SMITH

```

This is a single play with a single task -- you can take note of the descriptions found next to the `name` key, but remember the file itself is the playbook.  The playbook consists of a list of plays and each play consists of a list of tasks.  

In the task above, there are three SNMP commands defined.  This task will ensure those commands exist on the devices that are defined next to the `hosts:` key in the play definition.


Here are some other details on the task you should be aware of:
  * `ios_config` is the module name
  * Technically `lines` is the parameter and `commands` is an alias for `lines` since they are just "lines" within a config file.
  * Take note of the data type of `commands` - it is a list as can be inferred from the hyphens in YAML.
  * `name` is an optional task attribute that maps to arbitrary text that is displayed when you run the playbook providing context on where in the playbook execution you are.  You'll see this in the next step!



##### Step 7

Execute the playbook using the following Linux command:

```
ntc@ntc:ansible$ ansible-playbook -i inventory snmp-config-01.yml -u ntc -k
```

Few notes about this command:
* We are using the `ansible-playbook` program to execute the playbook
* The `-i` flag maps to the inventory file to used when running this playbook - in our case, that's `inventory`
* `snmp-config-01.yml` is the playbook we are executing
* The `-u` flag maps to the username needed to login to the network devices
* The `-k` flag states to prompt for the password needed to login to the network devices

Now execute the playbook:

```
ntc@ntc:ansible$ ansible-playbook -i inventory snmp-config-01.yml -u ntc -k
SSH password: 


PLAY [PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS] **********************************************************

TASK [TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES] *******************************************
changed: [csr1]
changed: [csr2]
changed: [csr3]

PLAY RECAP ****************************************************************************************************
csr1                       : ok=1    changed=1    unreachable=0    failed=0   
csr2                       : ok=1    changed=1    unreachable=0    failed=0   
csr3                       : ok=1    changed=1    unreachable=0    failed=0   

ntc@ntc:ansible$ 
```

You should have seen **changed** for each device.  This is because the devices didn't have this configuration yet and an actual change was applied to each device.

Also take note of the **PLAY RECAP**.  This is a summary of:

* how many tasks by device occurred successfully denoted by _ok_
* how many tasks by device made a configuration change denoted by _changed_ 
* how many devices are unreachable and how many tasks failed, also broken down by device.


At this point, you've ran your first playbook and have successfully configured SNMP on several devices!

### Task 2 - Understanding Idempotency

##### Step 1

Re-run the same exact playbook as the last task:

```
ntc@ntc:ansible$ ansible-playbook -i inventory snmp-config-01.yml -u ntc -k
SSH password: 

PLAY [PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS] **********************************************************

TASK [TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES] *******************************************
ok: [csr2]
ok: [csr1]
ok: [csr3]

PLAY RECAP ****************************************************************************************************
csr1                       : ok=1    changed=0    unreachable=0    failed=0   
csr2                       : ok=1    changed=0    unreachable=0    failed=0   
csr3                       : ok=1    changed=0    unreachable=0    failed=0   

ntc@ntc:ansible$
```

Do you see the difference from the previous output?

This task is highlighting the fact that the **ios_config** module is idempotent.  

**This means you can now run the playbook 10000 times, but Ansible will only ever make the change once.**

> Note: Ansible itself is not idempotent--the modules are.  Therefore, there can be modules that are NOT idempotent.  Be sure to understand how each module works before running them in production.


### Task 3 - Managing SNMP Configuration Commands for Junos

##### Step 1

Add a _second_ play to the same playbook using the `junos_config` module to configure the same SNMP settings on the three Junos vMX devices.

```yaml
  - name: PLAY 2 - DEPLOYING SNMP CONFIGURATIONS ON JUNOS
    hosts: vmx
    connection: local
    gather_facts: no

    tasks:

      - name: TASK 1 in PLAY 2 - ENSURE SNMP COMMANDS EXIST ON JUNOS DEVICES
        junos_config:
          lines:
            - set snmp community public authorization read-only
            - set snmp location NYC_HQ
            - set snmp contact JOHN_SMITH
```

After adding this new play, the full playbook will look like this:

```yaml
---

  - name: PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS
    hosts: iosxe
    connection: network_cli
    gather_facts: no

    tasks:

      - name: TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES
        ios_config:
          commands:
            - snmp-server community ntc-course RO
            - snmp-server location NYC_HQ
            - snmp-server contact JOHN_SMITH

  - name: PLAY 2 - DEPLOYING SNMP CONFIGURATIONS ON JUNOS
    hosts: vmx
    connection: local
    gather_facts: no

    tasks:

      - name: TASK 1 in PLAY 2 - ENSURE SNMP COMMANDS EXIST ON JUNOS DEVICES
        junos_config:
          lines:
            - set snmp community public authorization read-only
            - set snmp location NYC_HQ
            - set snmp contact JOHN_SMITH
    
```

Save the new playbook.

##### Step 2

With the Juniper play added to the playbook, re-execute the playbook.

```
ntc@ntc:ansible$ ansible-playbook -i inventory snmp-config-01.yml -u ntc -k
SSH password: 

PLAY [PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS] **********************************************************

TASK [TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES] *******************************************
ok: [csr3]
ok: [csr2]
ok: [csr1]

PLAY [PLAY 2 - DEPLOYING SNMP CONFIGURATIONS ON JUNOS] ********************************************************

TASK [TASK 1 in PLAY 2 - ENSURE SNMP COMMANDS EXIST ON JUNOS DEVICES] *****************************************
changed: [vmx9]
changed: [vmx8]
changed: [vmx7]

PLAY RECAP ****************************************************************************************************
csr1                       : ok=1    changed=0    unreachable=0    failed=0   
csr2                       : ok=1    changed=0    unreachable=0    failed=0   
csr3                       : ok=1    changed=0    unreachable=0    failed=0   
vmx7                       : ok=1    changed=1    unreachable=0    failed=0   
vmx8                       : ok=1    changed=1    unreachable=0    failed=0   
vmx9                       : ok=1    changed=1    unreachable=0    failed=0   

ntc@ntc:ansible$
```

Take note of the PLAY RECAP.  You can see that the *changed* flag is 0 for all IOS CSR devices because no change occurred (because the **ios_config** module is idempotent).  

However, notice how *changed* is equal to 1 for each Juniper vMX device since a change occurred.

##### Step 3

Re-run the playbook one more time ensuring you don't see any changes.

```
ntc@ntc:ansible$ ansible-playbook -i inventory snmp-config-01.yml -u ntc -k
SSH password: 

PLAY [PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS] **********************************************************

TASK [TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES] *******************************************
ok: [csr2]
ok: [csr1]
ok: [csr3]

PLAY [PLAY 2 - DEPLOYING SNMP CONFIGURATIONS ON JUNOS] ********************************************************

TASK [TASK 1 in PLAY 2 - ENSURE SNMP COMMANDS EXIST ON JUNOS DEVICES] *****************************************
ok: [vmx8]
ok: [vmx9]
ok: [vmx7]

PLAY RECAP ****************************************************************************************************
csr1                       : ok=1    changed=0    unreachable=0    failed=0   
csr2                       : ok=1    changed=0    unreachable=0    failed=0   
csr3                       : ok=1    changed=0    unreachable=0    failed=0   
vmx7                       : ok=1    changed=0    unreachable=0    failed=0   
vmx8                       : ok=1    changed=0    unreachable=0    failed=0   
vmx9                       : ok=1    changed=0    unreachable=0    failed=0   

ntc@ntc:ansible$ 
```


### Task 3 - Using Inventory Parameters (Variables)

In this task, we're going to introduce two inventory parameters that are helpful to be aware of when using Ansible.  They are `ansible_host`, `ansible_pass` and will be used to simplify passing in credentials when executing playbooks.


##### Step 1

You probably don't want to enter your credentials every time you run a playbook.  

While not necessarily recommended for production, the next for learning Ansible, is to put your credentials in your inventory file.

Add the following to the top of your inventory file:

```
[all:vars]
ansible_user=ntc
```

This is assigning the value of "ntc" to the built-in Ansible variable called `ansible_user` for **all** devices.  The syntax above the variable is required for "group variables" in the inventory file.  In this case, the group name used is an implicit group called **all**.

##### Step 2

Execute the same playbook.  This time do not use the `-u` flag.

```
ntc@ntc:ansible$ ansible-playbook -i inventory snmp-config-01.yml -k
SSH password: 
# output omitted
```

Notice how the `ansible_user` parameter is being used for your device username now.

##### Step 3

Add the `ansible_ssh_pass` variable to your inventory file.  Assign it the value of `ntc123`.

```
[all:vars]
ansible_user=ntc
ansible_ssh_pass=ntc123



```

This is assigning the value of "ntc" to the built-in Ansible variable called `ansible_ssh_pass` which is used as the password to login to your devices.


##### Step 4

Re-run the playbook.  

This time DO NOT USE either the `-u` and `-k` flags.

```
ntc@ntc:ansible$ ansible-playbook -i inventory snmp-config-01.yml

# output omitted - same as Step 11
```


The updated playbook should look like this:

```yaml
---

  - name: PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS
    hosts: iosxe
    connection: network_cli
    gather_facts: no

    tasks:

      - name: TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES
        ios_config:
          commands:
            - snmp-server community ntc-course RO
            - snmp-server location NYC_HQ
            - snmp-server contact JOHN_SMITH

  - name: PLAY 2 - DEPLOYING SNMP CONFIGURATIONS ON JUNOS
    hosts: vmx
    connection: local
    gather_facts: no

    tasks:

      - name: TASK 1 in PLAY 2 - ENSURE SNMP COMMANDS EXIST ON JUNOS DEVICES
        junos_config:
          lines:
            - set snmp community public authorization read-only
            - set snmp location NYC_HQ
            - set snmp contact JOHN_SMITH
    

```


##### Step 5

Re-run the playbook ensuring everything is correct from a syntax perspective and still works.

```
ntc@ntc:ansible$ ansible-playbook -i inventory snmp-config-01.yml

```

