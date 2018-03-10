## Lab 3 - Using Check Mode and Verbosity

This lab builds on the first lab you did with sending SNMP configurations to network devices.

### Task 1 - Using Verbosity

##### Step 1

Copy your original playbook called `snmp-config-01.yml` to `snmp-config-03.yml`

```
ntc@ntc:ansible$ cp snmp-config-01.yml snmp-config-03.yml
ntc@ntc:ansible$
```

> Note: the `cp` command copies a file in Linux.

##### Step 2

Open the new playbook in your text editor.

##### Step 3

Remove the second play (Junos), so you're left with the following in your playbook:

> Note: if you prefer using Junos, you can following allow making the appropriate changes with Junos CLI commands instead of IOS.

```yaml
---

  - name: PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS
    hosts: iosxe
    connection: local
    gather_facts: no

    tasks:

      - name: TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES
        ios_config:
          provider:
          commands:
            - snmp-server community ntc-course RO
            - snmp-server location NYC_HQ
            - snmp-server contact JOHN_SMITH

```

##### Step 4

Verify the playbook is still functional (syntax, spacing) by executing the playbook.

```
ntc@ntc:ansible$ ansible-playbook -i inventory snmp-config-03.yml 

# output omitted
```

##### Step 5

Add a new SNMP command to the `commands` parameter so that you have the following 4 commands in the list:

```yaml
commands:
  - snmp-server community ntc-course RO
  - snmp-server community supersecret RW
  - snmp-server location NYC_HQ
  - snmp-server contact JOHN_SMITH
```

Save the playbook.

##### Step 6

Execute the playbook, but this time use the `-v` flag.  This will run the playbook in verbose mode showing JSON data that is returned by every module.

> Note: every module returns JSON data and you can view that data by running the playbook in verbose mode.  You can add more levels of verbosity using doing `-vv`, `-vvv`, etc. up to 5 v's.


The core `<os>_config` modules will return the commands being sent to the device when running the playbook in verbose mode.  

Let's take a look:

```
ntc@ntc:ansible$ ansible-playbook -i inventory snmp-config-03.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS] **********************************************************

TASK [TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES] *******************************************
changed: [csr1] => {"banners": {}, "changed": true, "commands": ["snmp-server community supersecret RW"], "failed": false, "updates": ["snmp-server community supersecret RW"]}
changed: [csr2] => {"banners": {}, "changed": true, "commands": ["snmp-server community supersecret RW"], "failed": false, "updates": ["snmp-server community supersecret RW"]}
changed: [csr3] => {"banners": {}, "changed": true, "commands": ["snmp-server community supersecret RW"], "failed": false, "updates": ["snmp-server community supersecret RW"]}

PLAY RECAP ****************************************************************************************************
csr1                       : ok=1    changed=1    unreachable=0    failed=0   
csr2                       : ok=1    changed=1    unreachable=0    failed=0   
csr3                       : ok=1    changed=1    unreachable=0    failed=0   

ntc@ntc:ansible$ 

```

This is telling us that Ansible is only sending ONE command to the device -- Ansible is NOT sending every command in the playbook because, by default, the _config modules are comparing the commands against a "show run" on the device.

##### Step 7

Re-run the playbook once more verifying idempotency, e.g. no changes should be made.

```
ntc@ntc:ansible$ ansible-playbook -i inventory snmp-config-03.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS] **********************************************************

TASK [TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES] *******************************************
ok: [csr1] => {"changed": false, "failed": false}
ok: [csr3] => {"changed": false, "failed": false}
ok: [csr2] => {"changed": false, "failed": false}

PLAY RECAP ****************************************************************************************************
csr1                       : ok=1    changed=0    unreachable=0    failed=0   
csr2                       : ok=1    changed=0    unreachable=0    failed=0   
csr3                       : ok=1    changed=0    unreachable=0    failed=0   
```

As you can see no commands were sent to the devices.

### Task 2 - Using Check Mode with Verbosity

You've now seen how to see what commands Ansible is sending to the devices.  What if you want to see what Ansible _will do_? Luckily, Ansible supports a "dry run" or "check mode" to see what commands _would_ get sent if the playbook is run.  This is called **check mode** and you use the `-C` or `--check` flags on the command line to use check mode.

##### Step 1

Change the SNMP command for location to be "NYC_HQ_COLO"

```yaml
- snmp-server location NYC_HQ_COLO
```

So that the complete playbook looks like this:

```yaml
---

  - name: PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS
    hosts: iosxe
    connection: local
    gather_facts: no

    tasks:

      - name: TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES
        ios_config:
          commands:
            - snmp-server community ntc-course RO
            - snmp-server community supersecret RW
            - snmp-server location NYC_HQ_COLO
            - snmp-server contact JOHN_SMITH

```


##### Step 2

Execute the playbook just with the "check mode" flag set:

```
ntc@ntc:ansible$ ansible-playbook -i inventory snmp-config-03.yml --check

PLAY [PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS] **********************************************************

TASK [TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES] *******************************************
changed: [csr3]
changed: [csr1]
changed: [csr2]

PLAY RECAP ****************************************************************************************************
csr1                       : ok=1    changed=1    unreachable=0    failed=0   
csr2                       : ok=1    changed=1    unreachable=0    failed=0   
csr3                       : ok=1    changed=1    unreachable=0    failed=0   

ntc@ntc:ansible$ 
```

Notice that this says "changed" for each device, but no change actually took place!!

##### Step 3

Verify the "old" configuration is still there by SSH'ing into CSR1:

```
csr1#
csr1#show run | inc snmp-server
snmp-server community ntc-course RO
snmp-server community supersecret RW
snmp-server location NYC_HQ
snmp-server contact JOHN_SMITH
csr1#
```

##### Step 4

**READ-ONLY STEP**

When you see "changed" when you run a playbook in check mode, it's telling you a change _will_ occur when you don't run it in check mode.  Check mode is often used at the beginning of change windows seeing if a change would occur.

Note that you saw verbose mode returns what commands are sent to the device and check mode returns if a change will be made. If you combine using check mode **and** verbose mode when you execute a playbook, you will see the commands that will get sent!

Let's try it.

##### Step 5

Run the playbook with check mode and verbose mode.

```
ntc@ntc:ansible$ ansible-playbook -i inventory snmp-config-03.yml --check -v
Using /etc/ansible/ansible.cfg as config file

PLAY [PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS] **********************************************************

TASK [TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES] *******************************************
changed: [csr3] => {"banners": {}, "changed": true, "commands": ["snmp-server location NYC_HQ_COLO"], "failed": false, "updates": ["snmp-server location NYC_HQ_COLO"]}
changed: [csr2] => {"banners": {}, "changed": true, "commands": ["snmp-server location NYC_HQ_COLO"], "failed": false, "updates": ["snmp-server location NYC_HQ_COLO"]}
changed: [csr1] => {"banners": {}, "changed": true, "commands": ["snmp-server location NYC_HQ_COLO"], "failed": false, "updates": ["snmp-server location NYC_HQ_COLO"]}

PLAY RECAP ****************************************************************************************************
csr1                       : ok=1    changed=1    unreachable=0    failed=0   
csr2                       : ok=1    changed=1    unreachable=0    failed=0   
csr3                       : ok=1    changed=1    unreachable=0    failed=0   

ntc@ntc:ansible$ 
```

You now know which commands are going to get sent to the device.  This is super-handy when troubleshooting syntax issues, typos, and bad commands.

##### Step 6

Now that you, as a network engineer, "approved" the commands that will get sent to the device, you can remove check mode (feel free to keep verbose mode).

```
ntc@ntc:ansible$ ansible-playbook -i inventory snmp-config-03.yml -v        
Using /etc/ansible/ansible.cfg as config file

PLAY [PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS] **********************************************************

TASK [TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES] *******************************************
changed: [csr1] => {"banners": {}, "changed": true, "commands": ["snmp-server location NYC_HQ_COLO"], "failed": false, "updates": ["snmp-server location NYC_HQ_COLO"]}
changed: [csr3] => {"banners": {}, "changed": true, "commands": ["snmp-server location NYC_HQ_COLO"], "failed": false, "updates": ["snmp-server location NYC_HQ_COLO"]}
changed: [csr2] => {"banners": {}, "changed": true, "commands": ["snmp-server location NYC_HQ_COLO"], "failed": false, "updates": ["snmp-server location NYC_HQ_COLO"]}

PLAY RECAP ****************************************************************************************************
csr1                       : ok=1    changed=1    unreachable=0    failed=0   
csr2                       : ok=1    changed=1    unreachable=0    failed=0   
csr3                       : ok=1    changed=1    unreachable=0    failed=0   

ntc@ntc:ansible$ 
```

##### Step 7

Finally, run the playbook one more time for verifying idempotency.

```
ntc@ntc:ansible$ ansible-playbook -i inventory snmp-config-03.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS] **********************************************************

TASK [TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES] *******************************************
ok: [csr3] => {"changed": false, "failed": false}
ok: [csr1] => {"changed": false, "failed": false}
ok: [csr2] => {"changed": false, "failed": false}

PLAY RECAP ****************************************************************************************************
csr1                       : ok=1    changed=0    unreachable=0    failed=0   
csr2                       : ok=1    changed=0    unreachable=0    failed=0   
csr3                       : ok=1    changed=0    unreachable=0    failed=0   

ntc@ntc:ansible$
```

Nice work.

