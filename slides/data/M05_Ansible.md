layout: true

.footer-picture[![Network to Code Logo](data/media/Footer2.PNG)]
.footnote-left[(C) 2018 Network to Code, LLC. All Rights Reserved. ]
.footnote-con[CONFIDENTIAL]

---

class: center, middle, title
.footer-picture[<img src="data/media/Footer1.PNG" alt="Blue Logo" style="alight:middle;width:350px;height:60px;">]

# Introduction to Ansible by RedHat


---

# What is Ansible by RedHat?

- Founded in 2012
- Acquired by RedHat in 2015
- Open source DevOps Configuration management, automation, and orchestration platform
- Low barrier to entry with no programming skills necessary
- Batteries included
- 900+ modules
- Built its home for application deployments in cloud environments
- Rapidly gaining traction for network automation


---

# Diving into Ansible

- Written in Python
- Extended in any language (not common for open source modules)
- Native integration with Jinja2 templates
- Automation instructions are defined in YAML
- **Agentless**

<br>

**We cover Jinja2 and YAML in the course.**

---

# How Ansible Works
.center[
<img src="data/media/how-ansible-works.png" alt="How Ansible Works" style="alight:middle;width:1025px;height:475px;">
]

---

# How Ansible Works
.left-column[
**Automating Linux Servers**

- Uses SSH to connect to the server
- Server does not have Ansible installed
- Copies Python code to the server (server must have Python execution engine)
- Server executes code and returns status of tasks


**Automating Network Devices**

- Python code runs _locally_ on the Ansible control host (where Ansible is installed)
- Equivalent of writing Python scripts on a single server
- No code is copied to the device
- Device does not need to support SSH or Python
]

.right-column[
<img src="data/media/ansible_ssh_both.png" alt="Ansible SSH" style="alight:right;width:500px;height:480px;">
]
---

# Ansible Architecture

.center[
<img src="data/media/ansible-arch.png" alt="Ansible Architecture" style="alight:middle;width:700px;height:480px;">
]


---

# Ansible Tower

.center[
<img src="data/media/ansible-arch-tower.png" alt="Ansible Tower" style="alight:middle;width:700px;height:475px;">
]

---


class: center, middle, title

.footer-picture[<img src="data/media/Footer1.PNG" alt="Blue Logo" style="alight:middle;width:350px;height:60px;">]


# What's Possible with Ansible?
## Example Ansible Playbooks

---


# Updating SNMP Community strings

```yaml
---

  - name: DEPLOY SNMP COMMUNITY STRINGS ON IOS DEVICES
    hosts: iosxe

    tasks:

    - name: USE COMMANDS IN THE PLAYBOOK
      ios_config:
        lines:
          - "snmp-server community ntc123 ro"

    - name: DEPLOY FROM CONFIG FILE
      ios_config:
        src: "configs/snmp.cfg"

    - name: DEPLOY USING JINJA2 TEMPLATE
      ios_config:
        src: "snmp.j2"


```




---

# Upgrade Cisco NX-OS Devices


```yaml
---

  - name: UPGRADE NEXUS SWITCHES
    hosts: nxos

    tasks:

      - name: ENSURE SCP SERVER IS ENABLED
        nxos_feature:
          feature: scp-server
          state: enabled

      - name: ENSURE FILE EXISTS ON DEVICE
        nxos_file_copy:
          local_file: "../os-images/cisco/nxos/nxos.7.0.3.I2.2d.bin"

      - name: PERFORM THE UPGRADE
        nxos_install_os:
          system_image_file: nxos.7.0.3.I2.2d.bin

```

Note: a more seamless upgrade requires a few more tasks.


---

# Backup Configuration and Restore

```yaml
---

  - name: BACKUP AND RESTORE
    hosts: "eos,junos"

    tasks:

      - name: BACKUP CONFIGS
        ntc_save_config:
          host={{ inventory_hostname }}
          username={{ ansible_user }}
          password={{ ansible_ssh_pass }}
          local_file=backups/{{ inventory_hostname }}.cfg
          platform={{ ntc_vendor }}_{{ ansible_network_os }}_{{ ntc_api }}
        tags: backup

      - name: DEPLOY CONFIGS
        napalm_install_config:
          hostname={{ inventory_hostname }}
          username={{ ansible_user }}
          password={{ ansible_ssh_pass }}
          config_file=backups/{{ inventory_hostname }}.cfg
          diff_file=diffs/{{ inventory_hostname }}.diffs
          replace_config=true
          commit_changes=true
          dev_os={{ ansible_network_os }}
        tags: restore

```

---

# Auto-Configure Interface Descriptions

Configure interface descriptions based on active neighbors

```yaml
---

  - name: Auto-configure port descriptions
    hosts: nxos

    tasks:

      - name: GET NEIGHBOR INFORMATION
        ntc_show_command:
          connection=ssh
          platform={{ ntc_vendor }}_{{ ansible_network_os }}
          command='show lldp neighbors'
        register: neighbors

      - name: AUTO-CONFIGURE PORT DESCRIPTIONS BASED ON LLDP DATA
        nxos_interface:
          interface: "{{ item.local_interface  }}"
          description: "Connects to {{ item.neighbor_interface }} on {{ item.neighbor }}"
        loop: "{{ neighbors.response|flatten(levels=1) }}"
        when: item.local_interface != 'mgmt0'
```


---

class: center, middle, title
.footer-picture[<img src="data/media/Footer1.PNG" alt="Blue Logo" style="alight:middle;width:350px;height:60px;">]

# Ansible for Network Automation


---

class: middle, segue

# Introduction to Ansible
### Ansible for Network Automation

---

# Ansible Terminology

.left-column2[
- Inventory
- Playbooks
- Plays
- Tasks
- Modules
- Parameters
- Variables
]

.right-column2[.med-code[
```yaml
---

- name: vlan testing
  hosts: dc1
  connection: network_cli
  gather_facts: no

  tasks:

    - name: ensure VLAN 10 exists
      nxos_vlan: vlan_id=10 name=web_vlan host={{ inventory_hostname }}

    - name: ensure VLAN 10 does NOT exist
      nxos_vlan: vlan_id=10 name=web_vlan host={{ inventory_hostname }} state=absent
```
]]

---


# Automating with Ansible

Two files are required to get started:

- **Inventory file**
- Playbook


---

# Inventory File

Inventory Basics

<br>


.left-column[
- ini like file that statically defines which devices are automated
- Uses IP addresses or FQDNs
- The name of the inventory file is arbitrary
]


.right-column[.big-code[
```ini
10.1.1.1
switch1.ntc.com
r1.ntc.com
r2

```
]]


---

# Inventory Groups (cont'd)


.left-column[.big-code[
All devices are in a implicit group called **all**.

```yaml
10.1.1.1
switch1.ntc.com
r1.ntc.com
r2

```
]]


.right-column[.big-code[
Three groups: **all**, **switches**, **routers**.

```yaml
[switches]
10.1.1.1
switch1.ntc.com

[routers]
r1.ntc.com
r2

```
]]

---

# Inventory Groups (cont'd)

.left-column[.big-code[
Three groups: **all**, **switches**, **routers**.

```yaml
[switches]
10.1.1.1
switch1.ntc.com

[routers]
r1.ntc.com
r2

```
]]

.right-column[.big-code[
Four groups: **all**, **switches**, **routers**, and **nyc**.

```yaml
[nyc:children]
switches
routers

[switches]
10.1.1.1
switch1.ntc.com

[routers]
r1.ntc.com
r2

```
]]


---


# Inventory Variables


- Group based variables
- Host based variables

<br>

**Host, or more specific variables, take priority.**


---

# Group Variables

.left-column[.big-code[
Four groups: **all**, **switches**, **routers**, and **nyc**.

Devices can be in more than one group.

```yaml
[nyc:children]
switches
routers

[switches]
10.1.1.1
switch1.ntc.com

[routers]
r1.ntc.com
r2

```
]]

.right-column[
Define group variables under `[<group-name>:vars]`

Location of group variables does not matter

```yaml
[all:vars]
ansible_user=ntc
ansible_ssh_pass=ntc123
snmp_ro=networktocode

[nyc:children]
switches
routers

[switches]
10.1.1.1
switch1.ntc.com

[routers]
r1.ntc.com
r2

[routers:vars]
snmp_ro=netcode-routers

```
]


---

# Host Variables

.left-column[
Define host variables on the same line as the host.

```yaml
[all:vars]
ansible_user=ntc
ansible_ssh_pass=ntc123
snmp_ro=networktocode

[nyc:children]
switches
routers

[switches]
10.1.1.1
switch1.ntc.com   snmp_ro=public123 password=ntc

[routers]
r1.ntc.com
r2                snmp_ro=not-secure

[routers:vars]
snmp_ro=netcode-routers

```
]



---

# Inventory File - Example

.left-column[
```bash
[all:vars]
location=AMERS
ansible_user=admin
ansible_ssh_pass=admin

[routers]
r1.ntc.com  mgmt_ip=1.1.1.1
r2.ntc.com  mgmt_ip=1.1.1.2

[routers:vars]
ansible_ssh_pass=secret

[switches]
s1.ntc.com  mgmt_ip=1.1.2.1  ansible_ssh_pass=supersecret
s2.ntc.com  mgmt_ip=1.1.2.2

[switches:vars]
location=EMEA

```

]

.right-column[
<html>
<head>
<style>
table {
    font-family: arial, sans-serif;
    font-size: 18px;
    border-collapse: collapse;
    width: 80%;
    margin-left: auto;
    margin-right: auto;
}

td, th {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 8px;
}

tr:nth-child(even) {
    background-color: #dddddd;
}
</style>
</head>
<body>

<table>
  <tr>
    <th></th>
    <th>username</th>
    <th>password</th>
    <th>mgmt_ip</th>
    <th>location</th>
  </tr>
  <tr>
    <td>r1.ntc.com</td>
    <td>admin</td>
    <td>secret</td>
    <td>1.1.1.1</td>
    <td>AMERS</td>
  </tr>
  <tr>
    <td>r2.ntc.com</td>
    <td>admin</td>
    <td>secret</td>
    <td>1.1.1.2</td>
    <td>AMERS</td>
  </tr>
  <tr>
    <td>s1.ntc.com</td>
    <td>admin</td>
    <td>supersecret</td>
    <td>1.1.2.1</td>
    <td>EMEA</td>
  <tr>
    <td>s2.ntc.com</td>
    <td>admin</td>
    <td>admin</td>
    <td>1.1.2.2</td>
    <td>EMEA</td>
  </tr>
</table>

</body>
</html>


]


---


# Automating with Ansible

Two files are required to get started:

- Inventory file
- **Playbook**


---

# What is the Playbook?

**Ansible uses sports terminology to define the tasks to be automated.**

- A playbook contains plays
- Plays contain tasks
- Tasks _do the automation_


---

# Playbook

.left-column[
- Contains instruction set on tasks to be automated
- name of the playbook is arbitrary
- Uses YAML data format
- Playbook contains one or more plays
]

.right-column[.big-code[
```yaml
---
















# empty playbook (pb.yml)
# blank canvas
```
]]

---

# Play(s)

.left-column[
- Begins with a hyphen
  - denotes list of plays (YAML list)
- `name`
  - arbitrary description of the play and is displayed to terminal when executed (optional)
- `hosts`
  - one or more hosts or groups as defined in inventory file or _expression_
- `connection: network_cli`
  - does not use default SSH connection mechanism / use method as defined *inside* modules
- Play contains one or more tasks
]

.right-column[.big-code[
```yaml
---

- name: Play 1 - Deploy router configs
  hosts: routers
  connection: network_cli
  gather_facts: no

  tasks:

    # list of tasks


```
]]
--
.right-column[.big-code[
```yaml
- name: Play 2 - Deploy vlans on switches
  hosts: switches
  connection: network_cli
  gather_facts: no

  tasks:

```
]]

---

# Task(s)

.left-column[
- One or more tasks comprise a play
- Executed on devices defined in inventory file
- Each task:
  - Executes a module using specified parameters (key/value pairs)
  - `name`: optional, arbitrary text displayed when task is executed
- There is more than one supported syntax
  - Native YAML is recommended
]

.right-column[.big-code[
```yaml
---

- name: PLAY 1 - Deploy vlans on switches
  hosts: switches
  connection: network_cli
  gather_facts: no

  tasks:

    - name: TASK ONE - DEPLOY THE NETWORK
      MODULE_NAME:
        key1: value1
        key2: value

    - name: TASK TWO - BACKUP CONFIG
      MODULE_NAME: k1=v1 k2=v2 k3=v3




```
]]

---

# Idempotency

- Modules that perform a change _should_ only make the change once (the first execution)
- You can run the task a 1000 and it'll only occur once

---


# Modules, Parameters, and Variables

.left-column[
- Modules
  - Idempotent
  - Mostly written in Python
  - Parameterized
- Parameters
- Variables are accessed by using curly braces
- `inventory_hostname` - built-in variable referencing device name in inventory file
]

.right-column[.med-code[
```yaml
---

- name: MANAGE VLANS
  hosts: switches
  connection: network_cli
  gather_facts: no

  tasks:

    - name: ensure VLAN exists
      nxos_vlan:
        vlan_id: 10
        name: web_vlan
        state: present
        host: "{{ inventory_hostname }}"
        username: "{{ ansible_user }}"
        password: "{{ ansible_ssh_pass }}"

```
]]

---

# Executing a Playbook


To execute the Playbook, Explicitly state which inventory file is used, and then the Playbook.

```bash
$ ansible-playbook -i <inventory-file> <playbook.yml>
```
```bash
$ ansible-playbook -i inventory deploy-vlans.yml
```


<br>

To prompt the user for a login username, use the `-u` or `--user=` flag, to prompt the user for a login password 
use the  `-k` or `--ask-pass` flag. 

```bash
$ ansible-playbook -i inventory snmp-config.yml -u ntc -k
SSH password: 

```



---

class: center, middle

# Before the First Lab

---

# Playbook Task Syntax

.left-column[

**Recommended YAML Syntax (key:value)**

```yaml
---

- name: MANAGE VLANS
  hosts: switches
  connection: network_cli
  gather_facts: no

  tasks:

    - name: ensure VLAN exists
      nxos_vlan:
        vlan_id: 10
        host: "{{ inventory_hostname }}"
        username: "{{ username }}"
        password: "{{ password }}"

    # no curly braces used with var parameter
    - debug:
        var: inventory_hostname

```
]

.right-column[

**Vertical and/or Horizontal (key=value)**

```yaml
---

- name: MANAGE VLANS
  hosts: switches
  connection: network_cli
  gather_facts: no

  tasks:

    - name: ensure VLAN exists
      nxos_vlan:
        vlan_id=10
        host={{ inventory_hostname }}
        username={{ username }}
        password={{ password }}

    - name: ensure VLAN exists
      nxos_vlan: vlan_id=10 host={{ inventory_hostname }} username={{ username }} password={{ password }}

    # no curly braces used with var parameter
    - debug: var=inventory_hostname

```
]

---

# Module Documentation

* Mini-demo
* Understand the parameters each module supports
  * Choices, defaults, and description
* [docs.ansible.com](docs.ansible.com)
* `ansible-doc nxos_vlan`


---

# Lab Time

- Lab 1 - Deploying "Basic" Configurations with Ansible
  - Write Your First Ansible Playbook that will configure SNMP setting on 6 devices! 
        - 3 IOS and 3 JUNOS devices
- Lab 2 - Deploying Configs From a File
  - Shows how to push configuration using files.


---

class: middle, segue

# Understanding Variables
### Ansible for Network Automation


---

# Variables

- Group based variables
- Host based variables
- Special variables
- Extra variables

<br>

There are more types that we'll cover, but we're still just getting started.

---

# Group Based Variables

- They can be defined in the inventory file or within a directory called `group_vars`
- Variables that are specific to a group.
- Accessible within playbooks and templates

```bash
# inventory
[eos]
eos-spine1
eos-spine2

[ios]
csr1
csr2
```

.med-code[
```bash
.
├── inventory
├── pb.yml
├── group_vars
│   ├── all.yml
│   ├── eos.yml
│   └── ios.yml
```
]


---

# Group Based Variables (cont'd)

- You can alternatively create a directory equal to the group name and have individual files in that directory

```bash
# inventory
[eos]
eos-spine1
eos-spine2

[ios]
csr1
csr2
```

.med-code[
```bash
.
├── inventory
├── pb.yml
├── group_vars
│   ├── eos
│   │   ├── aaa.yml
│   │   └── interfaces.yml
│   └── ios
│       ├── aaa.yml
│       └── interfaces.yml

```
]

---

# Host Based Variables

- They can be defined in the inventory file or within a directory called `host_vars`
- Variables that are specific to a host.
- Accessible within playbooks and templates

.big-code[
```bash
.
├── inventory
├── pb.yml
├── group_vars
│   ├── all.yml
│   ├── eos.yml
│   └── ios.yml
├── host_vars
│   ├── csr1.yml
│   ├── csr2.yml
│   ├── eos-spine1.yml
│   └── eos-spine2.yml
```
]

---


# Host Based Variables (cont'd)

- You can alternatively create a directory equal to the host name and have individual files in that directory

.big-code[
```bash
.
├── inventory
├── pb.yml
├── host_vars
│   ├── csr1
│   │   ├── aaa.yml
│   │   └── interfaces.yml
│   └── eos-spine1
│       ├── aaa.yml
│       └── interfaces.yml

```
]

---


# Variable Priority

- You can define host and group variables in the inventory file and respective host vars and group vars files
- The host variable file takes priority over the group variable file

<br>

You can **Prove** variable priority: using the **debug** module


---

# Special (Built-in) Variables

**Ansible has several built-in, _special_, variables**

<html>
<head>
<style>
table {
    font-family: arial, sans-serif;
    font-size: 18px;
    border-collapse: collapse;
    width: 80%;
    margin-left: auto;
    margin-right: auto;
}

td, th {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 8px;
}

tr:nth-child(even) {
    background-color: #dddddd;
}
</style>
</head>
<body>

<table>
  <tr>
    <th>Variable</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>inventory_hostname</td>
    <td>Name of the current host as defined in the inventory file.</td>
  </tr>
  <tr>
    <td>ansible_host</td>
    <td>Helpful if inventory hostname is not in DNS or /etc/hosts.  Set to IP address of host and use instead of inventory_hostname to access IP/FQDN</td>
  </tr>
  <tr>
    <td>hostvars</td>
    <td>Dictionary- it's keys are Ansible host names (inventory_hostname) and values is dictionary of every variable that host has (flattend)</td>
  </tr>
  <tr>
    <td>play_hosts</td>
    <td>A list of inventory hostnames that are in scope for the current play </td>
  </tr>
  <tr>
    <td>group_names</td>
    <td>List of all groups that the current host is a member of</td>
  </tr>
  <tr>
    <td>groups</td>
    <td>A dictionary- keys are all group names defined in the inventory file and values are list of host names that are members of the group.</td>
  </tr>
  <tr>
    <td>ansible_version</td>
    <td>Dictionary representing Ansible major, minor, revision of the release.</td>
  </tr>
</table>

</body>
</html>

---

# Extra Variables

- Known as "extra vars"
- Variables passed into a playbook upon execution.
- Highest priority

```yaml
---

  - name: DEMO PLAYBOOK
    hosts: "{{ devices }}"

    tasks:
      ...
      ...
      ...
```

Pass variables using `-e` or `--extra-vars`

```bash
$ ansible-playbook -i inventory playbook.yml -e "devices=all"
$ ansible-playbook -i inventory playbook.yml -e "devices=eos"
$ ansible-playbook -i inventory playbook.yml --extra-vars "devices=eos"
```

---

# User Input

You can request user input and capture the user response as a variable using the `var_prompt` module.  The `name` under `vars_prompt` is the variable name where the user input will be captured.

```yaml
---

- name: COLLECT USERNAME AND PASSWORD
  hosts: csr1
  gather_facts: no
  connection: network_cli

  vars_prompt:
    - name: un
      prompt: "Please enter the username"
      private: no
```

By default Ansible does not echo user input back to the terminal.  To allow user input to be echoed back to to the terminal set the `private` parameter to `no`.


---

class: middle

# debug module and Playbook Variables
### Print and Verify Variable Assignment

---

# Playbook Variables

Ansible uses Jinja2 syntax for variables within a playbook,
and uses curly brackets to indicate a variable, like `{{ vlan }}`


Variables within a playbook can be defined under the optional `vars` paramater

```yaml
---
- name: PRINT VLANS
  hosts: all
  gather_facts: no
  connection: network_cli
  
  vars:
    vlan: 300
  
  tasks:
    - name: PRINT HOSTNAME
      debug: 
        msg: "The VLAN is {{ vlan }}"
```


Since Ansible uses `“{{ var }}”` for variables, 
if a value after a colon starts with a “{”, YAML will think it is a Python dictionary,
 so you must put quotation marks around it, if it is not already enclosed in quotes



---

# Playbook Variable Results


.left-column[
As an example, the playbook below uses both a custom Playbook variable, `priority`, 
and the Ansible built-in `inventory_hostname` variable

```yaml
---
- name: PRINT HOSTS
  hosts: all
  gather_facts: no
  connection: network_cli
  
  vars:
    priority: "P1" 
  
  tasks:
    - name: PRINT HOSTNAME
      debug: 
        msg: "{{ inventory_hostname }} has a priority of {{ priority }}"
```


]

.right-column[
Note the inventory_hostname iterates through all the hosts, yet the `priority` variable stays the same

```bash
$ ansible-playbook -i inventory var_test.yml

PLAY [PRINT HOSTS] ******************************

TASK [PRINT HOSTNAME] ***************************

ok: [csr2] => {
    "msg": "csr2 has a priority of P1"
}
ok: [csr1] => {
    "msg": "csr1 has a priority of P1"
}
ok: [csr3] => {
    "msg": "csr3 has a priority of P1"
}
ok: [nxos-spine1] => {
    "msg": "nxos-spine1 has a priority of P1"
}
ok: [nxos-spine2] => {
    "msg": "nxos-spine2 has a priority of P1"
}
# other hosts truncated for brevity
```


]

---


# debug module

.left-column[
```bash
# inventory

[all:vars]
anisble_user=ntc
ansible_ssh_pass=ntc123

[datacenter]
leaf1 mgmt_ip=10.1.1.1 ansible_ssh_pass=admin123
leaf2 mgmt_ip=10.1.1.2

```


```yaml
---

  - name: DEBUGGING VARIABLES
    hosts: all
    connection: network_cli
    gather_facts: no

    tasks:

      - name: PRINT INVENTORY HOSTNAME
        debug: var=inventory_hostname
```

.med-code[
```bash
.
├── inventory
├── test-pb.yml
```
]


]
--

.right-column[.s2-code[
```bash
$ ansible-playbook -i inventory debug.yml

PLAY [DEBUGGING VARIABLES] **************************************************

TASK [PRINT INVENTORY HOSTNAME] *********************************************
ok: [leaf1] => {
    "inventory_hostname": "leaf1"
}
ok: [leaf2] => {
    "inventory_hostname": "leaf2"
}

PLAY RECAP ******************************************************************
leaf1                      : ok=1    changed=0    unreachable=0    failed=0
leaf2                      : ok=1    changed=0    unreachable=0    failed=0
```

]
]

---


# debug module

.left-column[
```bash
# inventory

[all:vars]
ansible_user=ntc
ansible_ssh_pass=ntc123

[datacenter]
leaf1 mgmt_ip=10.1.1.1 ansible_ssh_pass=admin123
leaf2 mgmt_ip=10.1.1.2

```


```yaml
---

  - name: DEBUGGING VARIABLES
    hosts: all
    connection: network_cli
    gather_facts: no

    tasks:

      - name: PRINT PASSWORD
        debug: var=ansible_ssh_pass
```

.med-code[
```bash
.
├── inventory
├── test-pb.yml
```
]


]
--

.right-column[.s2-code[
```bash
$ ansible-playbook -i inventory debug.yml

PLAY [DEBUGGING VARIABLES] **************************************************

TASK [PRINT INVENTORY HOSTNAME] *********************************************
ok: [leaf1] => {
    "ansible_ssh_pass": "admin123"
}
ok: [leaf2] => {
    "ansible_ssh_pass": "ntc123"
}

PLAY RECAP ******************************************************************
leaf1                      : ok=1    changed=0    unreachable=0    failed=0
leaf2                      : ok=1    changed=0    unreachable=0    failed=0
```

]
]


---

# debug module

.left-column[
```bash
# inventory

[all:vars]
ansible_user=ntc
ansible_ssh_pass=ntc123

[datacenter]
leaf1 mgmt_ip=10.1.1.1 ansible_ssh_pass=admin123
leaf2 mgmt_ip=10.1.1.2

```


```yaml
---

  - name: DEBUGGING VARIABLES
    hosts: all
    connection: network_cli
    gather_facts: no

    tasks:

      - name: PRINT MGMT IP
        debug: msg="THE MGMT IP IS {{ mgmt_ip }}"
```

.med-code[
```bash
.
├── inventory
├── test-pb.yml
```
]


]
--

.right-column[.s2-code[
```bash
$ ansible-playbook -i inventory debug.yml

PLAY [DEBUGGING VARIABLES] **************************************************

TASK [PRINT MGMT IP] ********************************************************
ok: [leaf1] => {
    "msg": "THE MGMT IP IS 10.1.1.1"
}
ok: [leaf2] => {
    "msg": "THE MGMT IP IS 10.1.1.2"
}

PLAY RECAP ******************************************************************
leaf1                      : ok=1    changed=0    unreachable=0    failed=0
leaf2                      : ok=1    changed=0    unreachable=0    failed=0


```
]
]



---

# Modules return JSON Data

* Every module returns JSON Data
* You can view this data by running a playbook in verbose mode (`-v`)
* For example, data returned includes commands being sent to the network device


```bash
PLAY [MANAGE VLANS] ************************************************************

TASK [ensure VLAN exists] ******************************************************
changed: [nxos-spine1] => {"changed": true, "end_state": {"admin_state": "up", "mapped_vni": "", "name": "VLAN0010",
"vlan_id": "10", "vlan_state": "active"}, "end_state_vlans_list": ["1", "10"], "existing": {},
"existing_vlans_list": ["1"], "proposed": {}, "proposed_vlans_list": ["10"], "updates": ["vlan 10", "exit"]}

TASK [ensure VLAN exists] ******************************************************
ok: [nxos-spine1] => {"changed": false, "end_state": {"admin_state": "up", "mapped_vni": "", "name": "VLAN0010",
"vlan_id": "10", "vlan_state": "active"}, "end_state_vlans_list": ["1", "10"], "existing": {"admin_state": "up",
"mapped_vni": "", "name": "VLAN0010", "vlan_id": "10", "vlan_state": "active"}, "existing_vlans_list": ["1", "10"],
"proposed": {}, "proposed_vlans_list": ["10"], "updates": []}

TASK [debug] *******************************************************************
ok: [nxos-spine1] => {
    "inventory_hostname": "nxos-spine1"
}

PLAY RECAP *********************************************************************
nxos-spine1                : ok=3    changed=0    unreachable=0    failed=0
```

---

# Understanding the "check" mode

* Does not make configuration changes - dry run
* Verbose mode in combination with the `--check` flag shows the actual commands

.left-column[
.s2-code[
``` yaml
---

  - name: PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS
    hosts: ios-xe
    connection: network_cli
    gather_facts: no

    tasks:

      - name: TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES
        ios_config:
          commands:
            - snmp-server community ntc-course RO
            - snmp-server community supersecret RW
            - snmp-server location NYC_HQ_COLO
            - snmp-server contact JOHN_SMITH
```
]
]
.right-column[
.small-code[
```bash
ntc@ntc:ansible$ ansible-playbook -i lab-inventory snmp-config-02.yml --check -v
Using /etc/ansible/ansible.cfg as config file

PLAY [PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS] *********************************

TASK [TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES] ******************
changed: [csr3] => {"banners": {}, "changed": true, "commands": ["snmp-server location
 NYC_HQ_COLO"], "failed": false, "updates": ["snmp-server location NYC_HQ_COLO"]}
changed: [csr2] => {"banners": {}, "changed": true, "commands": ["snmp-server location
 NYC_HQ_COLO"], "failed": false, "updates": ["snmp-server location NYC_HQ_COLO"]}
changed: [csr1] => {"banners": {}, "changed": true, "commands": ["snmp-server location
 NYC_HQ_COLO"], "failed": false, "updates": ["snmp-server location NYC_HQ_COLO"]}

PLAY RECAP ***************************************************************************
csr1                       : ok=1    changed=1    unreachable=0    failed=0
csr2                       : ok=1    changed=1    unreachable=0    failed=0
csr3                       : ok=1    changed=1    unreachable=0    failed=0

ntc@ntc:ansible$

```
]
]

---

# Lab Time

- Lab 3 - Using Check Mode and Verbosity
- Lab 4 - Building the course inventory file
- Lab 5 - Using the debug module
- Lab 6 - Prompting the User for Input

---

class: middle, segue

# Jinja2 Templates
### Ansible for Network Automation


---


# Templating


- Manual method:
  - Enterprises have golden configuration standard for type of device, location of device etc
  - This is updated and deployed, for a new device coming into the network


- Automated templates:
  - Jinja2 provides a way to write these golden configs as skeleton templates with variables
  - Ansible provides the variables to the template and renders configuration using the `template` module.



---

# Jinja2 Basics

A Jinja2 file is a text file with the `j2` file extension (optionally),
and indicates variables with double curly brackets `{{ variable }}`

Here is an example of a jinja file for an interface config. 

```
interface {{ int_type }} 1/1
  no shut
```

Jinja will render the template with the input of whatever the value of the variable 
`int_type` is set to be, such as "GigabitEthernet"

```
interface GigabitEthernet 1/1
  no shut
```

---

# Jinja2 Syntax
.left-column[
Jinja2 is a Python based template rendering language. The syntax for loops, conditionals and
dictionary look ups are similar to Python.

Sample input:
```yaml
snmp_config:
  ro:
    - public
    - ntc-course
  rw:
    - private
    - ntc-private
  contact: netops_team
  location: MILAN


```
]

.right-column[
Iterating over a List (nested within the dictionary of snmp_config)
 input will print the config line with each item in the list
```
{% for ro_comm in snmp_config.ro %}
snmp-server community {{ ro_comm }} RO
{% endfor %}
```

Accessing a dictionary value using the `.` operator like Python:
```
snmp-server location {{ snmp_config.location }}
```
]

---


# The Ansible template module
The basic usage of the template module in Ansible:


```yaml

    - name: RENDER CONFIGURATIONS
      template:
        src: device_config.j2
        dest: "./configs/{{ inventory_hostname }}.cfg

```

---


# Jinja2 and the *_config modules

Within the network core config modules (like ios_config, junos_config etc). You can specify a Jinja2 template as a src file rather than a config file.

```yaml
    - name: ENSURE THAT SNMP IS CONFIGURED ON IOS DEVICES
      ios_config:
        src: 02-ios-snmp.j2

```

```yaml
    - name: ENSURE THAT SNMP IS CONFIGURED ON JUNOS DEVICES
      junos_config:
        src: 02-junos-snmp.j2

```

---

# Lab Time

- Lab 7 - Getting Started with Jinja2 Templating in Ansible
- Lab 8 - Using Improved Jinja2 Templates


---

class: middle, segue

# Backing up and Restoring Configurations
### Ansible for Network Automation

---

# Backing Up Configuration Files

- **ntc_show_command** - built on top of `pyntc` and part of the **ntc-ansible** project
- Supports Junos, IOS, NX-OS, and EOS
- Save the running configuration as a file to the Ansible control host.

```yaml
  - name: BACKUP ALL CONFIGURATIONS
    hosts: all
    connection: network_cli
    gather_facts: no

    tasks:
      - name: BACKUP CONFIG
        ntc_show_command:
          platform: cisco_ios
          command: show running
          host: "{{ inventory_hostname }}"
          username: "{{ ansible_user }}"
          password: "{{ ansible_ssh_pass }}"
          local_file: ./backups/{{ inventory_hostname }}.cfg

```

**There are other way to backup config files too, which we'll look at later**

---

# Limit the Devices being Automated

* Use `--limit` command line flag to limit the groups or hosts being automated.
* Must be a sub-set of the devices in the `hosts: group` in the playbook.

```bash
ansible-playbook -i inventory playbook.yml --limit nxos
```

```bash
ansible-playbook -i inventory playbook.yml --limit nxos-spine1
```


```bash
ansible-playbook -i inventory playbook.yml --limit nxos,eos,csr1
```


---

class: middle, segue

# Introduction to NAPALM
### Managing Device Configuration (includes re-storing configurations)



---


# NAPALM

_NAPALM (Network Automation and Programmability Abstraction Layer with Multivendor support) is a Python library that implements a set of functions to interact with different network device Operating Systems using a unified API._

_NAPALM supports several methods to connect to the devices, to manipulate configurations or to retrieve data._

**Also has associated Ansible Modules**

https://napalm.readthedocs.io/en/latest/


---

# NAPALM

.left-column[
Three core functions:

* Retrieving Data
* Declarative Configuration Management
* Deployment Validation

All three are done in a uniform and vendor-neutral fashion
]

.right-column[.center[![NAPALM](data/media/napalm-logo.png)]
]


---

# NAPALM Support Matrix

* Palo Alto PANOS
* Cisco IOS
* Cisco NX-OS
* Cisco IOS-XR
* Arista EOS
* Juniper Junos
* IBM
* Pluribus
* FortiOS
* Cumulus Linux
* Actively growing


---

class: ubuntu

# Retrieving Data

**Uses a uniform and consistent data model across all device types supported by NAPALM**

.left-column[

- Facts
- ARP Table
- BGP Configuration
- BGP Neighbors
- BGP Neighbor Detail
- Interface
- Interface Counters
- LLDP neighbors
- LLDP neighbors detail
]

.right-column[
- NTP Peers
- NTP Stats
- NTP Servers
- ... plus another dozen and actively growing...
]


---


# NAPALM Facts

Network Device Facts

```bash
{
    "os_version": "4.15.2F-2663444.4152F",
    "uptime": 5837,
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

---


# Interfaces

.left-column[

```bash
{
    "Management1": {
        "is_enabled": true,
        "description": "",
        "last_flapped": 1467419703.0212176,
        "is_up": true,
        "mac_address": "2c:c2:60:0d:52:90",
        "speed": 1000
    },
    "Ethernet2": {
        "is_enabled": true,
        "description": "",
        "last_flapped": 1467419702.7812023,
        "is_up": true,
        "mac_address": "2c:c2:60:12:98:52",
        "speed": 1000
    },
    "Ethernet3": {
        "is_enabled": true,
        "description": "",
        "last_flapped": 1467419702.7812028,
        "is_up": true,
        "mac_address": "2c:c2:60:60:20:9b",
        "speed": 1000
    },
```
]

.right-column[

```bash
    "Ethernet1": {
        "is_enabled": true,
        "description": "",
        "last_flapped": 1467419702.781203,
        "is_up": true,
        "mac_address": "2c:c2:60:48:80:70",
        "speed": 1000
    },
    "Ethernet5": {
        "is_enabled": true,
        "description": "",
        "last_flapped": 1467419702.8092043,
        "is_up": true,
        "mac_address": "2c:c2:60:40:8d:10",
        "speed": 1000
    },
    "Ethernet4": {
        "is_enabled": true,
        "description": "",
        "last_flapped": 1467419702.7692015,
        "is_up": true,
        "mac_address": "2c:c2:60:2e:c6:f8",
        "speed": 1000
    }
}


```
]

---


# Layer 3 Interfaces

Get Interfaces IP Addresses

.big-code[
```bash
{
   "Management1":{
      "ipv4":{
         "10.0.0.11":{
            "prefix_length":24
         }
      },
      "ipv6":{

      }
   }
}
```
]

---



# Environment

Device Environment Status

.big-code[
```bash
{
    "fans": {},
    "cpu": {
        "0": {
            "%usage": 5.4
        }
    },
    "temperature": {},
    "power": {},
    "memory": {
        "available_ram": 99060,
        "used_ram": 1798476
    }
}
```
]


---

# NAPALM Configuration Management

Two main ways to manage device configurations with NAPALM

**Configuration Replace**

* Declarative configuration always pushing the full configuration
* Only commands required to get the device into its intended state are applied
* No "negation (no)" commands are sent to the device


**Configuration Merge**

* Send a set of commands or configuration stanza
* Only commands required to get the device into its intended state are applied
* You can use the merge for declarative management on a stanza based on OS

It does vary based on operating system.


---

# NAPALM Configuration Management

**Example Workflow**

Works slightly different than based on individual drivers and operating systems.

1. Connect to Device
2. Copy desired configuration to device (checkpoint file/rollback, candidate configuration, config session, bootflash as candidate_config.txt)
3. Use a vendor command to view diffs
4. Use a vendor command apply configuration changes
5. Optionally, rollback to a config that exists in the file system.

Note: you dictate if the supplied configuration is a full config file or partial configuration

---

# Configuration Replace

Focus on desired configuration commands.

There are no `no` commands used.  The underlying OS generates the diffs (for most NAPALM drivers).

.big-code[
```bash
$ more diffs/csr1.diffs
+hostname csr1
-hostname csr_old_name
-interface Loopback100
 -ip address 1.1.1.1 255.255.255.255
-interface Loopback200
 -ip address 22.2.1.1 255.255.255.255
-ip route 10.1.1.0 255.255.255.0 192.0.1.1
```
]

Full configuration is sent to the device, but only diffs are applied. You do not need to worry about going from A to B - you just focus on B.


---

# Configuration Merge

You can use NAPALM for declarative management for a sectional config too.

.left-column[
.med-code[
Current BGP Config
```bash
router bgp 65512
   neighbor 10.0.0.0 remote-as 65500
   neighbor 10.0.0.0 maximum-routes 12000
   neighbor 10.0.0.1 remote-as 65512
   neighbor 10.0.0.1 maximum-routes 12000
   network 20.20.20.0/24
!
```

Desired BGP Config (file sent to device)
```bash
router bgp 65512
   neighbor 10.0.0.2 remote-as 65500
   neighbor 10.0.0.2 maximum-routes 12000
   neighbor 10.0.0.1 remote-as 65512
   neighbor 10.0.0.1 maximum-routes 12000
   neighbor 10.0.0.10 remote-as 65512
   network 100.0.100.0/24
!

```
]
]

--

.right-column[
.med-code[
Diff Generated by NAPALM
```bash
    neighbor 10.0.0.0 maximum-routes 12000
    neighbor 10.0.0.1 remote-as 65512
    neighbor 10.0.0.1 maximum-routes 12000
+   neighbor 10.0.0.2 remote-as 65500
+   neighbor 10.0.0.2 maximum-routes 12000
+   neighbor 10.0.0.10 remote-as 65512
+   neighbor 10.0.0.10 maximum-routes 12000
    network 20.20.20.0/24
+   network 100.0.100.0/24
 !
 management api http-commands
    protocol http

```

]
]

---

# Configuration Merge (Advanced)

You can use NAPALM for declarative management for a sectional config too.

.left-column[
Current BGP Config
```bash
router bgp 65512
   neighbor 10.0.0.0 remote-as 65500
   neighbor 10.0.0.0 maximum-routes 12000
   neighbor 10.0.0.1 remote-as 65512
   neighbor 10.0.0.1 maximum-routes 12000
   network 20.20.20.0/24
!
```

Desired BGP Config (file sent to device)
```bash
no router bgp 65512
router bgp 65512
   neighbor 10.0.0.2 remote-as 65500
   neighbor 10.0.0.2 maximum-routes 12000
   neighbor 10.0.0.1 remote-as 65512
   neighbor 10.0.0.1 maximum-routes 12000
   neighbor 10.0.0.10 remote-as 65512
   network 100.0.100.0/24
!

```
]

--

.right-column[
Diff Generated by NAPALM
```bash
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


```
Be cautious of device support.  This is based on NAPALM driver implementation which is dictated by vendor OS support.  This example is EOS.
]

---

# NAPALM Ansible Module

.center[<img src="data/media/napalm-install-config.png" alt="NAPALM install_config" style="alight:middle;width:525px;height:515px;">]

---

# NAPALM Ansible Module (cont'd)

* NAPALM module using a task attribute called `tags`.
* Tags are used to selectively run particular tasks

```yaml

  # backup tasks

  - name: DEPLOY CONFIGURATION
    napalm_install_config:
      dev_os={{ ansible_network_os }}
      config_file=./backups/{{ inventory_hostname }}.cfg   # file with commands to apply
      commit_changes=true                                  # apply changes (or only generate diffs)
      replace_config=true                                  # full config replace or merge (just a few commands)
      diff_file=./diffs/{{ inventory_hostname }}.diffs     # file to save diffs.  You can view diffs before committing changes
      hostname={{ inventory_hostname }}
      username={{ ansible_user  }}
      password={{ ansible_ssh_pass }}
    tags: deploy
```

Save and Run the playbook.

```bash
$ ansible-playbook -i inventory backup.yml --limit nxos --tags=deploy
```

---

# Selectively Execute Tasks and/or Plays

* Can assign one or more tags (using a list)
* `tags` can be used for plays and/or tasks

.left-column[

```yaml
- name: VLAN CHANGE
  nxos_vlan:
    vlan_id: "10"
    host: "{{ inventory_hostname }}"
    username: "{{ username }}"
    password: "{{ password }}"
  tags: vlan
```

```yaml
- name: VLAN DEMO
  nxos_vlan: vlan_id=10 host={{ inventory_hostame }}
  tags:
    - cisco
    - nxos
    - vlan

```

```bash
ansible-playbook -i inventory playbook.yml --tags=vlan
```
]

.right-column[

```yaml
  - name: DATA CENTER AUTOMATION
    hosts: all
    gather_facts: no
    connection: network_cli
    tags: datacenter
```

```bash
ansible-playbook -i inventory playbook.yml --tags=datacenter
```

]



---

# lineinfile

- Add/Remove a line to a file
- Use regexes to match for position
- Insert before/after

```yaml
- name: Ensure a line does not exist
  lineinfile: line="Building configuration..." dest=backups/{{ inventory_hostname }}.cfg state=absent
```

```yaml
- name: Ensure the line that matches the regex does not exist
  lineinfile:
    dest: "backups/{{ inventory_hostname }}.cfg"
    regexp: "Current configuration .*"
    state: "absent"

```

```bash
!
Building configuration...

Current configuration 3942 Bytes
!
hostname nycr01
```

---

# Lab Time

- Lab 9 - Backup and Restore Network Configurations Part 1
- Lab 10 - Backup and Restore Network Configurations Part 2

---

class: middle, segue

# Build / Push Configuration Management
### Ansible for Network Automation

---

# Build / Push

- One approach to _pushing_ configurations is to use the _build / push_ method
- Especially useful for initial device provisioning

.center[
<img src="data/media/build-push.png" alt="Build Push" style="alight:middle;width:900px;height:400px;">
]

---

# Build

- De-compose existing configuration files (example)
  - VLANs
  - Interfaces
  - SNMP
- Create template(s)
- Create YAML Variable(s) files
- Render templates with variables

---

# Network Configuration Building

.center[
<img src="data/media/ansible-templating.png" alt="Ansible Templating" style="alight:middle;width:600px;height:405px;">
]

---

# Jinja2 Templates

.left-column[

Standard config file

```bash
snmp-server community PUBLIC123 RO 5
snmp-server community PRIVATE123 RW 95
snmp-server location GLOBAL
snmp-server contact LOCAL_ADMIN
snmp-server host 1.1.1.1

vlan 10
 name web_servers
vlan 20
vlan 30
 name db_servers

interface Ethernet1
  no shutdown
interface Ethernet2
  no shutdown
interface Ethernet3
  shutdown
interface Ethernet4
  no shutdown
interface Ethernet5
  shutdown
```

]
--
.right-column[

De-constructed config as a template

```bash
snmp-server community {{ snmp_ro }} RO 5
snmp-server community {{ snmp_rw }} RW 95
snmp-server location {{ snmp_location }}
snmp-server contact {{ snmp_contact }}
snmp-server host {{ snmp_trap_dest }}

{% for vlan in vlans %}
vlan {{ vlan.id }}
{% if vlan.get('name') %}
 name {{ vlan.name }}
{% endif %}
{% endfor %}

{% for interface in interfaces %}
interface {{ interface.name }}
{% if interface.admin == 'up' %}
  no shutdown
{% elif interface.admin == 'down' %}
  shutdown
{% endif %}
{% endfor %}
```
]

---


# Templates & Variables

.left-column[

`templates/config.j2`

```bash
snmp-server community {{ snmp_ro }} RO 5
snmp-server community {{ snmp_rw }} RW 95
snmp-server location {{ snmp_location }}
snmp-server contact {{ snmp_contact }}
snmp-server host {{ snmp_trap_dest }}


{% for vlan in vlans %}
vlan {{ vlan.id }}
{% if vlan.get('name') %}
 name {{ vlan.name }}
{% endif %}
{% endfor %}


{% for interface in interfaces %}
interface {{ interface.name }}
{% if interface.admin == 'up' %}
  no shutdown
{% elif interface.admin == 'down' %}
  shutdown
{% endif %}
{% endfor %}
```
]
--
.right-column[
`group_vars/all.yml`
```yaml
snmp_ro: PUBLIC123
snmp_rw: PRIVATE123
snmp_location: GLOBAL
snmp_contact: LOCAL_ADMIN
snmp_trap_dest: 1.1.1.1


vlans:
  - id: 10
    name: web_servers
  - id: 20
  - id: 30
    name: db_servers



interfaces:
  - name: Ethernet1
    admin: up
  - { name: Ethernet2, admin: up }
  - { name: Ethernet3, admin: down }
  - { name: Ethernet4, admin: up }
  - { name: Ethernet5, admin: down }

```
]

---

# Data Modeling & Variables

Think through data inputs and impact it has on templates

.left-column[

```yaml
snmp_ro: PUBLIC123
snmp_rw: PRIVATE123
snmp_location: GLOBAL
snmp_contact: LOCAL_ADMIN
snmp_trap_dest: 1.1.1.1






vlans:
  - id: 10
    name: web_servers
  - id: 20
  - id: 30
    name: db_servers

```
]

.right-column[
```yaml
snmp:
  ro:
    - PUBLIC123
  rw:
    - PRIVATE123
  location: GLOBAL
  contact: LOCAL_ADMIN
  trap_dest:
    - 1.1.1.1


vlans:
  '10':
    name: web_servers
  '20': {}
  '30':
    name: db_servers
```
]

---


# Building Configurations

`build-push.yml`

```yaml
---

  - name: BUILD CONFIGS
    hosts: all
    connection: network_cli

    tasks:

      - name: BUILD NETWORK CONFIGURATIONS
        template: src=config.j2 dest=configs/{{ inventory_hostname }}.conf

```
--


```bash
.
├── build-push.yml
├── configs
│   ├── leaf1.conf
│   ├── leaf2.conf
│   ├── leaf3.conf
│   ├── leaf4.conf
├── group_vars
│   └── all.yml       # variables in scope by all devices
├── inventory
└── templates
    └── config.j2

```


---

# Optimizing the BUILD Process

- Build a directory per device

```yaml
      - name: ENSURE DIRECTORY EXISTS PER DEVICE (AND PARTIALS SUB-DIR)
        file: path=/home/ntc/ansible/configs/{{ inventory_hostname }}/partials state=directory
```

--

- De-construct single Jinja2 Template into individual templates

.left-column[
```bash
# templates/01_snmp.j2

snmp-server community {{ snmp_ro }} RO 5
snmp-server community {{ snmp_rw }} RW 95
snmp-server location {{ snmp_location }}
snmp-server contact {{ snmp_contact }}
snmp-server host {{ snmp_trap_dest }}
```

```bash
# templates/02_vlans.j2

{% for vlan in vlans %}
vlan {{ vlan.id }}
{% if vlan.get('name') %}
 name {{ vlan.name }}
{% endif %}
{% endfor %}
```

]

.right-column[
```bash
# templates/03_interfaces.j2

{% for interface in interfaces %}
interface {{ interface.name }}
{% if interface.admin == 'up' %}
  no shutdown
{% elif interface.admin == 'down' %}
  shutdown
{% endif %}
{% endfor %}

```
]

---

# Optimizing the BUILD Process (cont'd)

- Create configuration snippets

```yaml
  - name: BUILD NETWORK CONFIGURATIONS
    template: src=templates/01_snmp.j2 dest=configs/{{ inventory_hostname }}/partials/01_snmp.conf

  - name: BUILD NETWORK CONFIGURATIONS
    template: src=templates/02_vlans.j2 dest=configs/{{ inventory_hostname }}/partials/02_vlans.conf

  - name: BUILD NETWORK CONFIGURATIONS
    template: src=templates/03_interfaces.j2 dest=configs/{{ inventory_hostname }}/partials/03_interfaces.conf
```

- Assemble configuration snippets

```yaml
  - name: ASSEMBLE PARTIAL CONFIGURATIONS PER DEVICE INTO SINGLE CONFIG FILE
    assemble: src=configs/{{ inventory_hostname }}/partials dest=configs/{{ inventory_hostname }}/{{ inventory_hostname }}.conf

```

--

- Use a loop (iterator) instead of doing each one individually

```yaml
    - name: BUILD NETWORK CONFIGURATIONS
      template: src={{ item }} dest={{ item | basename | replace('j2', 'conf') }}
      with_fileglob:
        - templates/*
```

---

# Play 1 - _BUILD_

.s2-code[
```yaml
---

  - name: BUILD PROCESS
    hosts: all
    connection: network_cli
    gather_facts: no

    tasks:

      - name: ENSURE DIRECTORY EXISTS PER DEVICE (AND PARTIALS SUB-DIR)
        file: path=/home/ansible/configs/{{ inventory_hostname }}/partials state=directory

      - name: BUILD NETWORK CONFIGURATIONS
        template: src={{ item }} dest=configs/{{ item | basename | replace('j2', 'conf') }}
        with_fileglob:
          - templates/*

      - name: ASSEMBLE PARTIAL CONFIGURATIONS PER DEVICE INTO SINGLE CONFIG FILE
        assemble: src=configs/{{ inventory_hostname }}/partials dest=configs/{{ inventory_hostname }}/{{ inventory_hostname }}.conf
```
]

---
# Play 2 - _PUSH_

```yaml
---

  - name: DEPLOY CONFIGURATIONS USING NAPALM
    hosts: all
    connection: network_cli

    tasks:

    - name: DEPLOY MERGE
      napalm_install_config:
        hostname={{ inventory_hostname }}
        username={{ ansible_user }}
        password={{ ansible_ssh_pass }}
        dev_os=eos
        config_file=configs/{{ inventory_hostname }}/{{ inventory_hostname }}.conf
        commit_changes=true
        replace_config=false
        diff_file=configs/{{ inventory_hostname }}/{{ inventory_hostname }}.diff
```

```bash
# inventory
[leaves]
leaf1
leaf2
leaf3
leaf4
leaf5
leaf6

```

---

# Build / Push Playbook

.small-code[
```yaml
---

  - name: BUILD PROCESS
    hosts: all
    connection: network_cli
    gather_facts: no
    tags: build

    tasks:

      - name: ENSURE DIRECTORY EXISTS PER DEVICE (AND PARTIALS SUB-DIR)
        file: path=/home/ansible/configs/{{ inventory_hostname }}/partials state=directory

      - name: BUILD NETWORK CONFIGURATIONS
        template: src={{ item }} dest=configs/{{ item | basename | replace('j2', 'conf') }}
        with_fileglob:
          - templates/*

      - name: ASSEMBLE PARTIAL CONFIGURATIONS PER DEVICE INTO SINGLE CONFIG FILE
        assemble: src=configs/{{ inventory_hostname }}/partials dest=configs/{{ inventory_hostname }}/{{ inventory_hostname }}.conf

  - name: DEPLOY CONFIGURATIONS USING NAPALM
    hosts: all
    connection: network_cli
    gather_facts: no
    tags: deploy

    tasks:

    - name: DEPLOY MERGE
      napalm_install_config:
        hostname={{ inventory_hostname }}
        username={{ ansible_user }}
        password={{ ansible_ssh_pass }}
        dev_os=eos
        config_file=configs/{{ inventory_hostname }}/{{ inventory_hostname }}.conf
        commit_changes=true
        replace_config=false
        diff_file=configs/{{ inventory_hostname }}/{{ inventory_hostname }}.diff
```

]


---

# Executing the Playbook

.med-code[
```bash
$ ansible-playbook build-push.yml --tags=build
```

- Only the push tasks

```bash
$ ansible-playbook build-push.yml --tags=push
```
- All

```bash
$ ansible-playbook build-push.yml
```
]

---

# Executing the Playbook (cont'd)

```bash
$ ansible-playbook -i inventory build-push.yml

PLAY [BUILD configs] **********************************************************

TASK: [ENSURE DIRs created per device] ****************************************
changed: [leaf1]
changed: [leaf2]
changed: [leaf3]
changed: [leaf4]
changed: [leaf5]
changed: [leaf6]

TASK: [BUILD service configs using template modules] **************************
changed: [leaf1] => (item=/home/ntc/ansible/templates/02_vlans.j2)
changed: [leaf1] => (item=/home/ntc/ansible/templates/01_snmp.j2)
changed: [leaf1] => (item=/home/ntc/ansible/templates/03_interfaces.j2)

TASK: [ASSEMBLE CONFIGS per device] *******************************************
changed: [leaf1]

PLAY [Push configs] ***********************************************************

TASK: [deploy configs] ********************************************************
changed: [leaf1]

PLAY RECAP ********************************************************************
leaf1                      : ok=4    changed=4    unreachable=0    failed=0

```

---


# Executing the Playbook (cont'd)


.left-column[

BEFORE:

```bash
.
├── build-push.yml
├── configs
├── group_vars
│   └── all.yml
├── inventory
└── templates
    ├── 01_snmp.j2
    ├── 02_vlans.j2
    └── 03_interfaces.j2
```
]

.right-column[
AFTER (for 2 devices):


```bash
.
├── build-push.yml
├── configs
│   └── leaf1
│       ├── leaf1.conf
│       └── partials
│           ├── 01_snmp.conf
│           ├── 02_vlans.conf
│           └── 03_interfaces.conf
│   └── leaf2
│       ├── leaf2.conf
│       └── partials
│           ├── 01_snmp.conf
│           ├── 02_vlans.conf
│           └── 03_interfaces.conf
├── group_vars
│   └── all.yml
├── inventory
└── templates
    ├── 01_snmp.j2
    ├── 02_vlans.j2
    └── 03_interfaces.j2

```
]



---


# List Tasks

- View all tasks that will be executed
- Great for architecture discussions and planning playbooks

```bash
$ ansible-playbook -i inventory build-push.yml --list-tasks

playbook: build-push.yml

  play #1 (BUILD PROCESS):  TAGS: [build]
    ENSURE DIRECTORY EXISTS PER DEVICE (AND PARTIALS SUB-DIR) TAGS: [build]
    BUILD NETWORK CONFIGURATIONS    TAGS: [build]
    ASSEMBLE PARTIAL CONFIGURATIONS PER DEVICE INTO SINGLE CONFIG FILE: [build]

  play #2 (Push configs):   TAGS: [push]
    DEPLOY MERGE  TAGS: [push]

```



---

# Summary

- Build requires building out one or more templates for your environment
  - Template per role
  - Template per service per role
  - Templates could become fragile
  - Good for initial device configuration
  - Possible to use ALL the time (install_config)
- Push
  - NAPALM provides a nice abstraction for pushing full and partial configurations to several device types
  - Always always test

---

# Lab Time

- Lab 11 - Build / Push with NAPALM
  - You will use the "template" and "napalm_install_config" modules
  - Choose any *1* vendor to complete this lab

---

class: middle, segue

# Ansible Core Modules
### Ansible for Network Automation

---

# Base Modules

We cover two types of base modules:

- *_command - Run arbitrary commands on devices
- *_config - Manage configuration sections on devices

The modules are vendor specific and usually support SSH plus a vendor API:
- iosxr_*
- ios_*
- eos_*
- junos_*
- nxos_*
- ops_*
- actively growing

---

# *_command

.left-column[

While the _config modules are used to make configuration changes and execute configuration commands, the _command module is used to pass enable and exec mode commands to the device.

The _command modules are often used to execute show commands and gather data from devices.

- `commands` parameter can accept a single command or a list of commands
- Refer to `ansible-docs` for full list of parameters
]

.right-column[
.med-code[
```yaml
---

  - name: EXECUTE SHOW COMMANDS IOS DEVICES
    hosts: ios

    tasks:

    - name: EXECUTE A SINGLE COMAND
      ios_command:
        commands: "show version"
        username: ntc
        password: ntc123
        host: "{{ inventory_hostname }}"

    - name: EXECUTE LIST OF COMMANDS
      ios_command:
        commands:
          - "show version"
          - "show ip int brief"



```
]
]



---

# *_command (cont'd)

.left-column[
.med-code[
```yaml
    - name: SINGLE COMMAND
      nxos_command:
        commands: show version

    - name: LIST OF COMMAND STRINGS
      nxos_command:
        commands:
          - show version
          - show hostname

    - name: LIST OF DICTIONARIES
      nxos_command:
        commands:
          - command: show version
            output: json
          - command: show version
            output: text
        transport: cli

```
]
]

.right-column[
.med-code[
```yaml
  - hosts: junos
    connection: network_cli
    gather_facts: no

    tasks:

      - name: EXECUTE JUNOS COMMANDS - JSON
        junos_command:
          commands:
            - show version
            - show interfaces

      - name: EXECUTE JUNOS COMMANDS - TEXT
        junos_command:
          format: text
          commands:
            - show version
            - show interfaces
```
]
]

---

# Playbook Execution

Sample playbook execution:

.med-code[
```bash
$ ansible-playbook -i inventory gather.yml

PLAY [RUN COMMANDS] *********************************************************************

TASK [SINGLE COMMAND] *********************************************************************
ok: [csr1]
ok: [csr2]
ok: [csr3]

PLAY RECAP *********************************************************************
csr1            : ok=1    changed=0    unreachable=0    failed=0
csr2            : ok=1    changed=0    unreachable=0    failed=0
csr3            : ok=1    changed=0    unreachable=0    failed=0

```
]

---


class: center, middle, title
.footer-picture[<img src="data/media/Footer1.PNG" alt="Blue Logo" style="alight:middle;width:350px;height:60px;">]

# How do you see the data being gathered?


---

# Viewing Response Data

There are two ways to view data returned from a module.

Remember every module returns JSON data.
<br>
<br>
There are two ways to see it:

.left-column[

- Execute playbooks in verbose mode `-v`
- Use the register task attribute

]

.right-column[
.med-code[
```yaml
    - name: EXECUTE COMMANDS
      nxos_command:
        commands:
          - show version
      register: output

    - debug: var=output
```
]
]

---

# *_command

* Run arbitrary commands on devices.
* Based on transport type, the return data will be a string or structured data
* Show command data stored in `stdout` (always a list)

.left-column[
```yaml

  - name: SEND SHOW VERSION TO DEVICE
    nxos_command:
      commands:
        - 'show version'
    register: output

  - debug: var=output

```
]

.right-column[
.s2-code[
```yaml

TASK [debug] ********************************************************
ok: [nxos-spine1] => {
    "output": {
        "changed": false,
        "stdout": [
            {
                "bootflash_size": 1582402,
                "chassis_id": "NX-OSv Chassis",
                "cpu_name": "Intel(R) Xeon(R) CPU @ 2.50G",
                "host_name": "nxos-spine1",
                "sys_ver_str": "7.3(1)D1(1) [build 7.3(1)D1(0.10)]"
                <---output omitted--->
            }
        ],
        "stdout_lines": [], # list closed for slide formatting
        "warnings": []
    }
}

```
]
]

---

# assert

- Ensure certain conditions exist within the network
- Leverage data that you previously _registered_
- Validate routes exist, changes happen, and configuration is as desired

.med-code[
```yaml
  - name: IOS show version
    ios_command:
      commands:
        - show version
    register: output

  - name: Ensure OS version is correct
    assert:
      that:
        - "'Version 16.03.01' in output.stdout[0]"

```
]

---


class: center, middle, title
.footer-picture[<img src="data/media/Footer1.PNG" alt="Blue Logo" style="alight:middle;width:350px;height:60px;">]

# How do you Iterate over items in a Playbook?

---

# Iterators - Loop

- `loop` is the keyword to iterate over lists and dictionaries
- to iterate over a list use the `flatten` filter like this:

```yaml
loop: "{{ device_list|flatten(levels=1) }}" 
```

- to iterate over a dictionary use either the `dict2items` filters with `loop`

```yaml
loop: "{{ interface_dict|dict2items }}" 
```

* to iterate over files in a list of directories use `with_fileglob`, (often for templates)
```yaml
      - name: BUILD CONFIGS
        template: src={{ item }} dest=configs/{{ inventory_hostname }}.conf
        with_fileglob:
          - templates/0*
```
---


# loop with flatten filter

* Iterate over a list of strings
* `item` is built-in variable equal to an element of the list as you're iterating
* In this case, `item` is a string

```yaml
  - name: ITERATE OVER LIST OF STRINGS
    hosts: iosxe
    connection: network_cli
    gather_facts: no

    vars:
      commands:
        - show ip int brief
        - show version
        - show ip route

    tasks:
      - name: SEND A SERIES OF SHOW COMMANDS
        ios_command:
          commands:
            "{{ item }}"
        loop: "{{ commands|flatten(levels=1) }}"
```

---


# loop Continued

* Iterate over a list of dictionaries
* `item` is built-in variable equal to an element of the list as you're iterating
* In this case, `item` is a dictionary

```yaml
---

  - name: ITERATE OVER LIST OF STRINGS
    hosts: iosxe
    connection: network_cli
    gather_facts: no

    vars:
      commands:
        - command: show ip int brief
        - command: show version
        - command: show ip route

    tasks:
      - name: SEND A SERIES OF SHOW COMMANDS
        ios_command:
          commands:
            "{{ item.command }}"
        loop: "{{ commands|flatten(levels=1) }}"
```



---

# loop dict2items filter

.left-column[
* Iterate over a dictionary
* Root keys are `item.key`
* Values are `item.value`
]

.right-column[
```yaml
---

  - name: ITERATE OVER DICT
    hosts: iosxe
    connection: network_cli
    gather_facts: no
    vars:
      locations:
        amer: sjc-branch
        apac: hk-dc

    tasks:
      - name: PRINT ALL LOCATIONS
        debug:
          msg: "Region is {{ item.key }} and Site is {{ item.value }}"
        loop: "{{ locations|dict2items }}"
```

* Sample output:
```
"msg": "Regions are apac and Sites is hk-dc"
"msg": "Regions are amer and Sites is sjc-branch"
```
]

---

# Lab Time

- Lab 12 - Getting Started with the Command Module
- Lab 13 - Validating Reachability with the Command Module
- Lab 14 - Continuous Compliance with Ansible

---


class: center, middle, title
.footer-picture[<img src="data/media/Footer1.PNG" alt="Blue Logo" style="alight:middle;width:350px;height:60px;">]

# Jinja Filters

---

# Jinja Filters
.left-column[
- Filters transform data within a parameter or Jinja Expression
- Are used with the operator `|` like `hostname | upper` will transform 
the hostname variable using the upper built-in filter to be uppercase
- Custom filters are possible, and Ansible has built-in filters in addition to
Jinja2 built-in filters
]
.right-column[
```yaml
    vars:
      hostname: nycr1
      device_ip: 10.1.1.1
      bad_ip: X.10.Y.2

    tasks:
      - name: COVNERT HOSTNAME TO UPPERCASE
        debug:
          var: hostname | upper

      - name: CHECK TO SEE IF A IP ADDR IS VALID
        debug:
          var: device_ip | ipaddr

      - name: CHECK TO SEE IF A IP ADDR IS VALID
        debug:
          var: bad_ip | ipaddr
``` 

Sample Output:

```
"hostname | upper": "NYCR1"
"device_ip | ipaddr": "10.1.1.1"
"bad_ip | ipaddr": false
```
]
---

# Parsing Response Data

When running commands use the core command module it is often necessary to parse needed information from the command response data.

The following methods can be used to parse the response data:

- `parse_cli`
- `parse_cli_textfsm`
- `regex_search`
- `regex_findall`

You will notice that these methods are the same as methods used to parse data in Python.


---

# Parsing Data Using parse_cli_textfsm

The `parse_cli_textfsm` Jinja2 filter can use the same `textfsm` templates that are used in Python to parse data in Ansible.

```yaml
---

  - name: TEST PARSE USING PARSE_CLI_TEXTFSM
    hosts: csr1
    connection: network_cli
    gather_facts: no

    vars:
      template_path: "/etc/ntc/ansible/library/ntc-ansible/ntc-templates/templates/"
      show_version_path: "{{ template_path }}cisco_ios_show_version.template"

    tasks:

      - name: GET SHOW COMMANDS
        ios_command:
          commands: show version
        register: config_data

      - set_fact:
          show_version: "{{ config_data.stdout.0 | parse_cli_textfsm(show_version_path) }}"

      - debug:
          var: show_version
```


---

# Parsing Data Using parse_cli_textfsm

You will see that `parse_cli_textfsm` will return structured data.

```bash
TASK [debug] ***************************************************
ok: [csr1] => {
    "show_version": [
        {
            "CONFIG_REGISTER": "0x2102",
            "HARDWARE": [
                "CSR1000V"
            ],
            "HOSTNAME": "csr1",
            "ROMMON": "IOS-XE",
            "RUNNING_IMAGE": "packages.conf",
            "SERIAL": [
                "9KIBQAQ3OPE"
            ],
            "UPTIME": "6 hours, 18 minutes",
            "VERSION": "16.6.2"
        }
    ]
}
```


---

# Parsing Data Using parse_cli

The `parse_cli` Jinja2 filter uses RegEx "spec" files to parse data into a structured format.

These files are in the YAML format.

```yaml
---

keys:
  interfaces:
    value:
      key: "{{ item.iface_name }}"
      values:
        interface: "{{ item.iface_name }}"
        ip_addr: "{{ item.ip_addr }}"
        status: "{{ item.status }}"
        protocol: "{{ item.protocol }}"
    items: "^(?P<iface_name>(\\S+))\\s+(?P<ip_addr>(\\S+)|(\\w+))\\s+(?P<ok>(\\w+))\\s+(?P<method>(\\S+))\\s+(?P<status>
      (administratively down|\\w+))\\s+(?P<protocol>(\\S+))"
```

You will see that the spec file specifies how the data should be structured.  Then `items` is defined using the regex string to match the variables in the structure.

---

# Parsing Data Using parse_cli

Now you can reference the new parser using `parse_cli`:

```yaml
---

  - name: TEST PARSE USING PARSE_CLI
    hosts: csr1
    connection: network_cli
    gather_facts: no

    tasks:

      - name: GET SHOW COMMANDS
        ios_command:
          commands: show ip interface brief
        register: output

      - set_fact:
          show_brief: "{{ output.stdout.0 | parse_cli('./parsers/show_ip_interface_brief-dict.yml') }}"

      - debug:
          var: show_brief
```


---

# Parsing Data Using parse_cli

The filter will return data structured as a nested dictionary.

```bash
TASK [debug] ********************************************************************************
ok: [csr1] => {
    "show_brief": {
        "interfaces": {
            "GigabitEthernet1": {
                "interface": "GigabitEthernet1",
                "ip_addr": "10.0.0.51",
                "protocol": "up",
                "status": "up"
            },
            "GigabitEthernet2": {
                "interface": "GigabitEthernet2",
                "ip_addr": "10.254.13.1",
                "protocol": "up",
                "status": "up"
            },
            < output omitted>
        }
    }
}
```


---

# Parsing Data Using parse_cli

You can adjust the spec file to ouput the data as a list of dicitonaries:

```yaml
---

keys:
  interfaces:
    type: list
    value:
      interface: "{{ item.iface_name }}"
      ip_addr: "{{ item.ip_addr }}"
      status: "{{ item.status }}"
      protocol: "{{ item.protocol }}"
    items: "^(?P<iface_name>(\\S+))\\s+(?P<ip_addr>(\\S+)|(\\w+))\\s+(?P<ok>(\\w+))\\s+(?P<method>(\\S+))\\s+(?P<status>
      (administratively down|\\w+))\\s+(?P<protocol>(\\S+))"
```


---

# Parsing Data Using parse_cli

Output form new spec file:

```bash
ok: [csr1] => {
    "show_brief": {
        "interfaces": [
            {
                "interface": "GigabitEthernet1",
                "ip_addr": "10.0.0.51",
                "protocol": "up",
                "status": "up"
            },
            {
                "interface": "GigabitEthernet2",
                "ip_addr": "10.254.13.1",
                "protocol": "up",
                "status": "up"
            },
            {
                "interface": "GigabitEthernet3",
                "ip_addr": "unassigned",
                "protocol": "down",
                "status": "administratively down"
            },
            <output ommited>
        ]
    }
}
```

---

# Parsing Data Using regex_search and regex_findall

You can also use the `regex_search` and `regex_findall` Jinja2 filters to parse data.

In this example we issued the ping command from an IOS device and want to parse out the success precentage.

```yaml
---

 - name: PING TEST AND TRACEROUTE
    hosts: csr1
    connection: network_cli
    gather_facts: no

    vars:
      dest: "8.8.8.8"

    tasks:

    - name: ISSUE PING
      ios_command:
        commands: "ping vrf MANAGEMENT {{ dest }} repeat 2"
      register: output
```

We are registering the response from the ping command to the `output` variable.

---

# Parsing Data Using regex_search and regex_findall

Using `regex_search` we can parse the `stdout` from the `output` variable to find the success percentage.

```yaml
    - name: PARSE PING RESPONSE TO OBTAIN % OF SUCCESS
      set_fact:
        ping_pct: "{{ output.stdout.0 | regex_search('Success rate is (\\d+)\\s+percent') | regex_search('(\\d+)') }}"
```

The filter has two back-to-back `regex_search` commands.  The first captures the `Success rate...` line and the second captures the percentage within the first capture and registers that value in the `ping_pct` variable.


---

# Parsing Data Using regex_search and regex_findall

Using `regex_findall` is another way to parse the `stdout` from the `output` variable to find the success percentage.

```yaml
    - name: PARSE PING RESPONSE TO OBTAIN % OF SUCCESS
      set_fact:
        ping_pct: "{{ output.stdout.0 | regex_findall('Success rate is (\\d+)\\s+percent') | first }}"
```

The filter has captures the success line and registers the percentage (\\d+) capture group.  The `first` filter returns the first capture group as the result.  This result is assigned to the variable `ping_pct`.


---

# Lab Time

- Lab 15 - Parsing Show Commands
- Lab 16 - Performing a Conditional Traceroute

---

# *_config

.left-column[

By default, it compares the lines against the running configuration

You can pass commands into the module a few different ways:

- Using the `lines` parameter
- Using the `src` parameter and point to a pre-built config file
- Using the `src` parameter and point to a Jinja2 template

]

.right-column[
```yaml
---

  - name: DEPLOY SNMP COMMUNITY STRINGS ON IOS DEVICES
    hosts: ios

    tasks:

    - name: USE COMMANDS IN THE PLAYBOOK
      ios_config:
        lines:
          - "snmp-server community ntc123 ro"
        username: ntc
        password: ntc123
        host: "{{ inventory_hostname }}"

    - name: DEPLOY FROM CONFIG FILE
      ios_config:
        src: "configs/snmp.cfg"



```
]

---

# *_config

```yaml
# Ensure these lines are present in the configuration
- nxos_config:
    commands:
      - snmp-server community public group network-operator
      - snmp-server community networktocode group network-operator

```

```yaml
# Ensure these lines are present in the configuration
- junos_config:
    src: snmp.conf

```


---

# *_config (cont'd)

.left-column[
- Modules support many parameters
- Use `ansible-doc` to view them all
- `parents` - ordered list of commands that identify the section the commands should be checked against

]

.right-column[
```yaml
- name: ENSURE GIGE4 IS CONFIGURED PROPERLY
  ios_config:
    parents:
      - interface GigabitEthernet4
    lines:
      - description Configured by Ansible
      - ip address 10.100.100.1 255.255.255.0

```
]

---

# *_config (cont'd)

.left-column[
- Modules support many parameters
- Use `ansible-doc` to view them all
- `parents` - ordered list of commands that identify the section the commands should be checked against
- `before` - ordered list of commands to be prepended to `lines` if a change needs to be made
- `after` - ordered list of commands to be appended to `lines` if a change needs to be made
- Note: these are just a sub-set of parameters supported

]

.right-column[
```yaml
# this would remove any other commands previously covered for
# the other ASN
    - name: ENSURE BGP CONFIG IS CORRECT
      ios_config:
        before: ['no router bgp 65512']
        parents:
          - router bgp 65512
        lines:
          - bgp router-id 10.10.10.10
          - bgp log-neighbor-changes
          - network 10.101.1.0 mask 255.255.255.0
          - network 10.101.2.0 mask 255.255.255.0
          - timers bgp 5 15
          - neighbor 10.10.10.2 remote-as 102
          - neighbor 10.10.10.2 description ISP_CARRIER_X
          - neighbor 10.10.10.2 send-community
          - neighbor 10.10.10.2 soft-reconfiguration inbound
        after: ['copy run start']
```
]

---
# *_config (cont'd)
.left-column[
The `save_when` parameter is needed to commit running config to the NVRAM. (Deprecated command `save` no longer works with Ansible 2.4 and above)
Available options for the  save_when parameter:

- always
- modified
- never

]

.right-column[

``` yaml

    - name: ENSURE THAT LOOPBACK 222 IS CONFIGURED
      ios_config:
        commands:
          - ip address 10.222.222.222 255.255.255.255
        parents:
          - interface loopback 222
        save_when: modified
```
]


---

# The diff_against Parameter

Introduced in Ansible 2.4. Test running configuration against:

- The startup configuration
    - Check if there are ephemeral configurations
- A configuration intent
    - Check whether running configuration deviates from compliance/golden configuration
- Pending configuration lines
    - Check exact configuration impact of config lines being pushed


*Invoked with `--diff` flag*

---

# diff_against -  startup

``` yaml
    - name: COMPARE RUNNING CONFIG WITH STARTUP
      ios_config:
        diff_against: startup
```

```bash
TASK [COMPARE RUNNING CONFIG WITH STARTUP] **************************************
--- before
+++ after
@@ -36,6 +63,8 @@
 redundancy
 lldp run
 cdp run
+interface Loopback222
+ ip address 10.222.222.222 255.255.255.255
 interface GigabitEthernet1
  vrf forwarding MANAGEMENT
  ip address 10.0.0.51 255.255.255.0

```

---

# The lookup plugin

.left-column[

Powerful Ansible plugin that is used access data from outside sources
  * Regular text file content
  * CSV
  * INI
  * DNS Lookup
  * MongoDB and many more

Can be used to assign values to variables
]

.right-column[

.s2-code[

``` yaml
vars:
  config_file: "{{ lookup('file', './backups/{{ inventory_hostname }}.cfg') }}"

tasks:
  - debug:
      msg: "The file name is {{ config_file }}"
```


.ubuntu[

```
ntc@ntc:ansible$ ansible-playbook -i inventory file_lookup_demo.yml

PLAY [DEMO FILE LOOKUPS] ****************************************************

TASK [debug] ****************************************************************
ok: [csr1] => {
    "msg": "The file name is snmp-server community PUBLIC123 RO 5\nsnmp-server community PRIVATE123 RW 95\nsnmp-server location GLOBAL\nsnmp-server contact LOCAL_ADMIN\nsnmp-server host 1.1.1.1\n\nvlan 10\n name web_servers\nvlan 20\nvlan 30\n name db_servers"
}

PLAY RECAP ******************************************************************
csr1                       : ok=1    changed=0    unreachable=0    failed=0


```

]
]
]


---

# diff_against - intended


``` yaml
  tasks:
    - name: VALIDATE CONFIGURATION INTENT
      ios_config:
        diff_against: intended
        intended_config: "{{ lookup('file', './backups/{{ inventory_hostname }}.cfg') }}"

```


```bash
TASK [VALIDATE CONFIGURATION INTENT] **************************************
--- before
+++ after
@@ -63,6 +63,8 @@
 redundancy
 lldp run
 cdp run
+interface Loopback222
+ ip address 10.222.222.222 255.255.255.255
 interface GigabitEthernet1
  vrf forwarding MANAGEMENT
  ip address 10.0.0.51 255.255.255.0

```


---

# diff_against -  impending configuration lines


``` yaml
    - name: ENSURE THAT LOOPBACK222 IS CONFIGURED
      ios_config:
        commands:
          - ip address 10.222.222.222 255.255.255.255
        parents:
          - interface loopback 222
        diff_against: running
```



```bash
TASK [ENSURE THAT LOOPBACK 222 IS CONFIGURED]
**************************************
+++ after
@@ -63,6 +63,8 @@
 redundancy
 lldp run
 cdp run
+interface Loopback222
+ ip address 10.222.222.222 255.255.255.255
 interface GigabitEthernet1
  vrf forwarding MANAGEMENT
  ip address 10.0.0.51 255.255.255.0

```

**Note: This task will actually make changes to the running config!**

---

# Declarative Configuration

- Data model

.med-code[
```yaml
snmp_communities:
  - community: ntc-public
    group: network-operator
  - community: ntc-private
    group: network-admin
```

- Template for Nexus

```jinja
{% for snmp in snmp_communities %}
snmp-server community {{ snmp.community }} group {{ snmp.group }}
{% endfor %}
```
]


---

# Declarative Configuration (cont'd)

- Generate configuration

```yaml
---
- name: Declarative Configuration
  hosts: nxos
  connection: network_cli
  gather_facts: False

  tasks:
    - name: GENERATE CONFIGURATION
      template:
        src: "./templates/snmp.j2"
        dest: "./snmp-config.cfg"
```

- snmp-config.cfg

```bash
snmp-server community ntc-public group network-operator
snmp-server community ntc-private group network-admin
```

---

# Declarative Configuration (cont'd)

- Push configuration

.med-code[
```yaml
    - name: PUSH SNMP COMMUNITIES
      nxos_config:
        src: "./snmp-config.cfg"
```
]


---

# Declarative Configuration (cont'd)

- Get existing SNMP communities and set fact

```yaml
    - name: GET CONFIG FOR SNMP PARSING
      nxos_command:
        commands:
          - show run section snmp
      register: output

    - name: GET EXISTING SNMP COMMUNITIES AND SET FACT
      set_fact: existing_snmp_communities="{{ output.stdout[0] | regex_findall('snmp-server community (\S+)') }}"

    - debug: var=existing_snmp_communities
```

.s2-code[
```bash
TASK [GET CONFIG FOR SNMP PARSING] *********************************************
ok: [nxos]

TASK [GET EXISTING SNMP COMMUNITIES AND SET FACT] ******************************
ok: [nxos]

TASK [debug] *******************************************************************
ok: [nxos] => {
    "existing_snmp_communities": [
        "ntc-public",
        "ntc-private",
        "public",
        "networktocode"
    ]
}

```
]

---

# Declarative Configuration (cont'd)

- **public** and **networktocode** communities are not part of the data model. Therefore, they may be undesired and need to be removed
- Calculate communities to remove

.s2-code[
```yaml
    - name: SET FACT FOR PROPOSED (DESIRED) COMMUNITIES
      set_fact:
        proposed_snmp_communities: "{{ snmp_communities|map(attribute='community')|list }}"

    - name: CALCULATE AND SET FACT FOR COMMUNITIES TO REMOVE
      set_fact:
        snmp_communities_to_remove: "{{ existing_snmp_communities|difference(proposed_snmp_communities) }}"

    - debug: var=snmp_communities_to_remove
```

```bash
TASK [SET FACT FOR PROPOSED (DESIRED) COMMUNITIES] *****************************
ok: [nxos]

TASK [CALCULATE AND SET FACT FOR COMMUNITIES TO REMOVE] ************************
ok: [nxos]

TASK [debug] *******************************************************************
ok: [nxos] => {
    "snmp_communities_to_remove": [
        "public",
        "networktocode"
    ]
}
```
]

---

# Declarative Configuration (cont'd)

- Remove undesired communities


```yaml
    - name: PURGE SNMP COMMUNITIES
      nxos_config:
        commands:
          - "no snmp-server community {{ item }}"
      with_items: "{{ snmp_communities_to_remove }}"
```

```bash
TASK [PURGE SNMP COMMUNITIES] **************************************************
changed: [nxos] => (item=public)
changed: [nxos] => (item=networktocode)
```

---

# Summary

* Modules are under active development
* Currently performing "offline" diffs
* Great for achieving idempotency on config sections
* You can use the base **template** module to build a config and still push with these modules (as we did with NAPALM)

---

# Lab Time

- Lab 17 - Using the Config Module

---



class: middle, segue

# Data Collection & Reporting
### Ansible for Network Automation

---

# Modules

- Core Facts Modules
  - nxos_facts
  - eos_facts
  - junos_facts
  - ios_facts
- 3rd Party Facts and Data Collection
  - ntc_get_facts
  - ntc_show_command
  - napalm_get_facts
  - snmp_facts
  - snmp_device_version
- Dynamics Groups & REST APIs

---

# Core Facts

Core facts modules collect a number of useful pieces of information:

  * All IP addresses
  * Filesystems
  * Hostname
  * Image
  * All interfaces with some Layer 2 and Layer 3 attributes
  * Serial Number
  * OS Version
  * Neighbors broken down by interface

---

# Collecting Facts

Sample playbook gathering IOS facts:

.left-column[
```yaml
  - name: GATHER IOS FACTS
    hosts: iosxe
    connection: network_cli
    gather_facts: no

    tasks:
      - name: GET FACTS
        ios_facts:
```
]
--

.right-column[

* Default value for `gather_subset` is  **!config**

```yaml
  - name: GATHER ALL FACTS
    ios_facts:
      gather_subset: all

  - name: GATHER A SHOW RUN AND DEFAULT SYSTEM FACTS
    ios_facts:
      gather_subset:
        - config

  - name: GATHER ALL FACTS EXCEPT HARDWARE FACTS
   ios_facts:
    gather_subset:
      - "!hardware"
```

]


---

# Collecting Facts

```yaml
  - name: GATHER IOS FACTS
    hosts: iosxe
    connection: network_cli
    gather_facts: no

    tasks:
      - name: GET FACTS
        ios_facts:
        register: ntc_ios_facts

      - debug: var=ntc_ios_facts
```

---



# Sample Response (IOS)

.left-column[
```bash
    "ntc_ios_facts": {
        "ansible_facts": {
            "ansible_net_all_ipv4_addresses": [
                "10.0.0.53"
            ],
            "ansible_net_all_ipv6_addresses": [],
            "ansible_net_filesystems": [
                "bootflash:"
            ],
            "ansible_net_hostname": "csr3",
            "ansible_net_image": "bootflash:packages.conf",
            "ansible_net_interfaces": {
                "GigabitEthernet1": {
                    "bandwidth": 1000000,
                    "description": null,
                    "duplex": "Full",
                    "ipv4": {
                        "address": "10.0.0.53",
                        "masklen": 24
                    },
                    "lineprotocol": "up ",
                    "macaddress": "2cc2.604c.4e06",
                    "mediatype": "RJ45",
                    "mtu": 1500,
                    "operstatus": "up",
                    "type": "CSR vNIC"
                }
            }
```
]
.right-column[
```bash
            "ansible_net_memfree_mb": 322777,
            "ansible_net_memtotal_mb": 2047264,
            "ansible_net_model": null,
            "ansible_net_neighbors": {
                "Gi1": [
                    {
                        "host": "eos-leaf1.ntc.com",
                        "port": "Management1"
                    },
                    {
                        "host": "eos-leaf2.ntc.com",
                        "port": "Management1"
                    }
                ]
            },
            "ansible_net_serialnum": "9KXI0D7TVFI",
            "ansible_net_version": "16.3.1"
        }

```
]

---


# Viewing Facts For a Device


.left-column[
**OPTION 1**
```yaml


- name: GET FACTS
  ios_facts:
  register: ntc_ios_facts

- debug: var=ntc_ios_facts

- debug: var=ntc_ios_facts['ansible_facts']['ansible_net_hostname']
```

**OPTION 2**
```yaml

- name: GET FACTS
  ios_facts:

- name: Display variables/facts known for a given host
  debug: var=hostvars[inventory_hostname]

- debug: var=ansible_net_hostname
```
]


.right-column[

**Note:** any key inside `ansible_facts` can be accessed directly

```json
    "ntc_ios_facts": {
        "ansible_facts": {
            "ansible_net_all_ipv4_addresses": [
                "10.0.0.53"
            ],
            "ansible_net_all_ipv6_addresses": [],
            "ansible_net_filesystems": [
                "bootflash:"
            ],
            "ansible_net_hostname": "csr3",
```
]


---

# ntc_get_facts

- uptime - Uptime of the device
- vendor - vendor of the device
- model - Device model
- hostname - Hostname of the device
- fqdn - FQDN of the device
- os_version - String with the OS version running on the device.
- serial_number - Serial number of the device
- interfaces - List of the interfaces of the device
- vlans - List of the vlans configured on the device


```yaml
- ntc_get_facts:
    provider: "{{ ntc_provider }}"
    platform: "{{ ntc_vendor }}"_{{ ansible_network_os }}_{{ ntc_api }}"
```


---

# ntc_show_command

- Multi-vendor Ansible module to streamline converting raw text into JSON key/value pairs
- Leverages TextFSM
- netmiko is used for transport to enable support for _all_ device

```yaml
tasks:

  - name: GET DATA
    ntc_show_command:
      connection=ssh
      platform=cisco_nxos
      command='show vlan'
      provider={{ ntc_provider }}
      template_dir: "/etc/ntc/ansible/library/ntc-ansible/ntc-templates/templates"

```

---

class: ubuntu

# ntc_show_command

- JSON data now available to re-use
- Use as inputs to other modules or in templates (docs)

```
TASK: [GET DATA] **************************************************************
ok: [n9k1] => {"changed": false, "response": [{"name": "default", "status": "active", "vlan_id": "1"}, {"name": "VLAN0002", "status": "active", "vlan_id": "2"}, {"name": "VLAN0003", "status": "active", "vlan_id": "3"}, {"name": "VLAN0004", "status": "active", "vlan_id": "4"}, {"name": "VLAN0005", "status": "active", "vlan_id": "5"}, {"name": "VLAN0006", "status": "active", "vlan_id": "6"}, {"name": "VLAN0007", "status": "active", "vlan_id": "7"}, {"name": "VLAN0008", "status": "active", "vlan_id": "8"}, {"name": "VLAN0009", "status": "active", "vlan_id": "9"}, {"name": "VLAN10_WEB", "status": "active", "vlan_id": "10"}, {"name": "VLAN0011", "status": "active", "vlan_id": "11"}, {"name": "VLAN0012", "status": "active", "vlan_id": "12"}, {"name": "VLAN0013", "status": "active", "vlan_id": "13"}, {"name": "VLAN0014", "status": "active", "vlan_id": "14"}, {"name": "VLAN0015", "status": "active", "vlan_id": "15"}, {"name": "VLAN0016", "status": "active", "vlan_id": "16"}, {"name": "VLAN0017", "status": "active", "vlan_id": "17"}, {"name": "VLAN0018", "status": "active", "vlan_id": "18"}, {"name": "VLAN0019", "status": "active", "vlan_id": "19"}, {"name": "peer_keepalive", "status": "active", "vlan_id": "20"}, {"name": "VLAN0022", "status": "active", "vlan_id": "22"}, {"name": "VLAN0030", "status": "active", "vlan_id": "30"}, {"name": "VLAN0040", "status": "active", "vlan_id": "40"}, {"name": "native", "status": "active", "vlan_id": "99"}, {"name": "VLAN0100", "status": "active", "vlan_id": "100"}, {"name": "VLAN0101", "status": "active", "vlan_id": "101"}, {"name": "VLAN0102", "status": "active", "vlan_id": "102"}, {"name": "VLAN0103", "status": "active", "vlan_id": "103"}, {"name": "VLAN0104", "status": "active", "vlan_id": "104"}, {"name": "VLAN0105", "status": "active", "vlan_id": "105"}, {"name": "VLAN0123", "status": "active", "vlan_id": "123"}, {"name": "VLAN0200", "status": "active", "vlan_id": "200"}]}
```

---

# snmp_facts

- Multi-vendor fact gathering using SNMP
- Returns:
  - All IPv4 addresses
  - interfaces
  - sys contact
  - sys description
  - uptime

```yaml
- snmp_facts: host={{ inventory_hostname }} version=v2c community=networktocode
```


---


# snmp_device_version

The `snmp_device_version` module can be used to discover the device vendor, os, and version.  These items are returned as variables `ansible_device_vendor`, `ansible_device_os`, and `ansible_device_version`.

Example Task:

```yaml
      - name: QUERY DEVICE VIA SNMP
        snmp_device_version:
          community: networktocode
          version: 2c
          host: "{{ inventory_hostname }}"
```

You can use these discovered variables for further processing devices in a dynamic fashion.

```yaml
  - ntc_show_command:
      platform: "{{ ansible_device_vendor }}_{{ ansible_device_os }}"
      ...
```

---


# Creating Dynamic Groups

You are able to create dynamic groups within Ansible using the `group_by` module.  Using the data collected by the `snmp_device_discovery` module we are able to dynamically group devices by vendor, os, or version.

In this example we are grouping the devices by vendor.  This will create a group named `vendor_` followed by the vendor name.  This group can be used in subsiquent plays within the playbook.

```yaml
---

  - name: DISCOVER VENDOR
    hosts: iosxe,nxos,vmx
    connection: network_cli
    gather_facts: no

    tasks:

      - name: QUERY DEVICE VIA SNMP
        snmp_device_version:
          community: networktocode
          version: 2c
          host: "{{ inventory_hostname }}"
        tags: snmp

      - group_by:
          key: vendor_{{ ansible_device_vendor }}
```


---

# Using the URI Module

The `uri` module can be used to make HTTP-based API calls.

```yaml
      - name: GET INTERFACE IP ADDRESS
        uri:
          url: https://{{ inventory_hostname }}/restconf/data/Cisco-IOS-XE-native:native/interface=GigabitEthernet/1/ip/address
          method: GET
          user: "{{ ansible_user }}"
          password: "{{ ansible_ssh_pass }}"
          return_content: yes
          validate_certs: no
          headers:
            Content-Type: application/yang-data+json
            Accept: application/yang-data+json
        register: response
```

This example shows how to make an API call against an IOSXE device to pull the IP address information for the `GigabitEthernet1` interface and assigning the returned value to the `response` variable.

You can test all of these settings using Postman before building your Ansible tasks.


---

# Tips: Using set_facts

.left-column[
- In contrast to using `register` to store the output of a task into a variable,
the `set_fact` module allows a task to define a variable
- Sometimes used to simplify the naming of a variable 
]

.right-column[
```yaml
vars:
  locations:
    amer:
      nyc:
        - nyc-dc
        - nyc-campus
      sjc:
        - sjc-branch
    apac:
      hk:
        - hk-dc
        - hk-campus

tasks:
  - name: PRINT ALL LOCATIONS
    debug:
      var: locations

  - name: SJC LOCATIONS
    set_fact:
      sjc_locations: "{{ locations['amer']['sjc'] }}"

  - name: PRINT ALL LOCATIONS
    debug:
      var: sjc_locations
```
]

---

# Tips: Using from_json Filter

- In a recent example, an API call to the IOSXE device received a JSON response
in python, `json.loads()` would be used to convert the JSON object to a dictionary
- In Ansible, instead use the `from_json` filter
- For example, assuming the `response` API variable is earlier in the play:

```yaml
      - set_fact:
          ip_info: "{{ response['content'] | from_json }}"

      - debug:
          var: ip_info['Cisco-IOS-XE-native:address']['primary']['address']
```

---

# Creating Documentation

.left-column[

You choose:

- text
- html
- markdown
- asciidoc
- ...
]


.right-column[
Then:
- publish
- alert
- chatops
- mail

]


---

# Know the Available Facts/Variables

.left-column[

- Template

```bash
# general.j2

Device: {{ inventory_hostname }}

Vendor:           {{ ntc_vendor }}
Platform:         {{ platform }}
Operating System: {{ ansible_network_os }}
Image:            {{ kickstart_image }}

```

- Playbook

```yaml
---

  - name: DC P1
    hosts: n9k1
    connection: network_cli
    gather_facts: no

    tasks:
      - nxos_facts:

      - template: src=general.j2 dest=files/general.md

```
]

--

.right-column[
- Document

```bash

Device: n9k1

Vendor:           cisco
Platform:         Nexus9000 C9396PX Chassis
Operating System: 7.0(3)I2(1)
Image:            7.0(3)I2(1)

```
]

---

# Documenting Neighbors

.left-column[

- Template

```bash
# neighbors.j2

DEVICE: {{ inventory_hostname }}

{% for neighbor in ntc_neighbors.response %}
NEIGHBOR:           {{ neighbor.neighbor }}
NEIGHBOR INTERFACE: {{ neighbor.neighbor_interface }}
LOCAL INTERFACE:    {{ neighbor.local_interace }}

{% endfor %}

```
- Playbook

.s2-code[
```yaml
---

  - name: DC P1
    hosts: eos-spine1
    connection: network_cli
    gather_facts: no

    tasks:
      - ntc_show_command:
          provider: "{{ ntc_provider }}"
          command: "show lldp neighbor"
        register: ntc_neighbors
      - template: src=neighbors.j2 dest=files/neighbors.md

```
]
]

--

.right-column[
- Document

```bash


Device: eos-spine1

NEIGHBOR:           leaf-tor1.arista.test
NEIGHBOR INTERFACE: Ethernet1
LOCAL INTERFACE:    Ethernet1

NEIGHBOR:           leaf-tor2.arista.test
NEIGHBOR INTERFACE: Ethernet1
LOCAL INTERFACE:    Ethernet2

NEIGHBOR:           spine2.arista.test
NEIGHBOR INTERFACE: Ethernet5
LOCAL INTERFACE:    Ethernet5

NEIGHBOR:           spine2.arista.test
NEIGHBOR INTERFACE: Ethernet6
LOCAL INTERFACE:    Ethernet6

NEIGHBOR:           spine2.arista.test
NEIGHBOR INTERFACE: Ethernet7
LOCAL INTERFACE:    Ethernet7

```
]

---

# Using a Table (Neighbors)

.left-column[

- Template

```bash
# neighbors-table.j2
| Source     | Interface    | Neighbor  | Interface    |
| ---------- |--------------| ----------|------------- |
{% for neighbor in ntc_neighbors.response %}
| {{ inventory_hostname }} | {{ neighbor.local_interface }} | {{ neighbor.neighbor }} | {{ neighbor.neighbor_interface }} |
{% endfor %}
```
- Playbook

```yaml
---

  - name: DC P1
    hosts: eos-spine1
    connection: network_cli
    gather_facts: no

    tasks:
      - eos_facts: host={{ inventory_hostname }}
      - template: src=neighbors-table.j2 dest=files/neighbors-table.md

```


]
--

.right-column[
- Markdown generated table
.center[
<img src="data/media/neighbor-table.png" alt="Neighbors Markdown Table" style="alight:middle;width:440px;height:340px;">
]
]

---

# Summary

- Understand the various ways to collect data about the network.
- Templating is great for documentation (not just configurations)
- Know your variables
  - Any variable can be used in the playbook **and** template
- Know your document formats
- Understand Jinja2
- Auto publish to github, web server, etc.
- Key modules:
  - template
  - assemble

---

# Lab Time

- Lab 18 - Making REST API Calls from Ansible
- Lab 19 - Discovering Device Types and Dynamically Creating Groups
- Lab 20 - Data Collection Modules & Reporting
  - Facts Data Collection Modules
  - Structured Data from CLI Devices (ntc_show_command)
  - Inventory Report

---

class: middle, segue

# Ansible Roles
### Ansible for Network Automation

---

# Reusable Abstractions

- include statement
- _includes_ tasks from another file


```yaml
# main playbook
---

  - name: PB
    connection: network_cli
    hosts: all

    tasks:

      - include: get-facts.yml
```

```yaml
---
# get-facts.yml

- name: GET FACTS FROM ARISTA DEVICES
  eos_facts: connection={{ inventory_hostname }}

  ...<more getter tasks>...
```



---

# Parameterized Include

- Pass parameters to _included_ tasks


```yaml
# main playbook
---
  - name: CONFIGURE DEVICES
    hosts: all
    connection: network_cli

    tasks:

      - include: get-facts.yml vendor={{ ntc_vendor }}
```

```yaml
# get-facts.yml
---

- name: GET FACTS FROM ARISTA DEVICES
  eos_facts: connection={{ inventory_hostname }}
  when: vendor == "arista"

- name: GET FACTS FROM CISCO NXOS DEVICES
  nxos_facts: connection={{ inventory_hostname }}
  when: vendor == "cisco"
```

---

# Roles

- re-usable abstraction of code (tasks, variables, and handlers)
- Ansible Galaxy shares roles


.left-column[

```bash
site.yml
inventory
roles/
   common/
     files/
     templates/
     tasks/
     handlers/
     vars/
     defaults/
   vlans/
     templates/
     tasks/
       main.yml
       eos.yml
       nxos.yml
       junos.yml
     vars/
   snmp/
     templates/
     tasks/
     vars/
```
]

.right-column[

```yaml
---

- name: SAMPLE PLAYBOOK USING ROLES
  hosts: leaves
  connection: network_cli

  roles:
     - common
     - vlans
```

- directory structure is an example
- no need to have tasks or vars for every role
- files in each sub-directory are called `main.yml`

]

---

# Parameterized Roles

```yaml
---

- hosts: spine
  connection: network_cli
  roles:
    - common
    - spine
    - role: vlan
      vlan_id: 10
    - role: snmp
      contact: Bob
```

---

# VLAN Role

.left-column[

```yaml
# main playbook
.---

  - name: DC P1
    hosts: datacenter
    connection: network_cli
    gather_facts: no

    roles:
      - vlans

```


```yaml
# roles/vlans/tasks/main.yml
---

- name: ARISTA VLANs
  eos_vlan: vlanid={{ item.id }} connection={{ inventory_hostname }}
  loop: "{{ vlans|flatten(levels=1) }}"
  when: vendor == "arista"

- name: CISCO VLANs
  nxos_vlan: vlan_id={{ item.id }} host={{ inventory_hostname }}
  loop: "{{ vlans|flatten(levels=1) }}"
  when: vendor == "cisco"
```



]

.right-column[

```bash
[datacenter]
spine1 vendor=arista
n9k1 vendor=cisco
```



```yaml
# group_vars/all.yml

vlans:
  - id: 10
    name: web_servers
  - id: 20
  - id: 30
    name: db_servers

```


]

---

# VLAN Role Improved

.left-column[

```yaml
# main playbook
.---
  - name: DC P1
    hosts: datacenter
    connection: network_cli
    gather_facts: no
    roles:
      - vlans

```


```yaml
# roles/vlans/tasks/main.yml
---
- include: "{{ ntc_vendor }}.yml"
```

```yaml
# roles/vlans/tasks/arista.yml
---
- name: ARISTA VLANs
  eos_vlan: vlanid={{ item.id }} connection={{ inventory_hostname }}
  loop: "{{ vlans|flatten(levels=1) }}"
```
```yaml
# roles/vlans/tasks/cisco.yml
- name: CISCO VLANs
  nxos_vlan: vlan_id={{ item.id }} host={{ inventory_hostname }}
  loop: "{{ vlans|flatten(levels=1) }}"
```
]

.right-column[

```bash
[datacenter]
spine1 vendor=arista
n9k1 vendor=cisco
```



```yaml
# group_vars/all.yml

vlans:
  - id: 10
    name: web_servers
  - id: 20
  - id: 30
    name: db_servers

```


]


---


# Summary

- Think about the functions, features, or applications of the device
- Big Picture vs. Details
- Encapsulate
- For networking- think mulit-vendor features

---

# Lab Time

- Lab 21 - Creating an Ansible Role
  - Create a multi-vendor VLAN role that works with Cisco and Arista devices

---


class: middle, segue

# Dynamic Inventory
### Ansible for Network Automation

---

# Inventory

- Ansible Inventory files are static
- Managing large YAML files doesn't scale
- Manage lots of YAML files doesn't scale
- Users usually already have a CMDB, NMS, etc.
- What if you have a dynamic environment?
  - AWS, Rackspace, VMs
- **Enter Dynamic Inventory**

---

# Executing Playbooks

.left-column[
- You currently use the `-i` flag to specify the inventory file
- You can also specify a script that is used to generate an inventory
  - Needs to return JSON k/v pairs
- `ansible-playbook -i dynamic_script.py site.yml`
- Script needs to be an executable (x)
]

.right-column[
- Sample Inventory generated from a script
- Groups, group vars, hosts, host vars (not shown)

.small-code[
```bash
{
    "hp": {
        "hosts": [
            "hp1.ntc.com",
            "hp2.ntc.com",
            "hp3.ntc.com",
            "hp4.ntc.com"
        ],
        "vars": {
            "platform": "comware7"
        }
    },
    "cisco": {
        "hosts": [
            "n9k1.ntc.com",
            "n9k2.ntc.com"
        ],
        "vars": {
            "platform": "nexus"
        }
    },
    "juniper": [
        "jnprfw.ntc.com"
    ],
    "arista": [
        "arista1.ntc.com",
        "arista2.ntc.com"
    ]
}
```
]


---

# Multiple Sources

- If the parameter used with the `-i` flag is a directory, multiple sources can be used
  - inventory file with scripts
  - multiple scripts

---

# Example Script

```python

#!/usr/bin/env python

import requests

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

---

# Executing a Playbook

```yaml
---

  - name: test playbook for dynamic inventory
    connection: network_cli
    gather_facts: no
    hosts: all


    tasks:

      - debug: var=inventory_hostname

```

---

# Viewing the Results

.left-column[

- JSON data generated from script

```json
{
    "cisco": {
        "hosts": [
            "n9k1.ntc.com",
            "n9k2.ntc.com"
        ],
        "vars": {
            "platform": "nexus"
        }
    },
    "arista": [
        "arista1.ntc.com",
        "arista2.ntc.com"
    ],
    "apic": [
        "aci.ntc.com"
    ]
}
```

]



.right-column[


- Playbook output

.small-code[
```bash
ansible-playbook -i dynamo.py site.yml

PLAY [test playbook for dynamic inventory] ************************************

TASK: [debug var=inventory_hostname] ******************************************
ok: [n9k2.ntc.com] => {
    "var": {
        "inventory_hostname": "n9k2.ntc.com"
    }
}
ok: [n9k1.ntc.com] => {
    "var": {
        "inventory_hostname": "n9k1.ntc.com"
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
ok: [arista2.ntc.com] => {
    "var": {
        "inventory_hostname": "arista2.ntc.com"
    }
}

PLAY RECAP ********************************************************************
aci.ntc.com                : ok=1    changed=0    unreachable=0    failed=0
arista1.ntc.com            : ok=1    changed=0    unreachable=0    failed=0
arista2.ntc.com            : ok=1    changed=0    unreachable=0    failed=0
n9k1.ntc.com               : ok=1    changed=0    unreachable=0    failed=0
n9k2.ntc.com               : ok=1    changed=0    unreachable=0    failed=0
```
]
]

---

# Summary

- YAML files do the trick _most_ of the time, especially for testing
- Custom dev work required for dynamic network inventories, i.e. HPOV, Solar Winds, etc.
- As with modules, can be done in any language
  - Just need to return JSON in the proper format

---

# Lab Time

- Lab 22 - Using a Dynamic Inventory Script
  - You will execute a playbook that uses a pre-created inventory script that queries a public REST API


---


class: middle

# The End


---



class: middle

# EXTRA - BONUS
# Creating Custom Ansible Modules
### Ansible for Network Automation

---

# Ansible Modules

.left-column[
- Over 400 Core modules
  - Linux
  - Windows
  - EC2
  - Rackspace
  - VMware
]

.right-column[
- Extras
- Galaxy Roles...
- You may need to:
  - Write your own
  - Help fix others

]

---

# Workflow

- Especially for those just getting started, build out your script in native Python first
- Write a main() function
  - This should call other functions needed
  - Conditional (idempotent) logic should exist within main() for this workflow
- if __name__ == "__main__" should just call main()
- Use variables to simulate all user inputs, i.e. Ansible parameters
- Finishing by returning a Python dictionary that'll include key/value pairs on what you want to see/use within a playbook, etc.

---

# Existing Python Script


```python
#!/usr/bin/env python

import socket
import json

from pycsco.nxos.device import Device
from pycsco.nxos.utils import nxapi_lib


def main():

    username = 'cisco'
    password = 'cisco'
    protocol = 'http'
    node = 'n9k1'
    host = socket.gethostbyname(node)

    device = Device(ip=host, username=username, password=password,
                    protocol=protocol)

    neighbors = nxapi_lib.get_neighbors(device)

    print neighbors   # returns a list

    neighs = dict(neighbors=neighbors)

if __name__ == "__main__":
    main()
```

---

# From Script to Module

.left-column[
.s2-code[
```python
#!/usr/bin/env python

import socket
import json

from pycsco.nxos.device import Device
from pycsco.nxos.utils import nxapi_lib


def main():

    username = 'cisco'
    password = 'cisco'
    protocol = 'http'
    node = 'n9k1'
    host = socket.gethostbyname(node)

    device = Device(ip=host, username=username, password=password,
                    protocol=protocol)

    neighbors = nxapi_lib.get_neighbors(device)

    print neighbors   # returns a list

    neighs = dict(neighbors=neighbors)

if __name__ == "__main__":
    main()

```
]]

.right-column[

.s2-code[
```python
def main():

    module = AnsibleModule(
        argument_spec=dict(
            type=dict(choices=['cdp', 'lldp'], default='cdp'),
            protocol=dict(choices=['http', 'https'], default='http'),
            host=dict(required=True),
            username=dict(type='str', required=True),
            password=dict(type='str', required=True),
        ),
        required_together=(
            ['host', 'password', 'username'],
        ),
        supports_check_mode=False

    username = module.params['username']
    password = module.params['password']
    protocol = module.params['protocol']
    host = socket.gethostbyname(module.params['host'])

    neigh_type = module.params['type'].lower()

    device = Device(ip=host, username=username, password=password,
                    protocol=protocol)

    neighbors = nxapi_lib.get_neighbors(device, neigh_type)
    hostname = nxapi_lib.get_hostname(device)

    results = {}
    results['resource'] = neighbors
    results['local_hostname'] = hostname

    module.exit_json(**results)

from ansible.module_utils.basic import *
main()

```
]
]

---

# AnsibleModule Initalization

.left-column[

- **AnsibleModule**
- **argument_spec**
- **choices**
- **default**
- **required**
- **required_together**
- required_one_of
- mutually_exclusive
- **supports_check_mode**
- module.exit_json(key=value, vlan=vlan_id)
- module.fail_json(msg='foo', key=value)
]

.right-column[
```python

def main():

    module = AnsibleModule(
        argument_spec=dict(
            type=dict(choices=['cdp', 'lldp'], default='cdp'),
            protocol=dict(choices=['http', 'https'], default='http'),
            host=dict(required=True),
            username=dict(type='str', required=True),
            password=dict(type='str', required=True),
        ),
        required_together=(
            ['host', 'password', 'username'],
        ),
        supports_check_mode=False

        # extract values from module.params
        username = module.params['username']

        # application code / from your script
        # call you rmethods, use your libs,etc.

        results = dict()
        # return dictionary
        module.exit_json(**results)

```
]

---


# Using the Module

.ubuntu[
- Place the module `get_cisco_neighbors.py` in the `library` directory

```
.
├── configs
│   └── leaf1
│       ├── leaf1.conf
│       └── partials
│           ├── 01_snmp.j2.conf
│           ├── 02_vlans.j2.conf
│           └── 03_interfaces.j2.conf
├── group_vars
│   └── all.yml
├── inventory
├── playbook.yml
├── library
│   └── get_cisco_neighbors.py
├── templates
│   ├── 01_snmp.j2
│   ├── 02_vlans.j2
│   └── 03_interfaces.j2

```
]

```yaml
- name: GET NEIGHBORS
  get_cisco_neighbors: host={{ inventory_hostname }} username=cisco password=cisco
```

---

# Multi-Vendor Modules

- Not many exist, expecially as it pertains to configuration automation
- Build on previous example on gathering neighbor information from Arista

What's needed?

--

- Device/Vendor parameter?
- Standardize keys (k/v)
  - neighbor
  - neighbor_interface
  - local_interface


---

# Idempotent Modules

- Check current state first
  - Perform a *get* or *show* operation
  - We'll call this existing state
- Parameters being sent in from from playbook
  - We'll call this proposed state
- Perform a diff / delta on proposed vs. existing
- Idempotent logic:
  - If there isn't a delta, exit `module.exit_json()` - run N times, make one change
  - If there is a delta, make *only* the needed changes
- *Your* own logic
  - Configuring a VLAN that doesn't exist globally, *fail_out* OR something already configured you want to know about if a change is being made, `module.fail_json`


---

# Example Code (VLAN module)

- existing = dictionary
- proposed = dictionary
- Convert a dictionary to a set and use the difference method to calculate a change set, or delta
- Perform logic


.left-column[
```python
    # snippet
    cmds = None
    if state == 'present':
        delta = dict(set(proposed.iteritems()).difference(
            existing.iteritems()))
        if delta:
            cmds = vlan.build(**delta)
    elif state == 'absent':
        if existing:
            vlan.remove()
    end_state = existing

```
]

.right-column[
```python
    if module.check_mode:
        module.exit_json(changed=True, commands=cmds)
    else:
        device.push_commands(cmds)
        end_state = vlan.get_config()
        changed = True

    results = {}
    results['proposed'] = proposed
    results['existing'] = existing
    results['state'] = state
    results['commands'] = commands
    results['changed'] = changed
    results['end_state'] = end_state

    module.exit_json(**results)
```
]

---

# Summary

- When getting started, write raw Python code first
- Use `module.exit_json(k=v, a=b)` for troubleshooting
- Return helpful data for troubleshooting
- Return helpful data that can be used as inputs for other modules
- Keep the module code small - use libs, functions, etc. to minimize change to the actual module

---

class: middle

# EXTRA - BONUS
# Using the Ansible Vault Feature
### Ansible for Network Automation

---
class: ubuntu

# Ansible Vault

The Ansible Vault functionality allows the user:
- To store sensitive data as a one-way hash on the filesystem
- Use unencrypted data on the fly during playbook execution

Typically used to store username and passwords on the control machine.

```
ntc@ntc:all$ ansible-vault create vaultfile.yml
New Vault password:
Confirm New Vault password:
```

---

# Ansible Vault

The unencrypted file itself, is standard `yaml` that contains structured YAML variables

``` yaml
---
user: ntc
pass: ntc123
```

The encrypted version of above data:

```shell

ntc@ntc:all$ ls
vaultfile.yml
ntc@ntc:all$ cat vaultfile.yml
$ANSIBLE_VAULT;1.1;AES256
38353863306139626235623263313439653437646261393562323036356531336432323736646534
3161333737316430396431313931633863646535303432660a353461636464303238353765343162
31346366353766663063303636386265326665643331326632613536363831346364663065316462
6365646337363838650a326563386465383662643733633930323264333065633034363338643735
33323566656238633436623732623062313562386465666664333961386161313034

```



---
class: ubuntu
# Ansible Vault

- Use the `--ask-vault-pass` flag while invoking the playbook.
- This will prompt you to enter the password used to encrypt the vault file.


```
ntc@ntc:ansible$ ansible-playbook -i inventory use_vault.yml --ask-vault-pass
Vault password:

PLAY [USE ENCRYPTED LOGIN] *******************************************************************************************************

TASK [COLLECT THE SERIAL NUMBER] ******************************************************************************************************
ok: [csr1]
ok: [csr2]
ok: [csr3]

....

```

---

# Ansible Vault - Summary

- Use to encrypt sensitive data on disk
- Encrypt using the `ansible-vault` command
- Invoke a playbook using flag `--ask-vault-pass`


---

class: middle, segue

# EXTRA - BONUS
# Cisco Nexus Ansible Modules
### Ansible for Network Automation

---

# Cisco Nexus Modules

All of these are in Ansible Core.

```bash
nxos_aaa_server_host.py         nxos_hsrp.py            nxos_pim.py             nxos_udld_interface.py
nxos_aaa_server.py              nxos_igmp_interface.py  nxos_pim_rp_address.py  nxos_udld.py
nxos_acl_interface.py           nxos_igmp.py            nxos_ping.py            nxos_vlan.py
nxos_acl.py                     nxos_igmp_snooping.py   nxos_portchannel.py     nxos_vpc_interface.py
nxos_bgp_af.py                  nxos_install_os.py      nxos_reboot.py          nxos_vpc.py
nxos_bgp_neighbor_af.py         nxos_interface_ospf.py  nxos_rollback.py        nxos_vrf_af.py
nxos_bgp_neighbor.py            nxos_interface.py       nxos_smu.py             nxos_vrf_interface.py
nxos_bgp.py                     nxos_ip_interface.py    nxos_snapshot.py        nxos_vrf.py
nxos_command.py                 nxos_mtu.py             nxos_snmp_community.py  nxos_vrrp.py
nxos_config.py                  nxos_ntp_auth.py        nxos_snmp_contact.py    nxos_vtp_domain.py
nxos_evpn_global.py             nxos_ntp_options.py     nxos_snmp_host.py       nxos_vtp_password.py
nxos_evpn_vni.py                nxos_ntp.py             nxos_snmp_location.py   nxos_vtp_version.py
nxos_facts.py                   nxos_nxapi.py           nxos_snmp_traps.py      nxos_vxlan_vtep.py
nxos_feature.py                 nxos_ospf.py            nxos_snmp_user.py       nxos_vxlan_vtep_vni.py
nxos_file_copy.py               nxos_ospf_vrf.py        nxos_static_route.py    nxos_gir_profile_management.py
nxos_overlay_global.py          nxos_switchport.py      nxos_gir.py             nxos_pim_interface.py

```


---

# nxos_facts

.left-column[
- Gathers facts from Nexus devices
  - fan_info
  - hostname
  - uptime
  - interfaces
  - last reboot reason
  - operating system
  - vlan_list
]

.right-column[
```yaml

  tasks:
    - nxos_facts:
```
]

---

# nxos_vlan

- Manages VLAN resources on a Nexus switch
- Parameters:
  - admin_state
  - name
  - vlan_id
  - vlan_state


```yaml
# ensure vlan 110 exists with a name configured
- nxos_vlan:
    vlan_id: 110
    name: DB_VLAN
```

---

# nxos_feature

- Manages features on a Nexus switch
- Parameters:
  - feature

```yaml
# ensure eigrp is disabled
- nxos_feature:
    feature: eigrp
    state: disabled
```

```yaml
# ensure lacp is enabled
- nxos_feature:
    feature: lacp
    state: enabled
```

---

# nxos_file_copy

- Copies a local file to bootflash (by default) of NXOS device using SCP
- Parameters
  - dest_file
  - source_file


```yaml
# copy latest NX-OS to NXOS switch
- nxos_file_copy:
    source_file: /home/cisco/Downloads/nxos.7.0.3.I2.1.bin
```

---

# nxos_portchannel

- Manage port-channel interfaces on Nexus devices
- Parameters:
  - group
  - min_links
  - members (list)
  - mode
- Complex args as a parameter must use YAML format

```yaml
# ensure port-channel 100 exists
- nxos_portchannel:
    group: 100
    min_links: 2
    members:
      - Ethernet1/28
      - Ethernet1/29
```
---

# nxos_vpc

.left-column[
- Manages global VPC configuration
- Parameters:
  - domain
  - role_priority
  - system_priority
  - pkl_src
  - pkl_dest
  - pkl_vrf
  - peer_gw
  - auto_recovery
  - delay_restore
]
.right-column[
```yaml
# ensure port-channel 100 exists
- nxos_vpc:
    domain: 100
    role_priority: 1000
    system_priority: 2000
    pkl_dest: 192.168.100.4
    pkl_src: 10.1.100.20
    peer_gw: true
    auto_recovery: true
```
]

---

# nxos_vpc_interface

- Manages interface VPC configuration
- Parameters:
  - portchannel
  - vpc
  - peer_link


```yaml
# ensure port-channel 100 exists
- nxos_vpc_interface:
    portchannel: 10
    vpc: 100
```


---


class: middle, segue

# EXTRA - BONUS
# Juniper Modules
### Ansible for Network Automation

---



# Juniper Modules

.left-column[
* **junos_commit** — Commit candidate configuration on device.
* **junos_get_config** — Retrieve configuration of device.
* **junos_get_facts** — Retrieve device-specific information from the host.
* **junos_install_config** — Modify the configuration of a device running Junos OS.
* **junos_install_os** — Install a Junos OS software package.
* **junos_rollback** — Rollback configuration of device.
* **junos_shutdown** — Shut down or reboot a device running Junos OS.

]

.right-column[
* **junos_srx_cluster** — Enable/Disable cluster mode for SRX devices
* **junos_zeroize** — Remove all configuration information and reset all key values on a device.
* **junos_cli** - Execute CLI command on device and save file locally
* **junos_rpc** - Execute Junos RPC on device and save file locally
* **junos_get_table** - Retrieve data from device using Junos Tables/Views

]

---

# junos_commit

- Commit candidate configuration on device.

```yaml
- name: COMMIT JUNOS CONFIGURATION
  junos_commit:
   host={{ inventory_hostname }}
   logfile=changes.log
   comment="Commit existing candidate"
```


---

# junos_rollback

- Rollback configuration of device.
- Parameters:
  - confirm - confirmation in minutes to the commit of the configuration
  - diffs_file - location where diffs are stored

```yaml
- junos_rollback:
   host: "{{ inventory_hostname }}"
   logfile=rollback.log
   diffs_file=rollback.diff
   rollback=1
   comment="Rolled back by Ansible"
   confirm=5
```

---

# junos_get_config

- Retrieve configuration of device.

```yaml
- name: GET CONFIG
  junos_get_config: user={{ ansible_user }} passwd={{ ansible_ssh_pass }} host={{ inventory_hostname }} filter="interfaces" dest=configs/interfaces.conf
```
```yaml
- name: GET CONFIG
  junos_get_config: user={{ ansible_user }} passwd={{ ansible_ssh_pass }} host={{ inventory_hostname }} filter="interfaces/protocols" dest=configs/intf_proto.conf
```

---

# junos_install_config

- Modify the configuration of a device running Junos OS.

```yaml
# load merge a change to the Junos OS configuration using NETCONF
- junos_install_config:
    host={{ inventory_hostname }}
    file=banner.conf

# load overwrite a new Junos OS configuration using the CONSOLE port
- junos_install_config:
    host={{ inventory_hostname }}
    console="--telnet={{TERMSERV}},{{TERMSERV_PORT}}"
    file=default_new_switch.conf
    overwrite=yes

# load replace a change to the Junos OS configuration using NETCONF
- junos_install_config:
    host={{ inventory_hostname }}
    file=snmp.conf
    replace=yes
```

---

# junos_install_os

- Install a Junos OS software package.
- Parameters:
    - reboot - booelan; reboots after the installation completes.
    - reboot_pause - Amount of time in seconds to wait after the reboot is issued.  default=10
    - version - Junos OS version string as it would be reported by the show version command
    - package - Absolute path on the local server to the Junos OS software package

```yaml
- junos_install_os:
    host={{ inventory_hostname }}
    version=12.1X46-D10.2
    package=/usr/local/junos/images/junos-vsrx-12.1X46-D10.2-domestic.tgz
```



---

# Summary

- Always test the modules
- Vendors and community are always adding new features
- Understand module idempotency
- Understand if the module supports check mode

---

class: middle, segue

# EXTRA - BONUS
# ntc-ansible Modules
### Ansible for Network Automation

---

# ntc-ansible Modules

- These are modules that are primarily built off of `pyntc`.
- NTC Modules  (covered here)
  - ntc_show_command - send arbitrary show commands and get back structured data
  - ntc_config_command - send arbitrary configuration commands
  - ntc_facts - gather facts
  - ntc_save_config - Save & backup configs
  - ntc_reboot - Reboot devices
  - ntc_file_copy - Copy files to devices
  - ntc_install_os - Upgrade devices
  - ntc_rollback  - creates local backup and restores upon failure in subsequent task

---

# Supported Parameters

Common module parameters between NTC Modules:
  * `platform`, `host`, `username`, `password`

IMPORTANT:
.left-column[

* `platform` values for **ntc_show_command** and **ntc_config_command**:
 * `{{ ntc_vendor }}_{{ ansible_network_os }}`
 * matches what Netmiko supports: **cisco_ios**, **cisco_nxos**, **arista_eos** (optionally _ssh can be added too, e.g. **cisco_ios_ssh**)
 * Anything Netmiko supports for `device_type` is supported here (all SSH)
]

.right-column[
* `platform` values for all other modules must be one of the following:
  * **cisco_ios_ssh**
  * **cisco_nxos_nxapi**
  * **arista_eos_eapi**
  * **juniper_junos_netconf**
]

---

# ntc_show_command

- Multi-vendor Ansible module to streamline converting raw text into JSON key/value pairs
- Leverages TextFSM
- netmiko is used for transport to enable support for all device

```yaml
  tasks:

    - name: GET DATA
      ntc_show_command:
        connection=ssh          # can be offline; if offline uses file parameter for parsing
        platform=cisco_ios
        command='show ip interface brief'
        provider={{ ntc_provider }}
        template_dir: "/etc/ntc/ansible/library/ntc-ansible/ntc-templates/templates"
        use_templates: yes
```

---

class: ubuntu

# ntc_show_command

- JSON data now available to re-use
- Use as inputs to other modules or in templates (docs)

```
$ ansible-playbook -i hosts test-playbook.yml -v

PLAY [GET STRUCTURED DATA BACK FROM CLI DEVICES] ******************************

TASK: [GET DATA] **************************************************************
ok: [csr1] => {"changed": false, "response": [{"intf": "GigabitEthernet1", "ipaddr": "10.0.0.50", "proto": "up", "status": "up"}, {"intf": "GigabitEthernet2", "ipaddr": "10.254.13.1", "proto": "up", "status": "up"}, {"intf": "GigabitEthernet3", "ipaddr": "unassigned", "proto": "down", "status": "administratively down"}, {"intf": "GigabitEthernet4", "ipaddr": "10.254.12.1", "proto": "up", "status": "up"}, {"intf": "Loopback100", "ipaddr": "1.1.1.1", "proto": "up", "status": "up"}]}

PLAY RECAP ********************************************************************
csr1                       : ok=1    changed=0    unreachable=0    failed=0

```

```
csr1#show ip int brief
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet1       10.0.0.50       YES NVRAM  up                    up
GigabitEthernet2       10.254.13.1     YES NVRAM  up                    up
GigabitEthernet3       unassigned      YES NVRAM  administratively down down
GigabitEthernet4       10.254.12.1     YES NVRAM  up                    up
Loopback100            1.1.1.1         YES manual up                    up
```


---

# ntc_config_command

- Send config command from a list or from a file
- This is simply a _wrapper_ for Netmiko
- If Netmiko supports it, ntc_config_command does
- Not idempotent (use core _config modules if they exist for your OS)

.left-column[
```yaml
# write from a command list
- ntc_config_command:
    connection: ssh
    platform: cisco_ios
    commands:
      - vlan 10
      - name vlan_10
      - end
    provider: "{{ ntc_provider }}"
```
]

.right-column[
```yaml
# write config from file
- ntc_config_command:
    connection: ssh
    platform: cisco_ios
    commands_file: "dynamically_created_config.txt"
    provider: "{{ ntc_provider }}"

```
]
---

# ntc_get_facts

.left-column[
Facts returned include:
  - uptime (string)
  - uptime (seconds)
  - model
  - vendor
  - os_version
  - serial_number
  - hostname
  - fqdn
  - vlans
  - interfaces
]

.right-column[
```yaml
- ntc_get_facts:
    platform: cisco_nxos_nxapi
    provider: "{{ ntc_provider }}"
    transport: http

- ntc_get_facts:
    platform: cisco_ios
    provider: "{{ ntc_provider }}"
```
]

---


# ntc_save_config

- Save the running configuration as the startup configuration or to a file on the network device.
  - Performs a commit on Juniper devices / copy run start on others
- **Optionally, save the running configuration as a file to the Ansible control host.**

```yaml
# does a copy run start
- ntc_save_config:
    platform: cisco_nxos_nxapi
    provider: "{{ ntc_provider }}"
    local_file: ./backups/{{ inventory_hostname }}.cfg
```



---

# ntc_reboot

Reboot a network device, optionally on a timer.

```yaml
# reboots the device in 5 minutes
- ntc_reboot:
    platform: cisco_ios
    confirm: true
    timer: 5
    provider: "{{ ntc_provider }}"
```

```yaml
# reboot immediately
- ntc_reboot:
    platform: cisco_ios
    confirm: true
    provider: "{{ ntc_provider }}"
```

---

# ntc_file_copy

- Copy local files to remote network devices using SCP
- Supported platforms
  - Cisco Nexus switches with NX-API
  - Arista switches with eAPI.
  - Cisco IOS switches or routers

```yaml
- ntc_file_copy:
    platform: cisco_nxos_nxapi
    local_file: ./images/{{ ansible_network_os }}/{{ os_version }}
    provider: "{{ ntc_provider }}"
    transport: http

- ntc_file_copy:
    platform=cisco_ios
    local_file=./images/c2800nm-adventerprisek9_ivs_li-mz.151-3.T4.bin
    provider: "{{ ntc_provider }}"

```

---

# ntc_install_os

- Set boot commands and/or upgrade devices (not supported on Juniper)

```yaml
- ntc_install_os:
    platform: cisco_nxos_nxapi
    provider: "{{ ntc_provider }}"
    transport: http
    system_image_file: n9000-dk9.6.1.2.I3.1.bin

- ntc_install_os:
    platform: cisco_nxos_nxapi
    provider: "{{ ntc_provider }}"
    system_image_file: n3000-uk9.6.0.2.U6.5.bin
    kickstart_image_file: n3000-uk9-kickstart.6.0.2.U6.5.bin

- ntc_install_os:
    platform: cisco_ios_ssh
    provider: "{{ ntc_provider }}"
    system_image_file: c2800nm-adventerprisek9_ivs_li-mz.151-3.T4.bin
```

---

# Upgrade Workflow

.left-column[
```yaml

# BACKUP CONFIG FILE

- ntc_save_config:
    platform: cisco_ios
    provider: "{{ ntc_provider }}"
    local_file: {{ inventory_hostname }}.cfg


# COPY IMAGE TO DEVICE

- ntc_file_copy:
    platform: cisco_ios
    local_file: "{{ image_file }}"
    provider: "{{ ntc_provider }}"



.
```
]

.right-column[
```yaml

# UPGRADE AND/OR JUST SET BOOT FILE

- ntc_install_os:
    platform: cisco_nxos_nxapi
    provider: "{{ ntc_provider }}"
    transport: http
    system_image_file: n9000-dk9.6.1.2.I3.1.bin

# OPTIONAL REBOOT: not needed for nxos

- ntc_reboot:
    platform: cisco_ios
    confirm: true
    timer: 5
    provider: "{{ ntc_provider }}"
```
]

---

# ntc_rollback

- Create checkpoint files
- Rollback to previously created checkpoint file

.left-column[
```yaml
- ntc_rollback:
    checkpoint_file: backup.cfg
    platform: cisco_nxos_nxapi
    provider: "{{ ntc_provider }}"

- ntc_rollback:
    rollback_to: backup.cfg
    platform: cisco_nxos_nxapi
    provider: "{{ ntc_provider }}"

```
]



---

# ntc_rollback

- Prior to Ansible 2.0, you would use ntc_rollback for a single task (as also done in an upcoming lab)
- Ansible 2.0 introduced blocks and error handling (`block`,`rescue`, `always`)


```yaml
    tasks:
      - block:
          - name: CREATE LAST KNOWN GOOD (CHECKPOINT)
            ntc_rollback:
              checkpoint_file=last_known_good.conf
              platform: "{{ ntc_vendor }}_{{ ansible_network_os }}_{{ ntc_api }}"
              provider: "{{ ntc_provider }}"
          - nxos_vlan:
              vlan_id: 500
              provider: "{{ provider }}"
          - nxos_vlan:
              vlan_id: 5000
              provider: "{{ provider }}"
        rescue:
          - name: ROLLBACK TO CHECKPOINT FILE UPON ERROR
            ntc_rollback:
              rollback_to: last_known_good.conf
              platform: "{{ ntc_vendor }}_{{ ansible_network_os }}_{{ ntc_api }}"
              provider: "{{ ntc_provider }}"



```




