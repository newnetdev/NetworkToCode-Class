## Lab 8 - Using Improved Jinja2 Templates

### Task 1 - Updating the SNMP Data Model
  
In the previous lab, the SNMP data was modeled as a set of invdividual key-value pairs. 
This works for a simple use case, but what if we had to configure multiple read-only and read-write strings?

This task will expand the data structure currently being used by the `AMER` and `EMEA` groups.


##### Step 1

Add the `snmp_config` variable into the `AMER.yml` file and also remove what was currently there from the last lab:


``` yaml
snmp_config:
  ro:
    - public
    - ntc-course
  rw:
    - private
    - ntc-private
  contact: netops_team
  location: NYC

```

Note: Ensure the existing four variables, e.g. `snmp_ro`, `snmp_rw`, `snmp_location`, and `snmp_contact` are no longer in this file.


##### Step 2

Repeat and add the `snmp_config` variable to the `EMEA.yml` file.


``` yaml
snmp_config:
  ro:
    - public
    - ntc-course
  rw:
    - private
    - ntc-private
  contact: netops_team
  location: MILAN


```

Note: Ensure the existing four variables, e.g. `snmp_ro`, `snmp_rw`, `snmp_location`, and `snmp_contact` are no longer in this file.


##### Step 3

But now, since our data model has changed, we need to also update our Jinja2 templates to correctly access the values.

Create a new file called `ios-snmpv2.j2` within the templates directory and open it with a text editor. 
We will use the following template to render the desired configuration.


``` 
{% for ro_comm in snmp_config.ro %}
snmp-server community {{ ro_comm }} RO
{% endfor %}
{% for rw_comm in snmp_config.rw %}
snmp-server community {{ rw_comm }} RW
{% endfor %}
snmp-server location {{ snmp_config.location }}
snmp-server contact {{ snmp_config.contact }}

```


Similarly, create a `junos-snmpv2.j2` template file, using the JUNOS configuration commands.

```
{% for ro_comm in snmp_config.ro %}
set snmp community {{ ro_comm }} authorization read-only
{% endfor %}
{% for rw_comm in snmp_config.rw %}
set snmp community {{ rw_comm }} authorization read-write
{% endfor %}
set snmp location {{ snmp_config.location }}
set snmp contact {{ snmp_config.contact }}

```


##### Step 4


Update the `src` parameter in the template task to point to the new templates that were created in the previous step.

At this point, the playbook should look as follows:

``` yaml
---
- name: GENERATE SNMP CONFIGS USING JINJA2 - AMERICAS
  hosts: AMER
  gather_facts: no

  tasks:
    - name: GENERATE IOS SNMP CONFIGURATIONS
      template:
        src: ios-snmpv2.j2
        dest: "./configs/{{ inventory_hostname }}-snmp.cfg"

- name: GENERATE SNMP CONFIGS USING JINJA2 - EMEA
  hosts: EMEA
  gather_facts: no

  tasks:
    - name: GENERATE JUNOS SNMP CONFIGURATIONS
      template:
        src: junos-snmpv2.j2
        dest: "./configs/{{ inventory_hostname }}-snmp.cfg"


```

##### Step 5

Now run the playbook.

```
ntc@ntc:ansible$ ansible-playbook -i inventory deploy-snmp.yaml 
```


##### Step 6

Validate that all device configurations are correct in the `configs` sub-directory.



### Task 2 - Managing Unique Devices
  
In the last task, you built configurations for all `AMER` devices (all CSRs) and for all `EMEA` devices (all vMXs).  In this task, you need to account for a one-off device that requires a different SNMP configuration than what has been defined in the `group_vars` directory.


##### Step 1

Create a new directory called `host_vars`.  

The name of the directory called `host_vars` is an important name within Ansible, just like you've seen with `group_vars`.  This directory will store "host based variables" - these map directly to a host that is found in the inventory file.  For example, the variables that end up in `host_vars/nxos-spine1.yml` will only be used and available to **nxos-spine1**.

##### Step 2

In the `host_vars` directory, create one `host_vars` file, called `csr3.yml`.  This is the device that requires a special configuration for SNMP.

##### Step 3

Add the following `snmp_config` variable into the `csr3.yml` file.

``` yaml
snmp_config:
  ro:
    - ntc-public
  rw:
    - private
    - ntc-private
  contact: netdevops_tiger_team
  location: NYC

```

##### Step 4

Now run the playbook.

```
ntc@ntc:ansible$ ansible-playbook -i inventory deploy-snmp.yaml 
```


##### Step 5

Validate that all device configurations are correct in the `configs` sub-directory focusing on **csr3**.  Compare its configuration to **csr1**.

##### Step 6

Add a `debug` statement to *each* play to debug the `snmp_config` variable for each group of devices, e.g. `AMER` and `EMEA`.

```yaml
    - name: DEBUG AND PRINT SNMP VARIABLES
      debug:
        var: snmp_config
```

This should be added for _each_ play.

##### Step 7

Execute the playbook.  

What do you see?  

What kind of data type is `snmp_config`?  

