## Lab 6 - Jinja2 Templating with Ansible


### Task 1 - Using Jinja2 to render a variable

In this task we will learn how to use Jinja2 templates in Ansible.


##### Step 1

Create a new playbook within the `ansible` directory by using the `touch` command


```
ntc@ntc:ansible$ touch render_snmp.yml

```


##### Step 2 
Open this file using any text editor and add the following play definition:

```yaml
---
- name: RENDER SNMP CONFIGS USING JINJA2 - AMERICAS
  hosts: AMER
  gather_facts: no
  connection: local
  
```

##### Step 3

Define a SNMP RO string as a variable, within the playbook file:

``` yaml
---
- name: RENDER SNMP CONFIGS USING JINJA2 - AMERICAS
  hosts: AMER
  gather_facts: no
  connection: local

  vars:
    snmp_ro: ntc_course
    
```

##### Step 4

Using the Ansible `template` module, create a task that will take this variables and render it :

``` yaml
---
- name: RENDER SNMP CONFIGS USING JINJA2 - AMERICAS
  hosts: AMER
  gather_facts: no
  connection: local

  vars:
    snmp_ro: ntc_course

  tasks:
    - name: RENDER IOS SNMP CONFIGURATIONS
      template:
        src: 01-ios-snmp.j2
        dest: "./configs/01_{{ inventory_hostname }}_snmp.cfg"
        
```

##### Step 5

In the previous step, the source of the template was identified as a `j2` file. Ansible by default will look in the current directory and a directory named `templates` for these files. Let us create this.

Create a `templates` directory within the `ansible` directory and navigate to that directory.

```
ntc@ntc:ansible$ 
ntc@ntc:ansible$ mkdir templates
ntc@ntc:ansible$ cd templates
ntc@ntc:templates$

```

##### Step 6

Here, create the template file we will be using to render the SNMP configuration, by using the `touch` command

```
ntc@ntc:templates$ touch 01-ios-snmp.j2 

```


##### Step 7

Open the `01-ios-snmp.j2` file using a text editor and add the snmp configuration template for it. This is simply a text file with the values for the SNMP variable "parameterized".

```
snmp-server community {{ snmp_ro }}  RO

```

Keep in mind that the values for this variable was defined in **Step3**, within the playbook. Ansible will pass those variables to the template, which will then render it.


##### Step 8

Run the playbook as follows:


```
ntc@ntc:ansible$ ansible-playbook -i inventory render_snmp.yml 

PLAY [RENDER SNMP CONFIGS USING JINJA2] *********************************************************************************

TASK [RENDER IOS SNMP CONFIGURATIONS] ***********************************************************************************
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

Now, validate that the variables have been rendered correctly by checking the files created in the `configs` directory.

```
#01_csr1_snmp.cfg 
snmp-server community ntc_course  RO
```

### Task 2 - Adding more SNMP variables to group_vars

In this task we will template the configuration for some additional SNMP variables. The "snmp location" will be different for the `AMER` group and the `EMEA` group.

##### Step 1

Create a directory called `group_vars` under `ansible` and within that directory, create the directories `AMER` and `EMEA`


```
ntc@ntc:ansible$ mkdir group_vars
ntc@ntc:ansible$ cd group_vars
ntc@ntc:group_vars$ mkdir AMER
ntc@ntc:group_vars$ mkdir EMEA

```



##### Step 2

Create a file called `snmp_vars.yml` inside `EMEA` and `AMER` directories

```
ntc@ntc:group_vars$ touch AMER/snmp_vars.yml
ntc@ntc:group_vars$ touch EMEA/snmp_vars.yml

```


The directory structure looks as follows:

```
├── group_vars
│   ├── AMER
│   │   └── snmp_vars.yml
│   └── EMEA
│       └── snmp_vars.yml

```


##### Step 3

Open the `AMER/snmp_vars.yml` using a text editor and update it with the following variables:

```yaml
snmp_ro: ntc_course
snmp_rw: ntc_private
snmp_location: NYC
snmp_contact: netops_team

```


##### Step 4

Similarly update `EMEA/snmp_vars.yml` to contain the EMEA region specific SNMP variables.

``` yaml
snmp_ro: ntc_course
snmp_rw: ntc_private
snmp_location: MILAN
snmp_contact: netops_team
```



##### Step 5

Update the `01-ios-snmp.j2` file to render the rest of the SNMP configurations

```
snmp-server community {{ snmp_ro }}  RO
snmp-server community {{ snmp_rw }}  RW
snmp-server contact {{ snmp_contact }}  
snmp-server location {{ snmp_location }}

```

##### Step 6

Create a `01-junos-snmp.j2` file in the templates directory to render the JUNOS configuration commands

```
set snmp community {{ snmp_ro }} authorization read-only
set snmp community {{ snmp_rw }} authorization read-write
set snmp location {{ snmp_location }}
set snmp contact {{ snmp_contact }}


```

##### Step 7

Since the `snmp_ro` variable has been defined as a group variable, we can now remove it from our playbook - `render_snmp.yml`.

``` yaml
---
- name: RENDER SNMP CONFIGS USING JINJA2 - AMERICAS
  hosts: AMER
  gather_facts: no
  connection: local

  tasks:
    - name: RENDER IOS SNMP CONFIGURATIONS
      template:
        src: 01-ios-snmp.j2
        dest: "./configs/01_{{ inventory_hostname }}_snmp.cfg"

```

##### Step 8

Add one more play to this playbook to also render the JUNOS specific commands used on the EMEA devices - `vmx7,8 & 9`

``` yaml
---
- name: RENDER SNMP CONFIGS USING JINJA2 - AMERICAS
  hosts: AMER
  gather_facts: no
  connection: local

  tasks:
    - name: RENDER IOS SNMP CONFIGURATIONS
      template:
        src: 01-ios-snmp.j2
        dest: "./configs/01_{{ inventory_hostname }}_snmp.cfg"

- name: RENDER SNMP CONFIGS USING JINJA2 - EMEA
  hosts: EMEA
  gather_facts: no
  connection: local

  tasks:
    - name: RENDER JUNOS SNMP CONFIGURATIONS
      template:
        src: 01-junos-snmp.j2
        dest: "./configs/01_{{ inventory_hostname }}_snmp.cfg"

```


##### Step 7

Now, run the playbook and validate that the configurations have been created in the `configs` directory.

```
ntc@ntc:ansible$ ansible-playbook -i inventory render_snmp.yaml 

PLAY [RENDER SNMP CONFIGS USING JINJA2 - AMERICAS] **********************************************************************

TASK [RENDER IOS SNMP CONFIGURATIONS] ***********************************************************************************
changed: [csr3]
changed: [csr2]
changed: [csr1]

PLAY [RENDER SNMP CONFIGS USING JINJA2 - EMEA] **************************************************************************

TASK [RENDER JUNOS SNMP CONFIGURATIONS] *********************************************************************************
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

### Task 3 - Deploy the configuration

Rather than render the configurations locally to the `configs` directory and then pushing to the devices. You can directly pass in the jinja2 template, to the `_config` (ios or junos_config) module to render and push the configuration in one task.


##### Step 1

Create a `provider` variable to login to the devices. Touch a file named `all.yml` under `group_vars` and open it with an editor. Add the following login info into it.

``` yaml

provider:
  username: "{{ un }}"
  password: "{{ pwd }}"
  host: "{{ inventory_hostname }}"

```

>Since we are creating this variable in the `all.yml` file, it will apply to all groups.



##### Step 2

Open the `render_snmp.yml` file using a text editor. Since we no longer need to render the configurations locally, go ahead and remove  the task from PLAY 1 and 2.


##### Step 3

Add a new task under PLAY 1, that uses the `ios_config` module to render and push the configurations.


``` yaml

---
- name: RENDER SNMP CONFIGS USING JINJA2 - AMERICAS
  hosts: AMER
  gather_facts: no
  connection: local

  tasks:
    - name: ENSURE THAT SNMP IS CONFIGURED ON AMER DEVICES
      ios_config:
        src: 01-ios-snmp.j2
        provider: "{{ provider }}"


```


##### Step 4

Similarly under PLAY 2, create a task that uses `junos_config` to render the template and push to the EMEA devices.


``` yaml
---
- name: RENDER SNMP CONFIGS USING JINJA2 - AMERICAS
  hosts: AMER
  gather_facts: no
  connection: local

  tasks:
    - name: ENSURE THAT SNMP IS CONFIGURED ON AMER DEVICES
      ios_config:
        src: 01-ios-snmp.j2
        provider: "{{ provider }}"

- name: RENDER SNMP CONFIGS USING JINJA2 - EMEA
  hosts: EMEA
  gather_facts: no
  connection: local

  tasks:
    - name: ENSURE THAT SNMP IS CONFIGURED ON AMER DEVICES
      junos_config:
        src: 01-junos-snmp.j2
        provider: "{{ provider }}"

```


##### Step 5

Now run the playbook.

```
ntc@ntc:ansible$ ansible-playbook -i inventory render_snmp.yaml 

PLAY [RENDER SNMP CONFIGS USING JINJA2 - AMERICAS] **********************************************************************

TASK [ENSURE THAT SNMP IS CONFIGURED ON AMER DEVICES] *******************************************************************
changed: [csr1]
changed: [csr2]
changed: [csr3]


PLAY [RENDER SNMP CONFIGS USING JINJA2 - EMEA] **************************************************************************

TASK [ENSURE THAT SNMP IS CONFIGURED ON AMER DEVICES] *******************************************************************
changed: [vmx7]
changed: [vmx8]
changed: [vmx9]

PLAY RECAP **************************************************************************************************************
csr1                       : ok=1    changed=1    unreachable=0    failed=0   
csr2                       : ok=1    changed=0    unreachable=0    failed=0   
csr3                       : ok=1    changed=0    unreachable=0    failed=0   
vmx7                       : ok=1    changed=1    unreachable=0    failed=0   
vmx8                       : ok=1    changed=0    unreachable=0    failed=0   
vmx9                       : ok=1    changed=0    unreachable=0    failed=0   

ntc@ntc:ansible$ 

```

##### Step 7

Login to the devices to ensure that the configuration changes were implemented correctly


```
#csr1

csr1#sh run | inc snmp
snmp-server community ntc-course RO
snmp-server community private RW
snmp-server community ntc-private RW
snmp-server community public RO
snmp-server location MILAN
snmp-server contact netops_team
csr1#

#vmx7

ntc@vmx7> show configuration snmp | display set 
set snmp location NYC
set snmp contact netops_team
set snmp community public authorization read-only
set snmp community ntc-course authorization read-only
set snmp community private authorization read-write
set snmp community ntc-private authorization read-write

ntc@vmx7> 


```



## BONUS TASKS: STOP! Only proceed if you have the time
### Bonus 1 - Updating the SNMP Data Model
  
In the previous task, the SNMP data was modeled as a set of 'key-value' pairs. This works for a simple use case. What if we had to configure multiple RO/RW strings?



##### Step 1


Add the `snmp` variable into the `AMER/snmp_vars.yml` file.


``` yaml
    snmp:
      ro:
        - public
        - ntc-course
      rw:
        - private
        - ntc-private
      contact: netops_team
      location: NYC

```

##### Step 2

Repeat and add the  `snmp` variable to the `EMEA/snmp_vars.yml` file.


``` yaml
    snmp:
      ro:
        - public
        - ntc-course
      rw:
        - private
        - ntc-private
      contact: netops_team
      location: MILAN


```



##### Step 3

But now, since our data model has changed, we need to also update our Jinja2 templates to correctly access the values.

Create a new file called `02-ios-snmp.j2` within the templates directory and open it with a text editor. We will use the following template to render the desired configuration.


``` 
set snmp_ro_comms = {{ snmp.ro }}
{% for ro_comm in snmp_ro_comms -%}
snmp-server community {{ ro_comm }} RO
{%- endfor %}
set snmp_rw_comms = {{ snmp.rw }}
{% for rw_comm in snmp_ro_comms -%}
snmp-server community {{ rw_comm }} RW
{%- endfor %}
snmp-server location {{ snmp_location }}
snmp-server contact {{ snmp_contact }}

```


Similarly, create a `02-junos-snmp.j2` template file, using the JUNOS configuration commands.

```
{% set snmp_ro_comms =  snmp.ro  %}
{% for ro_comm in snmp_ro_comms %}
set snmp community {{ ro_comm }} authorization read-only
{% endfor %}
{% set snmp_rw_comms =  snmp.rw  %}
{% for rw_comm in snmp_rw_comms %}
set snmp community {{ rw_comm }} authorization read-write
{% endfor %}
set snmp location {{ snmp.location }}
set snmp contact {{ snmp.contact }}

```


##### Step 4


Update the `src` parameter in the template task to point to the new templates that were created in the previous step.
At this point, the playbook should look as follows:

``` yaml
---
- name: RENDER SNMP CONFIGS USING JINJA2 - AMERICAS
  hosts: AMER
  gather_facts: no
  connection: local

  tasks:
    - name: RENDER IOS SNMP CONFIGURATIONS
      ios_config:
        src: 02-ios-snmp.j2
        provider: "{{ provider }}"


- name: RENDER SNMP CONFIGS USING JINJA2 - EMEA
  hosts: EMEA
  gather_facts: no
  connection: local

  tasks:
    - name: RENDER JUNOS SNMP CONFIGURATIONS
      junos_config:
        src: 02-junos-snmp.j2
        provider: "{{ provider }}"

```

##### Step 5

Now run the playbook.

```
ntc@ntc:ansible$ ansible-playbook -i inventory render_snmp.yaml 

PLAY [RENDER SNMP CONFIGS USING JINJA2 - AMERICAS] **********************************************************************

TASK [ENSURE THAT SNMP IS CONFIGURED ON AMER DEVICES] *******************************************************************
changed: [csr1]
changed: [csr2]
changed: [csr3]


PLAY [RENDER SNMP CONFIGS USING JINJA2 - EMEA] **************************************************************************

TASK [ENSURE THAT SNMP IS CONFIGURED ON AMER DEVICES] *******************************************************************
changed: [vmx7]
changed: [vmx8]
changed: [vmx9]

PLAY RECAP **************************************************************************************************************
csr1                       : ok=1    changed=1    unreachable=0    failed=0   
csr2                       : ok=1    changed=0    unreachable=0    failed=0   
csr3                       : ok=1    changed=0    unreachable=0    failed=0   
vmx7                       : ok=1    changed=1    unreachable=0    failed=0   
vmx8                       : ok=1    changed=0    unreachable=0    failed=0   
vmx9                       : ok=1    changed=0    unreachable=0    failed=0   

ntc@ntc:ansible$ 

```

##### Step 6

Validate that the devices have the updated configurations

```
#csr1

csr1#sh run | inc snmp
snmp-server community ntc-course RO
snmp-server community private RW
snmp-server community ntc-private RW
snmp-server community public RO
snmp-server location MILAN
snmp-server contact netops_team
csr1#

#vmx7

ntc@vmx7> show configuration snmp | display set 
set snmp location NYC
set snmp contact netops_team
set snmp community public authorization read-only
set snmp community ntc-course authorization read-only
set snmp community private authorization read-write
set snmp community ntc-private authorization read-write

ntc@vmx7> 


```


