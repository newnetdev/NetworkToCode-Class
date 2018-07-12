## Lab 13 - Issuing Ping Commands and Saving the Responses

This lab will have you ping a certain amount of destinations from _each_ router.  
Each of the resposnes will then be stored in its own file within a device sub-directory 
meaning we'll end up with a directory name of the hostname, e.g. "csr1" and "csr2" and 
in each directory will be files such as "to_8.8.8.8.txt" with the response from that router to that target IP.


##### Step 1


It's not possible to keep typing "mkdir" to create directories manually especially when you want a directory per device.  
This task will have you use the `file` module to auto-create a directory per device.


Create a new playbook called `ping.yml` in the `ansible` directory.  

```yaml
---

  - name: TEST REACHABILITY
    hosts: iosxe
    gather_facts: no

    vars:
      target_ips:
        - "8.8.8.8"
        - "4.4.4.4"
        - "198.6.1.4"
```

##### Step 2

Add a task to that will create a directory for each device inside a `ping-responses` directory.

```yaml

    tasks:

      - name: ENSURE DIRECTORY FOR EACH DEVICE EXISTS
        file:
          path: ./ping-responses/{{ inventory_hostname }}/
          state: directory


```


##### Step 3

Execute the playbook.

```
ntc@ntc:ansible$ ansible-playbook -i inventory ping.yml

PLAY [TEST REACHABILITY] ***************************************************************************

TASK [ENSURE DIRECTORY FOR EACH DEVICE EXISTS] *****************************************************
changed: [csr3]
changed: [csr2]
changed: [csr1]

PLAY RECAP *****************************************************************************************
csr1                       : ok=1    changed=1    unreachable=0    failed=0   
csr2                       : ok=1    changed=1    unreachable=0    failed=0   
csr3                       : ok=1    changed=1    unreachable=0    failed=0   
```

#### Step 4

Verify the directories are created.

```
ntc@ntc:ansible$ tree ping-responses/
ping-responses/
├── csr1
├── csr2
└── csr3

3 directories, 0 files
ntc@ntc:ansible$ 
```

##### Step 5

Add a task that'll loop over `target_ips` and send them to each device.

```yaml
      - name: SEND PING COMMANDS TO DEVICES
        ios_command:
          commands: "ping vrf MANAGEMENT {{ item }} repeat 2"
        loop: "{{ target_ips|flatten(levels=1) }}"
```

Remember, this task plus `target_ips` is equivalent to the following:

```yaml
      - name: SEND PING COMMANDS TO DEVICES
        ios_command:
          commands: "ping vrf MANAGEMENT {{ item }} repeat 2"
        loop:
          - "8.8.8.8"
          - "4.4.4.4"
          - "198.6.1.4"

```

##### Step 6

Execute the playbook.

You'll see the following output, but without seeing the ping responses.

Remember, there are two ways to see the response.  One is to use `-v` and the other is to combine the `register` task attribute and the `debug` module.

```
ntc@ntc:ansible$ ansible-playbook -i inventory ping.yml 

PLAY [TEST REACHABILITY] ***************************************************************************

TASK [ENSURE DIRECTORY FOR EACH DEVICE EXISTS] *****************************************************
ok: [csr3]
ok: [csr1]
ok: [csr2]

TASK [SEND PING COMMANDS TO DEVICES] ***************************************************************
ok: [csr3] => (item=8.8.8.8)
ok: [csr1] => (item=8.8.8.8)
ok: [csr2] => (item=8.8.8.8)
ok: [csr1] => (item=4.4.4.4)
ok: [csr2] => (item=4.4.4.4)
ok: [csr3] => (item=4.4.4.4)
ok: [csr3] => (item=198.6.1.4)
ok: [csr1] => (item=198.6.1.4)
ok: [csr2] => (item=198.6.1.4)

PLAY RECAP *****************************************************************************************
csr1                       : ok=2    changed=0    unreachable=0    failed=0   
csr2                       : ok=2    changed=0    unreachable=0    failed=0   
csr3                       : ok=2    changed=0    unreachable=0    failed=0   

ntc@ntc:ansible$ 
```


##### Step 7

Add the `register` task attribute creating a variable called `ping_responses` and debug the new variable to the terminal.

The updated playbook will look like this:

```yaml
---

  - name: TEST REACHABILITY
    hosts: iosxe
    gather_facts: no

    vars:
      target_ips:
        - "8.8.8.8"
        - "4.4.4.4"
        - "198.6.1.4"

    tasks:

      - name: ENSURE DIRECTORY FOR EACH DEVICE EXISTS
        file:
          path: ./ping-responses/{{ inventory_hostname }}/
          state: directory

      - name: SEND PING COMMANDS TO DEVICES
        ios_command:
          commands: "ping vrf MANAGEMENT {{ item }} repeat 2"
        register: ping_responses
        loop: "{{ target_ips|flatten(levels=1) }}"


      - name: VERIFY REGISTERED VARIABLE
        debug:
          var: ping_responses  
```

##### Step 8

Execute the playbook.

You'll see the following output.  Note: this is a sub-set of the output.

```
tc@ntc:ansible$ ansible-playbook -i inventory ping.yml 

PLAY [TEST REACHABILITY] ***************************************************************************

TASK [ENSURE DIRECTORY FOR EACH DEVICE EXISTS] *****************************************************
ok: [csr2]
ok: [csr3]
ok: [csr1]

TASK [SEND PING COMMANDS TO DEVICES] ***************************************************************
ok: [csr3] => (item=8.8.8.8)
ok: [csr1] => (item=8.8.8.8)
ok: [csr2] => (item=8.8.8.8)
ok: [csr1] => (item=4.4.4.4)
ok: [csr2] => (item=4.4.4.4)
ok: [csr3] => (item=4.4.4.4)
ok: [csr3] => (item=198.6.1.4)
ok: [csr1] => (item=198.6.1.4)
ok: [csr2] => (item=198.6.1.4)

TASK [VERIFY REGISTERED VARIABLE] ******************************************************************
ok: [csr1] => {
    "ping_responses": {
        "changed": false, 
        "msg": "All items completed", 
        "results": [
            {
                "_ansible_ignore_errors": null, 
                "_ansible_item_result": true, 
                "_ansible_no_log": false, 
                "_ansible_parsed": true, 
                "changed": false, 
                "failed": false, 
                "invocation": {
                    "module_args": {
                        "auth_pass": null, 
                        "authorize": null, 
                        "commands": [
                            "ping vrf MANAGEMENT 8.8.8.8 repeat 2"
                        ], 
                        "host": null, 
                        "interval": 1, 
                        "match": "all", 
                        "password": null, 
                        "port": null, 
                        "provider": null, 
                        "retries": 10, 
                        "ssh_keyfile": null, 
                        "timeout": null, 
                        "username": null, 
                        "wait_for": null
                    }
                }, 
                "item": "8.8.8.8", 
                "stdout": [
                    "Type escape sequence to abort.\nSending 2, 100-byte ICMP Echos to 8.8.8.8, timeout is 2 seconds:\n!!\nSuccess rate is 100 percent (2/2), round-trip min/avg/max = 2/2/2 ms"
                ], 
                "stdout_lines": [
```

We need to understand the datatype of `ping_responses`.

You can see that `ping_responses` is a dictionary, but there is a key called `results`.  `results`  is a list of all the responses - it is a list of dictionaries.

Pay attention to the following two keys within `results`:
  * `results[index]['item']`
  * `results[index]['stdout']`

`item` - is the IP address that is being looped over.  Above shows "8.8.8.8"
`stdout` - this is a list of 1 (because we're sending 1 command in each iteration of the for loop), so `stdout[0]` will be the actual text response.

##### Step 9

Add a debug task to loop over `ping_responses.results` proving how it's possible to access the data.

```yaml
      - name: TEST LOOPING OVER REGISTERED VARIABLE
        debug: 
          var: "{{ item }}"    
        with_items: "{{ ping_responses.results }}"  

 
```

##### Step 10

Save and execute the playbook.  It's recommended to use `--limit csr1` to limit the output so it's easier to read.

```
ntc@ntc:ansible$ ansible-playbook -i inventory ping.yml --limit csr1
```

##### Step 11

Now we have ALL data required in a single variable.  We need a way to create individual files for each response.  

Remember the datatype of `ping_responses.results` is a list of dictionaries and there are two keys that are important, i.e. `item` and `stdout`.

Use the `template` module to create the files.

```yaml
      - name: SAVE OUTPUTS TO INDIVIDUAL FILES
        template: 
          src: basic-copy-2.j2
          dest: TBD
        loop: "{{ ping_responses.results|flatten(levels=1) }}"
```

##### Step 12

Create the template that accesses the response during each iteration of the `loop`. 

Save the template as `basic-copy-2.j2`:

```
{{ item.stdout[0] }}
```

Notice how it's a very basic template -- it's just about understanding the data being looped over in the playbook.


##### Step 13

Update the `dest` parameter within the `template` module.

This is creating filenames such as `to_1.1.1.1.txt`:

```yaml
      - name: SAVE OUTPUTS TO INDIVIDUAL FILES
        template: 
          src: basic-copy-2.j2
          dest: ./ping-responses/{{ inventory_hostname }}/to_{{ item.item }}.txt
        loop: "{{ ping_responses.results|flatten(levels=1) }}"   
```

##### Step 14

Save and execute the playbook.

You should now see all of the files created.  Open a few of them to validate the pings passed or failed.

```
ntc@ntc:ansible$ tree ping-responses/
ping-responses/
├── csr1
│   ├── to_198.6.1.4.txt
│   ├── to_4.4.4.4.txt
│   └── to_8.8.8.8.txt
├── csr2
│   ├── to_198.6.1.4.txt
│   ├── to_4.4.4.4.txt
│   └── to_8.8.8.8.txt
└── csr3
    ├── to_198.6.1.4.txt
    ├── to_4.4.4.4.txt
    └── to_8.8.8.8.txt

3 directories, 9 files
ntc@ntc:ansible$ 
```

##### Check

Full and final playbook will look like this:

```yaml
---

  - name: TEST REACHABILITY
    hosts: iosxe
    gather_facts: no

    vars:
      target_ips:
        - "8.8.8.8"
        - "4.4.4.4"
        - "198.6.1.4"

    tasks:

      - name: ENSURE DIRECTORY FOR EACH DEVICE EXISTS
        file:
          path: ./ping-responses/{{ inventory_hostname }}/
          state: directory

      - name: SEND PING COMMANDS TO DEVICES
        ios_command:
          commands: "ping vrf MANAGEMENT {{ item }} repeat 2"
        register: ping_responses
        loop: "{{ target_ips|flatten(levels=1) }}"

      - name: VERIFY REGISTERED VARIABLE
        debug:
          var: ping_responses

      - name: TEST LOOPING OVER REGISTERED VARIABLE
        debug:
          var: "{{ item }}"
        loop: "{{ ping_responses.results|flatten(levels=1) }}"

      - name: SAVE OUTPUTS TO INDIVIDUAL FILES
        template:
          src: basic-copy-2.j2
          dest: ./ping-responses/{{ inventory_hostname }}/to_{{ item.item }}.txt
        loop: "{{ ping_responses.results|flatten(levels=1) }}"
```