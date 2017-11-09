## Lab 6 - Jinja2 Templating with Ansible

### Task 1 - Creating a golden SNMP configuration template

In this task, we will render SNMP configuration using a Jinja2 template for IOS and JUNOS devices.

##### Step 1

Create a new playbook within the `ansible` directory by using the `touch` command


```
ntc@ntc:ansible$ touch render_snmp.yaml

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

Define the following - "Americas" specific - variables for the SNMP configuration, within the playbook file:

``` yaml

  vars:
    snmp_ro: ntc_course
    snmp_rw: ntc_private
    snmp_location: NYC
    snmp_contact: netops_team
    
```

##### Step 4

Using the Ansible `template` module, create a task that will take these variables and render them :

``` yaml

  tasks:
    - name: RENDER IOS SNMP CONFIGURATIONS
      template:
        src: 01-ios-snmp.j2
        dest: "./configs/01_{{ inventory_hostname }}_snmp.cfg"
```


##### Step 5 

Add a second play, vars and task for the EMEA/JUNOS devices:

``` yaml
- name: RENDER SNMP CONFIGS USING JINJA2 - EMEA
  hosts: EMEA
  gather_facts: no
  connection: local

  vars:
    snmp_ro: ntc_course
    snmp_rw: ntc_private
    snmp_location: MILAN
    snmp_contact: netops_team

  tasks:
    - name: RENDER JUNOS SNMP CONFIGURATIONS
      template:
        src: 01-junos-snmp.j2
        dest: "./configs/01_{{ inventory_hostname }}_snmp.cfg"  
```


These tasks are going to render the configurations into the previously created directory - `configs`. 


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

Here, create the template file we will be using to render the SNMP configuration for `ios` and `junos` devices respectively, by using the `touch` command

```
ntc@ntc:templates$ touch 01-ios-snmp.j2 01-junos-snmp.j2

```


##### Step 8

Open the `01-ios-snmp.j2` file using a text editor and add the snmp configuration template for it. This is simply a text file with the values for the SNMP variables "parameterized".

```
snmp-server community {{ snmp_ro }}  RO
snmp-server community {{ snmp_rw }}  RW
snmp-server location {{ snmp_location }}        
snmp-server contact {{ snmp_contact }}

```

Keep in mind that the values for these variables were defined by us in **Step3**, within the playbook. Ansible will pass those variables to the template, which will then render it.

##### Step 9

Similarly edit the `01-junos-snmp.j2` file and add the Juniper specific snmp configuration commands, using the variable names:

```
set snmp community {{ snmp_ro }} authorization read-only
set snmp community {{ snmp_rw }} authorization read-write
set snmp location {{ snmp_location }}
set snmp contact {{ snmp_contact }}

```


##### Step 10

The final playbook should look similar to :

``` yaml
---
- name: RENDER SNMP CONFIGS USING JINJA2 - AMERICAS
  hosts: AMER
  gather_facts: no
  connection: local

  vars:
    snmp_ro: ntc_course
    snmp_rw: ntc_private
    snmp_location: NYC
    snmp_contact: netops_team

  tasks:
    - name: RENDER IOS SNMP CONFIGURATIONS
      template:
        src: 01-ios-snmp.j2
        dest: "./configs/{{ inventory_hostname }}_snmp.cfg"

- name: RENDER SNMP CONFIGS USING JINJA2 - EMEA
  hosts: EMEA
  gather_facts: no
  connection: local

  vars:
    snmp_ro: ntc_course
    snmp_rw: ntc_private
    snmp_location: MILAN
    snmp_contact: netops_team

  tasks:
    - name: RENDER JUNOS SNMP CONFIGURATIONS
      template:
        src: 01-junos-snmp.j2
        dest: "./configs/{{ inventory_hostname }}_snmp.cfg"         

```


##### Step 11


Finally, run the playbook as follows:


```
ntc@ntc:ansible$ ansible-playbook -i inventory render_snmp.yaml 

PLAY [RENDER SNMP CONFIGS USING JINJA2] *********************************************************************************

TASK [RENDER IOS SNMP CONFIGURATIONS] ***********************************************************************************
changed: [csr1]
changed: [csr2]
changed: [csr3]
changed: [vmx7]
changed: [vmx8]
changed: [vmx9]

TASK [RENDER JUNOS SNMP CONFIGURATIONS] *********************************************************************************
changed: [csr1]
changed: [csr2]
changed: [csr3]
changed: [vmx7]
changed: [vmx8]
changed: [vmx9]

PLAY RECAP **************************************************************************************************************
csr1                       : ok=2    changed=2    unreachable=0    failed=0   
csr2                       : ok=2    changed=2    unreachable=0    failed=0   
csr3                       : ok=2    changed=2    unreachable=0    failed=0   
vmx7                       : ok=2    changed=2    unreachable=0    failed=0   
vmx8                       : ok=2    changed=2    unreachable=0    failed=0   
vmx9                       : ok=2    changed=2    unreachable=0    failed=0   

ntc@ntc:ansible$ 

PLAY [RENDER SNMP CONFIGS USING JINJA2 - AMERICAS] **********************************************************************

TASK [RENDER IOS SNMP CONFIGURATIONS] ***********************************************************************************
changed: [csr1]
changed: [csr2]
changed: [csr3]

PLAY [RENDER SNMP CONFIGS USING JINJA2 - EMEA] **************************************************************************

TASK [RENDER JUNOS SNMP CONFIGURATIONS] *********************************************************************************
changed: [vmx7]
changed: [vmx8]
changed: [vmx9]

PLAY RECAP **************************************************************************************************************
csr1                       : ok=1    changed=1    unreachable=0    failed=0   
csr2                       : ok=1    changed=1    unreachable=0    failed=0   
csr3                       : ok=1    changed=1    unreachable=0    failed=0   
vmx7                       : ok=1    changed=1    unreachable=0    failed=0   
vmx8                       : ok=1    changed=1    unreachable=0    failed=0   
vmx9                       : ok=1    changed=1    unreachable=0   failed=0   


```

##### Step 12

Now, you should be able to see the rendered configurations in the `configs` directory

Sample files:

```
#01_csr1_snmp.cfg 
snmp-server community ntc_course  RO
snmp-server community ntc_private  RW
snmp-server location NYC        
snmp-server contact netops_team

#01_vmx7_snmp.cfg 
set snmp community ntc_course authorization read-only
set snmp community ntc_private authorization read-write
set snmp location MILAN
set snmp contact netops_team

```

## Task 2: Updating the SNMP Data Model
  
In the previous task, the SNMP data was modeled as a set of 'key-value' pairs. This works for a simple use case. What if we had to configure multiple RO/RW strings?



##### Step 1

Open the `render_snmp.yaml` in a text editor. Let's make a slight change in the way the SNMP variables have been modeled. Update the `vars:` directive for each play, configuring a new variable `snmp`, as a dictionary:


``` yaml
  vars:
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

This model allows for more flexibility than having a separate key/value for every variable.

Replicate this for PLAY2 as well, reflecting the location changes for EMEA.


##### Step 2

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


##### Step 3


Update the `src` parameter in the template task to point to the new templates that were created in the previous step.
At this point, the playbook should look as follows:

``` yaml
---
- name: RENDER SNMP CONFIGS USING JINJA2 - AMERICAS
  hosts: AMER
  gather_facts: no
  connection: local

  vars:
    snmp:
      ro:
        - public
        - ntc-course
      rw:
        - private
        - ntc-private
      contact: netops_team
      location: NYC


  tasks:
    - name: RENDER IOS SNMP CONFIGURATIONS
      template:
        src: 02-ios-snmp.j2
        dest: "./configs/02_{{ inventory_hostname }}_snmp.cfg"

- name: RENDER SNMP CONFIGS USING JINJA2 - EMEA
  hosts: EMEA
  gather_facts: no
  connection: local

  vars:
    snmp:
      ro:
        - public
        - ntc-course
      rw:
        - private
        - ntc-private
      contact: netops_team
      location: MILAN


  tasks:
    - name: RENDER JUNOS SNMP CONFIGURATIONS
      template:
        src: 02-junos-snmp.j2
        dest: "./configs/02_{{ inventory_hostname }}_snmp.cfg"         

```

##### Step 4

Now, run the playbook as follows:

``` 
ntc@ntc:ansible$ ansible-playbook  -i inventory render_snmp.yaml

PLAY [RENDER SNMP CONFIGS USING JINJA2 - AMERICAS] **********************************************************************

TASK [RENDER IOS SNMP CONFIGURATIONS] ***********************************************************************************
changed: [csr1]
changed: [csr2]
changed: [csr3]

PLAY [RENDER SNMP CONFIGS USING JINJA2 - EMEA] **************************************************************************

TASK [RENDER JUNOS SNMP CONFIGURATIONS] *********************************************************************************
changed: [vmx7]
changed: [vmx8]
changed: [vmx9]

PLAY RECAP **************************************************************************************************************
csr1                       : ok=1    changed=1    unreachable=0    failed=0   
csr2                       : ok=1    changed=1    unreachable=0    failed=0   
csr3                       : ok=1    changed=1    unreachable=0    failed=0   
vmx7                       : ok=1    changed=1    unreachable=0    failed=0   
vmx8                       : ok=1    changed=1    unreachable=0    failed=0   
vmx9                       : ok=1    changed=1    unreachable=0   failed=0   

```

##### Step 5

Confirm that the expected configurations were rendered by checking the files created in the `configs` directory.

```
#02_csr1_snmp.cfg
snmp-server community public  RO
snmp-server community ntc-course  RO
snmp-server community private  RW
snmp-server community ntc-private  RW
snmp-server location NYC
snmp-server contact netops_team


#02_vmx7_snmp.cfg 
set snmp community public authorization read-only
set snmp community ntc-course authorization read-only
set snmp community private authorization read-write
set snmp community ntc-private authorization read-write
set snmp location MILAN
set snmp contact netops_team

```

##### Step 6

Modify both templates to iterate over the `snmp.ro` and `snmp.rw` lists directly.

``` yaml
{% for ro_comm in snmp.ro %}
snmp-server community {{ ro_comm }}  RO
{% endfor %}
{% for rw_comm in snmp.rw %}
snmp-server community {{ rw_comm }}  RW
{% endfor %}
snmp-server location {{ snmp.location }}
snmp-server contact {{ snmp.contact }}

```
This avoids the need to assign the lists to a new variable and subsequently iterating over it.

##### Step 7

Re-run the playbook to confirm that the updated templates produce the same resulting configuration files.

``` 
ntc@ntc:ansible$ ansible-playbook render_snmp.yaml -i inventory  

PLAY [RENDER SNMP CONFIGS USING JINJA2 - AMERICAS] **********************************************************************

TASK [RENDER IOS SNMP CONFIGURATIONS] ***********************************************************************************
ok: [csr3]
ok: [csr2]
ok: [csr1]

PLAY [RENDER SNMP CONFIGS USING JINJA2 - EMEA] **************************************************************************

TASK [RENDER JUNOS SNMP CONFIGURATIONS] *********************************************************************************
ok: [vmx8]
ok: [vmx9]
ok: [vmx7]

PLAY RECAP **************************************************************************************************************
csr1                       : ok=1    changed=0    unreachable=0    failed=0   
csr2                       : ok=1    changed=0    unreachable=0    failed=0   
csr3                       : ok=1    changed=0    unreachable=0    failed=0   
vmx7                       : ok=1    changed=0    unreachable=0    failed=0   
vmx8                       : ok=1    changed=0    unreachable=0    failed=0   
vmx9                       : ok=1    changed=0    unreachable=0    failed=0   

ntc@ntc:ansible$ 

```

### Task 3 - Using run once

Ansible has an option that lets you run a task just once. This is extremely useful when you want to execute some task that is needed on the control machine - such as creating a directory structure or updating a file locally.

This allows you to avoid redoing the same task for every device in the inventory. 

##### Step 1

Add a new task to the `render_snmp.yaml` file that creates a regional sub-directory within the `configs` directory that will contain the region specific configurations. 

Add this task as the first task to PLAY 1
```yaml
  tasks:
    - name: ENSURE THAT A REGION DIR EXISTS
      file: 
        path: ./configs/amer/
        state: directory

```


Also, add an identical task as the first task to PLAY 2

```yaml
  tasks:
    - name: ENSURE THAT A REGION DIR EXISTS
      file: 
        path: ./configs/emea/
        state: directory

```


##### Step 2


Also update the previously existing task to render the configuration to the updated destination.

The playbook will now look like this:

``` yaml
---
- name: RENDER SNMP CONFIGS USING JINJA2 - AMERICAS
  hosts: AMER
  gather_facts: no
  connection: local

  vars:
    snmp:
      ro:
        - public
        - ntc-course
      rw:
        - private
        - ntc-private
      contact: netops_team
      location: NYC


  tasks:
    - name: ENSURE THAT A REGION DIR EXISTS
      file: 
        path: ./configs/amer/
        state: directory
  
    - name: RENDER IOS SNMP CONFIGURATIONS
      template:
        src: 02-ios-snmp.j2
        dest: "./configs/amer/02_{{ inventory_hostname }}_snmp.cfg"

- name: RENDER SNMP CONFIGS USING JINJA2 - EMEA
  hosts: EMEA
  gather_facts: no
  connection: local

  vars:
    snmp:
      ro:
        - public
        - ntc-course
      rw:
        - private
        - ntc-private
      contact: netops_team
      location: MILAN


  tasks:
    - name: ENSURE THAT A REGION DIR EXISTS
      file: 
        path: ./configs/emea/
        state: directory
  

    - name: RENDER JUNOS SNMP CONFIGURATIONS
      template:
        src: 02-junos-snmp.j2
        dest: "./configs/emea/02_{{ inventory_hostname }}_snmp.cfg"       
        
```

##### Step 3

Each of the tasks will be executed against every host referenced in the `hosts` directive of the plays. Run this playbook as is.


```
ntc@ntc:ansible$ ansible-playbook -i inventory render_snmp.yaml 

PLAY [RENDER SNMP CONFIGS USING JINJA2 - AMERICAS] **********************************************************************

TASK [ENSURE THAT A REGION DIR EXISTS] **********************************************************************************
changed: [csr3]
ok: [csr2]
ok: [csr1]

TASK [RENDER IOS SNMP CONFIGURATIONS] ***********************************************************************************
changed: [csr2]
changed: [csr3]
changed: [csr1]

PLAY [RENDER SNMP CONFIGS USING JINJA2 - EMEA] **************************************************************************

TASK [ENSURE THAT A REGION DIR EXISTS] **********************************************************************************
changed: [vmx8]
ok: [vmx9]
ok: [vmx7]

TASK [RENDER JUNOS SNMP CONFIGURATIONS] *********************************************************************************
changed: [vmx7]
changed: [vmx9]
changed: [vmx8]

PLAY RECAP **************************************************************************************************************
csr1                       : ok=2    changed=1    unreachable=0    failed=0   
csr2                       : ok=2    changed=1    unreachable=0    failed=0   
csr3                       : ok=2    changed=2    unreachable=0    failed=0   
vmx7                       : ok=2    changed=1    unreachable=0    failed=0   
vmx8                       : ok=2    changed=2    unreachable=0    failed=0   
vmx9                       : ok=2    changed=1    unreachable=0    failed=0   

ntc@ntc:ansible$ 

```

Observe the first task in each play. You can see that the directory creation occurred when the task ran for `csr3` in the output example above. Subsequent invocation of that same task for the rest of the devices resulted in no change.

This fact is also emphasized by the `PLAY RECAP`, wher you can see the count for the `changed` being 2 only for `csr3` and `vmx8` in the above example.


##### Step 4

Update Task1 in each play to only run once. 


``` yaml
# For PLAY 1

  tasks:
    - name: ENSURE THAT A REGION DIR EXISTS
      file: 
        path: ./configs/amer/
        state: directory
      run_once: yes


# For PLAY 2
  tasks:
    - name: ENSURE THAT A REGION DIR EXISTS
      file: 
        path: ./configs/emea/
        state: directory
      run_once: yes

```



##### Step 5

Now, rerun the playbook and observe task1.

``` 
ntc@ntc:ansible$ ansible-playbook -i inventory render_snmp.yaml 

PLAY [RENDER SNMP CONFIGS USING JINJA2 - AMERICAS] **********************************************************************

TASK [ENSURE THAT A REGION DIR EXISTS] **********************************************************************************
ok: [csr1]

TASK [RENDER IOS SNMP CONFIGURATIONS] ***********************************************************************************
ok: [csr3]
ok: [csr1]
ok: [csr2]

PLAY [RENDER SNMP CONFIGS USING JINJA2 - EMEA] **************************************************************************

TASK [ENSURE THAT A REGION DIR EXISTS] **********************************************************************************
ok: [vmx7]

TASK [RENDER JUNOS SNMP CONFIGURATIONS] *********************************************************************************
ok: [vmx9]
ok: [vmx7]
ok: [vmx8]

PLAY RECAP **************************************************************************************************************
csr1                       : ok=2    changed=0    unreachable=0    failed=0   
csr2                       : ok=1    changed=0    unreachable=0    failed=0   
csr3                       : ok=1    changed=0    unreachable=0    failed=0   
vmx7                       : ok=2    changed=0    unreachable=0    failed=0   
vmx8                       : ok=1    changed=0    unreachable=0    failed=0   
vmx9                       : ok=1    changed=0    unreachable=0    failed=0   

ntc@ntc:ansible$ 

```

This time, you can see that Task 1 for PLAY 1 and 2 was executed just once.


### Task 4 - Move the vars to `group_vars` directory.

##### Step 1

Create a directory called `group_vars` under `ansible` and within that directory, create the directories `AMER` and `EMEA`


```
ntc@ntc:ansible$ mkdir group_vars
ntc@ntc:ansible$ cd group_vars
ntc@ntc:group_vars$ mkdir AMER
ntc@ntc:group_vars$ mkdir EMEA

```



##### Step 2

Create a file called `snmp_vars.yaml` inside `EMEA` and `AMER` directories

```
ntc@ntc:group_vars$ touch AMER/snmp_vars.yaml
ntc@ntc:group_vars$ touch EMEA/snmp_vars.yaml

```


The directory structure looks as follows:

```
├── group_vars
│   ├── AMER
│   │   └── snmp_vars.yaml
│   └── EMEA
│       └── snmp_vars.yaml

```

##### Step 3

Open the `render_snmp.yaml` file in a text editor. Also open the `AMER/snmp_vars.yaml` file in another terminal or tab of the text editor.

Remove the following `vars` definition from PLAY 1.


``` yaml
  vars:
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

##### Step 4

Add the `snmp` variable into the `AMER/snmp_vars.yaml` file.


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

##### Step 5

Repeat step 2 for the second PLAY. This time, remove the `vars` variable from PLAY 2. And move the `snmp` variable to the `EMEA/snmp_vars.yaml` file.


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

##### Step 6

At this point, the playbook should look as follows:


``` yaml
---
- name: RENDER SNMP CONFIGS USING JINJA2 - AMERICAS
  hosts: AMER
  gather_facts: no
  connection: local

  tasks:
    - name: ENSURE THAT A REGION DIR EXISTS
      file: 
        path: ./configs/amer/
        state: directory
  
    - name: RENDER IOS SNMP CONFIGURATIONS
      template:
        src: 02-ios-snmp.j2
        dest: "./configs/amer/02_{{ inventory_hostname }}_snmp.cfg"

- name: RENDER SNMP CONFIGS USING JINJA2 - EMEA
  hosts: EMEA
  gather_facts: no
  connection: local


  tasks:
    - name: ENSURE THAT A REGION DIR EXISTS
      file: 
        path: ./configs/emea/
        state: directory
  

    - name: RENDER JUNOS SNMP CONFIGURATIONS
      template:
        src: 02-junos-snmp.j2
        dest: "./configs/emea/02_{{ inventory_hostname }}_snmp.cfg"       
        
```

We have thus improved the readability of our playbook, while at the same time, made it convenient to add or modify variables and values to our playbook by using the `group_vars` directory.


##### Step 7

Now run the playbook as follows and confirm that the configurations are rendered correctly as before.

```
ntc@ntc:ansible$ ansible-playbook -i inventory render_snmp.yaml 

PLAY [RENDER SNMP CONFIGS USING JINJA2 - AMERICAS] **********************************************************************

TASK [ENSURE THAT A REGION DIR EXISTS] **********************************************************************************
ok: [csr1]

TASK [RENDER IOS SNMP CONFIGURATIONS] ***********************************************************************************
ok: [csr3]
ok: [csr1]
ok: [csr2]

PLAY [RENDER SNMP CONFIGS USING JINJA2 - EMEA] **************************************************************************

TASK [ENSURE THAT A REGION DIR EXISTS] **********************************************************************************
ok: [vmx7]

TASK [RENDER JUNOS SNMP CONFIGURATIONS] *********************************************************************************
ok: [vmx7]
ok: [vmx8]
ok: [vmx9]

PLAY RECAP **************************************************************************************************************
csr1                       : ok=2    changed=0    unreachable=0    failed=0   
csr2                       : ok=1    changed=0    unreachable=0    failed=0   
csr3                       : ok=1    changed=0    unreachable=0    failed=0   
vmx7                       : ok=2    changed=0    unreachable=0    failed=0   
vmx8                       : ok=1    changed=0    unreachable=0    failed=0   
vmx9                       : ok=1    changed=0    unreachable=0    failed=0   


```

##### Task 5 - Deploy the configuration

Rather than render the configurations locally to the `configs` directory and then pushing to the devices. You can directly pass in the jinja2 template, to the `_config` (ios or junos_config) module to render and push the configuration in one task.


##### Step 1

Create a `provider` variable to login to the devices. Touch a file named `login_vars.yaml` under `group_vars/all.yaml` and open it with an editor. Add the following login info into it.

``` yaml

provider:
  username: "{{ un }}"
  password: "{{ pwd }}"
  host: "{{ inventory_hostname }}"

```

>Since we are creating this variable in the `all.yaml` file, it will apply to all groups.



##### Step 2

Open the `render_snmp.yaml` file using a text editor. Since we no longer need to render the configurations locally, go ahead and remove both the tasks from PLAY 1 and 2.


##### Step 3

Add a new task under PLAY 1, that uses the `ios_config` module to render and push the configurations.


``` yaml
  tasks:
    - name: ENSURE THAT SNMP IS CONFIGURED ON AMER DEVICES
      ios_config:
        src: 02-ios-snmp.j2
        provider: "{{ provider }}"

```


##### Step 4

Similarly under PLAY 2, create a task that uses `junos_config` to render the template and push to the EMEA devices.


``` yaml
  tasks:
    - name: ENSURE THAT SNMP IS CONFIGURED ON AMER DEVICES
      junos_config:
        src: 02-ios-snmp.j2
        provider: "{{ provider }}"

```


##### Step 5

At this point, the entire playbook should look as follows:

``` yaml
---
- name: RENDER SNMP CONFIGS USING JINJA2 - AMERICAS
  hosts: AMER
  gather_facts: no
  connection: local

  tasks:
    - name: ENSURE THAT SNMP IS CONFIGURED ON AMER DEVICES
      ios_config:
        src: 02-ios-snmp.j2
        provider: "{{ provider }}"

- name: RENDER SNMP CONFIGS USING JINJA2 - EMEA
  hosts: EMEA
  gather_facts: no
  connection: local

  tasks:
    - name: ENSURE THAT SNMP IS CONFIGURED ON EMEA DEVICES
      junos_config:
        src: 02-junos-snmp.j2
        provider: "{{ provider }}"


```

##### Step 6

Finally run the playbook as follows:

```
ntc@ntc:ansible$ ansible-playbook -i inventory render_snmp.yaml

PLAY [RENDER SNMP CONFIGS USING JINJA2 - AMERICAS] **********************************************************************

TASK [ENSURE THAT SNMP IS CONFIGURED ON AMER DEVICES] *******************************************************************
changed: [csr1]
changed: [csr2]
changed: [csr3]

PLAY [RENDER SNMP CONFIGS USING JINJA2 - EMEA] **************************************************************************

TASK [ENSURE THAT SNMP IS CONFIGURED ON EMEA DEVICES] *******************************************************************
changed: [vmx7]
changed: [vmx8]
changed: [vmx9]

PLAY RECAP **************************************************************************************************************
csr1                       : ok=1    changed=1    unreachable=0    failed=0   
csr2                       : ok=1    changed=1    unreachable=0    failed=0   
csr3                       : ok=1    changed=1    unreachable=0    failed=0   
vmx7                       : ok=1    changed=1    unreachable=0    failed=0   
vmx8                       : ok=1    changed=1    unreachable=0    failed=0   
vmx9                       : ok=1    changed=1    unreachable=0    failed=0   


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
