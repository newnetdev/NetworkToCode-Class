## Lab 20 - Data Collection Modules & Reporting

Network Automation, and automation in general, is often equated with configuring devices faster, but as you've seen by now, it offers greater predictability and more deterministic outcomes.

On top of that, it also offers even great value when it comes to collecting data and reporting.  In these next few tasks, you will use Ansible modules to automate the data collection process and also dynamically generate different types of reports.

### Task 1 - Exploring Ansible Core Facts Modules

In the first task, you will use facts modules to gather device information such as OS version, hostname, serial number, neighbors, and IP addresses on the network devices.  The modules you will use in this task are all in Ansible core.  That means they come with Ansible when you install Ansible.

Each module has the name of `<os>_facts`.

  * For IOS devices, the module is `ios_facts`
  * For NXOS devices, the module is `nxos_facts`
  * For EOS devices, the module is `eos_facts`
  * For Junos devices, the module is `junos_facts`

> Remember, you can use the `ansible-doc` utility on any of these modules to see how to use them and what data will be returned from them.

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
        register: ntc_ios_facts

      - debug:
          var: ntc_ios_facts

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
    "ntc_ios_facts['ansible_facts']['ansible_net_version']": "16.06.02"
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
TASK [DEBUG OS VERSION] ********************************************************
ok: [csr1] => {
    "ntc_ios_facts['ansible_facts']['ansible_net_version']": "16.06.02"
}

TASK [DEBUG SHORTHAND OS VERSION] **********************************************
ok: [csr1] => {
    "ansible_net_version": "16.06.02"
}

```

> Note: While you can access facts directly, using the register/debug combination provides an easy way to see exactly what's being collected in that specific task.


##### Step 10

Repeat Steps 1 - 9 for each device type you've been using in the labs.

**Add a new play for each one.** Tag each play accordingly so you can run them individually.


**IMPORTANT**
> Note: Ensure LLDP is enabled on the NXOS switches using the `feature lldp`.  Unfortunately, LLDP configurations do not persist through a reboot on virtual Nexus switches :(.

If you don't run the playbook, here are the commands to run on **nxos-spine1** and **nxos-spine2**:

```
config t
feature lldp
end
exit
```

**Status Check**

This is a sample playbook for running against all 4 device types (IOS, NXOS, JUNOS, EOS):

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
        register: ntc_ios_facts

      - name: DEBUG FACTS
        debug:
          var: ntc_ios_facts

      - name: DEBUG OS VERSION
        debug:
          var: ntc_ios_facts['ansible_facts']['ansible_net_version']

      - name: DEBUG SHORTHAND OS VERSION
        debug:
          var: ansible_net_version

  - name: GATHER NXOS FACTS
    hosts: nxos
    connection: local
    gather_facts: no
    tags: nxos

    tasks:
      - name: GET NXOS FACTS
        nxos_facts:
        register: ntc_nxos_facts

      - name: DEBUG FACTS
        debug:
          var: ntc_nxos_facts

      - name: DEBUG OS VERSION
        debug:
          var: ntc_nxos_facts['ansible_facts']['ansible_net_version']

      - name: DEBUG SHORTHAND OS VERSION
        debug:
          var: ansible_net_version

  - name: GATHER EOS FACTS
    hosts: eos
    connection: local
    gather_facts: no
    tags: eos

    tasks:
      - name: GET EOS FACTS
        eos_facts:
        register: ntc_eos_facts

      - name: DEBUG FACTS
        debug:
          var: ntc_eos_facts

      - name: DEBUG OS VERSION
        debug:
          var: ntc_eos_facts['ansible_facts']['ansible_net_version']

      - name: DEBUG SHORTHAND OS VERSION
        debug:
          var: ansible_net_version

  - name: GATHER JUNOS FACTS
    hosts: vmx
    connection: local
    gather_facts: no
    tags: junos

    tasks:
      - name: GET FACTS
        junos_facts:
        register: ntc_junos_facts

      - name: DEBUG FACTS
        debug:
          var: ntc_junos_facts

      - name: DEBUG OS VERSION
        debug:
          var: ntc_junos_facts['ansible_facts']['ansible_net_version']

      - name: DEBUG SHORTHAND OS VERSION
        debug:
          var: ntc_junos_facts
```


### Task 2 - Creating Automated Documentation and Reports

In the previous task, you looked at exploring the core facts modules that specifically perform data collection.  You saw that all modules including facts modules return data; this data is JSON, and can be viewed running the playbook in verbose mode.

**Now we will look at using and consuming this data to create dynamic reports and documentation.**

##### Step 1

Create a new playbook called `reports.yml`.  Create a play that requires the directories that are required to store the reports.  This will eliminate you from using `mkdir` on the command line.

```yaml
---

  - name: GATHER IOS FACTS
    hosts: iosxe
    connection: local
    gather_facts: no
    tags: ios

    tasks:

      - file:
          path: ./docs/csv/
          state: directory

      - file:
          path: ./docs/text/
          state: directory
```

##### Step 2

Our goal is to create the required Jinja2 templates to create reports that look like this for every device:

Text Report:

```
Hostname:      csr3
Vendor:        cisco
Model:         UNKNOWN
OS Version:    16.06.02
Serial Number:  9KIBQAQ3OPE
```

CSV Report:

```
csr3,cisco,UNKNOWN,16.06.02,9KIBQAQ3OPE
```

Create two new templates and save them in the `templates` directory: `facts-text.j2` and `facts-csv.j2`.

`facts-text.j2`:

```
Hostname:      {{ ansible_net_hostname }}
Vendor:        {{ vendor }}
Model:         {{ ansible_net_model or "UNKNOWN" }}
OS Version:    {{ ansible_net_version }}
Serial Number:  {{ ansible_net_serialnum or "UNKNOWN" }}

```

`facts-csv.j2`:

```
{{ ansible_net_hostname }},{{ vendor }},{{ ansible_net_model or "UNKNOWN" }},{{ ansible_net_version }},{{ ansible_net_serialnum or "UNKNOWN" }}
```

##### Step 3

Add a new play to create reports for each IOS device (for both report types).

```yaml
  - name: GATHER IOS FACTS
    hosts: iosxe
    connection: local
    gather_facts: no
    tags: ios

    tasks:
      - name: GET FACTS
        ios_facts:

      - name: DUMP FACTS INTO TEXT FILE
        template:
          src: facts-text.j2
          dest: ./docs/text/{{ inventory_hostname }}.md

      - name: DUMP FACTS INTO CSV FILE
        template:
          src: facts-csv.j2
          dest: ./docs/csv/{{ inventory_hostname }}.csv
```

##### Step 4

Exectute the playbook.

View all files that have been created.

##### Step 5

Create a 3rd play that will "assemble" all files in each respective directory and create a master report.

Note that this is running on `localhost` so it runs just once.

```yaml
  - name: FINAL TASK
    hosts: localhost
    connection: local
    gather_facts: no
    tags: assemble

    tasks:

        - name: CREATE MASTER TEXT REPORT
          assemble:
            src: ./docs/text/
            dest: ./docs/master-text.md
            delimiter: "---"

        - name: CREATE MASTER CSV REPORT
          assemble:
            src: ./docs/csv/
            dest: ./docs/master-csv.csv
```

##### Step 6

Execute the playbook.

View all files that have been created.

##### Step 7

There is still one thing missing from the CSV.  That is to inser the headers for the CSV.

```yaml
        - name: INSERT COLUMNS INTO CSV REPORT
          lineinfile:
            path: ./docs/master-csv.csv
            line: "Hostname,Vendor,Model,OS Version,Serial Number"
            insertbefore: BOF
            state: present
```

This task will go just below the `assemble` tasks.

##### Step 8

Execute the playbook.

View both final master reports.

##### Step 9

Repeat Step 3 for all NXOS, EOS, and JUNOS devices so the master report contains all devices.

Note: The existing FINAL TASK (assemble) must remain the final task, so insert those three new plays just below the IOS play.

##### Step 10

Execute the playbook.

The final playbook should look like this:

```yaml
---

  - name: GATHER IOS FACTS
    hosts: iosxe
    connection: local
    gather_facts: no
    tags: ios

    tasks:

      - file:
          path: ./docs/csv/
          state: directory

      - file:
          path: ./docs/text/
          state: directory

  - name: GATHER IOS FACTS
    hosts: iosxe
    connection: local
    gather_facts: no
    tags: ios

    tasks:
      - name: GET FACTS
        ios_facts:

      - name: DUMP FACTS INTO TEXT FILE
        template:
          src: facts-text.j2
          dest: ./docs/text/{{ inventory_hostname }}.md

      - name: DUMP FACTS INTO CSV FILE
        template:
          src: facts-csv.j2
          dest: ./docs/csv/{{ inventory_hostname }}.csv


  - name: GATHER NXOS FACTS
    hosts: nxos
    connection: local
    gather_facts: no
    tags: nxos

    tasks:
      - name: GET NXOS FACTS
        nxos_facts:

      - name: DUMP FACTS INTO FILE
        template:
          src: facts-text.j2
          dest: ./docs/text/{{ inventory_hostname }}.md

      - name: DUMP FACTS INTO FILE
        template:
          src: facts-csv.j2
          dest: ./docs/csv/{{ inventory_hostname }}.csv


  - name: GATHER EOS FACTS
    hosts: eos
    connection: local
    gather_facts: no
    tags: eos

    tasks:
      - name: GET EOS FACTS
        eos_facts:

      - name: DUMP FACTS INTO FILE
        template:
          src: facts-text.j2
          dest: ./docs/text/{{ inventory_hostname }}.md

      - name: DUMP FACTS INTO FILE
        template:
          src: facts-csv.j2
          dest: ./docs/csv/{{ inventory_hostname }}.csv

  - name: GATHER JUNOS FACTS
    hosts: vmx
    connection: local
    gather_facts: no
    tags: junos

    tasks:
      - name: GET FACTS
        junos_facts:

      - name: DUMP FACTS INTO FILE
        template:
          src: facts-text.j2
          dest: ./docs/text/{{ inventory_hostname }}.md

      - name: DUMP FACTS INTO FILE
        template:
          src: facts-csv.j2
          dest: ./docs/csv/{{ inventory_hostname }}.csv

  - name: FINAL TASK
    hosts: localhost
    connection: local
    gather_facts: no
    tags: assemble

    tasks:

        - name: CREATE MASTER TEXT REPORT
          assemble:
            src: ./docs/text/
            dest: ./docs/master-text.md
            delimiter: "---"

        - name: CREATE MASTER CSV REPORT
          assemble:
            src: ./docs/csv/
            dest: ./docs/master-csv.csv

        - name: INSERT COLUMNS INTO CSV REPORT
          lineinfile:
            path: ./docs/master-csv.csv
            line: "Hostname,Vendor,Model,OS Version,Serial Number"
            insertbefore: BOF
            state: present

```


The master CSV report generated will look like this:

```
ntc@ntc:ansible$ cat docs/master-csv.csv
Hostname,Vendor,Model,OS Version,Serial Number
csr1,cisco,UNKNOWN,16.06.02,9KIBQAQ3OPE
csr2,cisco,UNKNOWN,16.06.02,9KIBQAQ3OPE
csr3,cisco,UNKNOWN,16.06.02,9KIBQAQ3OPE
eos-leaf1,arista,vEOS,4.20.0F-7058194.bloomingtonrel (engineering build),UNKNOWN
eos-leaf2,arista,vEOS,4.20.0F-7058194.bloomingtonrel (engineering build),UNKNOWN
eos-spine1,arista,vEOS,4.20.0F-7058194.bloomingtonrel (engineering build),UNKNOWN
eos-spine2,arista,vEOS,4.20.0F-7058194.bloomingtonrel (engineering build),UNKNOWN
nxos-spine1,cisco,NX-OSv Chassis,7.3(1)D1(1) [build 7.3(1)D1(0.10)],TM602622D6B
nxos-spine2,cisco,NX-OSv Chassis,7.3(1)D1(1) [build 7.3(1)D1(0.10)],TM604B14E3B
vmx7,juniper,vmx,15.1F4.15,VMX2c
vmx8,juniper,vmx,15.1F4.15,VMX63
vmx9,juniper,vmx,15.1F4.15,VMX39
ntc@ntc:ansible$
```

And the final text report will look like this:

```
ntc@ntc:ansible$ cat docs/master-text.md
Hostname:      csr1
Vendor:        cisco
Model:         UNKNOWN
OS Version:    16.06.02
Serial Number:  9KIBQAQ3OPE
---
Hostname:      csr2
Vendor:        cisco
Model:         UNKNOWN
OS Version:    16.06.02
Serial Number:  9KIBQAQ3OPE
---
Hostname:      csr3
Vendor:        cisco
Model:         UNKNOWN
OS Version:    16.06.02
Serial Number:  9KIBQAQ3OPE
---
Hostname:      eos-leaf1
Vendor:        arista
Model:         vEOS
OS Version:    4.20.0F-7058194.bloomingtonrel (engineering build)
Serial Number:  UNKNOWN
---
Hostname:      eos-leaf2
Vendor:        arista
Model:         vEOS
OS Version:    4.20.0F-7058194.bloomingtonrel (engineering build)
Serial Number:  UNKNOWN
---
Hostname:      eos-spine1
Vendor:        arista
Model:         vEOS
OS Version:    4.20.0F-7058194.bloomingtonrel (engineering build)
Serial Number:  UNKNOWN
---
Hostname:      eos-spine2
Vendor:        arista
Model:         vEOS
OS Version:    4.20.0F-7058194.bloomingtonrel (engineering build)
Serial Number:  UNKNOWN
---
Hostname:      nxos-spine1
Vendor:        cisco
Model:         NX-OSv Chassis
OS Version:    7.3(1)D1(1) [build 7.3(1)D1(0.10)]
Serial Number:  TM602622D6B
---
Hostname:      nxos-spine2
Vendor:        cisco
Model:         NX-OSv Chassis
OS Version:    7.3(1)D1(1) [build 7.3(1)D1(0.10)]
Serial Number:  TM604B14E3B
---
Hostname:      vmx7
Vendor:        juniper
Model:         vmx
OS Version:    15.1F4.15
Serial Number:  VMX2c
---
Hostname:      vmx8
Vendor:        juniper
Model:         vmx
OS Version:    15.1F4.15
Serial Number:  VMX63
---
Hostname:      vmx9
Vendor:        juniper
Model:         vmx
OS Version:    15.1F4.15
Serial Number:  VMX39
ntc@ntc:ansible$
```

