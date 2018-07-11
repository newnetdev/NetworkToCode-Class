## Lab 21 - SNMP Ansible Roles

### Task 1 - Multi-Platform SNMP Role

In this task, you will learn how to create re-usable tasks called roles.  
You will create a role for configuring SNMP communities on both IOS and NXOS.

##### Step 1

In order to create a new role, you need a `roles` sub-directory.  
Create a roles directory within the `ansible` directory.

Now we need a directory that is equal to the role name.  
Our role name is `snmp`, so now create a sub-directory called `snmp` within the `roles` directory.

##### Step 2

In the `snmp` dir, create a new dir called `tasks`.  Within `tasks`, create a file called `main.yml`. 

This is a REQUIRED file within a file.  This is where tasks begin to execute within a role.  

In the `main.yml`, add the following statement:

```yaml
---

- include_tasks: "{{ ansible_network_os }}_deploy.yml"
```

Notice how it's a single include statement.  This will execute a file called `nxos.yml` or `ios.yml`.

Those files need to be created now, but will configure SNMP per OS type.

##### Step 3

Create two new files in the `tasks` sub-directory called `nxos_deploy.yml` and  `ios_deploy.yml`.

It should look like this:

```
.
├── roles
│   ├── snmp
│   │   └── tasks
│   │     ├── ios_deploy.yml
│   │     ├── main.yml
│   │     └── nxos_deploy.yml
```

##### Step 4

Open the `nxos_deploy.yml` file. 

Use the Ansible `nxos_config` module to configure SNMP community strings.

```yaml
---

- name: ENSURE SNMP COMMUNITIES EXIST IN NXOS
  nxos_config:
    commands:
      - "snmp-server community {{ item.community }} group {{ item.group }}"
  with_items: "{{ snmp_communities }}"

```

> Note: here we are using a variable called `snmp_communities` which will be passed by the main playbook executing the role.

##### Step 5

Just like in the last task, open the `ios_deploy.yml` file and use Ansible `ios_config` module to configure SNMP community strings.

```yaml
---

- name: ENSURE SNMP COMMUNITIES EXIST IN IOS
  ios_config:
    commands:
      - "snmp-server community {{ item.community }} {{ item.group }}"
  with_items: "{{ snmp_communities }}"
```

##### Step 6

Finally, we need to create a playbook to actually use this new role.

Create a new playbook called `snmp-role-pb.yml` in your `ansible` directory.

This playbook won't have any direct tasks per se, rather it will call the "snmp" role and execute the tasks within the role.

Notice you can also select two groups from the inventory file using the following line: `hosts: iosxe,nxos`.

```yaml
---

  - name: MULTI-PLATFORM SNMP
    hosts: iosxe,nxos
    gather_facts: no

    roles:
      - role: snmp
        snmp_communities:
          - community: ntc-public
            group: network-operator
          - community: ntc-private
            group: network-admin
```

Notice now as the playbook user, you no longer need to be aware of which tasks are actually performing the change 
or which vendor device is used as that's all taken care of within the role.


##### Step 7

Save and run the playbook. 

You will see the output below.


```
ntc@ntc:~/ansible$ ansible-playbook -i inventory snmp-role-pb.yml
```

```
PLAY [MULTI-PLATFORM SNMP] *****************************************************

TASK [snmp : include] **********************************************************
included: /home/ntc/ansible/roles/snmp/tasks/ios_deploy.yml for csr1, csr2, csr3
included: /home/ntc/ansible/roles/snmp/tasks/nxos_deploy.yml for nxos-spine1, nxos-spine2

TASK [snmp : ENSURE SNMP COMMUNITIES EXIST IN IOS] *****************************
changed: [csr3] => (item={u'group': u'network-operator', u'community': u'ntc-public'})
changed: [csr2] => (item={u'group': u'network-operator', u'community': u'ntc-public'})
changed: [csr1] => (item={u'group': u'network-operator', u'community': u'ntc-public'})
changed: [csr2] => (item={u'group': u'network-admin', u'community': u'ntc-private'})
changed: [csr3] => (item={u'group': u'network-admin', u'community': u'ntc-private'})
changed: [csr1] => (item={u'group': u'network-admin', u'community': u'ntc-private'})

TASK [snmp : ENSURE SNMP COMMUNITIES EXIST IN NXOS] ****************************
changed: [nxos-spine2] => (item={u'group': u'network-operator', u'community': u'ntc-public'})
changed: [nxos-spine1] => (item={u'group': u'network-operator', u'community': u'ntc-public'})
changed: [nxos-spine2] => (item={u'group': u'network-admin', u'community': u'ntc-private'})
changed: [nxos-spine1] => (item={u'group': u'network-admin', u'community': u'ntc-private'})

PLAY RECAP *********************************************************************
csr1                       : ok=2    changed=1    unreachable=0    failed=0
csr2                       : ok=2    changed=1    unreachable=0    failed=0
csr3                       : ok=2    changed=1    unreachable=0    failed=0
nxos-spine1                : ok=2    changed=1    unreachable=0    failed=0
nxos-spine2                : ok=2    changed=1    unreachable=0    failed=0
 
```


As you can see this is a very powerful concept and allows for the re-use of tasks. 
You _could_ have had each task in the role in the playbook, but now next time you need to update community strings, 
you can easily call this role.
