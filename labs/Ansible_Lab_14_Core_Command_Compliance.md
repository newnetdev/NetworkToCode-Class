## Lab 14 - Continuous Compliance with IOS

This lab introduces a methodology to perform real-time validation and compliance of network configuration and operational state.

### Task 1

In order to perform any type of compliance, we must first gather data from the device.  We'll do this with the `_command` module similar to the last few labs.

##### Step 1

Create a new playbook called `compliance-ios.yml` in the `ansible` directory.  

Use the following playbook to gather `show version` for the IOS devices.

```yaml
---

  - name: IOS COMPLIANCE
    hosts: iosxe
    connection: network_cli
    gather_facts: no


    tasks:

      - name: IOS show version
        ios_command:
          commands: 
            - show version
        register: output

```

##### Step 2

Add a task that will _assert_ that version "16.6.2" is running each device and that the config register is set properly to "0x2102".

```yaml
      - name: CHECK OS AND CONFIG REGISTER
        assert:
          that:
           - "'16.6.2' in output['stdout'][0]"
           - "'0x2102' in output['stdout'][0]"

```

Since IOS doesn't return structured data (JSON), we're simply seeing if strings are inside other strings.  

> Note: In an upcoming lab, we'll look at parsing this data and converting it to structured data.

##### Step 3

Execute the playbook.

```
ntc@ntc:ansible$ ansible-playbook -i inventory compliance-ios.yml   

PLAY [IOS COMPLIANCE] ***********************************************************************

TASK [IOS show version] *********************************************************************
ok: [csr1]
ok: [csr2]
ok: [csr3]

TASK [CHECK OS AND CONFIG REGISTER] *********************************************************
ok: [csr1] => {
    "changed": false, 
    "msg": "All assertions passed"
}
ok: [csr2] => {
    "changed": false, 
    "msg": "All assertions passed"
}
ok: [csr3] => {
    "changed": false, 
    "msg": "All assertions passed"
}


PLAY RECAP **********************************************************************************
csr1                       : ok=2    changed=0    unreachable=0    failed=0   
csr2                       : ok=2    changed=0    unreachable=0    failed=0   
csr3                       : ok=2    changed=0    unreachable=0    failed=0   

ntc@ntc:ansible$ 
```

##### Check

Full and final playbook will look like this:

```yaml
---

  - name: IOS COMPLIANCE
    hosts: iosxe
    connection: network_cli
    gather_facts: no


    tasks:

      - name: IOS show version
        ios_command:
          commands:
            - show version
        register: output

      - name: CHECK OS AND CONFIG REGISTER
        assert:
          that:
           - "'16.6.2' in output['stdout'][0]"
           - "'0x2102' in output['stdout'][0]"

```

