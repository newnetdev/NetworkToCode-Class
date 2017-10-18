## Lab 6.3 - Building and Pushing Network Configuration Files

This lab will show how to use Ansible to automate the process of building full network configuration files and pushing them to network devices.  

You will take existing configuration files, de-construct them, and then create Jinja2 templates and YAML based variable files.  The templates and variables will be rendered together using the Ansible *template* module to create configuration files.  They will then be pushed to network devices using an open source module from the NAPALM team.

### Task 1 - Create Templates and Vars Files

In this task, you will automate the creation of 3 configuration files using several Junos configuration templates.

##### Step 1

Within the `ansible` directory, create a directory called `templates`.  

It'll be on the same level as your inventory file.

You can use the `tree` command within the terminal to view the directory structure:

```
ntc@ntc:~/ansible$ tree
.
├── inventory
└── templates

1 directory, 1 file
```

The configuration below is from one of the devices, namely *vmx8*.  The same configuration needs to be applied across all routers - with minor changes such as IP address, interface descriptions, etc.

The task is to create templates and the associated group vars and host vars files to simplify the process of config creation.

```
version 15.1F4.15;
groups {
    global {
        system {
            login {
                user ntc {
                    uid 2000;
                    class super-user;
                    authentication {
                        encrypted-password "$5$9dE0bRr9$.VvWkJKa3J7HW95.G3KxW9x01nUoVi0PnXuZBlpOUH9"; ##
 SECRET-DATA
                    }
                }
            }
        }
    }
}
apply-groups global;
system {
    host-name vmx8;
    domain-name ntc.com;
    root-authentication {
        encrypted-password "$5$1FR588oW$dWnmaj9S4t/GHEYL/gn8tOz3.yXoIMYHrCDyn.4hIo0"; ## SECRET-DATA
    }
    services {
        ssh;
        netconf {
            ssh;
        }
    }
    syslog {
        user * {
            any emergency;
        }
        file messages {
            any notice;
            authorization info;
        }
        file interactive-commands {
            interactive-commands any;
        }
    }
}
interfaces {
    ge-0/0/0 {
        description CONNECTS_vmx7;
        unit 0 {
            family inet {
                address 10.254.13.1/24;
            }
        }
    }
    ge-0/0/1 {
        disable;
        description UNUSED;
        unit 0 {
            family inet;
        }
    }
    ge-0/0/2 {
        description CONNECTS_vmx9;
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
                address 10.0.0.38/24;
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
snmp {
    location NYC_NY_DC1;
    contact NETWORK_ADMIN;
    community networktocode {
        authorization read-only;
    }
    community public {
        authorization read-only;
    }
}
routing-options {
    static {
        route 0.0.0.0/0 next-hop 10.0.0.2;
    }
    router-id 1.1.1.1;
}
protocols {
    ospf {
        area 0.0.0.0 {
            interface ge-0/0/0;
            interface ge-0/0/2;
            interface lo0;
        }
    }
    lldp {
        interface all;
    }
}
```

##### Step 2

Now, we will start to break down the configuration file into a series of Jinja2 template files and variables data files.

We will break this down into sections in order to create the appropriate template files.

First, we'll look at a configuration snippet going top down in the configuration file:

Create a file called `01_static.j2` in the `templates` directory and open it. It will serve as the first template for the device.  

This template only has one variable, which is the hostname of the device.  Everything else is a static or base configuration.

Take note of the line that has `    host-name {{ inventory_hostname }};`.  This will ensure the hostname of the device becomes what it is in the inventory file.  Remember *inventory_hostname* is a special built-in variable in Ansible.

```
version 15.1F4.15;
groups {
    global {
        system {
            login {
                user ntc {
                    uid 2000;
                    class super-user;
                    authentication {
                        encrypted-password "$5$9dE0bRr9$.VvWkJKa3J7HW95.G3KxW9x01nUoVi0PnXuZBlpOUH9";
                    }
                }
            }
        }
    }
}
apply-groups global;
system {
    host-name {{ inventory_hostname }};
    domain-name ntc.com;
    root-authentication {
        encrypted-password "$5$1FR588oW$dWnmaj9S4t/GHEYL/gn8tOz3.yXoIMYHrCDyn.4hIo0";
    }
    services {
        ssh;
        netconf {
            ssh;
        }
    }
    syslog {
        user * {
            any emergency;
        }
        file messages {
            any notice;
            authorization info;
        }
        file interactive-commands {
            interactive-commands any;
        }
    }
}

```


##### Step 3

Create four new template files and ensure they are in the `templates` directory:

* 02_interfaces.j2
* 03_snmp.j2
* 04_routing.j2
* 05_protocols.j2

You will create a template for each configuration stanza that exists on the CLI.

##### Step 4

Open the interfaces template `02_interfaces.j2`.  Ensure you use the following template.

Take your time to review the template.  You will notice all this is, is Juniper CLI commands with variables, loops, and if statements added to it.

```
interfaces {
{% for interface in interfaces %}
    {{ interface.name }} {
{% if interface.get('state') == 'down' %}
        disable;
{% endif %}
        description {{ interface.description }};
        unit 0 {
{% if interface.get('ip') %}
            family inet {
                address {{ interface.ip }}/{{ interface.mask }};
            }
{% else %}
            family inet;
{% endif %}
        }
    }
{% endfor %}
}
```


##### Step 5

Create a `host_vars` directory (if you don't already have one), and create three files in it: `vmx8.yml`, `vmx9.yml`, and `vmx7.yml`.

The names of these files are significant.  They match the names as they are defined in the inventory file.

```
ntc@ntc:~/ansible$ mkdir host_vars

ntc@ntc:~/ansible$ cd host_vars/
```

Open the newly created files and ensure they have the vars as defined below in them.

`host_vars/vmx8.yml`

```yaml
---

interfaces:
  - name: ge-0/0/0
    state: up
    ip: 10.254.13.1
    mask: 24
    description: 'CONNECTS_vmx7'
  - name: ge-0/0/1
    state: down
    description: 'UNUSED'
  - name: ge-0/0/2
    state: up
    ip: 10.254.12.1
    mask: 24
    description: 'CONNECTS_vmx9' 
  - name: fxp0
    state: up
    ip: 10.0.0.38
    mask: 24
    description: 'MANAGEMENT'
  - name: lo0
    state: up
    ip: 1.1.1.1
    mask: 32
    description: 'OSPF_ROUTER_ID' 

```

Notice how we are using a different syntax for the next two host vars file to create lists of dictionaries.  Either option works - it's up to you.

`host_vars/vmx9.yml`

```yaml
---

interfaces:
  - { name: ge-0/0/0, state: down, description: 'UNUSED' }
  - { name: ge-0/0/1, state: up, ip: 10.254.23.2, mask: 24, description: 'CONNECTS_vmx7'}
  - { name: ge-0/0/2, state: up, ip: 10.254.12.2, mask: 24, description: 'CONNECTS_vmx8'}
  - { name: fxp0, state: up, ip: 10.0.0.39, mask: 24, description: 'MANAGEMENT'}
  - { name: lo0, state: up, ip: 2.2.2.2, mask: 32, description: 'OSPF_ROUTER_ID' }

```


`host_vars/vmx7.yml`

```yaml
---

interfaces:
  - { name: ge-0/0/0, state: up, ip: 10.254.13.3, mask: 24, description: 'CONNECTS_vmx8'}
  - { name: ge-0/0/1, state: up, ip: 10.254.23.3, mask: 24, description: 'CONNECTS_vmx9'}
  - { name: ge-0/0/2, state: down, description: 'UNUSED' }
  - { name: fxp0, state: up, ip: 10.0.0.37, mask: 24, description: 'MANAGEMENT'}
  - { name: lo0, state: up, ip: 3.3.3.3, mask: 32, description: 'OSPF_ROUTER_ID' }


```


Now review the interfaces template again to ensure you understand how the data is modeled in the YAML variables files and how it maps back to the interfaces template.


##### Step 6

Open the SNMP template `03_snmp.j2`.  Ensure you use the following template.

Take your time to review the template.  You will notice all this is, is Juniper CLI commands with variables and for loop added to it.

```
snmp {
    location {{ snmp.location }};
    contact {{ snmp.contact }};
{% for community in snmp.communities %}
    community {{ community.string }} {
        authorization {{ community.auth }};
    }
{% endfor %}
}

```


##### Step 7

Now create a new directory called `group_vars` (if you don't already have it created), and in this directory create a file called `vmx.yml`.  

> Note: The name of the directory called `group_vars` is an important name within Ansible.  It will store "group based variables".

> The names of the files in the `group_vars` directory map directly to the groups that are found in the inventory file.  For example, the variables that end up in `group_vars/all.yml` will be available, and in scope, for all devices in the *vmx8* group, i.e. vmx8, vmx9, and vmx7.  For this step, we could use `all.yml` or `vmx.yml`.  

Since the SNMP configuration is the same across all devices in the group, you can use a group based variable file as compared to host based vars file, which you used for the interfaces.

`group_vars/vmx.yml`

```yaml
---

snmp:
  location: NYC_NY_DC1
  contact: NETWORK_ADMIN
  communities:
    - string: networktocode
      auth: read-only
    - string: public
      auth: read-only
```


##### Step 8

Open the routing template `04_routing.j2 `.  Ensure you use the following template.

Take your time to review the template.  You will notice all this is, is Juniper CLI commands with variables and for loop added to it.

```
routing-options {
    static {
        route 0.0.0.0/0 next-hop {{ mgmt_default_route_next_hop }};
    }
    router-id {{ router_id }};
}

```

##### Step 9

As you could tell from the routing template, there is a group variable, i.e. `mgmt_default_route_next_hop`, but also a host-specific variable, i.e. `router_id`.

This means, the group vars needs to be changed in `group_vars/vmx.yml`, and the host vars need to be changed in each respective host var file.

This var needs to be added to `group_vars/vmx.yml`:

```yaml

mgmt_default_route_next_hop: 10.0.0.2

```

These updates are needed for each host_var file:

`host_vars/vmx8.yml`

```yaml

router_id: 1.1.1.1

```

`host_vars/vmx9.yml`

```yaml

router_id: 2.2.2.2

```


`host_vars/vmx7.yml`

```yaml

router_id: 3.3.3.3

```

##### Step 10

Finally, open the protocols template file `05_protocols.j2`.

Use the following template.

```
protocols {
{% if ospf is defined %}
    ospf {
{% for each_area in ospf %}
        area {{ each_area.area }} {
{% for interface in each_area.interfaces %}
            interface {{ interface }};
{% endfor %}
        }
{% endfor %}
    }
{% endif %}
    lldp {
        interface all;
    }
}
```

##### Step 11

If all of the interfaces being enabled for OSPF were the same across devices, you could use the group vars file, but that is not the case for this lab.  

Instead, ensure you add the following variable to each of the host vars files.

`host_vars/vmx8.yml`

```yaml
ospf:
  - area: 0.0.0.0
    interfaces:
      - ge-0/0/0
      - ge-0/0/2
      - lo0

```

`host_vars/vmx9.yml`

```yaml

ospf:
  - area: 0.0.0.0
    interfaces:
      - ge-0/0/1
      - ge-0/0/2
      - lo0

```


`host_vars/vmx7.yml`

```yaml

ospf:
  - area: 0.0.0.0
    interfaces:
      - ge-0/0/1
      - ge-0/0/2
      - lo0

```

##### Step 12

**Status check:**  make sure your vars files look like this (order of variables does not matter):

`group_vars/vmx.yml`:

```yaml
---

mgmt_default_route_next_hop: 10.0.0.2

snmp:
  location: NYC_NY_DC1
  contact: NETWORK_ADMIN
  communities:
    - string: networktocode
      auth: read-only
    - string: public
      auth: read-only

```

`host_vars/vmx8.yml`

```yaml

---

interfaces:
  - name: ge-0/0/0
    state: up
    ip: 10.254.13.1
    mask: 24
    description: 'CONNECTS_vmx7'
  - name: ge-0/0/1
    state: down
    description: 'UNUSED' 
  - name: ge-0/0/2
    state: up
    ip: 10.254.12.1
    mask: 24
    description: 'CONNECTS_vmx9' 
  - name: fxp0
    state: up
    ip: 10.0.0.38
    mask: 24
    description: 'MANAGEMENT'
  - name: lo0
    state: up
    ip: 1.1.1.1
    mask: 32
    description: 'OSPF_ROUTER_ID' 

router_id: 1.1.1.1

ospf:
  - area: 0.0.0.0
    interfaces:
      - ge-0/0/0
      - ge-0/0/2
      - lo0


```

`host_vars/vmx9.yml`

```yaml

---

interfaces:
  - { name: ge-0/0/0, state: down, description: 'UNUSED' }
  - { name: ge-0/0/1, state: up, ip: 10.254.23.2, mask: 24, description: 'CONNECTS_vmx7'}
  - { name: ge-0/0/2, state: up, ip: 10.254.12.2, mask: 24, description: 'CONNECTS_vmx8'}
  - { name: fxp0, state: up, ip: 10.0.0.39, mask: 24, description: 'MANAGEMENT'}
  - { name: lo0, state: up, ip: 2.2.2.2, mask: 32, description: 'OSPF_ROUTER_ID' }

router_id: 2.2.2.2

ospf:
  - area: 0.0.0.0
    interfaces:
      - ge-0/0/1
      - ge-0/0/2
      - lo0


```


`host_vars/vmx7.yml`

```yaml

---

interfaces:
  - { name: ge-0/0/0, state: up, ip: 10.254.13.3, mask: 24, description: 'CONNECTS_vmx8'}
  - { name: ge-0/0/1, state: up, ip: 10.254.23.3, mask: 24, description: 'CONNECTS_vmx9'}
  - { name: ge-0/0/2, state: down, description: 'UNUSED' }
  - { name: fxp0, state: up, ip: 10.0.0.37, mask: 24, description: 'MANAGEMENT'}
  - { name: lo0, state: up, ip: 3.3.3.3, mask: 32, description: 'OSPF_ROUTER_ID' }

router_id: 3.3.3.3

ospf:
  - area: 0.0.0.0
    interfaces:
      - ge-0/0/1
      - ge-0/0/2
      - lo0

```


##### Step 13

Once the new config snippets are generated and created from the templates and vars files, they need to be stored somewhere.  We will store them in a `configs` directory, and give each device their own sub-directory.

We will create these directories dynamically in an Ansible playbook.

Create a new playbook called `juniper-build.yml` and store it in the `ansible` directory.

For now, just include one task that will create the required directories per host.

This play should be limited to the `vmx` group in the inventory file, so use the `hosts: vmx` in the play definition.

```yaml
---

  - name: BUILD PUSH JUNIPER
    connection: local
    gather_facts: no
    hosts: vmx

    tasks:

      - name: ENSURE DIRs created per device
        file: path=/home/ntc/ansible/configs/{{ inventory_hostname }}/partials state=directory
```

Save the playbook.

#####  Step 13

Run the playbook.

```
ntc@ntc:~/ansible$ ansible-playbook -i inventory juniper-build.yml

PLAY [BUILD PUSH JUNIPER] *****************************************************

TASK: [ENSURE DIRs created per device] ****************************************
changed: [vmx8]
changed: [vmx9]
changed: [vmx7]

PLAY RECAP ********************************************************************
vmx8                       : ok=1    changed=1    unreachable=0    failed=0   
vmx9                       : ok=1    changed=1    unreachable=0    failed=0   
vmx7                       : ok=1    changed=1    unreachable=0    failed=0
```

Issue the `tree` command see what happened:

```
ntc@ntc:~/ansible$ tree
.
├── configs
│   ├── vmx8
│   │   └── partials
│   ├── vmx9
│   │   └── partials
│   └── vmx7
│       └── partials
# shortened for brevity

```


You should see that a `configs` directory was created, which has 3 sub-directories, one per device.  And in each sub-directory, there is another directory called `partials`.

We are going to store the *partial* configs in the `partial` directory, assemble the partials into a complete config, and then put the final config file in the root of the vmx* directories.

##### Step 14

Add new tasks to the playbook that will build the partial configs for the top/base config and for interfaces.

```yaml
      - name: BUILD TOP/BASE CONFIG
        template: src=templates/01_static.j2 dest=configs/{{ inventory_hostname }}/partials/01_static.conf

      - name: BUILD INTERFACES CONFIG
        template: src=templates/02_interfaces.j2 dest=configs/{{ inventory_hostname }}/partials/02_interfaces.conf
```

After these tasks are added, re-run the playbook.

```
ntc@ntc:~/ansible$ ansible-playbook -i inventory juniper-build.yml

PLAY [BUILD PUSH JUNIPER] *****************************************************

TASK: [ENSURE DIRs created per device] ****************************************
ok: [vmx9]
ok: [vmx8]
ok: [vmx7]

TASK: [BUILD TOP/BASE CONFIG] *************************************************
changed: [vmx9]
changed: [vmx8]
changed: [vmx7]

TASK: [BUILD INTERFACES CONFIG] ***********************************************
changed: [vmx9]
changed: [vmx7]
changed: [vmx8]

PLAY RECAP ********************************************************************
vmx8                       : ok=3    changed=2    unreachable=0    failed=0   
vmx9                       : ok=3    changed=2    unreachable=0    failed=0   
vmx7                       : ok=3    changed=2    unreachable=0    failed=0   
```

##### Step 15

Examine the files that were created:

```
.
├── configs
│   ├── vmx8
│   │   └── partials
│   │       ├── 01_static.conf
│   │       └── 02_interfaces.conf
│   ├── vmx9
│   │   └── partials
│   │       ├── 01_static.conf
│   │       └── 02_interfaces.conf
│   └── vmx7
│       └── partials
│           ├── 01_static.conf
│           └── 02_interfaces.conf

```

Feel free to open them and view the rendered partial configurations.

##### Step 16

Rather than have one task per template and have to hard-code the templates into the task,  you should use a more scalable option.

You should use a loop in Ansible called **with_fileglob** to loop over all template files in the template directory.  

**IMPORTANT**

**If you did a previous lab for Cisco/Arista devices, you should move those templates into another directory for this exercise.**

Replace the two tasks you added in the previous step with this one:

```
      - name: BUILD CONFIGS
        template: src={{ item }} dest=configs/{{ inventory_hostname }}/partials/{{ item | basename | regex_replace('\.j2','') }}.conf
        with_fileglob:
          - templates/*
```

This will loop over all files that exist in the `templates` directory.

> Note: _basename_ is a Jinja2 filter that returns just the name of the file.  This is required because by default, the full absolute path is returned when using with_fileglob.  We also remove .j2 extension as we build the conf files.

Save the playbook.

##### Step 17

Run the playbook.

```
ntc@ntc:~/ansible$ ansible-playbook -i inventory juniper-build.yml

PLAY [BUILD PUSH JUNIPER] *****************************************************

TASK: [ENSURE DIRs created per device] ****************************************
ok: [vmx8]
ok: [vmx9]
ok: [vmx7]

TASK: [BUILD CONFIGS] *************************************************
changed: [vmx8] => (item=/home/ntc/ansible/templates/03_snmp.j2)
changed: [vmx7] => (item=/home/ntc/ansible/templates/03_snmp.j2)
changed: [vmx9] => (item=/home/ntc/ansible/templates/03_snmp.j2)
changed: [vmx7] => (item=/home/ntc/ansible/templates/04_routing.j2)
changed: [vmx8] => (item=/home/ntc/ansible/templates/04_routing.j2)
changed: [vmx9] => (item=/home/ntc/ansible/templates/04_routing.j2)
changed: [vmx7] => (item=/home/ntc/ansible/templates/05_protocols.j2)
changed: [vmx8] => (item=/home/ntc/ansible/templates/05_protocols.j2)
changed: [vmx9] => (item=/home/ntc/ansible/templates/05_protocols.j2)
ok: [vmx7] => (item=/home/ntc/ansible/templates/02_interfaces.j2)
ok: [vmx8] => (item=/home/ntc/ansible/templates/02_interfaces.j2)
ok: [vmx9] => (item=/home/ntc/ansible/templates/02_interfaces.j2)
ok: [vmx7] => (item=/home/ntc/ansible/templates/01_static.j2)
ok: [vmx9] => (item=/home/ntc/ansible/templates/01_static.j2)
ok: [vmx8] => (item=/home/ntc/ansible/templates/01_static.j2)

PLAY RECAP ********************************************************************
vmx8                       : ok=2    changed=1    unreachable=0    failed=0   
vmx9                       : ok=2    changed=1    unreachable=0    failed=0   
vmx7                       : ok=2    changed=1    unreachable=0    failed=0   
```

Now view the files that were created.

```
ntc@ntc:~/ansible$ tree
.
├── configs
│   ├── vmx8
│   │   └── partials
│   │       ├── 01_static.conf
│   │       ├── 02_interfaces.conf
│   │       ├── 03_snmp.conf
│   │       ├── 04_routing.conf
│   │       └── 05_protocols.conf
│   ├── vmx9
│   │   └── partials
│   │       ├── 01_static.conf
│   │       ├── 02_interfaces.conf
│   │       ├── 03_snmp.conf
│   │       ├── 04_routing.conf
│   │       └── 05_protocols.conf
│   └── vmx7
│       └── partials
│           ├── 01_static.conf
│           ├── 02_interfaces.conf
│           ├── 03_snmp.conf
│           ├── 04_routing.conf
│           └── 05_protocols.conf
```

##### Step 18

There are now 5 partial configurations or snippets per device.  We need to assemble them now to create a full configuration file.

Add one more task to the playbook which will use the **assemble** module.


```yaml
      - name: ASSEMBLE PARTIAL CONFIGS
        assemble: src=configs/{{ inventory_hostname }}/partials dest=configs/{{ inventory_hostname }}/{{ inventory_hostname}
}.conf

```

The updated playbook should look like this:

```yaml
---

  - name: BUILD PUSH JUNIPER
    connection: local
    gather_facts: no
    hosts: vmx

    tasks:

      - name: ENSURE DIRs created per device
        file: path=/home/ntc/ansible//configs/{{ inventory_hostname }}/partials state=directory

      - name: BUILD CONFIGS
        template: src={{ item }} dest=configs/{{ inventory_hostname }}/partials/{{ item | basename }}.conf
        with_fileglob:
          - templates/*

      - name: ASSEMBLE PARTIAL CONFIGS
        assemble: src=configs/{{ inventory_hostname }}/partials dest=configs/{{ inventory_hostname }}/{{ inventory_hostname}}.conf

```


Save the playbook.  

##### Step 19

Run the playbook.

```
ntc@ntc:~/ansible$ ansible-playbook -i inventory juniper-build.yml

PLAY [BUILD PUSH JUNIPER] *****************************************************

TASK: [ENSURE DIRs created per device] ****************************************
ok: [vmx8]
ok: [vmx9]
ok: [vmx7]

TASK: [BUILD CONFIGS] *********************************************************
ok: [vmx9] => (item=/home/ntc/ansible/templates/03_snmp.j2)
ok: [vmx8] => (item=/home/ntc/ansible/templates/03_snmp.j2)
ok: [vmx7] => (item=/home/ntc/ansible/templates/03_snmp.j2)
ok: [vmx9] => (item=/home/ntc/ansible/templates/04_routing.j2)
ok: [vmx7] => (item=/home/ntc/ansible/templates/04_routing.j2)
ok: [vmx8] => (item=/home/ntc/ansible/templates/04_routing.j2)
ok: [vmx9] => (item=/home/ntc/ansible/templates/05_protocols.j2)
ok: [vmx7] => (item=/home/ntc/ansible/templates/05_protocols.j2)
ok: [vmx8] => (item=/home/ntc/ansible/templates/05_protocols.j2)
ok: [vmx9] => (item=/home/ntc/ansible/templates/02_interfaces.j2)
ok: [vmx7] => (item=/home/ntc/ansible/templates/02_interfaces.j2)
ok: [vmx8] => (item=/home/ntc/ansible/templates/02_interfaces.j2)
ok: [vmx9] => (item=/home/ntc/ansible/templates/01_static.j2)
ok: [vmx8] => (item=/home/ntc/ansible/templates/01_static.j2)
ok: [vmx7] => (item=/home/ntc/ansible/templates/01_static.j2)

TASK: [ASSEMBLE PARTIAL CONFIGS] **********************************************
changed: [vmx9]
changed: [vmx7]
changed: [vmx8]

PLAY RECAP ********************************************************************
vmx8                       : ok=3    changed=1    unreachable=0    failed=0   
vmx9                       : ok=3    changed=1    unreachable=0    failed=0   
vmx7                       : ok=3    changed=1    unreachable=0    failed=0   
```


You will see there is a full assembled configuration per device located at `configs/vmx8/vmx8.conf`, `configs/vmx8/vmx9.conf`, `configs/vmx8/vmx7.conf`.

Feel free to review them.

### Task 5 - Pushing the Configurations

Now that the configs are built, they are ready to be pushed.

##### Step 1

Review details on the module that will be used to push the configurations.

This module that'll be used to push the configurations is called **napalm_install_config**.

This module is a multi-vendor module supporting vendors such as Arista, Cisco IOS, Cisco Nexus, Cisco IOS-XR, Juniper, and many more.  It has the ability to automatically apply a configuration and make it the device's active running configuration.  By using this module, we will apply the configurations generated in the previous task.

The following parameters will be used for the napalm_install_config module (as shown below):
  - `hostname`: this is the IP / FQDN of the node you are automating.  We are using the IP from the inventory file
  - `username`: to login to the switch
  - `password`: to login to the switch
  - `dev_os`: platform of the target node
  - `config_file`: that will be sent and applied to the device.  Notice how we are using a variable to push the correct file.
  - `diff_file`: A path to the file where we store the "diff" between the running configuration and the new configuration.
  - `commit_changes`: if true, they will be applied (it's possible not to apply and just generate diffs)
  - `replace_config`: it's possible to do a replace/overwrite or a merge.  When this is true, it means you are replacing the full configuration (this is what you are doing for this lab.)

> Also take notice of the `tags` helper module below in the last line of the playbook.  This will allow us to run just this task from the terminal.

##### Step 2

First create a directory called `diffs` in your working directory using the `mkdir diffs` command.  This will store the diffs generated by the devices so we can see what changes are getting applied.

Then add the following task to the `juniper-build.yml` playbook:


```yaml
---

  - name: BUILD PUSH JUNIPER
    connection: local
    gather_facts: no
    hosts: vmx

    tasks:

      - name: ENSURE DIRs created per device
        file: path=/home/ntc/ansible//configs/{{ inventory_hostname }}/partials state=directory

      - name: BUILD CONFIGS
        template: src={{ item }} dest=configs/{{ inventory_hostname }}/partials/{{ item | basename }}.conf
        with_fileglob:
          - templates/*

      - name: ASSEMBLE PARTIAL CONFIGS
        assemble: src=configs/{{ inventory_hostname }}/partials dest=configs/{{ inventory_hostname }}/{{ inventory_hostname}}.conf

      - name: PUSH CONFIGS
        napalm_install_config:
          hostname={{ inventory_hostname }}
          username={{ un }}
          password={{ pwd }}
          dev_os={{ os }}
          config_file=configs/{{ inventory_hostname }}/{{ inventory_hostname}}.conf
          diff_file=diffs/{{ inventory_hostname }}.diffs
          commit_changes=true
          replace_config=true
        tags: push  

```

You can also see how we are using the variables that we defined in the inventory file such as `un`, `pwd`, and `os`.


##### Step 4

Execute ONLY the new task by using tags.

> SSH to any of the devices if you want to look at the configurations before they are modified.

Use this command:
```
ntc@ntc:~/ansible$ ansible-playbook -i inventory juniper-build.yml --tags=push
```

Congratulations!  You just pushed a new running configuration to three devices.

SSH to devices and look at the routing tables.

##### Step 5

Open one of the diff files created.  You can see that you can generate diffs so you see exactly what is changing on the device.  Additionally, you could have also done `commit_changes=false` to just generate diffs and not apply the config changes as part of a change workflow.

Remember the diffs are stored in the `diffs` directory created you created in the previous Step.

##### Step 6

Re-run the full playbook.  

Were there any changes?  Why or Why not?
