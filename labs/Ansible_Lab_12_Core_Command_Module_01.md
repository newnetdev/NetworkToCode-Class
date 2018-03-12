## Lab 12 - Using the Core Command Module

### Task 1 - Using the *_command module 

In this task, you will use the _command module to issue show commands against network devices and save the command outputs to a file.

##### Step 1

Create a new playbook called `core-command.yml` in the `ansible` directory.  You have your choice to automate IOS, EOS, or NXOS devices.  While all examples reflect IOS devices, it's the same workflow for any of them.


```yaml
---

  - name: BACKUP SHOW VERSION
    hosts: csr1
    connection: local
    gather_facts: no

    tasks:

```

##### Step 2

Add a task to issue the `show version` command.

```yaml
---

  - name: BACKUP SHOW VERSION
    hosts: csr1
    connection: local
    gather_facts: no

    tasks:
      - name: GET SHOW COMMANDS
        ios_command:
          commands: show version

```

##### Step 3

Execute the playbook.

Did you see the output anywhere?

##### Step 4

Execute the playbook using the `-v` verbose flag.

Did you see the output anywhere?

##### Step 5

In order to clean up the output, use `register` task attribute and debug the new variable to the terminal.

```yaml
      - name: GET SHOW COMMANDS
        ios_command:
          commands: show version
        register: config_data

      - debug:
          var: config_data 
```

##### Step 6

Execute the playbook.  Do not use the `-v` flag.

The output seen is much cleaner and easier to read than using the `-v` flag.

> Note that when you use `register`, it's creating a new variable and storing the JSON return data from the module into the variable name defined.  In this case, it's `config_data`.

##### Step 7

Take note of the data being debugged:

```

TASK [debug] ************************************************************************
ok: [csr1] => {
    "config_data": {
        "changed": false, 
        "failed": false, 
        "stdout": [
            "Cisco IOS XE Software, Version 16.06.02\nCisco IOS Software [Everest], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.6.2, RELEASE SOFTWARE (fc2)\nTechnical Support:
            ...
```

`config_data` is a JSON object (think dictionary) that has several key value pairs, e.g. `changed`, `failed`, `stdout`, and `stdout_lines` (not shown).

You can also see that `stdout` is a list given it has square brackets next to it.  

`stdout` is **ALWAYS** a list when you're using the "command" modules.  It is a list of show command responses.  It's a list that has a length equal to the number of commands sent to the device.  In this case, we sent 1 command, so it's a length of 1, thus we'd access the "show version" response as element 0.

##### Step 8

Our goal is to save the show command output to a file.  We are going to do this using the `template` module.

Create a new Jinja2 template called `basic-copy.j2` stored in the `templates` directory.  

It should look like this:

```
{{ config_data['stdout'][0] }}
```

Take a second to think about this object.  Remember the data type of `stdout`?

##### Step 9

Create a directory where we can store the command outputs.  

We'll use `command-outputs`.

```
ntc@ntc:ansible$ mkdir command-outputs
ntc@ntc:ansible$
```

##### Step 10

Add the required task using `template` to the playbook.

```yaml
      - name: SAVE SH VERSION TO FILE
        template: 
          src: basic-copy.j2
          dest: ./command-outputs/show_version.txt
```

##### Step 11

Execute the playbook.

##### Step 12

Make the required changes to save command output for all 3 CSR devices.

(1) Change `hosts: csr1` to `hosts: iosxe`


(2) Add a variable to the `dest` filename in the `template` module task:

```yaml
dest: ./command-outputs/{{ inventory_hostname}}-show_version.txt
```

