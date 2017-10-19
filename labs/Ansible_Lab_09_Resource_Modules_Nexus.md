## Lab 9.1 - Cisco NX-OS Modules

For the Nexus switches, you will not be building a particular topology.  Rather, you will learn how to use the Nexus modules with some other features of Ansible.

### Task 1 - Configure Layer 3 Interfaces

##### Step 1

Create a new playbook called `cisco.yml`.

It should have one task to add a new VLAN.  (VLAN ID 10 with name "web_vlan")

Ensure you still have `provider` built and stored in `group_vars/all.yml`.

```yaml

---

  - name: CISCO PLAYBOOK
    hosts: nxos-spines
    connection: local
    gather_facts: no

    tasks:

      - name: ENSURE VLANS EXIST
        nxos_vlan:
          vlan_id: 10
          provider: "{{ provider }}"

```

##### Step 2

Take a minute and use `ansible-doc` to learn how to use `nxos_vlan`.

Enter `ansible-doc nxos_vlan` on the Linux terminal.  This can be done for any module.

##### Step 3

Save and run the playbook.

```
ntc@ntc:~/ansible$ ansible-playbook -i inventory cisco.yml
```

##### Step 4

SSH into *nxos-spine2* and remove the VLAN that was just added using the `no vlan 10` global configurasstion command.

##### Step 5

Run the playbook again, but this time using verbose mode (using the `-v` flag).

```
ntc@ntc:ansible$ ansible-playbook -i inventory cisco.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [CISCO PLAYBOOK] *****************************************************************************************

TASK [ENSURE VLANS EXIST] *************************************************************************************
changed: [nxos-spine2] => {"changed": true, "commands": ["vlan 10", "exit"], "failed": false}
ok: [nxos-spine1] => {"changed": false, "commands": [], "failed": false}

PLAY RECAP ****************************************************************************************************
nxos-spine1                : ok=1    changed=0    unreachable=0    failed=0   
nxos-spine2                : ok=1    changed=1    unreachable=0    failed=0   

ntc@ntc:ansible$   
```

Remember that every module *returns* data (JSON object).  To display that data, you can use verbose mode.  This data can also be saved and stored to use as inputs into other tasks or in templates using the *register* directive.


##### Step 6

Run the playbook.

```
ntc@ntc:~/ansible$ ansible-playbook -i inventory cisco.yml
```

##### Step 7

Use **ansible-doc** to explore **nxos_interface**, **nxos_vrf**, **nxos_vrf_interface**, and **nxos_ip_interface**

Be sure to look at the examples for each.

##### Step 8


Create two new files in the `host_vars` sub-directory: 
  * `nxos-spine1.yml`
  * `nxos-spine2.yml`

We will use these files to configure interface IP addresses on the devices as they are specific to each device.

`host_vars/nxos-spine1.yml`

```yaml
---

interfaces:
  Eth2/3:
    ip: 10.100.100.1
    mask: 24
    vrf: NTC
    mode: layer3

```

`host_vars/nxos-spine2.yml`

```yaml
---

interfaces:
  Eth2/3:
    ip: 10.100.100.2
    mask: 24
    vrf: NTC
    mode: layer3

```


##### Step 9

Add a new task to first ensure interface Eth2/3 is a layer 3 port.

```yaml
---

  - name: CISCO PLAYBOOK
    hosts: nxos-spines
    connection: local
    gather_facts: no

    tasks:

      - name: ENSURE VLANS EXIST
        nxos_vlan:
          vlan_id: 10
          provider: "{{ provider }}"

      - nxos_interface:
          interface: Eth2/3
          mode: layer3
          provider: "{{ provider }}"
```

##### Step 10

Since we want it to be possible to easily create more Layer 3 interfaces, now add one more interface to `host_vars/nxos-spine1.yml` as such:

```yaml
---
interfaces:
  Eth2/3:
    ip: 10.100.100.1
    mask: 24
    vrf: NTC
    mode: layer3
  Eth2/4:
    ip: 10.1.99.1
    mask:24
    vrf: NTC
    mode: layer3
```

##### Step 11

Using an Ansible iterator (loop), loop through the interfaces in this same task:

```yaml
---

  - name: CISCO PLAYBOOK
    hosts: nxos-spines
    connection: local
    gather_facts: no

    tasks:

      - name: ENSURE VLANS EXIST
        nxos_vlan:
          vlan_id: 10
          provider: "{{ provider }}"

      - nxos_interface:
          interface: "{{ item.key }}"
          mode: "{{ item.value.mode }}"
          provider: "{{ provider }}"
        with_dict: "{{ interfaces }}"
```


Here we are showing how to use `with_dict` to iterate just over a dictionary.  `item` is equal to the root key and `item.value.<key>` is used to access individual children (nested key objects).

Reference Ansible [docs](http://docs.ansible.com/ansible/playbooks_loops.html#looping-over-hashes) to see more examples on how to use `with_dict`.

##### Step 12

Re-run the playbook.  Which device had a change and which did not?


##### Step 13

Add the required tasks now to ensure interface Eth2/3 is a routed port and is in the VRF named NTC and is assigned the correct IP address you defined in the variables files.

> Remember to use **ansible-doc** on **nxos_interface**, **nxos_vrf**, **nxos_vrf_interface**, and **nxos_ip_interface**

**Scroll down for the solution.**


### Task 2 - Managing NXOS Features

In this task, you will use Ansible to manage the enabling and disabling features on NX-OS devices.

##### Step 1

Add a new task using the **nxos_feature** module to ensure the VTP, VPC and VRRP features are enabled while ensuring HSRP is disabled.  

Create a list of features and use `with_items` in a SINGLE task to iterate through them.  Hint: it'll be a list of dictionaries and each dictionary that has two keys `feature` and `state`. You can store the list in the playbook or put them in `group_vars/nxos.yml`

Use a tag called "feature" so you can just selectively run this task.

Use [docs.ansible.com](docs.ansible.com) or ansible-doc accordingly.

**Scroll down for the solution.**


### Task 3 - Managing SNMP Community Strings

In this task, you will use Ansible to manage the deployment of SNMP community strings on NX-OS devices.

##### Step 1

Ensure the following two community strings on all nxos devices:

* Role: network-operator and Community: ntc-public
* Role: network-admin and Community: ntc-private

Note: use a list of dictionaries and store a variable called `snmp` in `group_vars/nxos.yml`.

Tag this task using a tag called "snmp" so you can just run this task.

Use [docs.ansible.com](docs.ansible.com) or ansible-doc accordingly.

**Scroll down for the solution.**


### Task 4 - Reachability Testing

In this task, you will use Ansible to test reachability between the Nexus switches.

##### Step 1

Use the **nxos_ping** module on *nxos-spine1* to ping the routed interface (Eth2/3) on *nxos-spine2*.

Tag this task using a tag called "ping".

When you run the playbook, you can use `--limit nxos-spine1`

##### Step 2

Use the **nxos_ping** module on *nxos-spine1* to ping the management interface (mgmt0) on *nxos-spine2*.

Tag this task using a tag called "ping".

When you run the playbook, you can use `--limit nxos-spine1`


# Solutions


### Task 1 - Step 11

```yaml
---

  - name: CISCO PLAYBOOK
    hosts: nxos-spines
    connection: local
    gather_facts: no

    tasks:

      - name: ENSURE VLANS EXIST
        nxos_vlan:
          vlan_id: 10
          provider: "{{ provider }}"

      - nxos_vrf:
          vrf: "{{ item.value.vrf }}"
          provider: "{{ provider }}"
        with_dict: "{{ interfaces }}"

      - nxos_vrf_interface:
          interface: "{{ item.key }}"
          vrf: "{{ item.value.vrf }}"
          provider: "{{ provider }}"
        with_dict: "{{ interfaces }}"

      - nxos_ip_interface:
          interface: "{{ item.key }}"
          addr: "{{ item.value.ip }}"
          mask: "{{ item.value.mask }}"
          provider: "{{ provider }}"
        with_dict: "{{ interfaces }}"
```


### Task 2

You could have also stored a `features` variable in a vars file if you didn't want to embed the list in the playbook as shown below.

New task:

```yaml
      - nxos_feature:
          feature: "{{ item.feature }}"
          state: "{{ item.state }}"
          provider: "{{ provider }}"
        with_items:
          - feature: vtp
            state: enabled
          - feature: vtp
            state: enabled
          - feature: vrrp
            state: enabled
          - feature: hsrp
            state: disabled
        tags: feature
```

### Task 3


`group_vars/nxos.yml`

```yaml
---


snmp:
    - community: ntc-public
      group: network-operator
    - community: ntc-private
      group: network-admin

```

New task:
```yaml
    - nxos_snmp_community:
        community: "{{ item.community }}"
        group: "{{ item.group }}"
        state: present
        host: "{{ inventory_hostname }}"
        username: "{{ un }}"
        password: "{{ pwd }}"
      with_items: "{{ snmp }}"
      tags: snmp
```

### Task 4

Ping the routed interface (Eth2/3) on nxos-spine2.

```yaml
      - nxos_ping:
          dest: "10.100.100.2"
          vrf: NTC
          provider: "{{ provider }}"
```

Ping the management interface (mgmt0) on nxos-spine2.
```yaml
      - nxos_ping:
          dest: "10.0.0.72"
          vrf: management
          provider: "{{ provider }}"
```
