## Lab 9.2 - Juniper Junos Modules

In the previous lab, you used the build/push method using templating to push full configurations to the devices.

In the build/push method, the playbook is simple and straightforward, but the Jinja template could end up being fairly complex.  When your templates start to become fragile, it's easy to understand the value in building reusable playbooks that use feature-specific idempotent modules.  This lab will review using Ansible modules for Juniper devices.

### Task 1

##### Step 1

Create a new playbook called `juniper.yml` in the `ansible` directory.  

This playbook will be used to explore a few Juniper Ansible modules to automate Junos devices.


##### Step 2

Open `juniper.yml` in your text editor.

Create a play that will automate only one host - *vmx1*.

In the first task, use the **junos_get_config** module to retrieve configuration stanzas or a full configuration from Junos devices.

Use the module to get the interfaces configuration.

Save the retrieved config in the `configs` directory.

```yaml
---

  - name: TEST JUNIPER MODULES
    hosts: vmx1
    connection: local
    gather_facts: no


    tasks:
      - name: GET CONFIG
        junos_get_config: user={{ un }} passwd={{ pwd }} host={{ inventory_hostname }} filter="interfaces" dest=configs/{{ inventory_hostname }}_get_test.conf

```

Save and run the playbook.

```
ntc@ntc:~/ansible$ ansible-playbook -i inventory juniper.yml

PLAY [TEST JUNIPER MODULES] ***************************************************

TASK: [GET CONFIG] ************************************************************
ok: [vmx1]

PLAY RECAP ********************************************************************
vmx1                       : ok=1    changed=0    unreachable=0    failed=0   

```


You can now view the new file.

```
ntc@ntc:~/ansible$ cat configs/vmx1_get_test.conf

## Last changed: 2016-02-25 11:36:57 UTC
interfaces {
    ge-0/0/0 {
        description CONNECTS_VMX3;
        unit 0 {
            family inet {
                address 10.254.13.1/24;
            }
        }
    }
    ge-0/0/1 {
        description UNUSED;
        disable;
        unit 0 {
            family inet;
        }
    }
    ge-0/0/2 {
        description CONNECTS_VMX2;
        unit 0 {
            family inet {
                address 10.254.12.1/24;
            }
        }
    }
    fxp0 {
        description MANAGEMENT;
        unit 0 {
            family inet {
                address 10.0.0.31/24;
            }
        }
    }
    lo0 {
        description OSPF_ROUTER_ID;
        unit 0 {
            family inet {
                address 1.1.1.1/32;
            }
        }
    }
}
```


##### Step 3

Update the filter so that you now retrieve the protocols configuration as well as the interfaces configuration.

To do this, you separate each configuration section with a `/` in the filter value as shown below.

```yaml
    tasks:
      - name: GET CONFIG
        junos_get_config: user={{ un }} passwd={{ pwd }} host={{ inventory_hostname }} filter="interfaces/protocols" dest=configs/{{ inventory_hostname }}_get_test.conf
```

**Save and re-run the playbook.**

Open and check the file to ensure it is as expected.

```
ntc@ntc:~/ansible$ cat configs/vmx1_get_test.conf

## Last changed: 2016-02-25 11:36:57 UTC
interfaces {
    ge-0/0/0 {
        description CONNECTS_VMX3;
        unit 0 {
            family inet {
                address 10.254.13.1/24;
            }
        }
    }
    ge-0/0/1 {
        description UNUSED;
        disable;
        unit 0 {
            family inet;
        }
    }
    ge-0/0/2 {
        description CONNECTS_VMX2;
        unit 0 {
            family inet {
                address 10.254.12.1/24;
            }
        }
    }
    fxp0 {
        description MANAGEMENT;
        unit 0 {
            family inet {
                address 10.0.0.31/24;
            }
        }
    }
    lo0 {
        description OSPF_ROUTER_ID;
        unit 0 {
            family inet {
                address 1.1.1.1/32;
            }
        }
    }
}
## Last changed: 2016-02-25 11:36:57 UTC
protocols {
    ospf {
        area 0.0.0.0 {
            interface ge-0/0/0.0;
            interface ge-0/0/2.0;
            interface lo0.0;
        }
    }
    lldp {
        interface all;
    }
}

```

> Note: the filter parameter is optional.  If you omit it, the full configuration file will be retrieved.

### Task 2

##### Step 1

In this task, you will use the **juniper_install_config** which is very similar to NAPALM, but it is Juniper specific.

Create a new template and save it as `templates/routing.j2`.  

This template will be used to generate a new configuration that will be merged on onto *vmx1* and *vmx2*. 

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

Add a new variable called `transit_ip` to the host_vars files for vmx1 and vmx2.

`host_vars/vmx1.yml`:

```yaml
transit_ip: 172.16.32.11
```

`host_vars/vmx2.yml`:

```yaml
transit_ip: 172.16.32.12
```

##### Step 3

Add a NEW  play to the playbook.  Notice how we are only automating *vmx1* and *vmx2* in this play

> The colon is used to select one _OR_ more hosts or groups.

```yaml

  - name: PUSHING CONFIGS
    hosts: vmx1,vmx2
    connection: local
    gather_facts: no
    tags: push

    tasks:

      - template: src=templates/routing.j2 dest=configs/{{ inventory_hostname }}_routing.conf


      - name: ENABLE ROUTING
        junos_install_config:
          file=configs/{{ inventory_hostname }}_routing.conf
          user={{ un }}
          passwd={{ pwd }}
          host={{ inventory_hostname }}

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
changed: [vmx1]
changed: [vmx2]

TASK: [ENABLE ROUTING] ********************************************************
changed: [vmx2]
changed: [vmx1]

PLAY RECAP ********************************************************************
vmx1                       : ok=2    changed=2    unreachable=0    failed=0   
vmx2                       : ok=2    changed=2    unreachable=0    failed=0   


```

SSH to the devices if you want to check out their configs.



### Task 3

In this task, you will use the **junos_cli** module to execute commands on Junos devices.

##### Step 1

Add a new play to your playbook with two tasks executing two CLI commands, namely `show version` and `show route`.  

Save the `show version` as XML, but save the save the `show route` output as text.

The new play should automate all vmx hosts.

Tag the play with the tag *cli*

Take note of the `dest` parameter where the operational data coming back will be stored.


```yaml

  - name: CLI on JUNOS
    hosts: vmx
    connection: local
    gather_facts: no
    tags: cli

    tasks:

      - name: EXECUTE SHOW VERSION
        junos_cli:
          cli='show version'
          dest=configs/{{ inventory_hostname }}_version.xml
          format=xml
          user={{ un }}
          passwd={{ pwd }}
          host={{ inventory_hostname }}

      - name: EXECUTE SHOW ROUTE
        junos_cli:
          cli='show route'
          dest=configs/{{ inventory_hostname }}_routes.text
          user={{ un }}
          passwd={{ pwd }}
          host={{ inventory_hostname }}

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
ok: [vmx2]
ok: [vmx1]
ok: [vmx3]

TASK: [EXECUTE SHOW ROUTE] ****************************************************
ok: [vmx1]
ok: [vmx2]
ok: [vmx3]

PLAY RECAP ********************************************************************
vmx1                       : ok=2    changed=0    unreachable=0    failed=0   
vmx2                       : ok=2    changed=0    unreachable=0    failed=0   
vmx3                       : ok=2    changed=0    unreachable=0    failed=0   
```


##### Step 3

Open up the outputs that were collected and view them.

```
ntc@ntc:~/ansible$ ls configs/
vmx1        vmx1_routing.conf  vmx2_routes.text    vmx3
vmx1_get_test.conf  vmx1_version.xml  vmx2_routing.text  vmx3_routes.conf
vmx1_routes.text     vmx2         vmx2_version.xml  vmx3_version.xml
```

Here is one of them:

```
ntc@ntc:~/ansible$ more configs/vmx1_routes.text

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

This task shows how you can use Juniper PyEZ Tables/View while using Ansible.

Create another new play in your playbook and use the tag called "tables".  Your goal is collect LLDP neighbors using the built-in LLDPNeighborTable that comes with PyEZ.

> Note: you need to specify the table name AND the filename of the YAML file that contains the table.
> By default, the module looks in the `op` directory in PyEZ

```yaml

  - name: GET OP DATA USING T/V
    connection: local
    gather_facts: no
    hosts: vmx
    tags: tables

    tasks:
      - name: GET NEIGHBOR INFO USING STANDARD LLDP TABLE
        junos_get_table: table=LLDPNeighborTable file=lldp.yml host={{ inventory_hostname }} user={{ un }} passwd={{ pwd }}
```


Run this playbook using the *tables* tag, but this time do it in verbose mode using the *-v* flag.

```
ntc@ntc:~/ansible$ ansible-playbook -i inventory juniper.yml --tags=tables -v

```

```
ntc@ntc:~/ansible$ ansible-playbook -i inventory juniper.yml --tags=tables -v

PLAY [GET OP DATA USING T/V] **************************************************

TASK: [GET NEIGHBOR INFO USING STANDARD LLDP TABLE] ***************************
ok: [vmx2] => {"changed": false, "resource": [{"local_int": "fxp0", "local_parent": "-", "remote_chassis_id": "00:05:86:71:a4:c0", "remote_port_desc": null, "remote_sysname": "vmx1", "remote_type": "Mac address"}, {"local_int": "ge-0/0/2", "local_parent": "-", "remote_chassis_id": "00:05:86:71:a4:c0", "remote_port_desc": null, "remote_sysname": "vmx1", "remote_type": "Mac address"}, {"local_int": "fxp0", "local_parent": "-", "remote_chassis_id": "00:05:86:71:db:c0", "remote_port_desc": null, "remote_sysname": "vmx3", "remote_type": "Mac address"}, {"local_int": "ge-0/0/1", "local_parent": "-", "remote_chassis_id": "00:05:86:71:db:c0", "remote_port_desc": null, "remote_sysname": "vmx3", "remote_type": "Mac address"}, {"local_int": "fxp0", "local_parent": "-", "remote_chassis_id": "28:03:82:9a:13:47", "remote_port_desc": null, "remote_sysname": "eos-spine1.ntc.com", "remote_type": "Mac address"}, {"local_int": "fxp0", "local_parent": "-", "remote_chassis_id": "28:03:82:9a:13:4b", "remote_port_desc": null, "remote_sysname": "eos-spine2.ntc.com", "remote_type": "Mac address"}]}
ok: [vmx3] => {"changed": false, "resource": [{"local_int": "fxp0", "local_parent": "-", "remote_chassis_id": "00:05:86:71:25:c0", "remote_port_desc": null, "remote_sysname": "vmx2", "remote_type": "Mac address"}, {"local_int": "ge-0/0/1", "local_parent": "-", "remote_chassis_id": "00:05:86:71:25:c0", "remote_port_desc": null, "remote_sysname": "vmx2", "remote_type": "Mac address"}, {"local_int": "fxp0", "local_parent": "-", "remote_chassis_id": "00:05:86:71:a4:c0", "remote_port_desc": null, "remote_sysname": "vmx1", "remote_type": "Mac address"}, {"local_int": "ge-0/0/0", "local_parent": "-", "remote_chassis_id": "00:05:86:71:a4:c0", "remote_port_desc": null, "remote_sysname": "vmx1", "remote_type": "Mac address"}, {"local_int": "fxp0", "local_parent": "-", "remote_chassis_id": "28:03:82:9a:13:47", "remote_port_desc": null, "remote_sysname": "eos-spine1.ntc.com", "remote_type": "Mac address"}, {"local_int": "fxp0", "local_parent": "-", "remote_chassis_id": "28:03:82:9a:13:4b", "remote_port_desc": null, "remote_sysname": "eos-spine2.ntc.com", "remote_type": "Mac address"}]}
ok: [vmx1] => {"changed": false, "resource": [{"local_int": "fxp0", "local_parent": "-", "remote_chassis_id": "00:05:86:71:25:c0", "remote_port_desc": null, "remote_sysname": "vmx2", "remote_type": "Mac address"}, {"local_int": "ge-0/0/2", "local_parent": "-", "remote_chassis_id": "00:05:86:71:25:c0", "remote_port_desc": null, "remote_sysname": "vmx2", "remote_type": "Mac address"}, {"local_int": "fxp0", "local_parent": "-", "remote_chassis_id": "00:05:86:71:db:c0", "remote_port_desc": null, "remote_sysname": "vmx3", "remote_type": "Mac address"}, {"local_int": "ge-0/0/0", "local_parent": "-", "remote_chassis_id": "00:05:86:71:db:c0", "remote_port_desc": null, "remote_sysname": "vmx3", "remote_type": "Mac address"}, {"local_int": "fxp0", "local_parent": "-", "remote_chassis_id": "28:03:82:9a:13:47", "remote_port_desc": null, "remote_sysname": "eos-spine1.ntc.com", "remote_type": "Mac address"}, {"local_int": "fxp0", "local_parent": "-", "remote_chassis_id": "28:03:82:9a:13:4b", "remote_port_desc": null, "remote_sysname": "eos-spine2.ntc.com", "remote_type": "Mac address"}]}

PLAY RECAP ********************************************************************
vmx1                       : ok=1    changed=0    unreachable=0    failed=0   
vmx2                       : ok=1    changed=0    unreachable=0    failed=0   
vmx3                       : ok=1    changed=0    unreachable=0    failed=0

```


> Note: You can also use the `path` parameter if you wish to change the search path to use custom Tables and not just the ones located in the `op` directory.

##### Step 2

Register the data coming back from the junos_get_table task and use the debug module to print it.

Save and execute the playbook (do not run it in verbose mode)