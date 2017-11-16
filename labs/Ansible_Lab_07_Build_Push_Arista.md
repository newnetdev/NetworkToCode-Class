## Lab 7.1 - Building and Pushing Network Configuration Files

This lab will show how to use Ansible to automate the process of building full network configuration files and pushing them to network devices.  

You will take existing configuration files, de-construct them, and then create Jinja2 templates and YAML based variable files.  The templates and variables will be rendered together using the Ansible *template* module to create configuration files.  They will then be pushed to network devices using an open source module from the NAPALM community.

### Task 1 - Create Templates and Vars Files

Your goal now is to create 2 configuration files using a leaf template.

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

The configuration below is from one of the leaf switches, namely *eos-leaf1*.  The same configuration needs to be applied across all leaf switches.

Your job is to create a leaf template and the associated group vars and host vars files.

```
! Command: show running-config
! device: eos-leaf1 (vEOS, EOS-4.14.7M)
!
! boot system flash:EOS.swi
!
transceiver qsfp default-mode 4x10G
!
hostname eos-leaf1
ip domain-name ntc.com
!
spanning-tree mode mstp
!
no aaa root
!
username admin privilege 15 role network-admin secret 5 $1$7yUmRiH6$9F1Io4WMwAWSc2GMjeK3h/
!
!
vlan 20
   name app
!
vlan 30
   name db
!
vlan 40
   name test
!
vlan 50
   name misc
!
interface Port-Channel10
  switchport mode trunk
!
interface Ethernet1
  description description uplink to spine
  channel-group 10 mode active
  no shutdown
!
interface Ethernet2
  description description uplink to spine
  channel-group 10 mode active
  no shutdown
!
interface Ethernet3
  shutdown
!
interface Ethernet4
  shutdown
!
interface Ethernet5
  switchport mode access
  shutdown
!
interface Ethernet6
  switchport mode access
  shutdown
!
interface Management1
   ip address 10.0.0.21/24
!
ip route 0.0.0.0/0 10.0.0.2
!
ip routing
!
management api http-commands
   no shutdown
!
!
end
```

##### Step 2

Create a file called `eos-leaf.j2` in the `templates` directory and open it. It will serve as the template for the leaf switches.

##### Step 3

Now create a new directory called `group_vars` and in this directory create a file called `eos-leaves.yml`.  

> Note: The name of the directory called `group_vars` is an important name within Ansible.  It will store "group based variables".

> The names of the files in the `group_vars` directory map directly to the groups that are found in the inventory file.  For example, the variables that end up in `group_vars/eos-leaves.yml` will be available, and in scope, for all devices in the *leaves* group, i.e. eos-leaf1 - eos-leaf10.

Updated directory structure:

```
ntc@ntc:~/ansible$ tree
.
├── group_vars
│   └── eos-leaves.yml
├── inventory
└── templates
    └── eos-leaf.j2

2 directories, 3 files
```

Ensure you have both `eos-leaf.j2` and `eos-leaves.yml` open in your text editor.

Now, we will start to break down the configuration file into a series of Jinja2 template snippets and variables.

We'll break this down into sections in order to create the appropriate template file.

> For real-world use, consider using different template files per service as reviewed in the lecture.

First, we'll look at this snippet going top down in the configuration file:

```
hostname eos-leaf1
ip domain-name ntc.com
!
spanning-tree mode mstp
!
no aaa root
!
username admin privilege 15 role network-admin secret 5 $1$7yUmRiH6$9F1Io4WMwAWSc2GMjeK3h/
!
```

There are always multiple ways to build a template for a given configuration file, but for this one, create variables for the following values:

- hostname
- domain name
- username
- privilege
- role
- secret

We'll use the following as variable names:

- inventory_hostname
- domain_name
- username
- priv
- role
- secret

> Note: remember that `inventory_hostname` is a built in variable that gets set to the name of the host as it is defined in the inventory file.

##### Step 4

Take the template snippet and put it into the `eos-leaf.j2` file.

```
! boot system flash:EOS.swi
!
transceiver qsfp default-mode 4x10G
!
hostname {{ inventory_hostname }}
ip domain-name {{ domain_name }}
!
spanning-tree mode mstp
!
no aaa root
!
username {{ username }} privilege {{ priv }} role {{ role }} secret 5 {{ secret }}
!
```

As you can see, all that is required is to substitute the proper values using double curly braces around your new variable name.  This is the easiest kind of template to work with.

##### Step 5

Within the `group_vars/eos-leaves.yml`  file, you now need to store the values you just removed from the config file.  Take the variables below and store them in `eos-leaves.yml` in `group_vars`

Variables Snippet (`group_vars/eos-leaves.yml`):

```yaml
---

domain_name: ntc.com

username: admin
priv: 15
role: network-admin
secret: $1$7yUmRiH6$9F1Io4WMwAWSc2GMjeK3h/
```

You're starting to de-couple the inputs from the underlying CLI syntax.  You can now version control each and just make changes to your vars files going forward.

##### Step 6

Next up are the VLANs:

```
!
vlan 20
   name app
!
vlan 30
   name db
!
vlan 40
   name test
!
vlan 50
   name misc
```

Anything that repeats itself should be screaming "use a loop".  We can reduce the VLANs down to a simple loop.  For our scenario, each VLAN will be equal to a dictionary and they will be stored in a list.  Thus, we'll need to iterate through a list of dictionaries in Jinja2 and store a list of dictionaries in YAML.  

Each VLAN dictionary should have two keys: `id` and `name`.

##### Step 7

Create the variables for VLANs (`group_vars/eos-leaves.yml`):

> This is one notation to depict a list of dicationaries.

```yaml
vlans:
  - { id: 20, name: app }
  - { id: 30, name: db }
  - { id: 40, name: test }
  - { id: 50, name: misc }
```

Save the VLANs YAML snippet right under the `secret` variable that already exists in the `eos-leaves.yml` file.

> Note: Another way to show a list of dictionaries in YAML is the following:
>```yaml
>vlans:
>  - id: 20
>    name: app
>  - id: 30
>    name: db
>```


##### Step 8

Create the Jinja snippet for VLANs and put it right below the template snippet that already exists in `eos-leaf.j2`.

This is no different than iterating over a list of dictionaries in Python other than the syntax.

```
!
{% for vlan in vlans %}
vlan {{ vlan.id }}
  name {{ vlan.name }}
{% endfor %}
!
```

You can see that `vlans` is a list and each element in the list is a dictionary.

##### Step 9

The next major section to de-compose is the interfaces section (mgmt is left out):

```python
!
interface Port-Channel10
  switchport mode trunk
!
interface Ethernet1
  description description uplink to spine
  channel-group 10 mode active
  no shutdown
!
interface Ethernet2
  description description uplink to spine
  channel-group 10 mode active
  no shutdown
!
interface Ethernet3
  shutdown
!
interface Ethernet4
  shutdown
!
interface Ethernet5
  switchport mode access
  shutdown
!
interface Ethernet6
  switchport mode access
  shutdown
!

```

It's worth stating there isn't a right or wrong way to create templates.  You have to find what works for you and your team, for your configuration.  

In this scenario, port-channel10 is always the port-channel that connects to the Spine, so we can keep that hard-coded in the template (for production, you may want to template the uplink port-channel to easily change which port-channel is used).

For the configuration per interface, you also need to see what type of requirements you have.For the config snippet here, we have a few basic parameters to worry about including state (shut or no shut), mode (access or trunk), channel group configs on the physical uplinks, and interface descriptions.  

##### Step 10

Create a list of dictionaries that can model the interface configuration along with the appropriate template that will build the proper configuration.

Variables `group_vars/eos-leaves.yml` - (place under VLANs variables):

```yaml

interfaces:
  - { name: Ethernet1, description: description uplink to spine, state: up, uplink: true }
  - { name: Ethernet2, description: description uplink to spine, state: up, uplink: true }
  - { name: Ethernet3, state: down }
  - { name: Ethernet4, state: down }
  - { name: Ethernet5, state: down, mode: access }
  - { name: Ethernet6, state: down, mode: access }

```

##### Step 11 

Associated Jinja2 template (place under VLANs snippet):

```
interface Port-Channel10
  switchport mode trunk
!
{% for interface in interfaces %}
interface {{ interface.name }}
{% if interface.get('description') %}
  description {{ interface.description }}
{% endif %}
{% if interface.get('mode') == "trunk" %}
  switchport mode trunk
{% elif interface.get('mode') == "access" %}
  switchport mode access
{% endif %}
{% if interface.get('uplink') %}
  channel-group 10 mode active
{% endif %}
{% if interface.get('state') == "up" %}
  no shutdown
{% elif interface.get('state') == "down" %}
  shutdown
{% endif %}
!
{% endfor %}
```

Take a minute and review the template carefully.

##### Step 12

Review the last config snippet including the Management1 interfce that needs to be de-composed:

```
interface Management1
   ip address 10.0.0.21/24
!
ip route 0.0.0.0/0 10.0.0.2
!
ip routing
!
management api http-commands
   no shutdown
!
!
end
```

##### Step 13

Create the template and variables for everything that needs to change between devices:

Variables Snippet (`group_vars/eos-leaves.yml`):

```yaml
management_ip_mask: "10.0.0.21/24"
```

Jinja2 Template Snippet: 

```
interface Management1
   ip address {{ management_ip_mask }}
!
ip route 0.0.0.0/0 10.0.0.2
!
ip routing
!
management api http-commands
   protocol http
   no shutdown
!
end
```

At this point, you have created the following template and variables files:

`templates/eos-leaf.j2`:

```
! boot system flash:EOS.swi
!
transceiver qsfp default-mode 4x10G
!
hostname {{ inventory_hostname }}
ip domain-name {{ domain_name }}
!
spanning-tree mode mstp
!
no aaa root
!
username {{ username }} privilege {{ priv }} role {{ role }} secret 5 {{ secret }}
!
{% for vlan in vlans %}
vlan {{ vlan.id }}
  name {{ vlan.name }}
{% endfor %}
!
interface Port-Channel10
  switchport mode trunk
!
{% for interface in interfaces %}
interface {{ interface.name }}
{% if interface.get('description') %}
  description {{ interface.description }}
{% endif %}
{% if interface.get('mode') == "trunk" %}
  switchport mode trunk
{% elif interface.get('mode') == "access" %}
  switchport mode access
{% endif %}
{% if interface.get('uplink') %}
  channel-group 10 mode active
{% endif %}
{% if interface.get('state') == "up" %}
  no shutdown
{% elif interface.get('state') == "down" %}
  shutdown
{% endif %}
!
{% endfor %}
!
interface Management1
   ip address {{ management_ip_mask }}
!
ip route 0.0.0.0/0 10.0.0.2
!
ip routing
!
management api http-commands
   protocol http
   no shutdown
!
end

```


`group_vars/eos-leaves.yml`:

```yaml

management_ip_mask: "10.0.0.21/24"

domain_name: ntc.com

username: admin
priv: 15
role: network-admin
secret: $1$7yUmRiH6$9F1Io4WMwAWSc2GMjeK3h/


vlans:
  - { id: 20, name: app }
  - { id: 30, name: db }
  - { id: 40, name: test }
  - { id: 50, name: misc }


interfaces:
  - { name: Ethernet1, description: description uplink to spine, state: up, uplink: true }
  - { name: Ethernet2, description: description uplink to spine, state: up, uplink: true }
  - { name: Ethernet3, state: down }
  - { name: Ethernet4, state: down }
  - { name: Ethernet5, state: down, mode: access }
  - { name: Ethernet6, state: down, mode: access }

```

##### Step 14

Once the new config is generated from the template and vars file, it needs to be stored somewhere.  

Create a new directory called `configs` that will store the new configuration files.

The new directory structure should look like this:

```
ntc@ntc:~/ansible$ tree
.
├── configs
├── group_vars
│   └── eos-leaves.yml
├── inventory
└── templates
    └── eos-leaf.j2

3 directories, 3 files
```


### Task 2 - Building the Configurations

It's time to create the playbook that will auto-generate all of the leaf configuration files.

##### Step 1

Create and open a file called `build-push.yml`.

Save it in the `ansible` directory.

```
ntc@ntc:~/ansible$ tree
.
├── build-push.yml
├── configs
├── group_vars
│   └── eos-leaves.yml
├── inventory
└── templates
    └── eos-leaf.j2

3 directories, 4 files

```


The playbook will consist of a single play and a single task.  The task will use the **template** module.

Two parameters will be passed to the module:  `src` which is the source template, i.e. `eos-leaf.j2` and the `dest`, which is the where the final rendered config file will be stored.

This play should be limited to the `eos-leaves` group in the inventory file, so use the `hosts: eos-leaves` in the play definition.

```yaml
---

  - name: Build Configuration Files
    hosts: eos-leaves
    connection: local
    gather_facts: no

    tasks:
      - name: BUILD CONFIGS
        template: src=templates/eos-leaf.j2 dest=configs/{{inventory_hostname }}.conf

```

> Note: we are using the variable `inventory_hostname` in the value for the `dest` parameter.  This will make a file with the name of the device as it is defined in the inventory file.


##### Step 2

Save the playbook (don't close it) and go back to the Linux command line.

Execute the playbook using the following command:

```
ntc@ntc:~/ansible$ ansible-playbook -i inventory build-push.yml
```

You will see the following output during execution:

```
ntc@ntc:~/ansible$ ansible-playbook -i inventory build-push.yml 

PLAY [Build Configuration Files] ********************************************** 

TASK: [BUILD CONFIGS] ********************************************************* 
changed: [eos-leaf1]
changed: [eos-leaf2]

PLAY RECAP ******************************************************************** 
eos-leaf1                      : ok=1    changed=1    unreachable=0    failed=0   
eos-leaf2                      : ok=1    changed=1    unreachable=0    failed=0     

```

##### Step 3

Take notice of your new file/directory structure.

```
ntc@ntc:~/ansible$ tree
.
├── build-push.yml
├── configs
│   ├── eos-leaf1.conf
│   └── eos-leaf2.conf
├── group_vars
│   └── eos-leaves.yml
├── inventory
└── templates
    └── eos-leaf.j2
```

Open a few of the configuration files and a take look at them.

Notice anything incorrect?

You should notice that every device has the same config even including the management IP address.  

> Note: the hostname is correct for each because the built-in variable called `inventory_hostname` was used.

`eos-leaves.yml` stores *group* variables.  We need a location to store host specific variables. These are the values that are different for EVERY host.  You can store these in the `host_vars` directory **or** in the inventory file.

##### Step 4

Create a `host_vars` directory and create two files in it: `eos-leaf1.yml` and `eos-leaf2.yml`.  

The names of these files are also significant.  They match the names as they are defined in the inventory file.

```
ntc@ntc:~/ansible$ mkdir host_vars

ntc@ntc:~/ansible$ cd host_vars/
```

Open the newly created files and ensure they have the vars as defined below in them.

`host_vars/eos-leaf1.yml`

```yaml
---
management_ip_mask: "10.0.0.21/24"
```

`host_vars/eos-leaf2.yml`

```yaml
---
management_ip_mask: "10.0.0.22/24"
```

**REMOVE** the `management_ip_mask` variable from `eos-leaves.yml`

##### Step 5

Status Check:

Your new directory structure should look like this:

```
ntc@ntc:~/ansible$ tree
.
├── build-push.yml
├── configs
│   ├── eos-leaf1.conf
│   └── eos-leaf2.conf
├── group_vars
│   └── eos-leaves.yml
├── host_vars
│   ├── eos-leaf1.yml
│   └── eos-leaf2.yml
├── inventory
└── templates
    └── eos-leaf.j2

```

##### Step 6

Re-run the playbook (ensure you are in the `ansible` directory):

```
ntc@ntc:~/ansible$ ansible-playbook -i inventory build-push.yml 

PLAY [Build Configuration Files] ********************************************** 

TASK: [BUILD CONFIGS] ********************************************************* 
changed: [eos-leaf2]
ok: [eos-leaf1]

PLAY RECAP ******************************************************************** 
eos-leaf1                      : ok=1    changed=0    unreachable=0    failed=0   
eos-leaf2                      : ok=1    changed=1    unreachable=0    failed=0   

```

Notice anything interesting?  You should have realize that *eos-leaf1* did not change.  This is because the **template** module, like most modules, is idempotent meaning a change is only made if it needs to be made, and the *eos-leaf1* config file was already in its desired state.

##### Step 7

Open the configs to make sure they updated correctly.

##### Step 8


OPTIONAL:
  - Create the required variables file called `eos-spines.yml` in the `group_vars` directory or `host_vars` files for *eos-spine1* and *eos-spine2* to build out all 4 configurations.


### Task 3 - Pushing the Configurations

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
  - `replace_config`: it's possible to do a replace/overwrite or a merge.  We are doing a merge.


> Also take notice of the `tags` helper module below in the last line of the playbook.  This will allow us to run just this task from the terminal.

##### Step 2

First create a directory called `diffs` in your working directory using the `mkdir diffs` command.  This will store the diffs generated by the devices so we can see what changes are getting applied.

Then add the following task to the `build-push.yml` playbook:

```yaml
---

  - name: Build Configuration Files
    hosts: eos-leaves
    connection: local
    gather_facts: no

    tasks:
      - name: BUILD CONFIGS
        template: src=templates/eos-leaf.j2 dest=configs/{{inventory_hostname }}.conf

      - name: PUSH CONFIGS
        napalm_install_config:
          hostname={{ inventory_hostname }}
          username={{ un }}
          password={{ pwd }}
          dev_os={{ os }}
          config_file=configs/{{ inventory_hostname }}.conf
          diff_file=diffs/{{ inventory_hostname }}.diffs
          commit_changes=true
          replace_config=false
        tags: push  

```

> Note: we aren't replacing the full existing file since we using replace_config=false.  Rather, we are doing a configuration merge.  However, for production environments, you may want to do a full replace, so should you want to, set replace_config=true.

You can also see how we are using the variables that we defined in the inventory file such as `un`, `pwd`, and `os`.

##### Step 3

Execute ONLY the new task by using tags.

> SSH to eos-leaf1 and/or eos-leaf2 if you want to look at the configs before and after you push the new configs.


Use this command:
```
ntc@ntc:~/ansible$ ansible-playbook -i inventory build-push.yml --tags=push
```


```

PLAY [Push configs] *********************************************************** 

TASK: [PUSH CONFIGS] ********************************************************** 
changed: [eos-leaf1]
changed: [eos-leaf2]

PLAY RECAP ******************************************************************** 
eos-leaf1                      : ok=1    changed=1    unreachable=0    failed=0   
eos-leaf2                      : ok=1    changed=1    unreachable=0    failed=0 
```

Congratulations!  You just pushed a new running configuration to two switches!

Now open one of the diff files created.  You can see that you can generate diffs so you see exactly what is changing on the device.  Additionally, you could have also done `commit_changes=false` to just generate diffs and not apply the config changes as part of a change workflow.

Remember the diffs are stored in the `diffs` created you created in the previous Step.

##### Step 4

In order to see the full workflow, delete/remove all of the conf files from the `configs` directory.

```
ntc@ntc:~/ansible$ rm configs/eos-leaf*.conf
```

You file/dir structure should look like this:

```yaml
ntc@ntc:~/ansible$ tree
.
├── build-push.yml
├── configs
├── group_vars
│   └── eos-leaves.yml
├── host_vars
│   ├── eos-leaf1.yml
│   └── eos-leaf2.yml
├── inventory
└── templates
    └── eos-leaf.j2


```

##### Step 5

Run the playbook without tags:

```
ntc@ntc:~/ansible$ ansible-playbook -i inventory build-push.yml
```

```

PLAY [Build Configuration Files] ********************************************** 

TASK: [BUILD CONFIGS] ********************************************************* 
changed: [eos-leaf1]
changed: [eos-leaf2]

TASK: [PUSH CONFIGS] ********************************************************** 
changed: [eos-leaf1]
changed: [eos-leaf2]

PLAY RECAP ******************************************************************** 
eos-leaf1                      : ok=2    changed=2    unreachable=0    failed=0   
eos-leaf2                      : ok=2    changed=2    unreachable=0    failed=0   

```

If you run it once more, you'll notice the BUILD CONFIGS task *doesn't* get changed because the configs are already good to go ( because the template module is idempotent).  You'll also notice the PUSH CONFIGS task *does not* get applied again since Arista only applies diffs.  If you view the diffs again, they should be empty!






