## Lab 5 - Backup and Restore Network Configurations

This lab will show how to use Ansible to manage network device configurations and focuses on the process of backing up and re-storing and deploying full configuration files.

We'll use two main modules to do this:  one that is used to backup the configurations (ntc_show_command) and another that is used to deploy the configurations (NAPALM).

### Task 1 - Backup Configurations

In this task, you will save and backup the current running configuration of all of your devices.

##### Step 1

Within the `ansible` directory, create a new directory called `backups`.

```
ntc@ntc:~/ansible$ mkdir backups
ntc@ntc:~/ansible$ 
```

Additionally, in the same `ansible` directory, create a playbook called `backup-restore.yml`

```
ntc@ntc:~/ansible$ touch backup-restore.yml
ntc@ntc:~/ansible$ 
```

##### Step 2

Open the newly created playbook in your text editor. 

Create a play that'll be executed against **all** hosts defined in the inventory file.

```yaml
---

  - name: BACKUP
    hosts: all
    connection: local
    gather_facts: no

```

##### Step 3

Add a variable in your playbook called `config`.  It should be a dictionary that contains 4 key-value pairs.  The keys should map to an OS and the value should be the command required to gather the existing running configuration.

```yaml
---
  
  - name: BACKUP
    hosts: all
    connection: local
    gather_facts: no
    tags: backup

    vars:
      config:
        eos: show run
        ios: show run
        nxos: show run
        junos: show config

```

By making an object like this, it'll allow us to use a single task to backup all configuration instead of neededing a task/pay per OS!

##### Step 4

Add a task to backup the running configuration using the module called `ntc_show_command`. 

All backup files should be saved locally inside the `backups` directory.


```yaml
---
  
  - name: BACKUP
    hosts: all
    connection: local
    gather_facts: no

    vars:
      config:
        eos: show run
        ios: show run
        nxos: show run
        junos: show config

    tasks:

      - name: BACKUP CONFIGS
        ntc_show_command:
          host={{ inventory_hostname }}
          username={{ un }}
          password={{ pwd }}
          command={{ config[os] }}
          local_file=./backups/{{ inventory_hostname }}.cfg
          platform={{ vendor }}_{{ os }}

```

**Pay attention to how we are using variables for the `platform` parameter**.  It's similar to what we did for the `config` command.

Supported platforms for this module actually matches anything Netmiko supports, e.g. vendor_os like cisco_ios, cisco_nxos, juniper_junos, arista_eos, etc.  Since we have those variables pre-built in our inventory file, we can use them as defined in the output above.

Save and Execute the playbook.

```
ntc@ntc:ansible$ ansible-playbook -i inventory backup-restore.yml 
```

You will see the following output during execution (this output doesn't include Nexus):

```
ntc@ntc:ansible$ ansible-playbook -i inventory backup-restore.yml 

PLAY [BACKUP] *************************************************************************************************

TASK [BACKUP CONFIGS] *****************************************************************************************
ok: [vmx7]
ok: [eos-spine2]
ok: [eos-leaf1]
ok: [eos-leaf2]
ok: [eos-spine1]
ok: [vmx8]
ok: [vmx9]
ok: [nxos-spine1]
ok: [nxos-spine2]
ok: [csr1]
ok: [csr2]
ok: [csr3]

PLAY RECAP ****************************************************************************************************
csr1                       : ok=1    changed=0    unreachable=0    failed=0   
csr2                       : ok=1    changed=0    unreachable=0    failed=0   
csr3                       : ok=1    changed=0    unreachable=0    failed=0   
eos-leaf1                  : ok=1    changed=0    unreachable=0    failed=0   
eos-leaf2                  : ok=1    changed=0    unreachable=0    failed=0   
eos-spine1                 : ok=1    changed=0    unreachable=0    failed=0   
eos-spine2                 : ok=1    changed=0    unreachable=0    failed=0   
nxos-spine1                : ok=1    changed=0    unreachable=0    failed=0   
nxos-spine2                : ok=1    changed=0    unreachable=0    failed=0   
vmx7                       : ok=1    changed=0    unreachable=0    failed=0   
vmx8                       : ok=1    changed=0    unreachable=0    failed=0   
vmx9                       : ok=1    changed=0    unreachable=0    failed=0   

ntc@ntc:ansible$ 

```

##### Step 4

Move to the `backups` directory and open the newly created files to verify everything worked as expected.  

Pay particular attention to the IOS configurations.  In these configurations, you'll see two lines at the top of each including:

* `Building configuration...` 
* `Current configuration : 4043 bytes` 

These CANNOT be included when we re-deploy them and push full configs back to each device.  The real reason for this is the `config replace` command being used by NAPALM, which is how we are going to do the config push, does not support having these lines in the config file.

We now need an automated way to remove them from each.

Add two tasks to cleanup the backup configs. While it's only relevant for IOS configs, there is no harm on running this against all devices.

```yaml

      # this goes below the existing tasks

      - name: CLEAN UP CONFIGS 1
        lineinfile: dest=backups/{{ inventory_hostname }}.cfg line="Building configuration..." state=absent
        tags: clean

      - name: CLEAN UP CONFIGS 2
        lineinfile: dest=backups/{{ inventory_hostname }}.cfg regexp="Current configuration .*" state=absent
        tags: clean
```

Notice how there are now tags embedded for each of these tasks.  This allows us to selectively run just these two tasks without having to run the backup task again.


Save the playbook and run it again with the following command.

```
ntc@ntc:~/ansible$ $ ansible-playbook -i inventory backup-restore.yml --tags=clean

```

Full output:

```
ntc@ntc:~/ansible$ ansible-playbook -i inventory backup-restore.yml --tags=clean

PLAY [BACKUP] *********************************************************

TASK [CLEAN UP CONFIGS 1] ******************************************************
ok: [vmx1]
ok: [eos-spine1]
ok: [eos-leaf1]
ok: [eos-leaf2]
ok: [eos-spine2]
ok: [vmx2]
changed: [csr2]
ok: [vmx3]
changed: [csr1]
changed: [csr3]

TASK [CLEAN UP CONFIGS 2] ******************************************************
ok: [eos-spine1]
ok: [eos-spine2]
ok: [eos-leaf2]
ok: [eos-leaf1]
ok: [vmx1]
ok: [vmx2]
changed: [csr1]
ok: [vmx3]
changed: [csr3]
changed: [csr2]

PLAY RECAP *********************************************************************
csr1                       : ok=2    changed=2    unreachable=0    failed=0   
csr2                       : ok=2    changed=2    unreachable=0    failed=0   
csr3                       : ok=2    changed=2    unreachable=0    failed=0   
eos-leaf1                  : ok=2    changed=0    unreachable=0    failed=0   
eos-leaf2                  : ok=2    changed=0    unreachable=0    failed=0   
eos-spine1                 : ok=2    changed=0    unreachable=0    failed=0   
eos-spine2                 : ok=2    changed=0    unreachable=0    failed=0   
vmx1                       : ok=2    changed=0    unreachable=0    failed=0   
vmx2                       : ok=2    changed=0    unreachable=0    failed=0   
vmx3                       : ok=2    changed=0    unreachable=0    failed=0   

ntc@ntc:~/ansible$

```

Open one or more of the new configuration files and a take look at them and notice how those lines are gone from the files.


### Task 2 - Restore Configuration 

##### Step 1

Create a new play in the playbook.  This requires a new play definition.  For the first execution, limit it to the IOS devices:

```yaml
  - name: DEPLOY CONFIGS
    hosts: iosxe
    connection: local
    gather_facts: no
```


##### Step 2

Using `napalm_install_config`, push back these configurations. Since we didn't change anything from the original backup, the task result should be idempotent i.e. no change should actually occur.

Additionally, ensure you use a "tag" called "push" for this new play so we can just run this play.

The task looks like this for now:

```yaml

  - name: DEPLOY CONFIGS
    hosts: iosxe
    connection: local
    gather_facts: no
    tags: push

    tasks:

      - name: PUSH CONFIGS
        napalm_install_config:
          hostname={{ inventory_hostname }}
          username={{ un }}
          password={{ pwd }}
          config_file=backups/{{ inventory_hostname }}.cfg
          replace_config=true
          commit_changes=true
          dev_os=ios
```

##### Step 3

Execute just this new play:

```
ntc@ntc:~/ansible$ ansible-playbook -i inventory backup-restore.yml --tags=push

PLAY [BACKUP] ******************************************************************

PLAY [DEPLOY CONFIGS] **********************************************************

TASK [PUSH CONFIGS] ************************************************************
ok: [csr3]
ok: [csr1]
ok: [csr2]

PLAY RECAP *********************************************************************
csr1                       : ok=1    changed=0    unreachable=0    failed=0   
csr2                       : ok=1    changed=0    unreachable=0    failed=0   
csr3                       : ok=1    changed=0    unreachable=0    failed=0  
```


The full playbook should look like this for now:

```yaml
---
  
  - name: BACKUP
    hosts: all
    connection: local
    gather_facts: no

    vars:
      config:
        eos: show run
        ios: show run
        nxos: show run
        junos: show config

    tasks:

      - name: BACKUP CONFIGS
        ntc_show_command:
          host={{ inventory_hostname }}
          username={{ un }}
          password={{ pwd }}
          command={{ config[os] }}
          local_file=./backups/{{ inventory_hostname }}.cfg
          platform={{ vendor }}_{{ os }}

      # this goes below the existing tasks

      - name: CLEAN UP CONFIGS 1
        lineinfile: dest=backups/{{ inventory_hostname }}.cfg line="Building configuration..." state=absent
        tags: clean

      - name: CLEAN UP CONFIGS 2
        lineinfile: dest=backups/{{ inventory_hostname }}.cfg regexp="Current configuration .*" state=absent
        tags: clean

  - name: DEPLOY CONFIGS
    hosts: iosxe
    connection: local
    gather_facts: no
    tags: push

    tasks:

      - name: PUSH CONFIGS
        napalm_install_config:
          hostname={{ inventory_hostname }}
          username={{ un }}
          password={{ pwd }}
          config_file=backups/{{ inventory_hostname }}.cfg
          replace_config=true
          commit_changes=true
          dev_os=ios
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
dev_os=ios
```

We need to update this to be the following since we already have the `os` pre-defined as a group based variable:

```
dev_os={{ os }}
```

##### Step 6

Execute the push task again:

```
ntc@ntc:~/ansible$ ansible-playbook -i inventory backup-restore.yml --tags=push

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

**IMPORTANT**

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

Update the napalm task for the following:
* Save the diffs to a file such that we can see the changes that will get applied
* Do not commit the changes since we just want to see the diffs

First, create a new directory called `diffs` in the `ansible` directory.

```
ntc@ntc:~/ansible$ mkdir diffs
ntc@ntc:~/ansible$ 
```

This directory will store all diffs that will eventually get applied to the devices.

Now update the napalm task with the two required changes.

```
          commit_changes=false
          diff_file=diffs/{{ inventory_hostname }}.diffs
```

This will ensure the changes are not applied, but we will still get back the diffs on what will be applied on the next commit.


##### Step 9

Save and re-run the playbook (just the push task).  

Notice we added a new flag to the command being used called `--limit`.  Since we added `eos` in the previous step and only made changes to the CSR routers, we can use `limit` to limit the scope of this job to just the Cisco IOS CSR devices.

```
ntc@ntc:~/ansible$ ansible-playbook -i inventory backup-restore.yml --tags=push --limit iosxe
```



```
ntc@ntc:~/ansible$ ansible-playbook -i inventory backup-restore.yml --tags=push --limit iosxe

PLAY [BACKUP and PUSH] **********************************************

TASK: [PUSH MODIFIED CONFIGS] *********************************************************
changed: [csr1]
changed: [csr3]
changed: [csr2]

PLAY RECAP ********************************************************************
csr1                       : ok=1    changed=0   unreachable=0    failed=0   
csr2                       : ok=1    changed=0    unreachable=0    failed=0   
csr3                       : ok=1    changed=0    unreachable=0    failed=0   

```

Note how are they are now __changed__.

##### Step 10

Navigate to the `diffs` directory and open the diff files. 

For example, `csr1.diffs` will look like this.

```
+interface Loopback10
 +description Done with Ansible
 +ip address 1.1.1.1 255.255.255.0
```

Feel free to SSH to the devices to ensure the configs are not yet applied.

##### Step 11

Update the playbook to commit these new configurations.

Simply update `commit_changes` to be **true**.

```
          commit_changes=true
```

##### Step 12

Save and Run the playbook.

```
ntc@ntc:~/ansible$ ansible-playbook -i inventory backup-restore.yml --tags=push --limit iosxe
```

SSH to the devices and ensure the configs are applied.


##### Step 13

Remove a particular configuration from the config files being used and see how there is not any "no" commands being applied.  While doing this, set commit_changes=False and view the diffs first before applying.

##### Check

Full and final playbook will look like this:

```yaml
---
  
  - name: BACKUP
    hosts: all
    connection: local
    gather_facts: no

    vars:
      config:
        eos: show run
        ios: show run
        nxos: show run
        junos: show config

    tasks:

      - name: BACKUP CONFIGS
        ntc_show_command:
          host={{ inventory_hostname }}
          username={{ un }}
          password={{ pwd }}
          command={{ config[os] }}
          local_file=./backups/{{ inventory_hostname }}.cfg
          platform={{ vendor }}_{{ os }}

      # this goes below the existing tasks

      - name: CLEAN UP CONFIGS 1
        lineinfile: dest=backups/{{ inventory_hostname }}.cfg line="Building configuration..." state=absent
        tags: clean

      - name: CLEAN UP CONFIGS 2
        lineinfile: dest=backups/{{ inventory_hostname }}.cfg regexp="Current configuration .*" state=absent
        tags: clean

  - name: DEPLOY CONFIGS
    hosts: iosxe,eos
    connection: local
    gather_facts: no
    tags: push

    tasks:

      - name: PUSH CONFIGS
        napalm_install_config:
          hostname={{ inventory_hostname }}
          username={{ un }}
          password={{ pwd }}
          config_file=backups/{{ inventory_hostname }}.cfg
          replace_config=true
          commit_changes=true
          dev_os=ios
```


  
