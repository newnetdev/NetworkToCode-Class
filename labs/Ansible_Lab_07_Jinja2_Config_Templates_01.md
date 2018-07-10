## Lab 7 - Getting Started with Jinja2 Templating in Ansible

### Task 1 - Using Jinja2 to Build Configuration Templates

In this task we will learn how to use Jinja2 templates in Ansible to dynamically build configuration files.

##### Step 1

Since we're going to be generating configuration files, we need a place to store them.  

Create a `configs` sub-directory in the `ansible` directory.

```
ntc@ntc:ansible$ mkdir configs
ntc@ntc:ansible$
```


##### Step 2

Create a new playbook within the `ansible` directory:

```
ntc@ntc:ansible$ touch deploy-snmp.yml
ntc@ntc:ansible$
```


##### Step 3

Open this file using any text editor and add the following play definition:

```yaml
---
- name: GENERATE SNMP CONFIGS USING JINJA2 - AMERICAS
  hosts: AMER
  gather_facts: no
  connection: network_cli
  
```

##### Step 4

Define a SNMP RO string as a variable within the playbook:

``` yaml
---

- name: GENERATE SNMP CONFIGS USING JINJA2 - AMERICAS
  hosts: AMER
  gather_facts: no
  connection: network_cli

  vars:
    snmp_ro: ntc_course
    
```

##### Step 5

Using the Ansible `template` module, create a task that will take this variable and render it with a Jinja template (that is yet to be created):

``` yaml
---

- name: GENERATE SNMP CONFIGS USING JINJA2 - AMERICAS
  hosts: AMER
  gather_facts: no
  connection: network_cli

  vars:
    snmp_ro: ntc_course

  tasks:
    - name: GENERATE IOS SNMP CONFIGURATIONS
      template:
        src: ios-snmp.j2
        dest: "./configs/{{ inventory_hostname }}-snmp.cfg"
        
```



##### Step 6

In the previous step, the source of the template was identified as a `j2` file. Ansible by default will look in the current directory and a directory named `templates` for these files. Let us create this.

Create a `templates` directory within the `ansible` directory and navigate to that directory.

```
ntc@ntc:ansible$ 
ntc@ntc:ansible$ mkdir templates
ntc@ntc:ansible$ cd templates
ntc@ntc:templates$

```

##### Step 7

In the `templates` directory, create the Jinja template we will be using to render the SNMP configuration, by using the `touch` command.

> Note: this already referenced in the playbook.

```
ntc@ntc:templates$ touch ios-snmp.j2 
ntc@ntc:templates$
```


##### Step 8

Open the `ios-snmp.j2` file using a text editor and add the snmp configuration template for it. This is simply a text file with the values for the SNMP variable "parameterized".

```
snmp-server community {{ snmp_ro }}  RO

```

Keep in mind that the value for this variable was defined in **Step 4** within the playbook.  

**Ansible auto-loads all variables it's aware of at run-time and makes those variables available to the playbook and any template.**


##### Step 8

Run the playbook as follows:

```
ntc@ntc:ansible$ ansible-playbook -i inventory deploy-snmp.yml 

PLAY [GENERATE SNMP CONFIGS USING JINJA2] *********************************************************************************

TASK [GENERATE IOS SNMP CONFIGURATIONS] ***********************************************************************************
changed: [csr1]
changed: [csr2]
changed: [csr3]

PLAY RECAP **************************************************************************************************************
csr1                       : ok=1    changed=1    unreachable=0    failed=0   
csr2                       : ok=1    changed=1    unreachable=0    failed=0   
csr3                       : ok=1    changed=1    unreachable=0    failed=0   

ntc@ntc:ansible$ 


```

##### Step 9

Validate that the variables have been rendered correctly by checking the files created in the `configs` directory.

```
ntc@ntc:ansible$ cd configs
ntc@ntc:configs$ cat csr1-snmp.cfg 

snmp-server community ntc_course  RO
```


### Task 2 - Expanding the Jinaj2 Template and Using Group Variables

In this task we will template the configuration for some additional SNMP parameters, which will be different for the `AMER` group and the `EMEA` group.

##### Step 1

Create a new directory called `group_vars`.  

The name of the directory called `group_vars` is an important name within Ansible.  It will store "group based variables" - these map directly to the groups that are found in the inventory file.  For example, the variables that end up in `group_vars/all.yml` will be available to all devices. In this directory, create two group_vars files, called `AMER.yml` and `EMEA.yml`


```
ntc@ntc:ansible$ mkdir group_vars
ntc@ntc:ansible$ cd group_vars
ntc@ntc:group_vars$ touch AMER.yml
ntc@ntc:group_vars$ touch EMEA.yml
ntc@ntc:group_vars$

```


##### Step 2

Open the `AMER.yml` using a text editor and update it with the following variables:

```yaml
snmp_ro: ntc_course
snmp_rw: ntc_private
snmp_location: NYC
snmp_contact: netops_team

```

##### Step 3

Similarly update `EMEA.yml` to contain the EMEA region specific SNMP variables.

``` yaml
snmp_ro: ntc_course
snmp_rw: ntc_private
snmp_location: MILAN
snmp_contact: netops_team
```



##### Step 4

Update the `ios-snmp.j2` file to render the rest of the SNMP configurations:

```
snmp-server community {{ snmp_ro }}  RO
snmp-server community {{ snmp_rw }}  RW
snmp-server contact {{ snmp_contact }}  
snmp-server location {{ snmp_location }}

```

##### Step 5

Create a `junos-snmp.j2` file in the templates directory to render the JUNOS configuration commands

```
set snmp community {{ snmp_ro }} authorization read-only
set snmp community {{ snmp_rw }} authorization read-write
set snmp location {{ snmp_location }}
set snmp contact {{ snmp_contact }}


```

##### Step 6

Since the `snmp_ro` variable has been defined as a group variable, we can now remove it from the top of the playbook `deploy-snmp.yml`.

``` yaml
---
- name: GENERATE SNMP CONFIGS USING JINJA2 - AMERICAS
  hosts: AMER
  gather_facts: no
  connection: network_cli

  tasks:
    - name: GENERATE IOS SNMP CONFIGURATIONS
      template:
        src: ios-snmp.j2
        dest: "./configs/{{ inventory_hostname }}-snmp.cfg"

```

##### Step 7

Add one more play to this playbook to also build the JUNOS specific configurations used on the EMEA devices.

``` yaml
---
- name: GENERATE SNMP CONFIGS USING JINJA2 - AMERICAS
  hosts: AMER
  gather_facts: no
  connection: network_cli

  tasks:
    - name: GENERATE IOS SNMP CONFIGURATIONS
      template:
        src: ios-snmp.j2
        dest: "./configs/{{ inventory_hostname }}-snmp.cfg"

- name: GENERATE SNMP CONFIGS USING JINJA2 - EMEA
  hosts: EMEA
  gather_facts: no
  connection: network_cli

  tasks:
    - name: GENERATE JUNOS SNMP CONFIGURATIONS
      template:
        src: junos-snmp.j2
        dest: "./configs/{{ inventory_hostname }}-snmp.cfg"

```


##### Step 8

Execute the playbook:

```
ntc@ntc:ansible$ ansible-playbook -i inventory deploy-snmp.yml 

PLAY [GENERATE SNMP CONFIGS USING JINJA2 - AMERICAS] **********************************************************************

TASK [GENERATE IOS SNMP CONFIGURATIONS] ***********************************************************************************
changed: [csr3]
changed: [csr2]
changed: [csr1]

PLAY [GENERATE SNMP CONFIGS USING JINJA2 - EMEA] **************************************************************************

TASK [GENERATE JUNOS SNMP CONFIGURATIONS] *********************************************************************************
changed: [vmx8]
changed: [vmx7]
changed: [vmx9]

PLAY RECAP **************************************************************************************************************
csr1                       : ok=1    changed=1    unreachable=0    failed=0   
csr2                       : ok=1    changed=1    unreachable=0    failed=0   
csr3                       : ok=1    changed=1    unreachable=0    failed=0   
vmx7                       : ok=1    changed=1    unreachable=0    failed=0   
vmx8                       : ok=1    changed=1    unreachable=0    failed=0   
vmx9                       : ok=1    changed=1    unreachable=0    failed=0   

ntc@ntc:ansible$ 

```


##### Step 9

Validate that the configurations have been created in the `configs` directory:

```
ntc@ntc:ansible$ ls configs/
# output omitted
```



