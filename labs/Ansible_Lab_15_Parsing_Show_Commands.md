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
