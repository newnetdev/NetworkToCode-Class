## Lab 1 - Deploying "Basic" Configurations with Ansible

### Task 1

This lab provides an introduction to using Ansible creating your first playbook to deploy basic configurations.

##### Step 1

While in your home directory, create a new directory called `ansible` and then navigate into this new directory.

```
ntc@ntc:~$ mkdir ansible

ntc@ntc:~$ cd ansible/
ntc@ntc:ansible$ 
```

##### Step 2

Create an Ansible inventory file.  The name of this file is arbitrary--we'll use the name `lab-devices`. 

```
ntc@ntc:ansible$ touch lab-inventory
ntc@ntc:ansible$ 
```

##### Step 3

Open the file `lab-inventory` in your text editor of choice.


##### Step 4

For now, this will just be a very basic inventory file.  It'll only have a handful devices.

Based on your topology, you can add either three IOS devices to your inventory file or three IOS and Junos devices to your inventory for this lab. It is based on your course topology.

For now, you need to pick IOS **or** Junos devices.

After adding these devices, your inventory file should look like this

**Inventory File**

```
[ios-xe]
csr1
csr2
csr3

[junos]
vmx7
vmx8
vmx9

```

This inventory file has TWO groups: **ios-xe** and **junos**.  Each group has THREE devices.  For the course, each of these devices are reachable by name, but you can also use an IP address if you didn't have devices in DNS or `/etc/hosts`.


> Note: you should be able to ping each device by name


We now have a _very_ basic inventory file that we can use to get started.

##### Step 5

Create a file called `snmp-config-01.yml`.  This will be your first playbook.

Once it's created, open the file in your text editor.

##### Step 6

Add the following to your playbook.

```yaml
---

  - name: PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS
    hosts: ios-xe
    connection: local
    gather_facts: no

    tasks:

      - name: TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES
        ios_config:
          provider:
            host: "{{ inventory_hostname }}"
          commands:
            - snmp-server community ntc-course RO
            - snmp-server location NYC_HQ
            - snmp-server contact JOHN_SMITH

```

This is a single play with a single task -- you can take note of the descriptions found next to the `name` key, but remember the file itself is the playbook.  The playbook consists of a list of plays and each play consists of a list of tasks.  

In the task above, there are three SNMP commands defined.  This task will ensure those commands exist on the devices that are defined next to the `hosts:` key in the play definition.


Here are some other details on the task you should be aware of:
  * `ios_config` is the module name
  * `provider` and `commands` are parameters the module supports, e.g. the parameters are passed into the module.  
  * Technically `lines` is the parameter and `commands` is an alias for `lines` since they are just "lines" within a config file.
  * Take note of the data type of each parameter.  `provider` is a dictionary - you can see this based on the indentation.  `commands` is a list as can be inferred from the hyphens in YAML.
  * `name` is an optional task attribute that maps to arbitrary text that is displayed when you run the playbook providing context on where in the playbook execution you are.  You'll see this in the next step!



##### Step 7

Execute the playbook using the following Linux command:

```
ansible-playbook -i lab-inventory snmp-config-01.yml -u ntc -k
```

Few notes about this command:
* We are using the `ansible-playbook` program to execute the playbook
* The `-i` flag maps to the inventory file to used when running this playbook - in our case, that's `lab-inventory`
* `snmp-config-01.yml` is the playbook we are executing
* The `-u` flag maps to the username needed to login to the network devices
* The `-k` flag states to prompt for the password needed to login to the network devices

Now execute the playbook:

```
ntc@ntc:ansible$ ansible-playbook -i lab-inventory snmp-config-01.yml -u ntc -k
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


##### Step 8

Re-run the exame exact playbook.

```
ntc@ntc:ansible$ ansible-playbook -i lab-inventory snmp-config-01.yml -u ntc -k
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

This task is highlighting the fact that the **ios_config** module is idempotent.  This means you can now run the playbook 10000 times, but Ansible will only ever make the change once.

> Note: Ansible itself is not idempotent--the modules are.  Therefore, there can be modules that are NOT idempotent.  Be sure to understand how each module works before running them in production.


##### Step 9

Add a _second_ play to the playbook using the `junos_config` module to configure the same SNMP settings on the three Junos vMX devices.

```yaml
  - name: PLAY 2 - DEPLOYING SNMP CONFIGURATIONS ON JUNOS
    hosts: junos
    connection: local
    gather_facts: no

    tasks:

      - name: TASK 1 in PLAY 2 - ENSURE SNMP COMMANDS EXIST ON JUNOS DEVICES
        junos_config:
          provider:
            host: "{{ inventory_hostname }}"
          lines:
            - set snmp community public authorization read-only
            - set snmp location NYC_HQ
            - set snmp contact JOHN_SMITH
```

After adding this new play, the full playbook will look like this:

```yaml
---

  - name: PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS
    hosts: ios-xe
    connection: local
    gather_facts: no

    tasks:

      - name: TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES
        ios_config:
          provider:
            host: "{{ inventory_hostname }}"
          commands:
            - snmp-server community ntc-course RO
            - snmp-server location NYC_HQ
            - snmp-server contact JOHN_SMITH

  - name: PLAY 2 - DEPLOYING SNMP CONFIGURATIONS ON JUNOS
    hosts: junos
    connection: local
    gather_facts: no

    tasks:

      - name: TASK 1 in PLAY 2 - ENSURE SNMP COMMANDS EXIST ON JUNOS DEVICES
        junos_config:
          provider:
            host: "{{ inventory_hostname }}"
          lines:
            - set snmp community public authorization read-only
            - set snmp location NYC_HQ
            - set snmp contact JOHN_SMITH
    
```

Save the new playbook.

##### Step 10

With the Juniper play added to the playbook, re-execute the playbook.

```
ntc@ntc:ansible$ ansible-playbook -i lab-inventory snmp-config-01.yml -u ntc -k
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

Take note of the PLAY RECAP.  You can see that the *changed* flag is 0 for all IOS CSR devices because no change occurred.  However, notice how *changed* is 1 for each Juniper vMX device since a change occurred.

##### Step 11

Re-run the playbook one more time ensuring you don't see any changes.

```
ntc@ntc:ansible$ ansible-playbook -i lab-inventory snmp-config-01.yml -u ntc -k
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


##### Step 12

You probably don't want to enter your credentials every time you run a playbook.  

While not recommended for production, the next for learning Ansible, is to put your credentials in your playbook.

Update the `provider` parameter in both tasks to the following:

```yaml
          provider:
            host: "{{ inventory_hostname }}"
            username: ntc
            password: ntc123
```


##### Step 13

Re-run the playbook.  This time DO NOT USE the `-u` and `-k` flags.

```
ntc@ntc:ansible$ ansible-playbook -i lab-inventory snmp-config-01.yml

# output omitted - same as Step 11
```


##### Step 14

Clearly, you don't want to hard-code names and passwords into a playbook.  For one, it's not secure, and two, you'd have to change them in multiple locations if your password ever changes.

For group called "all", add two group based variables back in your inventory file.  

* `un` and set it to "ntc"
* `pwd` and set it to "ntc123"

The updated inventory file should look like this:

```
[all:vars]
un=ntc
pwd=ntc123

[ios-xe]
csr1
csr2
csr3

[junos]
vmx7
vmx8
vmx9
```

##### Step 15

Now that the inventory file is updated, we need to reference the new variables in the playbook.  Remove the hard-coded usernames and passwords and reference the variables as such:

```yaml
          provider:
            host: "{{ inventory_hostname }}"
            username: "{{ un }}"
            password: "{{ pwd }}"
```


The updated playbook should look like this:

```yaml
---

  - name: PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS
    hosts: ios-xe
    connection: local
    gather_facts: no

    tasks:

      - name: TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES
        ios_config:
          provider:
            host: "{{ inventory_hostname }}"
            username: "{{ un }}"
            password: "{{ pwd }}"
          commands:
            - snmp-server community ntc-course RO
            - snmp-server location NYC_HQ
            - snmp-server contact JOHN_SMITH

  - name: PLAY 2 - DEPLOYING SNMP CONFIGURATIONS ON JUNOS
    hosts: junos
    connection: local
    gather_facts: no

    tasks:

      - name: TASK 1 in PLAY 2 - ENSURE SNMP COMMANDS EXIST ON JUNOS DEVICES
        junos_config:
          provider:
            host: "{{ inventory_hostname }}"
            username: "{{ un }}"
            password: "{{ pwd }}"
          lines:
            - set snmp community public authorization read-only
            - set snmp location NYC_HQ
            - set snmp contact JOHN_SMITH
    

```


##### Step 16

Re-run the playbook ensuring everything is correct from a syntax perspective and still works.


```
ntc@ntc:ansible$ ansible-playbook -i lab-inventory snmp-config-01.yml

```


In upcoming labs, we'll show how to simplify using `provider` even more when we get into more depth on variables and module parameters!

### Task 2 - Deploying from a file

##### Step 1

Create a directory called `configs` and navigate to the directory.


```
ntc@ntc:ansible$ mkdir configs
ntc@ntc:ansible$ cd configs
ntc@ntc:configs$

```

##### Step 2

Create 2 files that will contain the SNMP configuration - one for Cisco and one for Juniper respectively.

```
ntc@ntc:configs$ touch junos-snmp.cfg 
ntc@ntc:configs$ touch ios-snmp.cfg
ntc@ntc:configs$
```

##### Step 3

Open the `ios-snmp.cfg` file in vi, nano, sublime text etc. and copy the following configuration lines to it.

```
snmp-server community ntc-course RO
snmp-server location NYC_HQ        
snmp-server contact JOHN_SMITH     
                                   
```

Save this file.


##### Step 4

Now open `junos-snmp.cfg` in a text editor and copy the following `junos` snmp configuration commands into it.

```
set snmp community public authorization read-only
set snmp location NYC_HQ
set snmp contact JOHN_SMITH
```

Save this file.

##### Step 5

Navigate back to the `ansible` directory and touch a new playbook file.

```
ntc@ntc:ansible$ touch snmp-config-02.yml
ntc@ntc:ansible$
```

##### Step 6

Open this file with a text editor and create 2 plays similar to **Task1** to deploy the changes. This time, however, we will use the source file to deploy the configuration.


```yaml
---

  - name: PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS
    hosts: ios-xe
    connection: local
    gather_facts: no

    tasks:

      - name: TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES
        ios_config:
          provider:
            host: "{{ inventory_hostname }}"
            username: "{{ un }}"
            password: "{{ pwd }}"
          src: ./configs/ios-snmp.cfg

  - name: PLAY 2 - DEPLOYING SNMP CONFIGURATIONS ON JUNOS
    hosts: junos
    connection: local
    gather_facts: no

    tasks:

      - name: TASK 1 in PLAY 2 - ENSURE SNMP COMMANDS EXIST ON JUNOS DEVICES
        junos_config:
          provider:
            host: "{{ inventory_hostname }}"
            username: "{{ un }}"
            password: "{{ pwd }}"
          src: ./configs/junos-snmp.cfg
    

```

##### Step 7

Run the playbook.


```
ntc@ntc:ansible$ ansible-playbook -i lab-inventory snmp-config-02.yml
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

