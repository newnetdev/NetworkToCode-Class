## Lab 15 - Parsing Show Commands with Ansible

In the next few labs, we'll introduce a few different methodologies for parsing show commands with Ansible looking at several different built-in Jinja2 filters.  They are `regex_search`, `regex_findall`, `parse_cli`, and `parse_cli_textfsm`.

This lab use the `parse_` filters whereas the next lab will use the `regex_` filters.

### Task 1

In the first task, we'll parse show data on IOS using a pre-built TextFSM template for the "show version" command called `parse_cli_textfsm`.

##### Step 1

Create a new playbook called `parse-ios.yml` in the `ansible` directory.

Use the following playbook to gather `show version` for the IOS devices.

```yaml
---

  - name: PING TEST
    hosts: csr1
    connection: local
    gather_facts: no
    tags: play2

    vars:
      template_path: "/etc/ntc/ansible/library/ntc-ansible/ntc-templates/templates/"
      show_version_path: "{{ template_path }}cisco_ios_show_version.template"

    tasks:

      - name: GET SHOW COMMANDS
        ios_command:
          commands: show version
        register: config_data


```

> Note: we've also defined two variables to know the path and file that should be used for the parsing.

Feel free to open the TextFSM template so you can review it.

##### Step 2

Add two new tasks:

  * One that will _parse_ the "show version" response using the pre-built TextFSM template and save it as a new variable using the `set_fact` module.
  * One that will debug the new variable.

```yaml
      - set_fact:
          show_version: "{{ config_data.stdout.0 | parse_cli_textfsm(show_version_path) }}"

      - debug:
          var: show_version
```

##### Step 3

Execute the playbook.

```
ntc@ntc:ansible$ ansible-playbook -i inventory parse-ios.yml

```

Looking at the relevant debug output, you should see the following:

```
TASK [debug] ********************************************************************************
ok: [csr1] => {
    "show_version": [
        {
            "CONFIG_REGISTER": "0x2102",
            "HARDWARE": [
                "CSR1000V"
            ],
            "HOSTNAME": "csr1",
            "ROMMON": "IOS-XE",
            "RUNNING_IMAGE": "packages.conf",
            "SERIAL": [
                "9KIBQAQ3OPE"
            ],
            "UPTIME": "50 minutes",
            "VERSION": "16.6.2"
        }
    ]
}
```


##### Step 4

Add "assert" statements to validate the OS version and configuration register.

```yaml
      - name: CHECK OS AND CONFIG REGISTER
        assert:
          that:
           - show_version[0]['VERSION'] == '16.6.2'
           - show_version[0]['CONFIG_REGISTER'] == '0x2102'
```

##### Step 5

Save and execute the playbook.


### Task 2 - DO NOT DO THIS TASK

In this task, we'll use another Jinja2 filter for parsing.  This one is called `parse_cli` that uses Ansible specific RegEx "spec" files that have the regular expression definitions defined.

##### Step 1

Create a new sub-directory called `parsers` within the `ansible` directory and navigate to that directory.

```
ntc@ntc:ansible$ mkdir parsers
ntc@ntc:ansible$ cd parsers
ntc@ntc:parsers$
```

##### Step 2

Create a file called `show_ip_interface_brief-dict.yml` and save the following inside this file:

```yaml
---

keys:
  interfaces:
    value:
      key: "{{ item.iface_name }}"
      values:
        interface: "{{ item.iface_name }}"
        ip_addr: "{{ item.ip_addr }}"
        status: "{{ item.status }}"
        protocol: "{{ item.protocol }}"
    items: "^(?P<iface_name>(\\S+))\\s+(?P<ip_addr>(\\S+)|(\\w+))\\s+(?P<ok>(\\w+))\\s+(?P<method>(\\S+))\\s+(?P<status>(administratively down|\\w+))\\s+(?P<protocol>(\\S+))"

```

##### Step 3

Add a new task to your playbook to issue the `show ip int brief` command against the IOS devices:

```yaml
      - name: GET SHOW COMMANDS
        ios_command:
          commands: show ip interface brief
        register: output
```

##### Step 4

Add two more new tasks to the playbook to parse and print the required data.

```yaml
      - set_fact:
          show_brief: "{{ output.stdout.0 | parse_cli('./parsers/show_ip_interface_brief-dict.yml') }}"

      - debug:
          var: show_brief
```

Add two new tasks:

  * One that will _parse_ the "show ip int brief" response using the pre-built Ansible spec file and save it as a new variable using the `set_fact` module.
  * One that will debug the new variable.

##### Step 5

Save and execute the playbook.

You should see the following output for **csr1**:

```
TASK [debug] ********************************************************************************
ok: [csr1] => {
    "show_brief": {
        "interfaces": {
            "GigabitEthernet1": {
                "interface": "GigabitEthernet1",
                "ip_addr": "10.0.0.51",
                "protocol": "up",
                "status": "up"
            },
            "GigabitEthernet2": {
                "interface": "GigabitEthernet2",
                "ip_addr": "10.254.13.1",
                "protocol": "up",
                "status": "up"
            },
            "GigabitEthernet3": {
                "interface": "GigabitEthernet3",
                "ip_addr": "unassigned",
                "protocol": "down",
                "status": "administratively down"
            },
            "GigabitEthernet4": {
                "interface": "GigabitEthernet4",
                "ip_addr": "10.254.12.1",
                "protocol": "up",
                "status": "up"
            },
            "Loopback100": {
                "interface": "Loopback100",
                "ip_addr": "1.1.1.2",
                "protocol": "up",
                "status": "up"
            },
            "Loopback101": {
                "interface": "Loopback101",
                "ip_addr": "unassigned",
                "protocol": "up",
                "status": "up"
            }
        }
    }
}
```


##### Step 6 (DO NOT DO THIS STEP)

Save the following into a new spec parser file called `show_ip_interface_brief-list.yml` in the `parsers` directory.

```yaml
---

keys:
  interfaces:
    type: list
    value:
      interface: "{{ item.iface_name }}"
      ip_addr: "{{ item.ip_addr }}"
      status: "{{ item.status }}"
      protocol: "{{ item.protocol }}"
    items: "^(?P<iface_name>(\\S+))\\s+(?P<ip_addr>(\\S+)|(\\w+))\\s+(?P<ok>(\\w+))\\s+(?P<method>(\\S+))\\s+(?P<status>(administratively down|\\w+))\\s+(?P<protocol>(\\S+))"
```

Update the playbook or add a task to use the "new" parser.

Save and execute the playbook.

The output you should see is this:


```
ok: [csr1] => {
    "show_brief": {
        "interfaces": [
            {
                "interface": "GigabitEthernet1",
                "ip_addr": "10.0.0.51",
                "protocol": "up",
                "status": "up"
            },
            {
                "interface": "GigabitEthernet2",
                "ip_addr": "10.254.13.1",
                "protocol": "up",
                "status": "up"
            },
            {
                "interface": "GigabitEthernet3",
                "ip_addr": "unassigned",
                "protocol": "down",
                "status": "administratively down"
            },
            {
                "interface": "GigabitEthernet4",
                "ip_addr": "10.254.12.1",
                "protocol": "up",
                "status": "up"
            },
            {
                "interface": "Loopback100",
                "ip_addr": "1.1.1.2",
                "protocol": "up",
                "status": "up"
            },
            {
                "interface": "Loopback101",
                "ip_addr": "unassigned",
                "protocol": "up",
                "status": "up"
            }
        ]
    }
}
```

Notice how the first output was a nested dictionary and this one is a list of dictionaries.
