## Lab 9.2 - Juniper Junos Modules

In the previous lab, you used the build/push method using templating to push full configurations to the devices.

In the build/push method, the playbook is simple and straightforward, but the Jinja template could end up being fairly complex.  When your templates start to become fragile, it's easy to understand the value in building reusable playbooks that use feature-specific idempotent modules.  This lab will review using Ansible modules for Juniper devices.

### Task 1

##### Step 1

Create a new playbook called `juniper.yml` in the `ansible` directory.  

This playbook will be used to explore a few Juniper Ansible modules to automate Junos devices.


##### Step 2

Open `juniper.yml` in your text editor.

Create a play that will automate only one host - *vmx7*.


In the first task, use the **junos_facts** module to retrieve hardware, configuration and interfaces data from JUNOS devices.


``` yaml
---

  - name: TEST JUNIPER MODULES
    hosts: vmx7
    connection: local
    gather_facts: no
    
    vars:
      provider:
        username: "{{ un }}"
        password: "{{ pwd }}"
        host: "{{ inventory_hostname }}"

    tasks:
      - name: GET ALL DATA
        junos_facts:
          provider: "{{ provider }}"

```
##### Step 3

Run the playbook using the `-v` option to see the data being collected by the task. Keep in mind that we have not registered the output to any new variable

```

ntc@ntc:ansible$ ansible-playbook -i inventory juniper.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [TEST JUNIPER MODULES] *****************************************************************************************************************

TASK [GET ALL DATA] *************************************************************************************************************************
ok: [vmx7] => {"ansible_facts": {"ansible_net_filesystems": ["/dev/ad0s1a", "devfs", "/dev/md0", "/dev/md1", "/dev/md2", "/dev/md3", "/dev/md4", "/dev/md5", "/dev/md6", "/dev/md7", "/dev/md8", "/dev/md9", "/dev/md10", "/dev/md11", "/dev/md12", "/dev/md13", "/dev/md14", "/dev/md15", "/dev/md16", "/dev/md17", "/dev/md18", "/dev/md19", "/dev/md20", "/dev/md21", "/dev/md22", "/dev/md23", "/dev/md24", "/dev/md25", "/dev/md26", "/dev/md27", "/dev/md28", "/dev/md29", "/dev/md30", "/dev/md31", "/dev/md32", "/dev/md33", "/dev/md34", "/dev/md35", "/dev/md36", "/dev/md37", "/dev/md38", "/dev/md39", "/dev/md40", "/dev/md41", "/dev/md42", "/dev/md43", "/dev/md44", "/dev/md45", "procfs", "/dev/ad1s1e", "/dev/ad1s1f", "/var/jails/rest-api"], "ansible_net_gather_subset": ["hardware", "default", "interfaces"], "ansible_net_hostname": "vmx7", "ansible_net_interfaces": {".local.": {"admin-status": "up", "macaddress": "Unspecified", "mtu": "Unlimited", "oper-status": "up", "speed": "Unlimited", "type": "Loopback"}, "cbp0": {"admin-status": "up", "macaddress": "00:05:86:71:fd:11", "mtu": "1514", "oper-status": "up", "speed": "Unspecified", "type": "Ethernet"}, "demux0": {"admin-status": "up", "macaddress": "Unspecified", "mtu": "9192", "oper-status": "up", "speed": "Unspecified", "type": "Software-Pseudo"}, "dsc": {"admin-status": "up", "macaddress": "Unspecified", "mtu": "Unlimited", "oper-status": "up", "speed": "Unspecified", "type": "Software-Pseudo"}, "em1": {"admin-status": "up", "macaddress": "2c:c2:60:5d:a8:78", "mtu": "1514", "oper-status": "up", "speed": "1000mbps", "type": "Ethernet"}, "em2": {"admin-status": "up", "macaddress": "2c:c2:60:0c:f5:a3", "mtu": "1514", "oper-status": "up", "speed": "1000mbps", "type": "Ethernet"}, "esi": {"admin-status": "up", "macaddress": "Unspecified", "mtu": "Unlimited", "oper-status": "up", "speed": "Unlimited", "type": "Software-Pseudo"}, "fxp0": {"admin-status": "up", "macaddress": "2c:c2:60:28:fd:a0", "mtu": "1514", "oper-status": "up", "speed": "1000mbps", "type": "Ethernet"}, "ge-0/0/0": {"admin-status": "up", "macaddress": "2c:c2:60:55:1b:3f", "mtu": "1514", "oper-status": "up", "speed": "1000mbps", "type": null}, "ge-0/0/1": {"admin-status": "up", "macaddress": "2c:c2:60:0a:15:95", "mtu": "1514", "oper-status": "up", "speed": "1000mbps", "type": null}, "ge-0/0/2": {"admin-status": "up", "macaddress": "2c:c2:60:58:83:14", "mtu": "1514", "oper-status": "up", "speed": "1000mbps", "type": null}, "ge-0/0/3": {"admin-status": "up", "macaddress": "2c:c2:60:62:2b:08", "mtu": "1514", "oper-status": "up", "speed": "1000mbps", "type": null}, "ge-0/0/4": {"admin-status": "up", "macaddress": "2c:c2:60:5e:4f:af", "mtu": "1514", "oper-status": "up", "speed": "1000mbps", "type": null}, "ge-0/0/5": {"admin-status": "up", "macaddress": "2c:c2:60:29:dc:cd", "mtu": "1514", "oper-status": "up", "speed": "1000mbps", "type": null}, "ge-0/0/6": {"admin-status": "up", "macaddress": "00:05:86:71:fd:06", "mtu": "1514", "oper-status": "down", "speed": "1000mbps", "type": null}, "ge-0/0/7": {"admin-status": "up", "macaddress": "00:05:86:71:fd:07", "mtu": "1514", "oper-status": "down", "speed": "1000mbps", "type": null}, "ge-0/0/8": {"admin-status": "up", "macaddress": "00:05:86:71:fd:08", "mtu": "1514", "oper-status": "down", "speed": "1000mbps", "type": null}, "ge-0/0/9": {"admin-status": "up", "macaddress": "00:05:86:71:fd:09", "mtu": "1514", "oper-status": "down", "speed": "1000mbps", "type": null}, "gre": {"admin-status": "up", "macaddress": null, "mtu": "Unlimited", "oper-status": "up", "speed": "Unlimited", "type": "GRE"}, "ipip": {"admin-status": "up", "macaddress": null, "mtu": "Unlimited", "oper-status": "up", "speed": "Unlimited", "type": "IPIP"}, "irb": {"admin-status": "up", "macaddress": "00:05:86:72:04:f0", "mtu": "1514", "oper-status": "up", "speed": "Unspecified", "type": "Ethernet"}, "jsrv": {"admin-status": "up", "macaddress": "38:08:00:00:00:00", "mtu": "1514", "oper-status": "up", "speed": "Unspecified", "type": "Ethernet"}, "lc-0/0/0": {"admin-status": "up", "macaddress": "Unspecified", "mtu": "0", "oper-status": "up", "speed": "800mbps", "type": "Unspecified"}, "lo0": {"admin-status": "up", "macaddress": "Unspecified", "mtu": "Unlimited", "oper-status": "up", "speed": "Unspecified", "type": "Loopback"}, "lsi": {"admin-status": "up", "macaddress": "Unspecified", "mtu": "Unlimited", "oper-status": "up", "speed": "Unlimited", "type": "Software-Pseudo"}, "mtun": {"admin-status": "up", "macaddress": null, "mtu": "Unlimited", "oper-status": "up", "speed": "Unlimited", "type": "Multicast-GRE"}, "pfe-0/0/0": {"admin-status": "up", "macaddress": "Unspecified", "mtu": "0", "oper-status": "up", "speed": "800mbps", "type": "Unspecified"}, "pfh-0/0/0": {"admin-status": "up", "macaddress": "Unspecified", "mtu": "0", "oper-status": "up", "speed": "800mbps", "type": "Unspecified"}, "pimd": {"admin-status": "up", "macaddress": null, "mtu": "Unlimited", "oper-status": "up", "speed": "Unlimited", "type": "PIMD"}, "pime": {"admin-status": "up", "macaddress": null, "mtu": "Unlimited", "oper-status": "up", "speed": "Unlimited", "type": "PIME"}, "pip0": {"admin-status": "up", "macaddress": "00:05:86:71:04:b0", "mtu": "1514", "oper-status": "up", "speed": "Unspecified", "type": "Ethernet"}, "pp0": {"admin-status": "up", "macaddress": "Unspecified", "mtu": "1532", "oper-status": "up", "speed": "Unspecified", "type": "PPPoE"}, "tap": {"admin-status": "up", "macaddress": "Unspecified", "mtu": "Unlimited", "oper-status": "up", "speed": "Unlimited", "type": "Software-Pseudo"}, "vtep": {"admin-status": "up", "macaddress": "Unspecified", "mtu": "Unlimited", "oper-status": "up", "speed": "Unlimited", "type": "Software-Pseudo"}}, "ansible_net_memfree_mb": 3085568, "ansible_net_memtotal_mb": 4170896, "ansible_net_model": "vmx", "ansible_net_serialnum": "VMXac", "ansible_net_version": "15.1F4.15"}, "changed": false, "failed": false}

PLAY RECAP **********************************************************************************************************************************
vmx7                       : ok=1    changed=0    unreachable=0    failed=0   

ntc@ntc:ansible$ 


```

> The above data includes information about the filesystems, network, hostname, interfaces, serial number, OS version, memeory etc.


##### Step 4

Retry the above using the parameter, `gather_subset: all`.

```
ntc@ntc:ansible$ ansible-playbook -i inventory juniper.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [TEST JUNIPER MODULES] *****************************************************************************************************************

TASK [GET ALL DATA] *************************************************************************************************************************
ok: [vmx7] => {"ansible_facts": {"HOME": "/var/home/ntc", "RE0": {"last_reboot_reason": "0x200:normal shutdown", "mastership_state": "master", "model": "RE-VMX", "status": "OK", "up_time": "30 minutes, 14 seconds"}, "RE1": null, "RE_hw_mi": false, "ansible_net_config": "## Last changed: 2017-11-13 16:57:05 UTC\nversion 15.1F4.15;\ngroups {\n    global {\n        system {\n            login {\n                user ntc {\n                    uid 2000;\n                    class super-user;\n                    authentication {\n                        encrypted-password \"$5$9dE0bRr9$.VvWkJKa3J7HW95.G3KxW9x01nUoVi0PnXuZBlpOUH9\";\n                    }\n                }\n            }\n        }\n    }\n}\napply-groups global;\nsystem {\n    host-name vmx7;\n    domain-name ntc.com;\n    root-authentication {\n        encrypted-password \"$5$1FR588oW$dWnmaj9S4t/GHEYL/gn8tOz3.yXoIMYHrCDyn.4hIo0\";\n    }\n    login {\n        class super-user-local {\n            idle-timeout 3600;\n            permissions all;\n        }\n        user ntc {\n            class super-user-local;\n        }\n    }\n    services {\n        ssh;\n        netconf {\n            ssh;\n        }\n    }\n    syslog {\n        user * {\n            any emergency;\n        }\n        file messages {\n            any notice;\n            authorization info;\n        }\n        file interactive-commands {\n            interactive-commands any;\n        }\n    }\n}\ninterfaces {\n    ge-0/0/0 {\n        unit 0 {\n            family inet {\n                address 10.1.254.2/30;\n            }\n        }\n    }\n    ge-0/0/1 {\n        unit 0 {\n            family inet {\n                address 10.1.254.6/30;\n            }\n        }\n    }\n    ge-0/0/2 {\n        unit 0 {\n            family inet;\n        }\n    }\n    ge-0/0/3 {\n        unit 0 {\n            family inet;\n        }\n    }\n    fxp0 {\n        unit 0 {\n            family inet {\n                address 10.0.0.37/24;\n            }\n        }\n    }\n}\nsnmp {\n    location MILAN;\n    contact netops_team;\n    community ntc_course {\n        authorization read-only;\n    }\n    community ntc_private {\n        authorization read-write;\n    }\n}\nrouting-options {\n    static {\n        route 0.0.0.0/0 next-hop 10.0.0.2;\n    }\n}\nprotocols {\n    lldp {\n        port-id-subtype interface-name;\n        interface all;\n    }\n}", "ansible_net_filesystems": ["/dev/ad0s1a", "devfs", "/dev/md0", "/dev/md1", "/dev/md2", "/dev/md3", "/dev/md4", "/dev/md5", "/dev/md6", "/dev/md7", "/dev/md8", "/dev/md9", "/dev/md10", "/dev/md11", "/dev/md12", "/dev/md13", "/dev/md14", "/dev/md15", "/dev/md16", "/dev/md17", "/dev/md18", "/dev/md19", "/dev/md20", "/dev/md21", "/dev/md22", "/dev/md23", "/dev/md24", "/dev/md25", "/dev/md26", "/dev/md27", "/dev/md28", "/dev/md29", "/dev/md30", "/dev/md31", "/dev/md32", "/dev/md33", "/dev/md34", "/dev/md35", "/dev/md36", "/dev/md37", "/dev/md38", "/dev/md39", "/dev/md40", "/dev/md41", "/dev/md42", "/dev/md43", "/dev/md44", "/dev/md45", "procfs", "/dev/ad1s1e", "/dev/ad1s1f", "/var/jails/rest-api"], "ansible_net_gather_subset": ["hardware", "default", "interfaces", "config"], "ansible_net_hostname": "vmx7", "ansible_net_interfaces": {".local.": {"admin-status": "up", "macaddress": "Unspecified", "mtu": "Unlimited", "oper-status": "up", "speed": "Unlimited", "type": "Loopback"}, "cbp0": {"admin-status": "up", "macaddress": "00:05:86:71:fd:11", "mtu": "1514", "oper-status": "up", "speed": "Unspecified", "type": "Ethernet"}, "demux0": {"admin-status": "up", "macaddress": "Unspecified", "mtu": "9192", "oper-status": "up", "speed": "Unspecified", "type": "Software-Pseudo"}, "dsc": {"admin-status": "up", "macaddress": "Unspecified", "mtu": "Unlimited", "oper-status": "up", "speed": "Unspecified", "type": "Software-Pseudo"}, "em1": {"admin-status": "up", "macaddress": "2c:c2:60:5d:a8:78", "mtu": "1514", "oper-status": "up", "speed": "1000mbps", "type": "Ethernet"}, "em2": {"admin-status": "up", "macaddress": "2c:c2:60:0c:f5:a3", "mtu": "1514", "oper-status": "up", "speed": "1000mbps", "type": "Ethernet"}, "esi": {"admin-status": "up", "macaddress": "Unspecified", "mtu": "Unlimited", "oper-status": "up", "speed": "Unlimited", "type": "Software-Pseudo"}, "fxp0": {"admin-status": "up", "macaddress": "2c:c2:60:28:fd:a0", "mtu": "1514", "oper-status": "up", "speed": "1000mbps", "type": "Ethernet"}, "ge-0/0/0": {"admin-status": "up", "macaddress": "2c:c2:60:55:1b:3f", "mtu": "1514", "oper-status": "up", "speed": "1000mbps", "type": null}, "ge-0/0/1": {"admin-status": "up", "macaddress": "2c:c2:60:0a:15:95", "mtu": "1514", "oper-status": "up", "speed": "1000mbps", "type": null}, "ge-0/0/2": {"admin-status": "up", "macaddress": "2c:c2:60:58:83:14", "mtu": "1514", "oper-status": "up", "speed": "1000mbps", "type": null}, "ge-0/0/3": {"admin-status": "up", "macaddress": "2c:c2:60:62:2b:08", "mtu": "1514", "oper-status": "up", "speed": "1000mbps", "type": null}, "ge-0/0/4": {"admin-status": "up", "macaddress": "2c:c2:60:5e:4f:af", "mtu": "1514", "oper-status": "up", "speed": "1000mbps", "type": null}, "ge-0/0/5": {"admin-status": "up", "macaddress": "2c:c2:60:29:dc:cd", "mtu": "1514", "oper-status": "up", "speed": "1000mbps", "type": null}, "ge-0/0/6": {"admin-status": "up", "macaddress": "00:05:86:71:fd:06", "mtu": "1514", "oper-status": "down", "speed": "1000mbps", "type": null}, "ge-0/0/7": {"admin-status": "up", "macaddress": "00:05:86:71:fd:07", "mtu": "1514", "oper-status": "down", "speed": "1000mbps", "type": null}, "ge-0/0/8": {"admin-status": "up", "macaddress": "00:05:86:71:fd:08", "mtu": "1514", "oper-status": "down", "speed": "1000mbps", "type": null}, "ge-0/0/9": {"admin-status": "up", "macaddress": "00:05:86:71:fd:09", "mtu": "1514", "oper-status": "down", "speed": "1000mbps", "type": null}, "gre": {"admin-status": "up", "macaddress": null, "mtu": "Unlimited", "oper-status": "up", "speed": "Unlimited", "type": "GRE"}, "ipip": {"admin-status": "up", "macaddress": null, "mtu": "Unlimited", "oper-status": "up", "speed": "Unlimited", "type": "IPIP"}, "irb": {"admin-status": "up", "macaddress": "00:05:86:72:04:f0", "mtu": "1514", "oper-status": "up", "speed": "Unspecified", "type": "Ethernet"}, "jsrv": {"admin-status": "up", "macaddress": "38:08:00:00:00:00", "mtu": "1514", "oper-status": "up", "speed": "Unspecified", "type": "Ethernet"}, "lc-0/0/0": {"admin-status": "up", "macaddress": "Unspecified", "mtu": "0", "oper-status": "up", "speed": "800mbps", "type": "Unspecified"}, "lo0": {"admin-status": "up", "macaddress": "Unspecified", "mtu": "Unlimited", "oper-status": "up", "speed": "Unspecified", "type": "Loopback"}, "lsi": {"admin-status": "up", "macaddress": "Unspecified", "mtu": "Unlimited", "oper-status": "up", "speed": "Unlimited", "type": "Software-Pseudo"}, "mtun": {"admin-status": "up", "macaddress": null, "mtu": "Unlimited", "oper-status": "up", "speed": "Unlimited", "type": "Multicast-GRE"}, "pfe-0/0/0": {"admin-status": "up", "macaddress": "Unspecified", "mtu": "0", "oper-status": "up", "speed": "800mbps", "type": "Unspecified"}, "pfh-0/0/0": {"admin-status": "up", "macaddress": "Unspecified", "mtu": "0", "oper-status": "up", "speed": "800mbps", "type": "Unspecified"}, "pimd": {"admin-status": "up", "macaddress": null, "mtu": "Unlimited", "oper-status": "up", "speed": "Unlimited", "type": "PIMD"}, "pime": {"admin-status": "up", "macaddress": null, "mtu": "Unlimited", "oper-status": "up", "speed": "Unlimited", "type": "PIME"}, "pip0": {"admin-status": "up", "macaddress": "00:05:86:71:04:b0", "mtu": "1514", "oper-status": "up", "speed": "Unspecified", "type": "Ethernet"}, "pp0": {"admin-status": "up", "macaddress": "Unspecified", "mtu": "1532", "oper-status": "up", "speed": "Unspecified", "type": "PPPoE"}, "tap": {"admin-status": "up", "macaddress": "Unspecified", "mtu": "Unlimited", "oper-status": "up", "speed": "Unlimited", "type": "Software-Pseudo"}, "vtep": {"admin-status": "up", "macaddress": "Unspecified", "mtu": "Unlimited", "oper-status": "up", "speed": "Unlimited", "type": "Software-Pseudo"}}, "ansible_net_memfree_mb": 3082432, "ansible_net_memtotal_mb": 4170896, "ansible_net_model": "vmx", "ansible_net_serialnum": "VMXac", "ansible_net_version": "15.1F4.15", "current_re": ["re0", "master", "node", "fwdd", "member", "pfem"], "domain": "ntc.com", "fqdn": "vmx7.ntc.com", "has_2RE": false, "hostname": "vmx7", "hostname_info": {"re0": "vmx7"}, "ifd_style": "CLASSIC", "junos_info": {"re0": {"object": {"build": 15, "major": [15, 1], "minor": "4", "type": "F"}, "text": "15.1F4.15"}}, "master": "RE0", "model": "VMX", "model_info": {"re0": "VMX"}, "personality": "MX", "re_info": {"default": {"0": {"last_reboot_reason": "0x200:normal shutdown", "mastership_state": "master", "model": "RE-VMX", "status": "OK"}, "default": {"last_reboot_reason": "0x200:normal shutdown", "mastership_state": "master", "model": "RE-VMX", "status": "OK"}}}, "re_master": {"default": "0"}, "serialnumber": "VMXac", "srx_cluster": null, "srx_cluster_id": null, "srx_cluster_redundancy_group": null, "switch_style": "BRIDGE_DOMAIN", "vc_capable": false, "vc_fabric": null, "vc_master": null, "vc_mode": null, "version": "15.1F4.15", "version_RE0": "15.1F4.15", "version_RE1": null, "version_info": {"build": 15, "major": [15, 1], "minor": "4", "type": "F"}, "virtual": true}, "changed": false, "failed": false}

PLAY RECAP **********************************************************************************************************************************
vmx7                       : ok=1    changed=0    unreachable=0    failed=0   


```

> This output now also contains the configuration of the device. By default, the configuration is omitted from the `facts` modules to improve readability.

##### Step 5

Now, lets collect just the configuration output from the device. Replace `all` with `config` and optionally specify the output format of the configuration. We can also save this to the `configs` directory 

``` yaml
---

  - name: TEST JUNIPER MODULES
    hosts: vmx7
    connection: local
    gather_facts: no
    
    vars:
      provider:
        username: "{{ un }}"
        password: "{{ pwd }}"
        host: "{{ inventory_hostname }}"

    tasks:
      - name: GET ALL DATA
        junos_facts:
          provider: "{{ provider }}"
          gather_subset: config
          config_format: set


      - name: SAVE THE CONFIGS LOCALLY
        copy: 
          content: "{{ ansible_net_config }}"
          dest: "./configs/{{ inventory_hostname }}_junosfacts.cfg"

 
```

##### Step 6

This time, run the playbook without using the `-v` option.


```
ntc@ntc:ansible$ ansible-playbook -i inventory juniper.yml 

PLAY [TEST JUNIPER MODULES] *****************************************************************************************************************

TASK [GET ALL DATA] *************************************************************************************************************************
ok: [vmx7]

TASK [SAVE THE CONFIGS LOCALLY] *************************************************************************************************************
changed: [vmx7]

PLAY RECAP **********************************************************************************************************************************
vmx7                       : ok=2    changed=1    unreachable=0    failed=0   

ntc@ntc:ansible$ 

```


##### Step 7 

Validate that the saved file contains the configuration of the device.


```
#configs/vmx7_junosfacts.cfg 

set version 15.1F4.15
set groups global system login user ntc uid 2000
set groups global system login user ntc class super-user
set groups global system login user ntc authentication encrypted-password "$5$9dE0bRr9$.VvWkJKa3J7HW95.G3KxW9x01nUoVi0PnXuZBlpOUH9"
set apply-groups global
set system host-name vmx7
set system domain-name ntc.com
set system root-authentication encrypted-password "$5$1FR588oW$dWnmaj9S4t/GHEYL/gn8tOz3.yXoIMYHrCDyn.4hIo0"
set system login class super-user-local idle-timeout 3600
set system login class super-user-local permissions all
set system login user ntc class super-user-local
set system services ssh
set system services netconf ssh
set system syslog user * any emergency
set system syslog file messages any notice
set system syslog file messages authorization info
set system syslog file interactive-commands interactive-commands any
set interfaces ge-0/0/0 unit 0 family inet address 10.1.254.2/30
set interfaces ge-0/0/1 unit 0 family inet address 10.1.254.6/30
set interfaces ge-0/0/2 unit 0 family inet
set interfaces ge-0/0/3 unit 0 family inet
set interfaces fxp0 unit 0 family inet address 10.0.0.37/24
set snmp location MILAN
set snmp contact netops_team
set snmp community ntc_course authorization read-only
set snmp community ntc_private authorization read-write
set routing-options static route 0.0.0.0/0 next-hop 10.0.0.2
set protocols lldp port-id-subtype interface-name
set protocols lldp interface all
```


### Task 2

##### Step 1

In this task, you will use the **juniper_config** to push configuration to the Juniper devices.

Create a new template and save it as `templates/routing.j2`.  

This template will be used to generate a new configuration that will be merged on onto *vmx7* and *vmx8*. 

```
interfaces {
    ge-0/0/3 {
        description CONNECTS_TO_PUBLIC_TRANSIT;
        unit 0 {
            family inet {
                address {{ transit_ip }}/24;
            }
        }
    }
}
routing-options {
    static {
        route 10.100.100.0/24 next-hop 172.16.32.1;
    }
    router-id 1.1.1.1;
}

```

##### Step 2

Add a new variable called `transit_ip` to the host_vars files for vmx7 and vmx8.

`host_vars/vmx7.yml`:

```yaml
transit_ip: 172.16.32.11
```

`host_vars/vmx8.yml`:

```yaml
transit_ip: 172.16.32.12
```

##### Step 3

Add a NEW  play to the playbook.  Notice how we are only automating *vmx7* and *vmx8* in this play

> The colon is used to select one _OR_ more hosts or groups.

```yaml

  - name: PUSHING CONFIGS
    hosts: vmx7,vmx8
    connection: local
    gather_facts: no
    tags: push

    vars:
      provider:
        username: "{{ un }}"
        password: "{{ pwd }}"
        host: "{{ inventory_hostname }}"

    tasks:

      - template: 
          src: templates/routing.j2
          dest: "configs/{{ inventory_hostname }}_routing.conf"


      - name: ENABLE ROUTING
        junos_config:
          provider: "{{ provider }}"
          src: "configs/{{ inventory_hostname }}_routing.conf"
          confirm_commit: yes

```

##### Step 4

Save and run the playbook using the "push" tag so that only the new play gets executed.

```
ntc@ntc:~/ansible$ ansible-playbook -i inventory juniper.yml --tags=push
```


```
ntc@ntc:~/ansible$ ansible-playbook -i inventory juniper.yml --tags=push

PLAY [PUSHING CONFIGS] ********************************************************

TASK: [UPDATE ROUTING CONFIG FILE] ********************************************
changed: [vmx7]
changed: [vmx8]

TASK: [ENABLE ROUTING] ********************************************************
changed: [vmx8]
changed: [vmx7]

PLAY RECAP ********************************************************************
vmx7                       : ok=2    changed=2    unreachable=0    failed=0   
vmx8                       : ok=2    changed=2    unreachable=0    failed=0   


```

SSH to the devices if you want to check out their configs.



### Task 3

In this task, you will use the **junos_ccommand** module to execute commands on Junos devices.

##### Step 1

Add a new play to your playbook with two tasks executing two CLI commands, namely `show version` and `show route`.  

Save the `show version` as XML, but save the save the `show route` output as text.

The new play should automate all vmx hosts.

Tag the play with the tag *cli*


```yaml

  - name: CLI on JUNOS
    hosts: vmx
    connection: local
    gather_facts: no
    tags: cli

    tasks:

      - name: EXECUTE SHOW VERSION
        junos_command:
          commands:
            - show version
          provider: "{{ provider }}"
          display: xml
        register: show_version
        
      - name: EXECUTE SHOW ROUTE
        junos_command:
          commands: 
            - show route
          display: text
          provider: "{{ provider }}"
        register: show_route
        
      - name: SAVE XML OUTPUT
        copy:
          content: "{{ show_version.stdout[0] }}"
          dest: "./configs/{{ inventory_hostname }}_version.xml"
      
      - name: SAVE TEXT OUTPUT
        copy:
          content: "{{ show_route.stdout[0] }}"
          dest: "./configs/{{ inventory_hostname }}_routes.txt"
        
        
```

Save the playbook.

##### Step 2

Run the playbook using the "cli" tag.

```
ntc@ntc:~/ansible$ ansible-playbook -i inventory juniper.yml --tags=cli
```

Output:

```
PLAY [CLI on JUNOS] ***********************************************************

TASK: [EXECUTE SHOW VERSION] **************************************************
ok: [vmx8]
ok: [vmx7]
ok: [vmx9]

TASK: [EXECUTE SHOW ROUTE] ****************************************************
ok: [vmx7]
ok: [vmx8]
ok: [vmx9]

PLAY RECAP ********************************************************************
vmx7                       : ok=2    changed=0    unreachable=0    failed=0   
vmx8                       : ok=2    changed=0    unreachable=0    failed=0   
vmx9                       : ok=2    changed=0    unreachable=0    failed=0   
```


##### Step 3

Open up the outputs that were collected and view them.

Here is one of them:

```
ntc@ntc:~/ansible$ more configs/vmx7_routes.txt

inet.0: 10 destinations, 11 routes (10 active, 0 holddown, 0 hidden)
+ = Active Route, - = Last Active, * = Both

0.0.0.0/0          *[Static/5] 05:00:58
                    > to 10.0.0.2 via fxp0.0
1.1.1.1/32         *[Direct/0] 05:00:58
                    > via lo0.0
10.0.0.0/24        *[Direct/0] 05:00:58
                    > via fxp0.0
10.0.0.70/32       *[Local/0] 05:00:58
                      Local via fxp0.0
10.254.12.0/24     *[Direct/0] 04:12:34
                    > via ge-0/0/2.0
10.254.12.1/32     *[Local/0] 04:12:37
                      Local via ge-0/0/2.0
10.254.13.0/24     *[Direct/0] 04:12:34
                    > via ge-0/0/0.0
10.254.13.1/32     *[Local/0] 04:12:37
                      Local via ge-0/0/0.0
172.16.32.11/32    *[Direct/0] 00:08:56
                    > via ge-0/0/3.0
                    [Local/0] 00:08:56
                      Local via ge-0/0/3.0
224.0.0.5/32       *[OSPF/10] 05:01:03, metric 1
                      MultiRecv
```


### Task 4

##### Step 1

This tasks shows how you can use a declarative approach to manage VRFs on Juniper devices, using the **junos_vrf** module.

Create another new play in your playbook and use the tag called "vrfs".  


```yaml

  - name: CONFIGURE VLANS
    connection: local
    gather_facts: no
    hosts: vmx
    tags: vrfs

    vars:
      provider:
        username: "{{ un }}"
        password: "{{ pwd }}"
        host: "{{ inventory_hostname }}"

    tasks:
    
      - name: ENSURE THAT TENANT-A VRF EXISTS
        junos_vrf:
          provider: "{{ provider }}"
          name: tenant-a
          description: VRF for tenant-a
          interfaces:
            - ge-0/0/3
          rd: 1.1.1.1:10
          target: target:65512:10
```


Run this playbook using the *vrfs* tag

```
ntc@ntc:ansible$ ansible-playbook -i inventory juniper.yml --tags=vrfs 

PLAY [TEST JUNIPER MODULES] *****************************************************************************************************************

PLAY [PUSHING CONFIGS] **********************************************************************************************************************

PLAY [CLI on JUNOS] *************************************************************************************************************************

PLAY [CONFIGURE VLANS] **********************************************************************************************************************

TASK [ENSURE THAT TENANT-A VRF EXISTS] ******************************************************************************************************
changed: [vmx7]
changed: [vmx8]
changed: [vmx9]

PLAY RECAP **********************************************************************************************************************************
vmx7                       : ok=1    changed=1    unreachable=0    failed=0   
vmx8                       : ok=1    changed=1    unreachable=0    failed=0   
vmx9                       : ok=1    changed=1    unreachable=0    failed=0   

ntc@ntc:ansible$
```

Log in to the device and ensure that the configuration has been applied.

> Subsequent, repeated run of this task will not recreate the vrf. If the vrf is present, no changes are made, else, the vrf is created, therefore, declarative.

##### Step 2


We can create multiple vrfs simultaneously by supplying a list of "tenants" to the `junos_vrf` module. This can be done using the `aggregate` option of the module.

Add the vrfs for tenants x, y and z in the `host_vars/vmx7.yml` file for `vmx7`

``` yaml

tenants:
  - name: tenant-x
    description: VRF for tenant-x
    interfaces: 
      - ge-0/0/0
    rd: 1.1.1.1:100
    target: target:65512:100
  - name: tenant-y
    description: VRF for tenant-y
    interfaces:
      - ge-0/0/1
    rd: 1.1.1.1:200
    target: target:65512:200
  - name: tenant-z
    description: VRF for tenant-z
    interfaces: 
      - ge-0/0/2
    rd: 1.1.1.1:300
    target: target:65512:300
```
 
##### Step 3

In the previous step we essentially created a data-model for our intended vrfs on the device. Now use the `aggregate` option with the `junos_vrf` and ensure that these vrfs exist on the device.


``` yaml
---
- name: ESTABLISH VRFS ON VMX
  hosts: vmx7
  gather_facts: no
  connection: local

  vars:
    provider:
      host: "{{ inventory_hostname }}"
      username: "{{ un }}"
      password: "{{ pwd }}"

  tasks:

    - name: ENSURE THAT THE VRFS EXIST
      junos_vrf:
        aggregate: "{{ tenants }}"
        purge: yes
        provider: "{{ provider }}"
```

Save the playbook

##### Step 4

Run the playbook as follows:

```
ntc@ntc:ansible$ ansible-playbook -i inventory juniper_vrfs.yml 

PLAY [ESTABLISH VRFS ON VMX] ****************************************************************************************************************

TASK [ENSURE THAT THE VRFS EXIST] ***********************************************************************************************************
changed: [vmx7]

PLAY RECAP **********************************************************************************************************************************
vmx7                       : ok=1    changed=1    unreachable=0    failed=0   

ntc@ntc:ansible$ 


```

##### Step 5

Log into the `vmx7` and ensure that the vrfs for tenants x, y and z have been established.


