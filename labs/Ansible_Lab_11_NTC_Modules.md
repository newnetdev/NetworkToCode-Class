## Lab 11 - Using NTC Modules

In this section, we'll look at how to use multi-vendor modules to perform system level change on the device.  These modules map directly back to what we did with `pyntc` in Module 2.

### Task 1 - Performing Operational Tasks with ntc-ansible Modules

##### Step 1

Navigate to the `ansible` sub-directory in your home directory.

**Ensure you have a sub-directory called `backups` within the `ansible` directory.**

##### Step 2

Create a new playbook called `ntcpb.yml` in the `ansible` directory.

It should have one task that will save the running config AND backup the running configs of all five devices in the inventory file.

Save the configs in the backups directory with each filename following the format of `<hostname>_ansible.cfg`.

You will use the Ansible module called `ntc_save_config` to do this.


```yaml
---

  - name: Multi-Vendor testing
    hosts: all
    connection: local
    gather_facts: no

    vars:
      ntc_provider:
        host: "{{ inventory_hostname }}"
        username: "{{ un }}"
        password: "{{ pwd }}"
        platform: "{{ vendor }}_{{ os }}_{{ api }}"

    tasks:

      - name: BACKUP CURRENT RUNNING CONFIGS
        ntc_save_config:
          local_file=backups/{{ inventory_hostname }}_ansible.cfg
          provider={{ ntc_provider }}

```

Notice what we are doing with the `platform` parameter.  We can concatenating three strings as the input for `platform` because platform must be cisco_nxos_nxapi, arista_eos_eapi, juniper_junos_netconf, or cisco_ios_ssh for this particular module.

##### Step 4

Execute the playbook with the following command:

```
ntc@ntc:~/ansible$ ansible-playbook -i inventory ntcpb.yml
```

```
ntc@ntc:~/ansible$ ansible-playbook -i inventory ntcpb.yml

PLAY [Multi-Vendor testing] *************************************************** 

TASK: [BACKUP CURRENT RUNNING CONFIGS] **************************************** 
changed: [csr1]
changed: [csr2]
changed: [csr3]
changed: [nxos-spine1]
changed: [nxos-spine2]
changed: [eos-spine1]
changed: [eos-spine2]
changed: [eos-leaf1]
changed: [eos-leaf2]

PLAY RECAP ******************************************************************** 
csr1                       : ok=1    changed=1    unreachable=0    failed=0   
csr2                       : ok=1    changed=1    unreachable=0    failed=0   
csr3                       : ok=1    changed=1    unreachable=0    failed=0   
nxos-spine1                : ok=1    changed=1    unreachable=0    failed=0   
nxos-spine2                : ok=1    changed=1    unreachable=0    failed=0   
eos-spine1                 : ok=1    changed=1    unreachable=0    failed=0   
eos-spine2                 : ok=1    changed=1    unreachable=0    failed=0   
eos-leaf1                  : ok=1    changed=1    unreachable=0    failed=0   
eos-leaf2                  : ok=1    changed=1    unreachable=0    failed=0   

```

> This output may not include every device you have in your pod.

##### Step 5

View the backups directory.

```
ntc@ntc:~/ansible$ ls backups/
csr1_ansible.cfg  csr3_ansible.cfg   eos-leaf2_ansible.cfg   eos-spine2_ansible.cfg   nxos-spine2_ansible.cfg
csr2_ansible.cfg  eos-leaf1_ansible.cfg  eos-spine1_ansible.cfg  nxos-spine1_ansible.cfg

```

##### Step 6

Re-run the playbook in verbose mode.

```
ntc@ntc:~/ansible$ ansible-playbook -i inventory ntcpb.yml -v

PLAY [Multi-Vendor testing] *************************************************** 

TASK: [BACKUP CURRENT RUNNING CONFIGS] **************************************** 
changed: [eos-leaf2] => {"changed": true, "local_file": "backups/eos-leaf2_ansible.cfg", "remote_file": "(Startup Config)", "remote_save_successful": true}
changed: [eos-leaf1] => {"changed": true, "local_file": "backups/eos-leaf1_ansible.cfg", "remote_file": "(Startup Config)", "remote_save_successful": true}
changed: [nxos-spine1] => {"changed": true, "local_file": "backups/nxos-spine1_ansible.cfg", "remote_file": "(Startup Config)", "remote_save_successful": true}
changed: [eos-spine1] => {"changed": true, "local_file": "backups/eos-spine1_ansible.cfg", "remote_file": "(Startup Config)", "remote_save_successful": true}
changed: [nxos-spine2] => {"changed": true, "local_file": "backups/nxos-spine2_ansible.cfg", "remote_file": "(Startup Config)", "remote_save_successful": true}
changed: [eos-spine2] => {"changed": true, "local_file": "backups/eos-spine2_ansible.cfg", "remote_file": "(Startup Config)", "remote_save_successful": true}
changed: [csr1] => {"changed": true, "local_file": "backups/csr1_ansible.cfg", "remote_file": "(Startup Config)", "remote_save_successful": true}
changed: [csr2] => {"changed": true, "local_file": "backups/csr2_ansible.cfg", "remote_file": "(Startup Config)", "remote_save_successful": true}
changed: [csr3] => {"changed": true, "local_file": "backups/csr3_ansible.cfg", "remote_file": "(Startup Config)", "remote_save_successful": true}

PLAY RECAP ******************************************************************** 
csr1                       : ok=1    changed=1    unreachable=0    failed=0   
csr2                       : ok=1    changed=1    unreachable=0    failed=0   
csr3                       : ok=1    changed=1    unreachable=0    failed=0   
eos-leaf1                  : ok=1    changed=1    unreachable=0    failed=0   
eos-leaf2                  : ok=1    changed=1    unreachable=0    failed=0   
eos-spine1                 : ok=1    changed=1    unreachable=0    failed=0   
eos-spine2                 : ok=1    changed=1    unreachable=0    failed=0   
nxos-spine1                : ok=1    changed=1    unreachable=0    failed=0   
nxos-spine2                : ok=1    changed=1    unreachable=0    failed=0   
  
```

You can see where the local file is being saved, ensure it was successful, and also see where the running config was save on the box.  For example, we didn't specify `remote_file` in the task, but if we did, we can do the equivalent of `copy run filename`.  In the absence of the `remote_file` parameter, a `copy run start` is being performed.

##### Step 7

Create a new file in the `ansible` directory called `fake_config.cfg` and put any arbitrary text in it.

Our goal is to copy this over to each of the five devices using the `ntc_file_copy` module.

##### Step 8

Add a new task in the playbook and use the tag called "copy".  Using tags allows us to selectively execute this tasks without re-executing other tasks.

```yaml
      - name: COPY FAKE FILE TO DEVICES
        ntc_file_copy:
          local_file=fake_config.cfg
          provider={{ ntc_provider }}
        tags: copy
```

So the full playbook will look like this:

```yaml
---

  - name: Multi-Vendor testing
    hosts: all
    connection: local
    gather_facts: no

    vars:
      ntc_provider:
        host: "{{ inventory_hostname }}"
        username: "{{ un }}"
        password: "{{ pwd }}"
        platform: "{{ vendor }}_{{ os }}_{{ api }}"

    tasks:

      - name: BACKUP CURRENT RUNNING CONFIGS
        ntc_save_config:
          local_file=backups/{{ inventory_hostname }}_ansible.cfg
          provider={{ ntc_provider }}

      - name: COPY FAKE FILE TO DEVICES
        ntc_file_copy:
          local_file=fake_config.cfg
          provider={{ ntc_provider }}
        tags: copy

```

##### Step 9

Execute the playbook using the "copy" tag.

```
ntc@ntc:~/ansible$ ansible-playbook -i inventory ntcpb.yml --tags=copy

PLAY [Multi-Vendor testing] *************************************************** 

TASK: [COPY FAKE FILE TO DEVICES] ********************************************* 
changed: [csr1]
changed: [csr2]
changed: [csr3]
changed: [nxos-spine1]
changed: [nxos-spine2]
changed: [eos-spine1]
changed: [eos-spine2]
changed: [eos-leaf1]
changed: [eos-leaf2]

PLAY RECAP ******************************************************************** 
csr1                       : ok=1    changed=1    unreachable=0    failed=0   
csr2                       : ok=1    changed=1    unreachable=0    failed=0   
csr3                       : ok=1    changed=1    unreachable=0    failed=0   
nxos-spine1                : ok=1    changed=1    unreachable=0    failed=0   
nxos-spine2                : ok=1    changed=1    unreachable=0    failed=0   
eos-spine1                 : ok=1    changed=1    unreachable=0    failed=0   
eos-spine2                 : ok=1    changed=1    unreachable=0    failed=0   
eos-leaf1                  : ok=1    changed=1    unreachable=0    failed=0   
eos-leaf2                  : ok=1    changed=1    unreachable=0    failed=0    

```

Feel free to verify the fake config file has been transferred to each device.


##### Step 10

Re-run the playbook using the same command.

```
 ansible-playbook -i inventory ntcpb.yml --tags=copy

PLAY [Multi-Vendor testing] *************************************************** 

TASK: [COPY FAKE FILE TO DEVICES] ********************************************* 
ok: [nxos-spine2]
ok: [nxos-spine1]
ok: [csr2]
ok: [csr1]
ok: [csr3]
ok: [eos-spine1]
ok: [eos-spine2]
ok: [eos-leaf1]
ok: [eos-leaf2]

PLAY RECAP ******************************************************************** 
csr1                       : ok=1    changed=0    unreachable=0    failed=0   
csr2                       : ok=1    changed=0    unreachable=0    failed=0   
csr3                       : ok=1    changed=0    unreachable=0    failed=0   
nxos-spine1                : ok=1    changed=0    unreachable=0    failed=0   
nxos-spine2                : ok=1    changed=0    unreachable=0    failed=0 
eos-spine1                 : ok=1    changed=0    unreachable=0    failed=0   
eos-spine2                 : ok=1    changed=0    unreachable=0    failed=0   
eos-leaf1                  : ok=1    changed=0    unreachable=0    failed=0   
eos-leaf2                  : ok=1    changed=0    unreachable=0    failed=0 
```


You can see now everything is "OK" because the file already exists on switch, so no copy is being performed. This happens because a file with the same name and MD5 exists on the switch already.

##### Step 11

In this step, we will make configuration changes to the IOS devices using the `ntc_config_command` module.

You will add a new local user and configure a new SNMP community read-only string.

Rather than create a new task, this time, create a new play.  Use the tag called "config".

The new play should look like this:

> IMPORTANT: ntc_config_command and ntc_show_command do not use APIs, they use SSH so the platform parameter is a bit different.


```yaml
  - name: Send commands to CSR routers
    hosts: iosxe
    connection: local
    gather_facts: no

    vars:
      ntc_provider:
        host: "{{ inventory_hostname }}"
        username: "{{ un }}"
        password: "{{ pwd }}"
        platform: "{{ vendor }}_{{ os }}_{{ api }}"

    tasks:

      - name: SEND CONFIG COMMANDS AS LIST
        ntc_config_command:
          connection: ssh
          commands:
            - username testuser password testpass
            - snmp-server community newrostring ro
            - end
          provider: "{{ ntc_provider }}"
        tags: config
```

As you can see there is also a parameter called `secret` that is commented out.  If you have an enable secret on the device, you would need to use this parameter.

Additionally, there is a parameter not shown that allows you to send commands from a file too.

Connect to your devices if you want to verify the commands were sent properly.

##### Step 12

Run the playbook using the following command:

```
$ ansible-playbook -i inventory ntcpb.yml --tags=config
```


```
ntc@ntc:~/ansible$ ansible-playbook -i inventory ntcpb.yml --tags=config

PLAY [Send commands to CSR routers] ******************************************* 

TASK: [SEND CONFIG COMMANDS AS LIST] ****************************************** 
changed: [csr2]
changed: [csr3]
changed: [csr1]

PLAY RECAP ******************************************************************** 
csr1                       : ok=1    changed=1    unreachable=0    failed=0   
csr2                       : ok=1    changed=1    unreachable=0    failed=0   
csr3                       : ok=1    changed=1    unreachable=0    failed=0   

```

##### Step 13

In this step, you will gather data from each device using the `ntc_get_facts` module.

Add the following task to your **second** play:

```yaml
      - name: GET FACTS
        ntc_get_facts:
          provider={{ ntc_provider }}
        tags: facts
```

##### Step 14

Run the playbook.  This time only for the "facts" tag and in verbose mode.

You will see the following output.

```
$ ansible-playbook -i inventory ntcpb.yml --tags=facts -v

PLAY [Send commands to CSR routers] ******************************************* 

TASK: [GET FACTS] ************************************************************* 
ok: [csr2] => {"ansible_facts": {"fqdn": "N/A", "hostname": "csr2", "interfaces": ["GigabitEthernet1", "GigabitEthernet2", "GigabitEthernet3", "GigabitEthernet4"], "ios": {"config_register": "0x2102"}, "model": "CSR1000V", "os_version": "15.5(1)S1", "serial_number": "", "uptime": 5160, "uptime_string": "00:01:26:00", "vendor": "cisco", "vlans": []}, "changed": false}
ok: [csr3] => {"ansible_facts": {"fqdn": "N/A", "hostname": "csr3", "interfaces": ["GigabitEthernet1", "GigabitEthernet2", "GigabitEthernet3", "GigabitEthernet4", "Loopback100"], "ios": {"config_register": "0x2102"}, "model": "CSR1000V", "os_version": "15.5(1)S1", "serial_number": "", "uptime": 5160, "uptime_string": "00:01:26:00", "vendor": "cisco", "vlans": []}, "changed": false}
ok: [csr1] => {"ansible_facts": {"fqdn": "N/A", "hostname": "csr1", "interfaces": ["GigabitEthernet1", "GigabitEthernet2", "GigabitEthernet3", "GigabitEthernet4", "Loopback100"], "ios": {"config_register": "0x2102"}, "model": "CSR1000V", "os_version": "15.5(1)S1", "serial_number": "", "uptime": 5160, "uptime_string": "00:01:26:00", "vendor": "cisco", "vlans": []}, "changed": false}

PLAY RECAP ******************************************************************** 
csr1                       : ok=1    changed=0    unreachable=0    failed=0   
csr2                       : ok=1    changed=0    unreachable=0    failed=0   
csr3                       : ok=1    changed=0    unreachable=0    failed=0   
```

In the section on the data collection and reporting, we'll look at how to use this data to dynamically generate reports.

##### Step 15

This step is informational.  Please note there are a few other "ntc" modules that include:

* ntc_show_command - covered in the data collection and reporting section
* ntc_rollback - covered in the next lab
* ntc_reboot - available, and feel free to try it, but it reboots devices so be careful!
* ntc_install_os - sets boot loader and upgrades the device (based on platform)


### Task 2 - Multi-Vendor Configuration Rollback

Devices, features, platforms, and Ansible modules all operate different.  It may be based on intent or an unknown bug in the system.  Offering the ability to create a last known good config (checkpoint file) and then roll back to that config if there is an error is critical for production environments.  

This is what the **ntc_rollback** module does.

##### Step 1

Create a new playbook called `rollback.yml`.

##### Step 2

Create the play definition and choose to automate Nexus or Arista devices.

```yaml
---

  - name: ROLLBACK PLAYBOOK
    hosts: nxos
    connection: local
    gather_facts: no

    vars:
      nxos_provider:
        host: "{{ inventory_hostname }}"
        username: "{{ un }}"
        password: "{{ pwd }}"
        transport: "nxapi"
```


##### Step 3

Execute the playbook.

```yaml
---

  - name: ROLLBACK PLAYBOOK
    hosts: nxos
    connection: local
    gather_facts: no
    
    tasks:
      - nxos_vlan:
          vlan_id=500
          provider={{ nxos_provider }}
          
      - nxos_vlan:
          vlan_id=5000
          provider={{ nxos_provider }}
```



You can see that using `provider` is optional and if you don't you need to use specify all params for every task.

Execute the playbook:

```
ansible-playbook -i inventory rollback.yml
```

Your playbook should have failed because VLAN 5000 is in invalid VLAN ID.

While it is clear this configuration would fail, there are always going to circumstances when things do fail unexpectedly and with networking, there is the possibility of partial configurations.  

To help mitigate this, we will use ntc_rollback along with Ansible blocks.

##### Step 4

Ensure you have both providers and the `block` to your plabook.

```yaml
---

  - name: ROLLBACK PLAYBOOK
    hosts: nxos
    connection: local
    gather_facts: no

    vars:
      ntc_provider:
        host: "{{ inventory_hostname }}"
        username: "{{ un }}"
        password: "{{ pwd }}"
        platform: "{{ vendor }}_{{os}}_{{ api }}"
      nxos_provider:
        host: "{{ inventory_hostname }}"
        username: "{{ un }}"
        password: "{{ pwd }}"
        transport: nxapi
    
    tasks:
      - block:
          - name: CREATE LAST KNOWN GOOD (CHECKPOINT)
            ntc_rollback:
              provider={{ ntc_provider }}
              checkpoint_file=ntc.conf
          - nxos_vlan:
              vlan_id=500
              provider={{ nxos_provider }}
              transport=nxapi
          - nxos_vlan:
              vlan_id=5000
              provider={{ nxos_provider }}
              transport=nxapi
        rescue:    
          - name: ROLLBACK TO CHECKPOINT FILE UPON ERROR
            ntc_rollback:
              provider={{ ntc_provider }}
              rollback_to=ntc.conf
```

##### Step 5

SSH into a switch and issue the command `show vlan brief` while the playbook runs.  You will notice that VLAN 500 gets added and is then removed because an error is raised and the config is rolled back.

Note: to see the same exact output as below, SSH into each Nexus before running the final playbook and remove VLAN 500 (as it was added in the previous task).


Execute the playbook.

```
ntc@ntc:~$ ansible-playbook -i inventory rollback.yml

PLAY [ROLLBACK PLAYBOOK] *******************************************************

TASK [CREATE LAST KNOWN GOOD (CHECKPOINT)] *************************************
changed: [nxos-spine2]
changed: [nxos-spine1]

TASK [nxos_vlan] ***************************************************************
changed: [nxos-spine2]
changed: [nxos-spine1]

TASK [nxos_vlan] ***************************************************************
fatal: [nxos-spine1]: FAILED! => {"changed": false, "clierror": "Syntax error while parsing 'show vlan id 5000  | xml '\n\n\nCmd exec error.\n", "code": "400", "failed": true, "input": "show vlan id 5000", "msg": "Input CLI command error"}
fatal: [nxos-spine2]: FAILED! => {"changed": false, "clierror": "Syntax error while parsing 'show vlan id 5000  | xml '\n\n\nCmd exec error.\n", "code": "400", "failed": true, "input": "show vlan id 5000", "msg": "Input CLI command error"}

TASK [ROLLBACK TO CHECKPOINT FILE UPON ERROR] **********************************
changed: [nxos-spine2]
changed: [nxos-spine1]

PLAY RECAP *********************************************************************
nxos-spine1                : ok=3    changed=3    unreachable=0    failed=0   
nxos-spine2                : ok=3    changed=3    unreachable=0    failed=0   


```

Note: while this example shows ntc_rollback being used for Nexus and Arista switches, it's supported on IOS, and Junos too - you just need to add the proper tasks in the block of tasks to test.

