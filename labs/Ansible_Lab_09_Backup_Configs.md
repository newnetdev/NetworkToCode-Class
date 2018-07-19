## Lab 09 - Backup and Restore Network Configurations Part 1

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

Additionally, in the same `ansible` directory, create a playbook called `backup.yml`

```
ntc@ntc:~/ansible$ touch backup.yml
ntc@ntc:~/ansible$ 
```

##### Step 2

Open the newly created playbook in your text editor. 

Create a play that'll be executed against **all** hosts defined in the inventory file.

```yaml
---
  
  - name: BACKUP CONFIGURATIONS
    hosts: all
    gather_facts: no


```

##### Step 3

Add a variable in your playbook called `backup_command`.  It should be a dictionary that contains 4 key-value pairs.  The keys should map to an OS and the value should be the command required to gather the existing running configuration.

```yaml
---
  
  - name: BACKUP CONFIGURATIONS
    hosts: all
    gather_facts: no

    vars:
      backup_command:
        eos: show run
        ios: show run
        nxos: show run
        junos: show configuration

```

By making an object like this, it'll allow us to use a single task to backup all configuration instead of needing a task/play per OS!


##### Step 4

Since, we're using a 3rd party module, credentials and connection properties are handled a little differently.  We need to pass them into the module.

Add a variable to handle the login to the devices. Often referred to as a provider variable, this is a dictionary that can be passed to the `provider` parameter of the `ntc` and `napalm` modules.


``` yaml
---
  
  - name: BACKUP CONFIGURATIONS
    hosts: all
    gather_facts: no

    vars:
      backup_command:
        eos: show run
        ios: show run
        nxos: show run
        junos: show configuration
      connection_details:
        username: "{{ ansible_user }}"
        password: "{{ ansible_ssh_pass }}"
        host: "{{ inventory_hostname }}"
        

```



##### Step 5

Add a task to backup the running configuration using the module called `ntc_show_command`. 

All backup files should be saved locally inside the `backups` directory.


```yaml
---
  
  - name: BACKUP CONFIGURATIONS
    hosts: all
    gather_facts: no

    vars:
      backup_command:
        eos: show run
        ios: show run
        nxos: show run
        junos: show configuration
      connection_details:
        username: "{{ ansible_user }}"
        password: "{{ ansible_ssh_pass }}"
        host: "{{ inventory_hostname }}"

    tasks:

      - name: BACKUP CONFIGS FOR ALL DEVICES
        ntc_show_command:
          provider: "{{ connection_details }}"
          command: "{{ backup_command[ansible_network_os] }}"
          local_file: "./backups/{{ inventory_hostname }}.cfg"
          platform: "{{ ntc_vendor }}_{{ ansible_network_os }}"

```

**Pay attention to how we are using variables for the `platform` parameter**.  It's similar to what we did for the `config` command.

Supported platforms for this module actually matches anything Netmiko supports, e.g. vendor_os like cisco_ios, cisco_nxos, juniper_junos, arista_eos, etc.  Since we have those variables pre-built in our inventory file, we can use them as defined in the output above.

Save and Execute the playbook.

```
ntc@ntc:ansible$ ansible-playbook -i inventory backup.yml 
```

You will see the following output during execution (this output doesn't include Nexus):

```
ntc@ntc:ansible$ ansible-playbook -i inventory backup.yml 

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

##### Step 6

Move to the `backups` directory and open the newly created files to verify everything worked as expected.  

Pay particular attention to the IOS configurations.  In these configurations, you'll see two lines at the top of each including:

* `Building configuration...` 
* `Current configuration : 4043 bytes` 

These CANNOT be included when we re-deploy them and push full configs back to each device.  This is not supported by IOS (you can try copying and pasting a full config from the CLI--you'll see this first hand)

We need an automated way to remove them from each.

##### Step 7

Add two tasks to cleanup the backup configs. While it's only relevant for IOS configs, there is no harm on running this against all devices.

```yaml

      # this goes below the existing tasks

      - name: CLEAN UP IOS CONFIGS - LINE 1
        lineinfile:
          dest: ./backups/{{ inventory_hostname }}.cfg
          line: "Building configuration..." 
          state: absent
        tags: clean

      - name: CLEAN UP IOS CONFIGS - LINE 2
        lineinfile:
          dest: ./backups/{{ inventory_hostname }}.cfg
          regexp: "Current configuration .*"
          state: absent
        tags: clean
```

Notice how there are now tags embedded for each of these tasks.  This allows us to selectively run just these two tasks without having to run the backup task again.

##### Step 8


Save the playbook and run it again with the following command.

```
ntc@ntc:~/ansible$ $ ansible-playbook -i inventory backup.yml --tags=clean

```

Full output:

```
ntc@ntc:~/ansible$ ansible-playbook -i inventory backup.yml --tags=clean
```

Relevant output:

```

TASK [CLEAN UP IOS CONFIGS LINE 1] ******************************************************
ok: [vmx7]
ok: [eos-spine1]
ok: [eos-leaf1]
ok: [eos-leaf2]
ok: [eos-spine2]
ok: [vmx8]
changed: [csr2]
ok: [vmx9]
changed: [csr1]
changed: [csr3]

TASK [CLEAN UP IOS CONFIGS LINE 2] ******************************************************
ok: [eos-spine1]
ok: [eos-spine2]
ok: [eos-leaf2]
ok: [eos-leaf1]
ok: [vmx7]
ok: [vmx8]
changed: [csr1]
ok: [vmx9]
changed: [csr3]
changed: [csr2]
```

Open one or more of the new configuration files and a take look at them and notice how those lines are gone from the files.

##### Step 9

At the top of your playbook are two variables: `backup_command` and `connection_details`.  It's not great practice to keep variables hard-coded in your playbook as you cannot re-use them in other playbooks or areas of your project.

Re-locate both of these variables to `group_vars/all.yml`.

The final updated playbook should look like this:

```yaml
---
  
  - name: BACKUP CONFIGURATIONS
    hosts: all
    gather_facts: no

    tasks:

      - name: BACKUP CONFIGS FOR ALL DEVICES
        ntc_show_command:
          provider: "{{ connection_details }}"
          command: "{{ backup_command[ansible_network_os] }}"
          local_file: "./backups/{{ inventory_hostname }}.cfg"
          platform: "{{ ntc_vendor }}_{{ ansible_network_os }}"

      - name: CLEAN UP IOS CONFIGS - LINE 1
        lineinfile:
          dest: ./backups/{{ inventory_hostname }}.cfg
          line: "Building configuration..." 
          state: absent
        tags: clean

      - name: CLEAN UP IOS CONFIGS - LINE 2
        lineinfile:
          dest: ./backups/{{ inventory_hostname }}.cfg
          regexp: "Current configuration .*"
          state: absent
        tags: clean


```

And `group_vars/all.yml` should now have both variables:

```yaml
---

backup_command:
  eos: show run
  ios: show run
  nxos: show run
  junos: show configuration
connection_details:
  username: "{{ ansible_user }}"
  password: "{{ ansible_ssh_pass }}"
  host: "{{ inventory_hostname }}"

```


Note: in future labs, we'll see how you can also backup configurations using "core" modules.  We started with the 3rd party module because it's possible within a single task for more than one vendor.

