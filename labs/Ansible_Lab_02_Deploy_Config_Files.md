## Lab 2 - Deploying Configs From a File

In the last lab, you deployed configurations while hard-coding commands in a playbook.  In this lab, you will deploy from a pre-built configuration file.

##### Step 1

Create a sub-directory called `configs` **inside** the `ansible` directory.  After creating it, navigate inside it:

```
ntc@ntc:ansible$ mkdir configs
ntc@ntc:ansible$ cd configs
ntc@ntc:configs$

```

##### Step 2

Create two files that will contain the SNMP configuration - one for Cisco and one for Juniper respectively.

```
ntc@ntc:configs$ touch junos-snmp.cfg 
ntc@ntc:configs$ touch ios-snmp.cfg
ntc@ntc:configs$
```

##### Step 3

Open the `ios-snmp.cfg` file in your text editor and copy the following configuration into it:

```
snmp-server community ntc-course RO
snmp-server location NYC_HQ        
snmp-server contact JOHN_SMITH     
                                   
```

Save this file.


##### Step 4

Now open `junos-snmp.cfg` in a text editor and copy the following `junos` snmp configuration commands into it.

```
set snmp location NYC_HQ
set snmp contact JOHN_SMITH
set snmp community public authorization read-only
```

Save this file.

##### Step 5

Navigate back to the `ansible` directory and create a new playbook file.

```
ntc@ntc:ansible$ touch snmp-config-02.yml
ntc@ntc:ansible$
```

##### Step 6

Open this file with a text editor and create two plays similar to **Lab 1** to deploy the changes. This time, however, we will use the source file to deploy the configuration instead of using commands inside the playbook.


```yaml
---

  - name: PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS
    hosts: iosxe
    connection: local
    gather_facts: no

    tasks:

      - name: TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES
        ios_config:
          src: ./configs/ios-snmp.cfg

  - name: PLAY 2 - DEPLOYING SNMP CONFIGURATIONS ON JUNOS
    hosts: vmx
    connection: local
    gather_facts: no

    tasks:

      - name: TASK 1 in PLAY 2 - ENSURE SNMP COMMANDS EXIST ON JUNOS DEVICES
        junos_config:
          src: ./configs/junos-snmp.cfg
    

```

##### Step 7

Run the playbook.


```
ntc@ntc:ansible$ ansible-playbook -i inventory snmp-config-02.yml
PLAY [PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS] **********************************************************

TASK [TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES] *******************************************
ok: [csr2]
ok: [csr1]
ok: [csr3]

PLAY [PLAY 2 - DEPLOYING SNMP CONFIGURATIONS ON JUNOS] ********************************************************

TASK [TASK 1 in PLAY 2 - ENSURE SNMP COMMANDS EXIST ON JUNOS DEVICES] *****************************************
ok: [vmx8]
ok: [vmx9]
ok: [vmx7]

PLAY RECAP ****************************************************************************************************
csr1                       : ok=1    changed=0    unreachable=0    failed=0   
csr2                       : ok=1    changed=0    unreachable=0    failed=0   
csr3                       : ok=1    changed=0    unreachable=0    failed=0   
vmx7                       : ok=1    changed=0    unreachable=0    failed=0   
vmx8                       : ok=1    changed=0    unreachable=0    failed=0   
vmx9                       : ok=1    changed=0    unreachable=0    failed=0   

ntc@ntc:ansible$ 
```

You should see zero changes as these configs are the same configs that were deployed in the first lab.  Feel free to make a change to the config files and re-run the playbook.
