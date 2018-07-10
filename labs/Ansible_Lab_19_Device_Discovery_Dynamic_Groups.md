## Lab 19 - Discovering Device Types and Dynamically Creating Groups

Ansible is best known for issuing configuration commands, but as you've seen, you can also issue show commands to the device and collect data.  Because Ansible is extensible, it's possible to perform anything inside a module that you could write a script for. 

In this Lab, we'll use an open source module called `snmp_device_version` that queries devices based on commmunity and returns a set of attributes including vendor, OS type, and OS version.


### Task 1 - Preparing the Devices

We need to ensure there is a baseline community string on every device, so in this first task, you'll execute a playbook that'll configure the "networktocode" community on all IOS, NXOS, and JUNOS devices in the course.

##### Step 1

Create a playbook called `configure-snmp.yml` and insert the following into it:

```yaml
---
  
  - name: IOS PLAY
    hosts: iosxe
    connection: network_cli
    gather_facts: no
    tags: ios 

    tasks:

      - name: IOS SNMP
        ios_config:
          commands: "snmp-server community networktocode RO"

  - name: NXOS PLAY
    hosts: nxos
    connection: network_cli
    gather_facts: no
    tags: nxos

    tasks:

      - name: NXOS SNMP
        nxos_config:
          commands: "snmp-server community networktocode group network-operator"

  - name: JUNOS PLAY
    hosts: vmx
    gather_facts: no
    tags: vmx

    tasks:

      - name: JUNOS SNMP 
        junos_config:
          lines: "set snmp community networktocode authorization read-only"

```

##### Step 2

Save and execute the playbook.


### Task 2 - Discover Devices with SNMP

Now that all devices have the "networktocode" SNMP community string configured, we discovery attributes of the device querying that string for certain MIBs.

##### Step 1

Create a new playbook called `snmp-discovery.yml`.

In the first step, you'll query the devices using the `snmp_device_version`  module.


```yaml
---

  - name: PLAY 1 - DISCOVER OS 
    hosts: iosxe,nxos,vmx
    connection: network_cli
    gather_facts: no

    tasks:

      - name: QUERY DEVICE VIA SNMP
        snmp_device_version:
          community: networktocode
          version: 2c
          host: "{{ inventory_hostname }}"
```

##### Step 2

Execute the playbook using verbose mode and limit the playbook to just **csr1** and **nxos-spine1**.

```

ntc@ntc:ansible$ ansible-playbook -i inventory snmp-discovery.yml --limit csr1,nxos-spine1 -v 
Using /etc/ansible/ansible.cfg as config file

PLAY [PLAY 1 - DISCOVER OS] ****************************************************

TASK [QUERY DEVICE VIA SNMP] ***************************************************
ok: [nxos-spine1] => {"ansible_facts": {"ansible_device_os": "nxos", "ansible_device_vendor": "cisco", "ansible_device_version": "7.3(1)D1(1)"}, "changed": false}
ok: [csr1] => {"ansible_facts": {"ansible_device_os": "ios", "ansible_device_vendor": "cisco", "ansible_device_version": "16.6.2"}, "changed": false}
```

See the data discovered for each device?

##### Step 3

Note that whenever you see `ansible_facts`, you can access that variable directly without using `register`.

Add debug statements for each of the three values coming back.


```yaml
      - debug:
          var: ansible_device_os
      - debug:
          var: ansible_device_version
      - debug:
          var: ansible_device_vendor
```


##### Step 4

Save and re-run the playbook just for both devices again--still using verbose mode.

```
PLAY [PLAY 1 - DISCOVER OS] ****************************************************

TASK [QUERY DEVICE VIA SNMP] ***************************************************
ok: [csr1] => {"ansible_facts": {"ansible_device_os": "ios", "ansible_device_vendor": "cisco", "ansible_device_version": "16.6.2"}, "changed": false}
ok: [nxos-spine1] => {"ansible_facts": {"ansible_device_os": "nxos", "ansible_device_vendor": "cisco", "ansible_device_version": "7.3(1)D1(1)"}, "changed": false}

TASK [debug] *******************************************************************
ok: [csr1] => {
    "ansible_device_os": "ios"
}
ok: [nxos-spine1] => {
    "ansible_device_os": "nxos"
}

TASK [debug] *******************************************************************
ok: [csr1] => {
    "ansible_device_version": "16.6.2"
}
ok: [nxos-spine1] => {
    "ansible_device_version": "7.3(1)D1(1)"
}

TASK [debug] *******************************************************************
ok: [csr1] => {
    "ansible_device_vendor": "cisco"
}
ok: [nxos-spine1] => {
    "ansible_device_vendor": "cisco"
}
```


### Task 3 - Creating Dynamic Groups

It's difficult to create groups for data such as OS version or anything that could be variable over time.  In this case, you can use dynamic groups. This task will create dynamic groups using the data collected via SNMP.

You'll create three ad-hoc dynamic groups called "os_ios", "os_nxos", and "os_junos".


##### Step 1

Add a task to the same playbook from Task 2.

This task will show you how to use the `group_by` module.

```yaml
---


  - name: PLAY 1 - DISCOVER OS 
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

      - debug:
          var: ansible_device_os
      - debug:
          var: ansible_device_version
      - debug:
          var: ansible_device_vendor

      - group_by:
          key: os_{{ ansible_device_os }}    
```

As soon as the playbook reaches the `group_by` task, it'll create dynamic groups using the `key` paramemter resulting in new groups that map back to the `ansible_device_os` variable.

##### Step 2

Let's prove the dynamic groups are created and create 3 more plays that automate each new group simply printing the hostname of each device in each new group.

Add the following PLAYS to the same playbook.


```yaml
  - name: AUTOMATE IOS DEVICES
    hosts: os_ios
    connection: network_cli
    gather_facts: no

    tasks:

      - debug: var=inventory_hostname

  - name: AUTOMATE NEXUS DEVICES
    hosts: os_nxos
    connection: network_cli
    gather_facts: no

    tasks:

      - debug: var=inventory_hostname

  - name: AUTOMATE JUNOS DEVICES
    hosts: os_junos
    connection: network_cli
    gather_facts: no

    tasks:

      - debug: var=inventory_hostname
```


The full playbook should look like this:

```yaml
---


  - name: PLAY 1 - DISCOVER OS 
    hosts: iosxe,nxos,vmx
    connection: network_cli
    gather_facts: no
    tags: discover

    tasks:

      - name: QUERY DEVICE VIA SNMP
        snmp_device_version:
          community: networktocode
          version: 2c
          host: "{{ inventory_hostname }}"
        tags: snmp  

      - debug:
          var: ansible_device_os
      - debug:
          var: ansible_device_version
      - debug:
          var: ansible_device_vendor

      - group_by:
          key: os_{{ ansible_device_os }}    

  - name: AUTOMATE IOS DEVICES
    hosts: os_ios
    connection: network_cli
    gather_facts: no

    tasks:

      - debug: var=inventory_hostname

  - name: AUTOMATE NEXUS DEVICES
    hosts: os_nxos
    connection: network_cli
    gather_facts: no

    tasks:

      - debug: var=inventory_hostname

  - name: AUTOMATE JUNOS DEVICES
    hosts: os_junos
    connection: netconf
    gather_facts: no

    tasks:

      - debug: var=inventory_hostname
```

##### Step 3

Save and execute the playbook.

You should see this output proving the creation of 3 new groups:

```yaml
ntc@ntc:ansible$ ansible-playbook -i inventory snmp-discovery.yml

PLAY [PLAY 1 - DISCOVER OS] ****************************************************

TASK [QUERY DEVICE VIA SNMP] ***************************************************
ok: [nxos-spine1]
ok: [csr1]
ok: [csr2]
ok: [nxos-spine2]
ok: [csr3]
ok: [vmx7]
ok: [vmx8]
ok: [vmx9]

TASK [debug] *******************************************************************
ok: [csr1] => {
    "ansible_device_os": "ios"
}
ok: [csr2] => {
    "ansible_device_os": "ios"
}
ok: [csr3] => {
    "ansible_device_os": "ios"
}
ok: [nxos-spine1] => {
    "ansible_device_os": "nxos"
}
ok: [nxos-spine2] => {
    "ansible_device_os": "nxos"
}
ok: [vmx7] => {
    "ansible_device_os": "junos"
}
ok: [vmx8] => {
    "ansible_device_os": "junos"
}
ok: [vmx9] => {
    "ansible_device_os": "junos"
}

TASK [debug] *******************************************************************
ok: [csr1] => {
    "ansible_device_version": "16.6.2"
}
ok: [csr2] => {
    "ansible_device_version": "16.6.2"
}
ok: [csr3] => {
    "ansible_device_version": "16.6.2"
}
ok: [nxos-spine1] => {
    "ansible_device_version": "7.3(1)D1(1)"
}
ok: [nxos-spine2] => {
    "ansible_device_version": "7.3(1)D1(1)"
}
ok: [vmx7] => {
    "ansible_device_version": "15.1F4.15"
}
ok: [vmx8] => {
    "ansible_device_version": "15.1F4.15"
}
ok: [vmx9] => {
    "ansible_device_version": "15.1F4.15"
}

TASK [debug] *******************************************************************
ok: [csr1] => {
    "ansible_device_vendor": "cisco"
}
ok: [csr2] => {
    "ansible_device_vendor": "cisco"
}
ok: [csr3] => {
    "ansible_device_vendor": "cisco"
}
ok: [nxos-spine1] => {
    "ansible_device_vendor": "cisco"
}
ok: [nxos-spine2] => {
    "ansible_device_vendor": "cisco"
}
ok: [vmx7] => {
    "ansible_device_vendor": "juniper"
}
ok: [vmx8] => {
    "ansible_device_vendor": "juniper"
}
ok: [vmx9] => {
    "ansible_device_vendor": "juniper"
}

TASK [group_by] ****************************************************************
ok: [csr1]
ok: [csr2]
ok: [csr3]
ok: [nxos-spine1]
ok: [nxos-spine2]
ok: [vmx7]
ok: [vmx8]
ok: [vmx9]

PLAY [AUTOMATE IOS DEVICES] ****************************************************

TASK [debug] *******************************************************************
ok: [csr1] => {
    "inventory_hostname": "csr1"
}
ok: [csr2] => {
    "inventory_hostname": "csr2"
}
ok: [csr3] => {
    "inventory_hostname": "csr3"
}

PLAY [AUTOMATE NEXUS DEVICES] **************************************************

TASK [debug] *******************************************************************
ok: [nxos-spine1] => {
    "inventory_hostname": "nxos-spine1"
}
ok: [nxos-spine2] => {
    "inventory_hostname": "nxos-spine2"
}

PLAY [AUTOMATE JUNOS DEVICES] **************************************************

TASK [debug] *******************************************************************
ok: [vmx7] => {
    "inventory_hostname": "vmx7"
}
ok: [vmx8] => {
    "inventory_hostname": "vmx8"
}
ok: [vmx9] => {
    "inventory_hostname": "vmx9"
}

PLAY RECAP *********************************************************************
csr1                       : ok=6    changed=0    unreachable=0    failed=0   
csr2                       : ok=6    changed=0    unreachable=0    failed=0   
csr3                       : ok=6    changed=0    unreachable=0    failed=0   
nxos-spine1                : ok=6    changed=0    unreachable=0    failed=0   
nxos-spine2                : ok=6    changed=0    unreachable=0    failed=0   
vmx7                       : ok=6    changed=0    unreachable=0    failed=0   
vmx8                       : ok=6    changed=0    unreachable=0    failed=0   
vmx9                       : ok=6    changed=0    unreachable=0    failed=0   

ntc@ntc:ansible$ 
```
