## Lab 11 - Data Collection Modules & Reporting

Network Automation, and automation in general, is often equated with configuring devices faster, but as you've seen by now, it offers greater predictability and more deterministic outcomes.

On top of that, it also offers even great value when it comes to collecting data and reporting.  In these next few tasks, you will use Ansible modules to automate the data collection process and also dynamically generate different types of reports.

### Task 1 - Ansible Core Facts Modules

In the first task, you will use facts modules to gather device information such as OS version, hostname, serial number, neighbors, and IP addresses on the network devices.  The modules you will use in this task are all in Ansible core.  That means they come with Ansible when you install Ansible.

Each module has the name of `<os>_facts`.  

  * For IOS devices, the module is `ios_facts`
  * For NXOS devices, the module is `nxos_facts`
  * For EOS devices, the module is `eos_facts`
  * For Junos devices, the module is `junos_facts`

> Remember, you can use the `ansible-doc` utility on any of these modules to see how to use them and what data will be returned from them.

##### Step 0

Ensure the following providers are created in `group_vars/all.yml`:

```yaml

ios_provider:
  host: "{{ inventory_hostname }}"
  username: "{{ un }}"
  password: "{{ pwd }}"
  
ntc_provider:
  host: "{{ inventory_hostname }}"
  username: "{{ un }}"
  password: "{{ pwd }}"
eos_provider:
  host: "{{ inventory_hostname }}"
  username: "{{ un }}"
  password: "{{ pwd }}"
  transport: eapi
  validate_certs: false

nxos_provider:
  host: "{{ inventory_hostname }}"
  username: "{{ un }}"
  password: "{{ pwd }}"
  transport: nxapi

junos_provider:
  host: "{{ inventory_hostname }}"
  username: "{{ un }}"
  password: "{{ pwd }}"

```

* Ensure LLDP is enabled on the NXOS switches using the `feature lldp`.



##### Step 1

Create a playbook called `core-facts.yml` with a single task to execute against the `iosxe` group of devices.  

In this task in the play, use the `ios_facts` module to gather the device facts.




```yaml
---

  - name: GATHER IOS FACTS
    hosts: iosxe
    connection: local
    gather_facts: no

    tasks:
      - name: GET FACTS
        ios_facts:
          provider: "{{ ios_provider }}"

```

##### Step 2

Execute the playbook.

```
$ ansible-playbook -i inventory core-facts.yml 

PLAY [GATHER IOS FACTS] ********************************************************

TASK [GET FACTS] ***************************************************************
ok: [csr3]
ok: [csr2]
ok: [csr1]

PLAY RECAP *********************************************************************
csr1                       : ok=1    changed=0    unreachable=0    failed=0   
csr2                       : ok=1    changed=0    unreachable=0    failed=0   
csr3                       : ok=1    changed=0    unreachable=0    failed=0   


```

The task ran successfully on all three devices, but how do you see the data being collected?

By now you should know there are two options: (1) use verbose mode (running the playbook with `-v`) and (2) use the `register` task attribute with the `debug` module.

##### Step 3

Re-run the playbook using verbose mode and limit the playbook to just **csr1** to make the viewing of the output a little cleaner.

```
$ ansible-playbook -i inventory core-facts.yml -v --limit csr1

Using /etc/ansible/ansible.cfg as config file

PLAY [GATHER IOS FACTS] ********************************************************

TASK [GET FACTS] ***************************************************************
ok: [csr1] => {"ansible_facts": {"ansible_net_all_ipv4_addresses": ["10.0.0.51"], "ansible_net_all_ipv6_addresses": [], "ansible_net_filesystems": ["bootflash:"], "ansible_net_gather_subset": ["hardware", "default", "interfaces"], "ansible_net_hostname": "csr1", "ansible_net_image": "bootflash:packages.conf", "ansible_net_interfaces": {"GigabitEthernet1": {"bandwidth": 1000000, "description": null, "duplex": "Full", "ipv4": {"address": "10.0.0.51", "masklen": 24}, "lineprotocol": "up ", "macaddress": "2cc2.6009.d3a8", "mediatype": "RJ45", "mtu": 1500, "operstatus": "up", "type": "CSR vNIC"}, "GigabitEthernet2": {"bandwidth": 1000000, "description": null, "duplex": "Full", "ipv4": null, "lineprotocol": "down ", "macaddress": "2cc2.6049.c853", "mediatype": "RJ45", "mtu": 1500, "operstatus": "administratively down", "type": "CSR vNIC"}, "GigabitEthernet3": {"bandwidth": 1000000, "description": null, "duplex": "Full", "ipv4": null, "lineprotocol": "down ", "macaddress": "2cc2.601b.84ef", "mediatype": "RJ45", "mtu": 1500, "operstatus": "administratively down", "type": "CSR vNIC"}, "GigabitEthernet4": {"bandwidth": 1000000, "description": null, "duplex": "Full", "ipv4": null, "lineprotocol": "down ", "macaddress": "2cc2.605b.754f", "mediatype": "RJ45", "mtu": 1500, "operstatus": "administratively down", "type": "CSR vNIC"}}, "ansible_net_memfree_mb": 327297, "ansible_net_memtotal_mb": 2047264, "ansible_net_model": null, "ansible_net_neighbors": {"Gi1": [{"host": "csr2.ntc.com", "port": "Gi1"}, {"host": "eos-leaf1.ntc.com", "port": "Management1"}, {"host": "csr3.ntc.com", "port": "Gi1"}, {"host": "eos-leaf2.ntc.com", "port": "Management1"}, {"host": "eos-spine2.ntc.com", "port": "Management1"}, {"host": "eos-spine1.ntc.com", "port": "Management1"}]}, "ansible_net_serialnum": "9KXI0D7TVFI", "ansible_net_version": "16.3.1"}, "changed": false, "failed_commands": []}

PLAY RECAP *********************************************************************
csr1                       : ok=1    changed=0    unreachable=0    failed=0   


```

Feel free to run it again on all three devices (without using `limit`).


##### Step 4

As you can see using verbose mode doesn't show the data being returned in an easy to read format.  Now add the `register` attribute along with a new task using the `debug` module to print the facts to the terminal when the playbook runs.

Register the return data and use the variable `ntc_ios_facts` to do so.

The updated playbook should look like this:


```yaml
---

  - name: GATHER IOS FACTS
    hosts: iosxe
    connection: local
    gather_facts: no

    tasks:
      - name: GET FACTS
        ios_facts:
          provider: "{{ ios_provider }}"
        register: ntc_ios_facts

      - name: DEBUG FACTS
        debug: var=ntc_ios_facts

```

##### Step 5

Execute the playbook.  This time **not** using verbose mode, but still limiting it to **csr1**.



```
$ ansible-playbook -i inventory core-facts.yml --limit csr1

PLAY [GATHER IOS FACTS] ********************************************************

TASK [GET FACTS] ***************************************************************
ok: [csr1]

TASK [DEBUG FACTS] *************************************************************
ok: [csr1] => {
    "ntc_ios_facts": {
        "ansible_facts": {
            "ansible_net_all_ipv4_addresses": [
                "10.0.0.51"
            ], 
            "ansible_net_all_ipv6_addresses": [], 
            "ansible_net_filesystems": [
                "bootflash:"
            ], 
            "ansible_net_gather_subset": [
                "hardware", 
                "default", 
                "interfaces"
            ], 
            "ansible_net_hostname": "csr1", 
            "ansible_net_image": "bootflash:packages.conf", 
            "ansible_net_interfaces": {
                "GigabitEthernet1": {
                    "bandwidth": 1000000, 
                    "description": null, 
                    "duplex": "Full", 
                    "ipv4": {
                        "address": "10.0.0.51", 
                        "masklen": 24
                    }, 
                    "lineprotocol": "up ", 
                    "macaddress": "2cc2.6009.d3a8", 
                    "mediatype": "RJ45", 
                    "mtu": 1500, 
                    "operstatus": "up", 
                    "type": "CSR vNIC"
                }, 
                "GigabitEthernet2": {
                    "bandwidth": 1000000, 
                    "description": null, 
                    "duplex": "Full", 
                    "ipv4": null, 
                    "lineprotocol": "down ", 
                    "macaddress": "2cc2.6049.c853", 
                    "mediatype": "RJ45", 
                    "mtu": 1500, 
                    "operstatus": "administratively down", 
                    "type": "CSR vNIC"
                }, 
                "GigabitEthernet3": {
                    "bandwidth": 1000000, 
                    "description": null, 
                    "duplex": "Full", 
                    "ipv4": null, 
                    "lineprotocol": "down ", 
                    "macaddress": "2cc2.601b.84ef", 
                    "mediatype": "RJ45", 
                    "mtu": 1500, 
                    "operstatus": "administratively down", 
                    "type": "CSR vNIC"
                }, 
                "GigabitEthernet4": {
                    "bandwidth": 1000000, 
                    "description": null, 
                    "duplex": "Full", 
                    "ipv4": null, 
                    "lineprotocol": "down ", 
                    "macaddress": "2cc2.605b.754f", 
                    "mediatype": "RJ45", 
                    "mtu": 1500, 
                    "operstatus": "administratively down", 
                    "type": "CSR vNIC"
                }
            }, 
            "ansible_net_memfree_mb": 327363, 
            "ansible_net_memtotal_mb": 2047264, 
            "ansible_net_model": null, 
            "ansible_net_neighbors": {
                "Gi1": [
                    {
                        "host": "csr2.ntc.com", 
                        "port": "Gi1"
                    }, 
                    {
                        "host": "eos-leaf1.ntc.com", 
                        "port": "Management1"
                    }, 
                    {
                        "host": "csr3.ntc.com", 
                        "port": "Gi1"
                    }, 
                    {
                        "host": "eos-leaf2.ntc.com", 
                        "port": "Management1"
                    }, 
                    {
                        "host": "eos-spine2.ntc.com", 
                        "port": "Management1"
                    }, 
                    {
                        "host": "eos-spine1.ntc.com", 
                        "port": "Management1"
                    }
                ]
            }, 
            "ansible_net_serialnum": "9KXI0D7TVFI", 
            "ansible_net_version": "16.3.1"
        }, 
        "changed": false, 
        "failed_commands": []
    }
}

PLAY RECAP *********************************************************************
csr1                       : ok=2    changed=0    unreachable=0    failed=0   


```

Feel free to run it again on all three devices.


##### Step 6

Add a new task to just print (debug) the operating system (`ansible_net_version`) of the network devices.

This is the new task that should be added:

```yaml
      - name: DEBUG OS VERSION
        debug: var=ntc_ios_facts['ansible_facts']['ansible_net_version']
```

##### Step 7

Execute the playbook.

The output for the new task will look like this:
```
TASK [DEBUG OS VERSION] ********************************************************
ok: [csr1] => {
    "ntc_ios_facts['ansible_facts']['ansible_net_version']": "16.3.1"
}


```

##### Step 8

Add a new task to print (debug) the operating system of the network devices, but do **NOT** use the registered variable.

This is often very confusing when just learning Ansible, but any _key_ inside `ansible_facts` can be accessed directly.  Let's try it.

**Add** the following task:

```yaml
      - name: DEBUG SHORTHAND OS VERSION
        debug: var=ansible_net_version
```

##### Step 9

Execute the playbook limiting the run to just **csr1**.

The associated new output for the playbook is the following:
```
TASK [DEBUG SHORTHAND OS VERSION] **********************************************
ok: [csr1] => {
    "ansible_net_version": "16.3.1"
}


```

> Note: While you can access facts directly, using the register/debug combination provides an easy way to see exactly what's being collected in that specific task.


##### Step 10

Repeat Steps 1 - 9 for each device type you've been using in the labs.  

**Add a new play for each one.** Tag each play accordingly so you can run them individually.

> Note: Ensure LLDP is enabled on the NXOS switches using the `feature lldp`.

This is a sample playbook for running against IOS, NXOS, and EOS devices:

```yaml
---

  - name: GATHER IOS FACTS
    hosts: iosxe
    connection: local
    gather_facts: no
    tags: ios

    tasks:
      - name: GET FACTS
        ios_facts:
          provider: "{{ ios_provider }}"
        register: ntc_ios_facts

      - name: DEBUG FACTS
        debug: var=ntc_ios_facts

      - name: DEBUG OS VERSION
        debug: var=ntc_ios_facts['ansible_facts']['ansible_net_version']

      - name: DEBUG SHORTHAND OS VERSION
        debug: var=ansible_net_version

  - name: GATHER NXOS FACTS
    hosts: nxos
    connection: local
    gather_facts: no
    tags: nxos

    tasks:
      - name: GET NXOS FACTS
        nxos_facts:
          provider: "{{ nxos_provider }}"
        register: ntc_nxos_facts

      - name: DEBUG FACTS
        debug: var=ntc_nxos_facts

      - name: DEBUG OS VERSION
        debug: var=ntc_nxos_facts['ansible_facts']['ansible_net_version']

      - name: DEBUG SHORTHAND OS VERSION
        debug: var=ansible_net_version

  - name: GATHER EOS FACTS
    hosts: eos
    connection: local
    gather_facts: no
    tags: eos

    tasks:
      - name: GET EOS FACTS
        eos_facts:
          provider: "{{ eos_provider }}"
        register: ntc_eos_facts

      - name: DEBUG FACTS
        debug: var=ntc_eos_facts

      - name: DEBUG OS VERSION
        debug: var=ntc_eos_facts['ansible_facts']['ansible_net_version']

      - name: DEBUG SHORTHAND OS VERSION
        debug: var=ansible_net_version
```


### Task 2 - Using a multi-vendor (NTC) facts module

There are several multi-vendor open source facts module including `napalm_get_facts`,  `ntc_get_facts`, and `snmp_facts`.  In this task, we are going to use `ntc_get_facts`.

##### Step 1

Create a new playbook called `ntc-facts.yml`.  

In a **single task**, gather facts from all devices.

Remember, NTC modules are multi-vendor and support a parameter called `platform`. This parameter gets set to the platform being automated, which should be equal to `<vendor>_<os>_<api>`.

Set the `platform` parameter equal to `{{ vendor }}_{{ os }}_{{ api }}` variable in your task.

> For NXOS and EOS, `api` must be set to "nxapi" and "eapi" respectively.


```yaml
---

  - name: GATHER NTC FACTS
    hosts: all
    connection: local
    gather_facts: no

    tasks:
      - name: GET NTC FACTS
        ntc_get_facts:
          provider: "{{ ntc_provider }}"
          platform: "{{ vendor }}_{{ os }}_{{ api}}"

```

##### Step 2

Execute the playbook in verbose mode.

The output is large, so here is just the command to run the playbook and expected summary:

```
$ ansible-playbook -i inventory ntc-facts.yml -v

< OUTPUT OMITTED; JUST SHOWING SUMMARY PLAY RECAP>

PLAY RECAP *********************************************************************
csr1                       : ok=1    changed=0    unreachable=0    failed=0   
csr2                       : ok=1    changed=0    unreachable=0    failed=0   
csr3                       : ok=1    changed=0    unreachable=0    failed=0   
eos-leaf1                  : ok=1    changed=0    unreachable=0    failed=0   
eos-leaf2                  : ok=1    changed=0    unreachable=0    failed=0   
eos-spine1                 : ok=1    changed=0    unreachable=0    failed=0   
eos-spine2                 : ok=1    changed=0    unreachable=0    failed=0   
nxos-spine1                : ok=1    changed=0    unreachable=0    failed=0   
nxos-spine2                : ok=1    changed=0    unreachable=0    failed=0   


```

##### Step 3

Register the results from the previous task using the variable called `ntc_facts` and debug it to the terminal.

The updated playbook will look like this:

```yaml
---

  - name: GATHER NTC FACTS
    hosts: all
    connection: local
    gather_facts: no

    tasks:
      - name: GET NTC FACTS
        ntc_get_facts:
          provider: "{{ ntc_provider }}"
          platform: "{{ vendor }}_{{ os }}_{{ api}}"
        register: ntc_facts

      - name: DEBUG FACTS
        debug: var=ntc_facts

```

##### Step 4

Execute the playbook NOT using verbose mode.

```
$ ansible-playbook -i  inventory ntc-facts.yml

<OUTPUT OMITTED>
```

##### Step 5

Add two new tasks to debug the `model` key within the facts returned.  First, debug using the registered variable then debug the `model` key directly proving you can always access any key within `ansible_facts` without needing to register. 

```yaml
      - name: DEBUG MODEL
        debug: var=ntc_facts['ansible_facts']['model']

      - name: DEBUG SHORT MODEL
        debug: var=model
```


##### Step 6

Execute the playbook again NOT using verbose mode.

```
$ ansible-playbook -i  ntc-facts.yml
```


At this point, we're still just getting familiar with access facts.  As you progress in this lab, you'll start doing more with the data being returned.


### Task 3 - Parsing Unstructured Data from Devices 

In this task, you will use an open source module by Network to Code that issues "show" commands on network devices and returns structured data back.  It is called `ntc_show_command` and uses "legacy" CLI/SSH to connect to the device, issues CLI commands, **converts the raw text response to JSON**, and then returns that data to Ansible.

> Note: `ntc_show_command` It is a wrapper combining Netmiko and TextFSM (clitable).

[Take note of all of the already-built templates](https://github.com/networktocode/ntc-templates/tree/master/templates)

##### Step 0

**ENSURE YOU HAVE LLDP ENABLED ON THE NEXUS SWITCHES**

Commands to enable LLDP:

```
ssh to nxos-spine1 and nxos-spine2
config t
feature lldp
end
exit
```

##### Step 1

Create a new playbook called `parse-output.yml`.  It should have just one task that is going to issue the command `show lldp neighbors`.

First create a `ntc_provider` variable in your `group_vars/all.yml` file.

```yaml
ntc_provider:
  username: "{{ un }}"
  password: "{{ pwd }}"
  host: "{{ inventory_hostname }}"

```

Ensure you also have the following providers built already as well too:

```yaml
ios_provider:
  username: "{{ un }}"
  password: "{{ pwd }}"
  host: "{{ inventory_hostname }}"

nxos_provider:
  username: "{{ un }}"
  password: "{{ pwd }}"
  host: "{{ inventory_hostname }}"
  transport: nxapi

eos_provider:
  username: "{{ un }}"
  password: "{{ pwd }}"
  host: "{{ inventory_hostname }}"
  transport: eapi
  validate_certs: false
```


Keep in mind this is going to issue the `show lldp neighbors` commands against IOS, NXOS, and EOS devices!  This will work as there are pre-built neighbor templates for each of these OSs in the ntc-templates repository already.

This task will connect via SSH, get raw text back, and inside the module, the output will be parsed and returned as structured data.

```yaml
---

  - name: PARSE UNSTRUCTURED DATA 
    hosts: all
    connection: local
    gather_facts: no

    tasks:
      - name: PARSE DATA
        ntc_show_command:
          provider: "{{ ntc_provider }}" 
          platform: "{{ vendor }}_{{ os }}"       
          template_dir: "/etc/ntc/ansible/library/ntc-ansible/ntc-templates/templates"
          command: 'show lldp neighbors' 

```

`ntc_show_command` supports several parameters as you can see above.  Here is a brief description of a few of them including some not shown in the previous example.  Remember, you can use `ansible-doc ntc_show_command` to see all supported parameters too.

 - `connection`: since we are connecting via ssh, this will be ssh.  Otherwise, it's also possible to use an "offline" mode for testing
 - `platform`: specifies various platform such nxos, ios, arista, hp, etc.
 - `template_dir`: location where the templates are stored.  Feel free browse the directory.  The templates define the structured data that will be returned
 - `command`: command to run on the device
 - `use_templates` - you can also disable parsing to just use this module for collecting raw outputs of show commands


##### Step 2

Execute the playbook in verbose mode limiting the execution to just **csr1**.

```
ntc@ntc:~/ansible$ ansible-playbook -i inventory parse-output.yml -v --limit csr1

Using /etc/ansible/ansible.cfg as config file

PLAY [PARSE UNSTRUCTURED DATA] *************************************************

TASK [PARSE DATA] **************************************************************
ok: [csr1] => {"changed": false, "response": [{"local_interface": "Gi1", "neighbor": "csr2.ntc.com", "neighbor_interface": "Gi1"}, {"local_interface": "Gi1", "neighbor": "eos-leaf1.ntc.com", "neighbor_interface": "Management1"}, {"local_interface": "Gi1", "neighbor": "csr3.ntc.com", "neighbor_interface": "Gi1"}, {"local_interface": "Gi1", "neighbor": "eos-leaf2.ntc.com", "neighbor_interface": "Management1"}, {"local_interface": "Gi1", "neighbor": "eos-spine2.ntc.com", "neighbor_interface": "Management1"}, {"local_interface": "Gi1", "neighbor": "eos-spine1.ntc.com", "neighbor_interface": "Management1"}], "response_list": []}

PLAY RECAP *********************************************************************
csr1                       : ok=1    changed=0    unreachable=0    failed=0   

```

As you can see in the response, we are getting back structured data making it very easy to parse, which we'll look at in the next few tasks.


##### Step 3

Add a new registered variable called `parsed_data` and debug that variable to the terminal.

The updated playbook will look like this:

```
---

  - name: PARSE UNSTRUCTURED DATA 
    hosts: all
    connection: local
    gather_facts: no

    tasks:
      - name: PARSE DATA
        ntc_show_command:
          provider: "{{ ntc_provider }}" 
          platform: "{{ vendor }}_{{ os }}"        
          template_dir: "/etc/ntc/ansible/library/ntc-ansible/ntc-templates/templates"
          command: 'show lldp neighbors'         
        register: parsed_data

      - name: DEBUG FACTS
        debug: var=parsed_data

```

##### Step 4

Execute the playbook for all devices. 

In this particular example, three (3) separate templates were used for parsing the data, one for each OS.  ntc_show_command selected the right template based on the `platform` and `command` being passed in as paramters.

This should highlight the value of `ntc_show_command` how it simplifies the parsing of "legacy" output when no API is available to use.  In the next task, we'll use this _gathered_ data to create automated documentation.


### Task 4 - Creating Automated Documentation and Reports

In the previous tasks, you looked at using modules that specifically perform data collection.  You saw that all modules return data; this data is JSON, and can be viewed running the playbook in verbose mode.  

**Now we will look at using and consuming this data to create dynamic reports and documentation.**

##### Step 1

In the `ansible` directory, create a sub-directory called `docs` and inside it create two sub-directories called `facts` and `table`.  This will store all auto-generated documentation and reports going forward.

```
ntc@ntc:ansible$ mkdir -p docs/facts
ntc@ntc:ansible$ mkdir -p docs/table

```

##### Step 2

Create a new playbook called `facts-report.yml`.

It's first task will be the same task we used for gathering facts in Task 2:

```yaml
---

  - name: GATHER NTC FACTS
    hosts: all
    connection: local
    gather_facts: no

    tasks:
      - name: GET NTC FACTS
        ntc_get_facts:
          provider: "{{ ntc_provider }}"
          platform: "{{ vendor }}_{{ os }}_{{ api}}"
        register: ntc_facts
```

##### Step 3

Add a new task that will dump the contents of `ntc_facts` (registered variable) into a new file called `./docs/facts/<hostname>.md`.

```yaml
      - name: DUMP FACTS INTO FILE
        template:
          src: ntc-facts.j2
          dest: ./docs/facts/{{ inventory_hostname }}.md

```

##### Step 4

Create a new Jinja2 template called `ntc-facts.j2` in your `templates` sub-directory.

The template should have only a single line in it:

```
{{ ntc_facts }}
```

##### Step 5

Execute the playbook.  Feel free to limit it for just one device for testing.

Here is a sample output of one of the files created: `./docs/facts/csr1.md`

```
{u'changed': False, u'ansible_facts': {u'uptime': 12900, u'vendor': u'cisco', u'uptime_string': u'00:03:35:00', u'interfac
es': [u'GigabitEthernet1', u'GigabitEthernet2', u'GigabitEthernet3', u'GigabitEthernet4'], u'hostname': u'csr1', u'fqdn': 
u'N/A', u'cisco_ios_ssh': {u'config_register': u'0x2102'}, u'os_version': u'16.3.1', u'serial_number': u'', u'model': u'CS
R1000V', u'vlans': []}}
```

##### Step 6

Note how the data isn't formatted very pretty in the output file.  Add the Jinja2 Filter called `to_nice_json` to the template.  

Your template will look like this:

```
{{ ntc_facts | to_nice_json }}
```

##### Step 7

Execute the playbook.

At this point, you can better see all data being returned in the files created: `./docs/facts/csr1.md` as an example.

```json
{
    "ansible_facts": {
        "cisco_ios_ssh": {
            "config_register": "0x2102"
        }, 
        "fqdn": "N/A", 
        "hostname": "csr1", 
        "interfaces": [
            "GigabitEthernet1", 
            "GigabitEthernet2", 
            "GigabitEthernet3", 
            "GigabitEthernet4"
        ], 
        "model": "CSR1000V", 
        "os_version": "16.3.1", 
        "serial_number": "", 
        "uptime": 14520, 
        "uptime_string": "00:04:02:00", 
        "vendor": "cisco", 
        "vlans": []
    }, 
    "changed": false
}
```


##### Step 8

Since the data is more readable, it's time to determine which data we want in the report.

The data in scope for this task is the following:
  * Hostname
  * Model
  * Serial number
  * Vendor
  * OS Version

Update the template so it is an actual report.  

After making the changes, the updated `ntc-facts.j2` Jinja2 template should look like the following:

```
## Device: {{ inventory_hostname }}

Hostname:       {{ hostname }}
Vendor:         {{ vendor }}
Model:          {{ model }}
OS Version:     {{ os_version }}
Serial Number: {% if serial_number %} {{ serial_number }} {% else %} UKNOWN {% endif %}

```

> Note: you can also use the long form way of accessing the variables too, i.e. `ntc_facts['ansible_facts']['vendor']`.

> Note: some serial numbers are null strings because virtual devices are being used.  The conditional is simply making sure it's not a null string; if it is, "UNKNOWN" is displayed.

> Note: `##` in markdown is a 2nd level heading (larger font).


##### Step 9

Execute the playbook.  Feel free to limit it for just one device for testing.

Here is a sample output of one of the files created: `./docs/facts/nxos-spine1.md`

```
## Device: nxos-spine1

Hostname:      nxos-spine1
Vendor:        cisco
Model:         NX-OSv Chassis
OS Version:    7.3(1)D1(1) [build 7.3(1)D1(0.10)]
Serial Number:  TM602622D6B 

```


##### Step 10

Add a new task as the last task in the playbook that assembles all of these individual device reports and creates a single report.  Use the `assemble` module.  

> Remember to use the `ansible-doc` utility to learn how to use new modules.

This task will assemble all files in the `./docs/facts` directory and create a new file called `facts.md` in the `docs` directory.

The task is also configured to use a delimiter of `---` which is a horizontal bar in markdown.

```yaml
      - name: ASSEMBLE FACTS REPORTS
        assemble:
          src: ./docs/facts/
          dest: ./docs/facts.md
          delimiter: "---"
        run_once: true
```

At this point, the full playbook should look like this:

```yaml
---

  - name: GATHER NTC FACTS
    hosts: all
    connection: local
    gather_facts: no

    tasks:
      - name: GET NTC FACTS
        ntc_get_facts:
          provider: "{{ ntc_provider }}"
          platform: "{{ vendor }}_{{ os }}_{{ api}}"
        register: ntc_facts
      
      - name: DUMP FACTS INTO FILE
        template:
          src: ntc-facts.j2
          dest: ./docs/facts/{{ inventory_hostname }}.md
  
      - name: ASSEMBLE FACTS REPORTS
        assemble:
          src: ./docs/facts/
          dest: ./docs/facts.md
          delimiter: "---"
        run_once: true

```

This creates the following `facts.md` file:

```
## Device: csr1

Hostname:      csr1
Vendor:        cisco
Model:         CSR1000V
OS Version:    16.3.1
Serial Number:  UKNOWN 


---
## Device: csr2

Hostname:      csr2
Vendor:        cisco
Model:         CSR1000V
OS Version:    16.3.1
Serial Number:  UKNOWN 


---
## Device: csr3

Hostname:      csr3
Vendor:        cisco
Model:         CSR1000V
OS Version:    16.3.1
Serial Number:  UKNOWN 


---
## Device: eos-leaf1

Hostname:      eos-leaf1
Vendor:        arista
Model:         vEOS
OS Version:    4.15.2F-2663444.4152F
Serial Number:  UKNOWN 


---
## Device: eos-leaf2

Hostname:      eos-leaf2
Vendor:        arista
Model:         vEOS
OS Version:    4.15.2F-2663444.4152F
Serial Number:  UKNOWN 


---
## Device: eos-spine1

Hostname:      eos-spine1
Vendor:        arista
Model:         vEOS
OS Version:    4.15.2F-2663444.4152F
Serial Number:  UKNOWN 


---
## Device: eos-spine2

Hostname:      eos-spine2
Vendor:        arista
Model:         vEOS
OS Version:    4.15.2F-2663444.4152F
Serial Number:  UKNOWN 


---
## Device: nxos-spine1

Hostname:      nxos-spine1
Vendor:        cisco
Model:         NX-OSv Chassis
OS Version:    7.3(1)D1(1) [build 7.3(1)D1(0.10)]
Serial Number:  TM602622D6B 


---
## Device: nxos-spine2

Hostname:      nxos-spine2
Vendor:        cisco
Model:         NX-OSv Chassis
OS Version:    7.3(1)D1(1) [build 7.3(1)D1(0.10)]
Serial Number:  TM604B14E3B 


```

To view the final rendered markdown, you have a few options:

  * Quick option is to paste the text table into the left pane on this site that auto-renders markdown: [https://stackedit.io/editor](https://stackedit.io/editor)
  * Commit it to GitHub and view it on GitHub
  * Download and install the Firefox plug-in and view it in Firefox.  You can google "firefox markdown viewer".  It's the first one in the list.


### Challenge

Create a NEW Jinaj2 template (not update the existing one) to create markdown tables of each of the device's facts.  Then assemble them creating a final report.

Store the invidual reports in `./docs/table` and the summary report in `.docs/facts-table.md`.


Hint for creating a markdown table:

```
| FACT | VALUE | 
|-------|--------|
|   FACT 1 |  FACT VALUE1    |
|   FACT 2 |  FACT VALUE2    |


# SCROLL DOWN FOR THE SOLUTION

```

























.
# FINAL PLAYBOOK

```

---

  - name: GATHER NTC FACTS
    hosts: all
    connection: local
    gather_facts: no

    tasks:
      - name: GET NTC FACTS
        ntc_get_facts:
          provider: "{{ ntc_provider }}"
          platform: "{{ vendor }}_{{ os }}_{{ api}}"
        register: ntc_facts
      
      - name: DUMP FACTS INTO FILE
        template:
          src: ntc-facts.j2
          dest: ./docs/facts/{{ inventory_hostname }}.md
  
      - name: CREATE TABLE
        assemble:
          src: ./docs/facts/
          dest: ./docs/facts.md
          delimiter: "---"
        run_once: true

      - name: DUMP FACTS INTO FILE
        template:
          src: ntc-facts-table.j2
          dest: ./docs/table/{{ inventory_hostname }}.md

      - name: CREATE TABLE
        assemble:
          src: ./docs/table/
          dest: ./docs/facts-table.md
          delimiter: "---"
        run_once: true


```

## TEMPLATES

```
::::::::::::::
templates/ntc-facts.j2
::::::::::::::
## Device: {{ inventory_hostname }}

Hostname:      {{ hostname }}
Vendor:        {{ vendor }}
Model:         {{ model }}
OS Version:    {{ os_version }}
Serial Number: {% if serial_number %} {{ serial_number }} {% else %} UNKNOWN {% endif %}


::::::::::::::
templates/ntc-facts-table.j2
::::::::::::::
## Device: {{ inventory_hostname }}

| FACT | VALUE |
|-------|--------|
| Hostname | {{ hostname }} |
| Vendor | {{ vendor }} |
| Model | {{ model }} |
| OS Version | {{ os_version }}|
| Serial Number | {% if serial_number %} {{ serial_number }} {% else %} UNKNOWN {% endif %}|



```
