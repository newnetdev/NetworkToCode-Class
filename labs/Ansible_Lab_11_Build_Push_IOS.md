## Lab 11.2 - Building and Pushing Network Configuration Files

This lab will show how to use Ansible to automate the process of building network configuration files and pushing them to network devices.  

You will take existing configuration files, de-construct them, and then create Jinja2 templates and YAML based variable files.  The templates and variables will be rendered together using the Ansible *template* module to create configuration files.  They will then be pushed to network devices using an open source module from the NAPALM project.

### Task 1 - Create Templates and Variables Files

Your goal is to create 3 configuration files using a single template and a variety of data files (YAML).

##### Step 1

The configuration below is a partial final config from one of the routers, namely *csr1*.  The same configuration needs to be applied across all switches (with the exception of hostname, IP addressing, router-id, etc.).


```
!
ip domain name ntc.com
!
no ip domain lookup
lldp run
cdp run
!
vrf definition MANAGEMENT
 !
 address-family ipv4
 exit-address-family
 !
 address-family ipv6
 exit-address-family
!
!
interface Loopback100
 description OSPF ROUTER ID
 ip address 1.1.1.1 255.255.255.255
 no shutdown
!
interface GigabitEthernet1
 description MANAGEMENT
 vrf forwarding MANAGEMENT
 ip address 10.0.0.51 255.255.255.0
 cdp enable
 no shutdown
!
interface GigabitEthernet2
 description CONNECTS_CSR3
 ip address 10.254.13.1 255.255.255.0
 cdp enable
 no shutdown
!
interface GigabitEthernet3
 shutdown
!
interface GigabitEthernet4
 description CONNECTS_CSR2
 ip address 10.254.12.1 255.255.255.0
 cdp enable
 no shutdown
!
!
router ospf 100
 router-id 1.1.1.1
 log-adjacency-changes
 network 1.1.1.1 0.0.0.0 area 0.0.0.0
 network 10.254.13.1 0.0.0.0 area 0.0.0.0
 network 10.254.12.1 0.0.0.0 area 0.0.0.0
!
ip route vrf MANAGEMENT 0.0.0.0 0.0.0.0 10.0.0.2
!
!
snmp-server community networktocode RO
snmp-server location NYC_NY_DC1
snmp-server contact NETWORK_ADMIN
!
!
end

```

Your job is to now create a single template and the associated groups vars and host vars files required to generate the require configuration files.


##### Step 2

Create a file called `csr-ospf.j2` in the `templates` directory and open it. It will serve as the template for the switches.

##### Step 3

Open the `all.yml` file created in the previous lab under the `group_vars` directory and ensure you have both `csr-ospf.j2` and `all.yml` open in your text editor.

Now, we will start to break down the configuration file into a series of Jinja2 template snippets and variables.

We'll break this down into sections in order to create the appropriate template file.

> **For real-world use, consider using different template files per service (per section of the configuration) as reviewed in the course.**

First we'll look at this snippet going top down from the partial configuration file:

```
!
ip domain name ntc.com
!
no ip domain lookup
lldp run
cdp run
!
vrf definition MANAGEMENT
 !
 address-family ipv4
 exit-address-family
 !
 address-family ipv6
 exit-address-family
!
```

There are always multiple ways to build a template for a given configuration file, but for this snippet, we will only be modifying the domain configuration and the cdp/lldp configuration.  The VRF definition will remain static as it should always be configured on the routers.

##### Step 4

Take the template snippet and put it into the `csr-ospf.j2` file.

```
!
ip domain name {{ domain_name }}
!
{% for feature in features %}
{% if feature.enabled %}
{{ feature.cmd }}
{% else %}
no {{ feature.cmd }}
{% endif %}
{% endfor %}
!
vrf definition MANAGEMENT
 !
 address-family ipv4
 exit-address-family
 !
 address-family ipv6
 exit-address-family
!
```

As you can see, all that is required is to substitute the proper values using double curly braces around your new variable name.  Pretty easy as you can see for the `domain_name`.

We also show an option for enabling/disabling features using a list of dictionaries.  We also could have done each feature separately too.

The snippet above *templated* a few features and the domain name.  The following lines designate the changes made to the file:

We now need to do something with the original configuration parameters for features.

##### Step 5

Within the `group_vars/all.yml`  file, you need to store the values you just removed from the config file (now the template).  Take the snippet and store it in `all.yml` in `group_vars`

Variables Snippet (`group_vars/all.yml`):

```yaml

---

config:
  eos: show run
  ios: show run
  nxos: show run
  junos: show config
connection_details:
  username: "{{ ansible_user }}"
  password: "{{ ansible_ssh_pass }}"
  host: "{{ inventory_hostname }}"

# other existing variables
# new ones for this task...

domain_name: ntc.com

features:
  - cmd: ip domain lookup
    enabled: false 
  - cmd: lldp run
    enabled: true
  - cmd: cdp run
    enabled: true


```

You're starting to de-couple the inputs from the underlying CLI syntax.  You can now version control each and just make changes to your vars files going forward.

As you can see, if you need to enable more global features on the switch, all you have to do now is modify the list called `features` in `all.yml`.  Of course, this model assumes `no` is used to remove the command, but this is why making templates could be fun (and tedious!).

##### Step 6

Next up are the interfaces.

This is the next section we'll template:

```
!
interface Loopback100
 description OSPF ROUTER ID
 ip address 1.1.1.1 255.255.255.255
 no shutdown
!
interface GigabitEthernet1
 description MANAGEMENT
 vrf forwarding MANAGEMENT
 ip address 10.0.0.51 255.255.255.0
 cdp enable
 no shutdown
!
interface GigabitEthernet2
 description CONNECTS_CSR3
 ip address 10.254.13.1 255.255.255.0
 cdp enable
 no shutdown
!
interface GigabitEthernet3
 shutdown
!
interface GigabitEthernet4
 description CONNECTS_CSR2
 ip address 10.254.12.1 255.255.255.0
 cdp enable
 no shutdown
!
```

Anything that repeats itself should be screaming "use a loop" for me!  We can reduce the interfaces down to a single for loop.  We will use a loop that will  iterate through a list of dictionaries.  

This time, we'll create the variables files first.

Create the variables (list of dictionaries) for the interfaces.  Remember, it needs to be done on a per-device basis because the IP addresses used per device are different for every device (think group_vars vs. host_vars).

Create a new directory called `host_vars` also in the `ansible` directory.

Now create three new files in the `host_vars` directory - one per device.  These files need to be named `csr1.yml`, `csr2.yml`, and `csr3.yml` because those are the names we gave them in the inventory file.

File: `host_vars/csr1.yml`

```yaml
---

interfaces:
  - name: Loopback100
    state: up
    ip: 1.1.1.2
    mask: 255.255.255.255
    description: OSPF ROUTER ID
  - name: GigabitEthernet1
    state: up
    ip: 10.0.0.51
    mask: 255.255.255.0
    description: MANAGEMENT
    cdp: true
    vrf: MANAGEMENT
  - name: GigabitEthernet2
    state: up
    ip: 10.254.13.1
    mask: 255.255.255.0
    description: CONNECTS_CSR3
    cdp: true
  - name: GigabitEthernet3
    state: down
    cdp: false
  - name: GigabitEthernet4
    state: up
    ip: 10.254.12.1
    mask: 255.255.255.0
    description: CONNECTS_CSR2
    cdp: true
```


File: `host_vars/csr2.yml`

```yaml
interfaces:
  - name: Loopback100
    state: up
    ip: 2.2.2.2
    mask: 255.255.255.255
    description: OSPF ROUTER ID
  - name: GigabitEthernet1
    state: up
    ip: 10.0.0.52
    mask: 255.255.255.0
    description: MANAGEMENT
    cdp: true
    vrf: MANAGEMENT
  - name: GigabitEthernet2
    state: down
    cdp: false
  - name: GigabitEthernet3
    state: up
    ip: 10.254.12.2
    mask: 255.255.255.0
    description: CONNECTS_CSR3
    cdp: true
  - name: GigabitEthernet4
    state: up
    ip: 10.254.23.2
    mask: 255.255.255.0
    description: CONNECTS_CSR2
    cdp: true

```


File: `host_vars/csr3.yml`

Notice the different syntax that can be used for a list of dictionaries.

```yaml
interfaces:
  - name: Loopback100
    state: up
    ip: 3.3.3.3
    mask: 255.255.255.255
    description: OSPF ROUTER ID
  - name: GigabitEthernet1
    state: up
    ip: 10.0.0.53
    mask: 255.255.255.0
    description: MANAGEMENT
    cdp: true
    vrf: MANAGEMENT
  - name: GigabitEthernet2
    state: up
    ip: 10.254.13.3
    mask: 255.255.255.0
    description: CONNECTS_CSR3
    cdp: true
  - name: GigabitEthernet3
    state: up
    ip: 10.254.23.3
    mask: 255.255.255.0
    description: CONNECTS_CSR2
    cdp: true 
  - name: GigabitEthernet4
    state: down
    cdp: false
```


##### Step 7

Add the associated template snippet to the `templates/csr-ospf.j2` template.

Please take a few minutes to go through this snippet slowly and look at the vars files simultaneously.

```
!
{% for interface in interfaces %}
interface {{ interface.name }}
{% if interface.get('description') %}
 description {{ interface.description }}
{% endif %}
{% if interface.get('vrf') %}
 vrf forwarding {{ interface.vrf }}
{% endif %}
{% if interface.get('ip') %}
 ip address {{ interface.get('ip') }} {{ interface.get('mask') }}
{% endif %}
{% if interface.get('cdp') %}
 cdp enable
{% endif %}
{% if interface.get('state') == "up" %}
 no shutdown
{% elif interface.get('state') == "down" %}
 shutdown
{% endif %}
!
{% endfor %}
!
```


##### Step 8

The last section that needs to be templated is this:

```
!
router ospf 100
 router-id 1.1.1.1
 log-adjacency-changes
 network 1.1.1.1 0.0.0.0 area 0.0.0.0
 network 10.254.13.1 0.0.0.0 area 0.0.0.0
 network 10.254.12.1 0.0.0.0 area 0.0.0.0
!
ip route vrf MANAGEMENT 0.0.0.0 0.0.0.0 10.0.0.2
!
!
snmp-server community networktocode RO
snmp-server location NYC_NY_DC1
snmp-server contact NETWORK_ADMIN
!
!
end
```

There are a few parameters that will be the same for each router such as OSPF instance tag (or process ID), enabling log-adjacency-changes, the static route, and SNMP settings, but there are also a few parameters that need to be different per device such as the router ID and interfaces that will have OSPF enabled on.  

Make the appropriate changes to the host vars files, and group vars `all.yml` file.  The text below is only showing what should be added to each vars file.

File: `group_vars/all.yml`

```yaml

domain_name: ntc.com

features:
  - cmd: ip domain lookup
    enabled: false 
  - cmd: lldp run
    enabled: true
  - cmd: cdp run
    enabled: true

ospf:
  instance_tag: 100
  area: 0.0.0.0
  log_adj: true

mgmt_default_route_next_hop: 10.0.0.2

snmp:
  ro_comm: networktocode
  location: NYC_NY_DC1
  contact: NETWORK_ADMIN

```


File: `host_vars/csr1.yml`

```yaml
router_id: 1.1.1.1

ospf_interfaces:
  - GigabitEthernet2
  - GigabitEthernet4
  - Loopback100

```


File: `host_vars/csr2.yml`

```yaml
router_id: 2.2.2.2

ospf_interfaces:
  - GigabitEthernet3
  - GigabitEthernet4
  - Loopback100

```


File: `host_vars/csr3.yml`

```yaml
router_id: 3.3.3.3

ospf_interfaces:
  - GigabitEthernet2
  - GigabitEthernet3
  - Loopback100

```


##### Step 9


Finally, this is last snippet to be added into the template:

```
router ospf {{ ospf.instance_tag }}
 router-id {{ router_id }}
{% if ospf.log_adj %}
 log-adjacency-changes
{% endif %}
{% for interface in interfaces %}
{% if interface.name in ospf_interfaces %}
 network {{ interface.get('ip')}} 0.0.0.0 area {{ ospf.area }}
{% endif %}
{% endfor %}
!
ip route vrf MANAGEMENT 0.0.0.0 0.0.0.0 {{ mgmt_default_route_next_hop }}
!
!
snmp-server community {{ snmp.ro_comm }} RO
snmp-server location {{ snmp.location }}
snmp-server contact {{ snmp.contact }}
!
!
end
```

Again, review this template with the vars files from the previous step to ensure you understand the logic and Jinja2 syntax.

Note:  Please note that there isn't a right or wrong way to create templates.  You have to find what works for you and your team, for your configuration.  

For the configuration per interface, you need to see what type of requirements you have in the given environment.  For the config snippet here, we have a few basic parameters to worry about including state (shut or no shut), mode (routed or access), and OSPF parameters, but as you know, there can be many more parameters configured on an interface.

##### Step 10

Status Check.

At this point, you should have created the following template and variables files:

TEMPLATE (`templates/csr-ospf.j2`):

```
!
ip domain name {{ domain_name }}
!
{% for feature in features %}
{% if feature.enabled %}
{{ feature.cmd }}
{% else %}
no {{ feature.cmd }}
{% endif %}
{% endfor %}
!
vrf definition MANAGEMENT
 !
 address-family ipv4
 exit-address-family
 !
 address-family ipv6
 exit-address-family
!
!
{% for interface in interfaces %}
interface {{ interface.name }}
{% if interface.get('description') %}
 description {{ interface.description }}
{% endif %}
{% if interface.get('vrf') %}
 vrf forwarding {{ interface.vrf }}
{% endif %}
{% if interface.get('ip') %}
 ip address {{ interface.get('ip') }} {{ interface.get('mask') }}
{% endif %}
{% if interface.get('cdp') %}
 cdp enable
{% endif %}
{% if interface.get('state') == "up" %}
 no shutdown
{% elif interface.get('state') == "down" %}
 shutdown
{% endif %}
!
{% endfor %}
!
router ospf {{ ospf.instance_tag }}
 router-id {{ router_id }}
{% if ospf.log_adj %}
 log-adjacency-changes
{% endif %}
{% for interface in interfaces %}
{% if interface.name in ospf_interfaces %}
 network {{ interface.get('ip')}} 0.0.0.0 area {{ ospf.area }}
{% endif %}
{% endfor %}
!
ip route vrf MANAGEMENT 0.0.0.0 0.0.0.0 {{ mgmt_default_route_next_hop }}
!
!
snmp-server community {{ snmp.ro_comm }} RO
snmp-server location {{ snmp.location }}
snmp-server contact {{ snmp.contact }}
!
!
end
```

VARS FILES:

`group_vars/all.yml`:

```yaml
---

# Possible other content from previous labs

domain_name: ntc.com

features:
  - cmd: ip domain lookup
    enabled: false 
  - cmd: lldp run
    enabled: true
  - cmd: cdp run
    enabled: true

ospf:
  instance_tag: 100
  area: 0.0.0.0
  log_adj: true

mgmt_default_route_next_hop: 10.0.0.2

snmp:
  ro_comm: networktocode
  location: NYC_NY_DC1
  contact: NETWORK_ADMIN

```


`host_vars/csr1.yml`

```yaml
---

# Possible other content from previous labs

interfaces:
  - name: Loopback100
    state: up
    ip: 1.1.1.2
    mask: 255.255.255.255
    description: OSPF ROUTER ID
  - name: GigabitEthernet1
    state: up
    ip: 10.0.0.51
    mask: 255.255.255.0
    description: MANAGEMENT
    cdp: true
    vrf: MANAGEMENT
  - name: GigabitEthernet2
    state: up
    ip: 10.254.13.1
    mask: 255.255.255.0
    description: CONNECTS_CSR3
    cdp: true
  - name: GigabitEthernet3
    state: down
    cdp: false
  - name: GigabitEthernet4
    state: up
    ip: 10.254.12.1
    mask: 255.255.255.0
    description: CONNECTS_CSR2
    cdp: true

router_id: 1.1.1.1

ospf_interfaces:
  - GigabitEthernet2
  - GigabitEthernet4
  - Loopback100


```

`host_vars/csr2.yml`

```yaml
---

# Possible other content from previous labs

interfaces:
  - name: Loopback100
    state: up
    ip: 2.2.2.2
    mask: 255.255.255.255
    description: OSPF ROUTER ID
  - name: GigabitEthernet1
    state: up
    ip: 10.0.0.52
    mask: 255.255.255.0
    description: MANAGEMENT
    cdp: true
    vrf: MANAGEMENT
  - name: GigabitEthernet2
    state: down
    cdp: false
  - name: GigabitEthernet3
    state: up
    ip: 10.254.12.2
    mask: 255.255.255.0
    description: CONNECTS_CSR3
    cdp: true
  - name: GigabitEthernet4
    state: up
    ip: 10.254.23.2
    mask: 255.255.255.0
    description: CONNECTS_CSR2
    cdp: true


router_id: 2.2.2.2

ospf_interfaces:
  - GigabitEthernet3
  - GigabitEthernet4
  - Loopback100

```

`host_vars/csr3.yml`

```yaml
---

# Possible other content from previous labs

interfaces:
  - name: Loopback100
    state: up
    ip: 3.3.3.3
    mask: 255.255.255.255
    description: OSPF ROUTER ID
  - name: GigabitEthernet1
    state: up
    ip: 10.0.0.53
    mask: 255.255.255.0
    description: MANAGEMENT
    cdp: true
    vrf: MANAGEMENT
  - name: GigabitEthernet2
    state: up
    ip: 10.254.13.3
    mask: 255.255.255.0
    description: CONNECTS_CSR3
    cdp: true
  - name: GigabitEthernet3
    state: up
    ip: 10.254.23.3
    mask: 255.255.255.0
    description: CONNECTS_CSR2
    cdp: true 
  - name: GigabitEthernet4
    state: down
    cdp: false

router_id: 3.3.3.3

ospf_interfaces:
  - GigabitEthernet2
  - GigabitEthernet3
  - Loopback100

```


##### Step 11

Once the new configurations are generated from the template and vars file, they need to be stored somewhere.  

We will store them in the directory called `configs`.

Create a new sub-directory if you don't already have it called `configs` within your `ansible` directory.

### Task 2 - Building the Configurations

It's time to create the playbook that will auto-generate all of the configuration files.

##### Step 1

Create and open a file called `build-push.yml`.

Save it in the `ansible` directory.

The playbook will consist of a single play and a single task.  The task will use the "template" module.

Two parameters will be passed to the module:  `src` which is the source template, i.e. `csr-ospf.j2` and the `dest`, which is the where the final rendered config file will be stored.

This play should be limited to the `iosxe` group in the inventory file, so use the `hosts: iosxe` in the play definition.

```yaml
---

  - name: Build & Deploy IOS Configurations
    hosts: iosxe
    gather_facts: no

    tasks:
      - name: BUILD CONFIGS
        template:
          src: csr-ospf.j2
          dest: ./configs/{{ inventory_hostname }}.cfg
        tags: build

```

> Note: we are using the variable `inventory_hostname` in the value for the `dest` parameter.  This will make a file with the name of the device as it is defined in the inventory file.


##### Step 2

Save the playbook (don't close it) and go back to the Linux command line.

Execute the playbook using the following command:

```
ntc@ntc:ansible$ ansible-playbook -i inventory build-push.yml
```

You will see the following output during execution:

```
ntc@ntc:ansible$ ansible-playbook -i inventory build-push.yml

PLAY [Build Configuration Files] **********************************************

TASK: [BUILD CONFIGS] *********************************************************
changed: [csr1]
changed: [csr3]
changed: [csr2]

PLAY RECAP ********************************************************************
csr1                       : ok=1    changed=1    unreachable=0    failed=0   
csr2                       : ok=1    changed=1    unreachable=0    failed=0   
csr3                       : ok=1    changed=1    unreachable=0    failed=0   

```

##### Step 3

Check to make sure your new configs in the `configs` directory were generated properly.

You should understand that the template was *rendered* with multiple variables (including all of the host vars and group vars) that you defined.

### Task 3 - Pushing the Configurations

Now that the configs are built, they are ready to be deployed.

##### Step 1

Review details on the module that will be used to push the configurations.

This module that'll be used to push the configurations is called **napalm_install_config**.

This module is a multi-vendor module supporting vendors such as Arista, Cisco IOS, Cisco Nexus, Cisco IOS-XR, Juniper, and many more.  It has the ability to automatically apply a configuration and make it the device's active running configuration.  By using this module, we will apply the configurations generated in the previous task.

The following parameters will be used for the napalm_install_config module (as shown below):
  - `hostname`: this is the IP / FQDN of the node you are automating.  We are using the IP from the inventory file
  - `username`: to login to the switch
  - `password`: to login to the switch
  - `dev_os`: platform of the target node
  - `provider`: wrapper for any other parameter supported (dict)
  - `config_file`: that will be sent and applied to the device.  Notice how we are using a variable to push the correct file.
  - `diff_file`: A path to the file where we store the "diff" between the running configuration and the new configuration.
  - `commit_changes`: if true, they will be applied (it's possible not to apply and just generate diffs)
  - `replace_config`: it's possible to do a replace/overwrite or a merge.  We are doing a merge.


> Also take notice of the `tags` attribute below in the last line of the playbook.  This will allow us to run just this task from the terminal.

##### Step 2

Add the following task to the `build-push.yml` playbook:

```yaml
---

  - name: Build & Deploy IOS Configurations
    hosts: iosxe
    gather_facts: no

    tasks:
      - name: BUILD CONFIGS
        template:
          src: csr-ospf.j2
          dest: ./configs/{{ inventory_hostname }}.cfg
        tags: build

      - name: DEPLOY CONFIGURATIONS
        napalm_install_config:
          provider: "{{ connection_details }}"
          config_file: ./configs/{{ inventory_hostname }}.cfg
          diff_file: ./diffs/{{ inventory_hostname }}.diffs
          replace_config: false
          commit_changes: true
          dev_os: "{{ ansible_network_os }}"
        tags: push


```

**IMPORTANT: ENSURE YOU HAVE THE CORRECT MANAGEMENT IP ADDRESS IN EACH OF THE HOST_VARS FILES.  OTHERWISE, YOU WILL LOSE CONNECTIVITY TO THE DEVICES!!!!**

##### Step 3

Execute ONLY the new task by using tags.

> SSH to one or more of the routers if you want to look at the configs before and after you push the new configs.

Use this command:
```
ntc@ntc:~/ansible$ ansible-playbook -i inventory build-push.yml --tags=push
```


```
ntc@ntc:~/ansible$ ansible-playbook -i inventory build-push.yml --tags=push

PLAY [Build Configuration Files] **********************************************

TASK: [PUSH CONFIGS] **********************************************************
changed: [csr2]
changed: [csr1]
changed: [csr3]

PLAY RECAP ********************************************************************
csr1                       : ok=1    changed=1    unreachable=0    failed=0   
csr2                       : ok=1    changed=1    unreachable=0    failed=0   
csr3                       : ok=1    changed=1    unreachable=0    failed=0  
```

Congratulations!  You just pushed configuration to three routers.

##### Step 4

In order to see the full workflow, delete/remove all of the cfg files from the `configs` directory.

```
ntc@ntc:ansible$ rm configs/*.cfg
```


##### Step 5

Run the playbook without tags:

```
ntc@ntc:~/ansible$ ansible-playbook -i inventory build-push.yml
```

You'll see the configs get built in real-time and then deployed. Once deployed, you should see OSPF adjacencies come up.
