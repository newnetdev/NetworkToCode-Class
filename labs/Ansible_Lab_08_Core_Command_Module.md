## Lab 8 - Using the Core Command Module

### Task 1 - Using the *_command module

In this task, you will use the _command module to gather information about network devices, save it as a new variable, and debug it to the terminal.

##### Step 1

Create a new playbook called `core-command.yml` in the `ansible` directory.  You have your choice to automate either Arista or Nexus devices.  In your play definition, you can enter one of the following if you want to automate Nexus or Arista switches.

```yaml
---
  - name: CORE MODULES
    hosts: nxos-spines
    connection: local
    gather_facts: no

```

```yaml
---
  - name: CORE MODULES
    hosts: eos-spines
    connection: local
    gather_facts: no


```

> Note: if you're using the Nexus devices, please SSH to each device and manually enable LLDP using the `feature lldp` command.  Alternatively, you can use the `nxos_feature` Ansible module to do this!

##### Step 2

Create a variable called `provider` in the playbook that will be used to easily pass the same parameters into the these Ansible core modules.

```yaml
---
  - name: CORE MODULES
    hosts: # <either eos-spines or nxos-spines based on Step 1>
    connection: local
    gather_facts: no

    vars:
      provider:
        username: "{{ un }}"
        password: "{{ pwd }}"
        host: "{{ inventory_hostname }}"
        transport: "{{ api }}"
        use_ssl: False

    tasks:
```

Create a new group based variable for the group(s) you are using in this play.

> Note: For a production deployment, you'd want to define `provider` in a group variables file rather than embed that variable in a playbook.

##### Step 3

Using either **eos_command** or **nxos_command** execute the commands `show version` and `show hostname` on the respective devices.  

Do this in a SINGLE task.

Use the command `ansible-doc nxos_command` or `ansible-doc eos_command` for assistance if needed.

##### Step 4

Save and execute the playbook.

```
$ ansible-playbook -i inventory core-command.yml
```

**Task 1 solutions are at the bottom of this page.**


### Task 2

In the previous task, you issued show commands, but didn't see the actual response data from the devices.  This task builds on Task 1 showing you how you can see the response data.

##### Step 1

Execute the playbook in verbose mode.

```
$ ansible-playbook -i inventory core-command.yml -v

output omitted
```

##### Step 2

Using verbose mode is one way to see the JSON output coming back from a module.  Another way is to use the **debug** module, which also pretty prints the data and make it easier to read.

Using the **register** directive and **debug** module, *debug* the value of the hostname and OS running on the devices.  The variables used in the debug statement should be as specific as possible to print out **just the value of the hostname/version of software running**

When you use **register** to save the output being returned, save it in a new variable called `output`.

For this step, you'll need to do 3 things:

1. Use the register task attribute in the task you are using the *_command module.
2. Use a debug task to print the OS version
3. Use a debug task to print the hostname


When you run the playbook after you've made these changes, do **NOT** run the playbook in verbose mode.

**Task 2 solutions are at the bottom of this page.**


### Task 3 - Device Compliance with *_command module

In this task, you will build on the playbook you just created to ensure that you are running a particular version of OS as well as validate you have the correct number of neighbors.

##### Step 1

Update your task to execute the two commands `show version` and `show lldp neighbors`.  Remove the command `show hostname` from the list.

If you're using NXOS devices, you need to SSH to the device and enable lldp with the `feature lldp` command in configuration mode.

##### Step 2

Add a new task using the **assert** module that will ensure the following:

- Your devices have the correct version of software running
- Your devices have the correct quantity of neighbors - login to the devices manually to check to see how many neighbors there are to know for sure how many to execpt.  

> Hint: you will need to use the Jinja2 filter called length for the second assertion.


**Task 3 solutions are at the bottom of this page.**



# Task 1 Solutions

### Cisco NXOS:

```yaml
---

  - name: CORE MODULES
    hosts: nxos-spines
    connection: local
    gather_facts: no

    vars:
      provider:
        username: "{{ un }}"
        password: "{{ pwd }}"
        host: "{{ inventory_hostname }}"
        transport: "{{ api }}"
    tasks:

      - nxos_command:
          commands:
            - 'show version'
            - 'show hostname'
          provider: "{{ provider }}"  
        register: output

```


### Arista EOS

```yaml
---

  - name: CORE
    hosts: eos-spines
    connection: local
    gather_facts: no

    vars:
      provider:
        username: "{{ un }}"
        password: "{{ pwd }}"
        host: "{{ inventory_hostname }}"
        transport: "{{ api }}"
        use_ssl: False
    tasks:
      - eos_command:
          commands:
            - 'show version'
            - 'show hostname'
          provider: "{{ provider }}"
        register: output


```



# Task 2 Solutions

### Cisco NXOS:

```yaml
---

  - name: CORE MODULES
    hosts: nxos-spines
    connection: local
    gather_facts: no

    vars:
      provider:
        username: "{{ un }}"
        password: "{{ pwd }}"
        host: "{{ inventory_hostname }}"
        transport: "{{ api }}"
    tasks:

      - nxos_command:
          commands:
            - 'show version'
            - 'show hostname'
          provider: "{{ provider }}"  
        register: output

      - debug: var=output.stdout[0]['sys_ver_str']

      - debug: var=output.stdout[1]['hostname']

```


### Arista EOS

```yaml
---

  - name: CORE
    hosts: eos-spines
    connection: local
    gather_facts: no

    vars:
      provider:
        username: "{{ un }}"
        password: "{{ pwd }}"
        host: "{{ inventory_hostname }}"
        transport: "{{ api }}"
        use_ssl: False
    tasks:
      - eos_command:
          commands:
            - 'show version'
            - 'show hostname'
          provider: "{{ provider }}"
        register: output

      - debug: var=output.stdout[0]['internalVersion']

      - debug: var=output.stdout[1]['hostname']


```


# Task 3 Solutions

### Cisco NXOS

```yaml
---
  - name: CORE MODULES
    hosts: nxos-spines
    connection: local
    gather_facts: no

    vars:
      provider:
        username: "{{ un }}"
        password: "{{ pwd }}"
        host: "{{ inventory_hostname }}"
        transport: "{{ api }}"
        use_ssl: False

    tasks:
    - name: NXOS show version
      nxos_command:
        commands:
          - show version
          - show lldp neighbors
        provider: "{{ provider }}"
      register: output

    - name: check OS version & neighbors
      assert:
        that:
          - output.stdout[0]['sys_ver_str'] == "7.3(1)D1(1) [build 7.3(1)D1(0.10)]"
          - output.stdout[1]['TABLE_nbor']['ROW_nbor']|length == 4

```

### Arista EOS

```yaml
---
  - name: CORE MODULES
    hosts: eos-spines
    connection: local
    gather_facts: no

    vars:
      provider:
        username: "{{ un }}"
        password: "{{ pwd }}"
        host: "{{ inventory_hostname }}"
        transport: "{{ api }}"
        use_ssl: False

    tasks:
    - name: EOS show version
      eos_command:
        commands:
          - show version
          - show lldp neighbors
        provider: "{{ provider }}"
      register: output

    - name: check OS version and neighbors
      assert:
        that:
          - output.stdout[0]['internalVersion'] == "4.15.2F-2663444.4152F"
          - output.stdout[1]['lldpNeighbors']|length == 7

```




