## Lab 9 - Using the Core _config Module

### Task 1 - Using the *_config module for Global Configurations

In this task, you will use the config module to ensure certain configurations exist on network devices.

##### Step 1

Create a new playbook called the `core-config.yml`.  You should use the config module, i.e. **eos_config**, **nxos_config**, or **ios_config**. 

In your play definition, you can enter one of the following if you want to automate Nexus or Arista switches or Cisco CSR routers.

```yaml
---
  - name: CORE MODULES
    hosts: nxos-spines
    connection: local
    gather_facts: no

```

```yaml
---
  - name: CORE MODULES
    hosts: eos-spines
    connection: local
    gather_facts: no
```

```yaml
---
  - name: CORE MODULES
    hosts: iosxe
    connection: local
    gather_facts: no

```



##### Step 2

Create a variable called `provider` in the playbook that will be used to easily pass the same parameters into the these Ansible core modules.

```yaml
---
  - name: CORE MODULES
    hosts: <hosts you selected from previous step>
    connection: local
    gather_facts: no

    vars:
      provider:
        username: "{{ un }}"
        password: "{{ pwd }}"
        host: "{{ inventory_hostname }}"
    
    tasks:

```


##### Step 3

Add a new task using `*_config`. Use a tag called `snmp`:

```yaml
---
  - name: CORE MODULES
    hosts: iosxe # choose the right devices or group based on your OS
    connection: local
    gather_facts: no

    vars:
      provider:
        username: "{{ un }}"
        password: "{{ pwd }}"
        host: "{{ inventory_hostname }}"
    
    tasks:
      - ios_config:  # (choose the proper module if you're using eos or nxos)
          commands:
            - snmp-server location SYDNEY
            - snmp-server contact NTC_ADMIN
          provider: "{{ provider }}"
        tags: snmp
```

##### Step 4

Execute the playbook and just run the new task using `tags=snmp` and run it in verbose mode:

```
$ ansible-playbook -i inventory core-config.yml --tags=snmp -v
Using /etc/ansible/ansible.cfg as config file

PLAY [CORE] ********************************************************************

TASK [nxos_config] *************************************************************
changed: [nxos-spine1] => {"changed": true, "responses": [{}, {}], "updates": ["snmp-server location SYDNEY", "snmp-server contact NTC_ADMIN"]}
changed: [nxos-spine2] => {"changed": true, "responses": [{}, {}], "updates": ["snmp-server location SYDNEY", "snmp-server contact NTC_ADMIN"]}

PLAY [CORE] ********************************************************************

PLAY RECAP *********************************************************************
nxos-spine1                : ok=1    changed=1    unreachable=0    failed=0   
nxos-spine2                : ok=1    changed=1    unreachable=0    failed=0   


```


##### Step 5

Re-run the same playbook.

```
ntc@ntc:~/testing$ ansible-playbook -i inventory core-config.yml --tags=snmp -v
Using /etc/ansible/ansible.cfg as config file

PLAY [CORE] ********************************************************************

TASK [nxos_config] *************************************************************
ok: [nxos-spine2] => {"changed": false, "updates": []}
ok: [nxos-spine1] => {"changed": false, "updates": []}

PLAY [CORE] ********************************************************************

PLAY RECAP *********************************************************************
nxos-spine1                : ok=1    changed=0    unreachable=0    failed=0   
nxos-spine2                : ok=1    changed=0    unreachable=0    failed=0   

```

You should notice the same commands were NOT sent to device again because this module is doing a comparison against the active running configuration (by default).  This is no different than you saw in the first lab.

### Task 2 - Using the *_config module for Interface Configurations

##### Step 1

Re-locate the `provider` variable to `group_vars/all.yml` so it's no longer embedded in the playbook.

```yaml
---

provider:
  username: "{{ un }}"
  password: "{{ pwd }}"
  host: "{{ inventory_hostname }}"
    
```

##### Step 2

Create a new play in the same playbook for this task.  Tag the new play with the tag of "interfaces".

Add and configure a loopback10 interface with the description of "configured by Ansible" and an IP Address of "100.5.1.1/32" on CSR1,  "100.5.1.2/32" on CSR2, and "100.5.1.3/32" on CSR3.

Feel free to perform the same task in this play for other devices instead of IOS devices.  The solutions is very similar!

Note: use `ansible-doc ios_config` to view the available parameters.  Scroll all the way down to view the examples too.

```
SCROLL FOR THE SOLUTION
























































```
 

### Task 3 - Using the *_config to Deploy Configs from File

Use the "_config" module to deploy the following configuration snippet on either NXOS or EOS devices from a pre-built configuration file.

```
vlan 100
  name vlan_100_web
vlan 200
  name vlan_200_app
vlan 300
  name vlan_300_misc    
```


Perform this task using a new play in the playbook and tag the play with "config".

> Note: you cannot use the `commands` or `lines` parameter for this task.


```
SCROLL FOR THE SOLUTION























```



# Task 2 Solutions

### Cisco IOS

```yaml
---
  - name: CORE MODULES - PLAY 1
    hosts: iosxe # choose the right devices or group based on your OS
    connection: local
    gather_facts: no

    tasks:
      - ios_config:  # (choose the proper module if you're using eos or nxos)
          commands:
            - snmp-server location SYDNEY
            - snmp-server contact NTC_ADMIN
          provider: "{{ provider }}"
        tags: snmp

  - name: CORE MODULES - PLAY 2
    hosts: iosxe 
    connection: local
    gather_facts: no
    tags: interfaces

    tasks:
      - name: Ensure interface configuration on IOSXE
        ios_config:
          commands:
            - description Configured with Ansible
            - ip address 100.5.1.{{ loopback_id }} 255.255.255.255
          parents:
            - interface loopback10
          provider: "{{ provider }}"
        tags: interface  
```

But you also need a "host variable" for each device.  In the solution, we used `loopback_id`.  You can define a host var in the inventory file or in host vars files in the `host_vars` directory.

`host_vars/csr1.yml`

```yaml
---

loopback_id: 1
```


`host_vars/csr2.yml`

```yaml
---

loopback_id: 2
```

`host_vars/csr3.yml`

```yaml
---

loopback_id: 3
```


# Task 3 Solutions

```yaml


  - name: CORE MODULES
    hosts: nxos-spines
    connection: local
    gather_facts: no
    tags: config

    tasks:
      - name: DEPLOY CONFIGS FROM FILE
        ios_config:
          src: vlans.conf
          provider: "{{ provider }}"
  
```

You also need to create a file that stores the VLANs config.  Here we chose to use the file called `vlans.conf` that stores the config to deploy to the device.



# FULL & FINAL PLAYBOOK

```yaml
---
  - name: CORE MODULES - PLAY 1
    hosts: iosxe # choose the right devices or group based on your OS
    connection: local
    gather_facts: no

    tasks:
      - ios_config:  # (choose the proper module if you're using eos or nxos)
          commands:
            - snmp-server location SYDNEY
            - snmp-server contact NTC_ADMIN
          provider: "{{ provider }}"
        tags: snmp

  - name: CORE MODULES - PLAY 2
    hosts: iosxe 
    connection: local
    gather_facts: no
    tags: interfaces

    tasks:
      - name: Ensure interface configuration on IOSXE
        ios_config:
          commands:
            - description Configured with Ansible
            - ip address 100.5.1.{{ loopback_id }} 255.255.255.255
          parents:
            - interface loopback10
          provider: "{{ provider }}"
        tags: interface  


  - name: CORE MODULES - PLAY 3
    hosts: nxos-spines
    connection: local
    gather_facts: no
    tags: config

    tasks:
      - name: DEPLOY CONFIGS FROM FILE
        ios_config:
          src: vlans.conf
          provider: "{{ provider }}"
  
```

