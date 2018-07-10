## Lab 10 - Backup and Restore Network Configurations Part 2

This lab will "restore" the configuration files you previously backed up.

For these two labs, we're using two main modules to do this:  one that is used to backup the configurations (ntc_show_command) and another that is used to deploy the configurations (NAPALM).


### Task 1 - Restore Configuration

##### Step 1

Create a new playbook called `restore.yml`.  In this file, and for the first execution, limit it to the IOS devices:

```yaml
---

  - name: DEPLOY & RESTORE CONFIGS
    hosts: iosxe
    connection: network_cli
    gather_facts: no
```


##### Step 2

Using `napalm_install_config`, push back these configurations. Since we didn't change anything from the original backup, the task result should be idempotent i.e. no change should actually occur.


```yaml
---

  - name: DEPLOY & RESTORE CONFIGS
    hosts: iosxe
    connection: network_cli
    gather_facts: no

    tasks:

      - name: DEPLOY CONFIGURATIONS
        napalm_install_config:
          provider: "{{ connection_details }}"
          config_file: ./backups/{{ inventory_hostname }}.cfg
          replace_config: true
          commit_changes: true
          dev_os: ios

```

##### Step 3

Execute this new play:

```
ntc@ntc:~/ansible$ ansible-playbook -i inventory restore.yml

PLAY [DEPLOY & RESTORE CONFIGS] **********************************************************

TASK [DEPLOY CONFIGURATIONS] ************************************************************
ok: [csr3]
ok: [csr1]
ok: [csr2]

PLAY RECAP *********************************************************************
csr1                       : ok=1    changed=0    unreachable=0    failed=0
csr2                       : ok=1    changed=0    unreachable=0    failed=0
csr3                       : ok=1    changed=0    unreachable=0    failed=0
```

Notice how there were NO changes. This is because you just pushed exactly what was already on the device.


The full playbook should look like this for now:

```yaml
---

  - name: DEPLOY & RESTORE CONFIGS
    hosts: iosxe
    connection: network_cli
    gather_facts: no

    tasks:

      - name: DEPLOY CONFIGURATIONS
        napalm_install_config:
          provider: "{{ connection_details }}"
          config_file: ./backups/{{ inventory_hostname }}.cfg
          replace_config: true
          commit_changes: true
          dev_os: ios


```


##### Step 4

Update the play definition of the second play to include another group.  Choose either the **vmx** or **eos** group.

You can add a group in the play definition using the following syntax:

```yaml
hosts: iosxe,eos
```


##### Step 5

Since we are automating more than one group, we need to parametrize the napalm task for the `dev_os`.

The last line in the playbook is as follows:

```
dev_os: ios
```

We need to update this to be the following since we already have the `os` pre-defined as a group based variable:

```yaml
dev_os: "{{ ntc_os }}"
```

##### Step 6

Execute the playbook again:

```
ntc@ntc:~/ansible$ ansible-playbook -i inventory restore.yml

PLAY [BACKUP] ******************************************************************

PLAY [DEPLOY CONFIGS] **********************************************************

TASK [PUSH CONFIGS] ************************************************************
ok: [csr3]
ok: [csr1]
ok: [csr2]
ok: [eos-spine1]
ok: [eos-spine2]
ok: [eos-leaf1]
ok: [eos-leaf2]

PLAY RECAP *********************************************************************
csr1                       : ok=1    changed=0    unreachable=0    failed=0
csr2                       : ok=1    changed=0    unreachable=0    failed=0
csr3                       : ok=1    changed=0    unreachable=0    failed=0
eos-leaf1                  : ok=1    changed=0    unreachable=0    failed=0
eos-leaf2                  : ok=1    changed=0    unreachable=0    failed=0
eos-spine1                 : ok=1    changed=0    unreachable=0    failed=0
eos-spine2                 : ok=1    changed=0    unreachable=0    failed=0
```

**IMPORTANT NOTE AGAIN:**

**Even though you are pushing a full configuration, there are NO changes being applied since we are applying the SAME exact configuration that already exists on the device.**

##### Step 7

Open the stored backup configs inside the `backups` directory and make some changes.

For example, create a new Loopback interface on each IOS device.

Add the following lines on `csr1.cfg`.

```
!
interface Loopback10
 description added by Ansible
 ip address 1.1.1.1 255.255.255.0
!
```

Add the following lines on `csr2.cfg`.

```
!
interface Loopback10
 description added by Ansible
 ip address 2.2.2.2 255.255.255.0
!
```

Add the following lines on `csr3.cfg`.

```
!
interface Loopback10
 description added by Ansible
 ip address 3.3.3.3 255.255.255.0
!
```


##### Step 8

Update the task for the following:
* Save the diffs to a file such that we can see the changes that will get applied
* Do not commit the changes since we just want to see the diffs

First, create a new directory called `diffs` in the `ansible` directory.

```
ntc@ntc:~/ansible$ mkdir diffs
ntc@ntc:~/ansible$
```

This directory will store all diffs that will eventually get applied to the devices.

##### Step 9

Now update the napalm task with the two required changes.

```
          commit_changes: false
          diff_file: ./diffs/{{ inventory_hostname }}.diffs
```

This will ensure the changes are not applied, but we will still get back the diffs on what will be applied on the next commit.

This updated task should look like this:

```yaml
      - name: DEPLOY CONFIGURATIONS
        napalm_install_config:
          provider: "{{ connection_details }}"
          config_file: ./backups/{{ inventory_hostname }}.cfg
          diff_file: ./diffs/{{ inventory_hostname }}.diffs
          replace_config: true
          commit_changes: false
          dev_os: "{{ ntc_os }}"
```

##### Step 10

Save and re-run the playbook using the `limit`  flag.

```
ntc@ntc:~/ansible$ ansible-playbook -i inventory restore.yml --limit iosxe
```

Notice we added a new flag to the command being used called `--limit`.  Since we added `eos` in the previous step and only made changes to the CSR routers, we can use `limit` to limit the scope of this job to just the Cisco IOS CSR devices.

Note how are they are now __changed__.  It doesn't mean this made the change, just that diffs are found and would be changed when commit is true.

##### Step 11

Navigate to the `diffs` directory and open the diff files.

For example, `csr1.diffs` will look like this.

```
+interface Loopback10
 +description Done with Ansible
 +ip address 1.1.1.1 255.255.255.0
```

Feel free to SSH to the devices to ensure the configs are not yet applied.

##### Step 12

Update the playbook to commit these new configurations.

Simply update `commit_changes` to be **true**.

```
          commit_changes: true
```

##### Step 13

Save and Run the playbook.

```
ntc@ntc:~/ansible$ ansible-playbook -i inventory restore.yml --limit iosxe
```

SSH to the devices and ensure the configs are applied.


##### Step 14

Remove a particular configuration from the config files being used and see how there is not any "no" commands being applied.  While doing this, set commit_changes=False and view the diffs first before applying.

##### Step 15

Notice how the playbook has hard-coded the devices to be automated.  As you've seen you can modify this manually or use the "limit" flag to _limit_ the execution to a sub-set of devices.

What if you wanted user input as in always forcing the user to pass in the device or group into the playbook on execution? You can do this with "extra vars".

Update your play definition to this:

```yaml
---

  - name: DEPLOY & RESTORE CONFIGS
    hosts: "{{ device }}"
    connection: network_cli
    gather_facts: no
```

This will require you to pass in a variable called `device` when the playbook runs.

##### Step 16

Re-run the playbook passing in the `device` variable.  You have two options using either the `--extra-vars` (or the `-e` flag).  Here we show an example using `--extra-vars`:

```
ntc@ntc:ansible$ ansible-playbook -i inventory restore.yml --extra-vars="device=csr1"

```


##### Check

Full and final playbook will look like this:

```yaml
---

  - name: DEPLOY & RESTORE CONFIGS
    hosts: "{{ device }}"
    connection: network_cli
    gather_facts: no

    tasks:

      - name: DEPLOY CONFIGURATIONS
        napalm_install_config:
          provider: "{{ connection_details }}"
          config_file: ./backups/{{ inventory_hostname }}.cfg
          diff_file: ./diffs/{{ inventory_hostname }}.diffs
          replace_config: true
          commit_changes: true
          dev_os: "{{ ntc_os }}"


```



