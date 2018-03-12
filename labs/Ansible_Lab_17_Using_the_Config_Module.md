## Lab 17 - Using the Config Module

### Task 1 - Configuring Interfaces

In prior labs, you've used the `src` and `commands` parameters of the `config` modules.  While you can deploy any commands using `src`, `commands` by itself are limited to global configurations.

This task introduces the `parents` parameter when using the `config` module to configure commands that have hierarchy.

##### Step 1

Create a playbook called `config-interfaces.yml` and insert the following into it:

```yaml
---

  - name: CONFIGURING INTERFACES
    hosts: iosxe
    connection: local
    gather_facts: no

    tasks:

    - name: IOS show version
      ios_config:
        parents:
          - interface Loopback200
        commands:
          - ip address 10.200.100.{{ inventory_hostname[-1] }} 255.255.255.255
```

##### Step 2

Save and execute the playbook in verbose mode to see the commands being sent to your devices.

### Task 2 - Diving Deeper into the Config Module Parameters

This task builds on the first and introduces even more parameters that the `config` module supports.

##### Step 1

**MANUAL STEP**

SSH into **csr1** and enter the following commands:

```
config t
line vty 0 30
privilege level 15
exit
aaa new-model
end
```

Keep the SSH session open.


##### Step 2

Create a new playbook called `aaa.yml`.

Use the following playbook as the getting started point to manage a AAA server group of TACACS+ servers.

```yaml
  - name: CONFIGURING AAA SERVER GROUPS
    hosts: csr1
    connection: local
    gather_facts: no

    tasks:
      - name: DEPLOYING AAA GROUP AND IPS 1
        ios_config:
          parents:
            - aaa group server tacacs+ TESTING
          commands:
            - server 1.2.3.4
            - server 2.1.3.4
            - server 3.2.1.4
        tags: starting_config 
```

##### Step 3

Execute the playbook in verbose mode using the "starting_config" tag:

```
ntc@ntc:ansible$ ansible-playbook -i inventory aaa.yml --tags=starting_config -v
```

Relevant task output:

```
TASK [DEPLOYING AAA GROUP AND IPS 1] **********************************************************
changed: [csr1] => {"banners": {}, "changed": true, "commands": ["aaa group server tacacs+ TESTING", "server 1.2.3.4", "server 2.1.3.4", "server 3.2.1.4"], "updates": ["aaa group server tacacs+ TESTING", "server 1.2.3.4", "server 2.1.3.4", "server 3.2.1.4"]}
```

You should see all commands getting applied properly.

##### Step 4

These servers should be defined in _priority_ order, or the order that they are used by the device.  In this step, we want to add a 4th server to the top of the list.

Take note of the new task using the tag of "append_server".

```yaml
  - name: CONFIGURING AAA SERVER GROUPS
    hosts: csr1
    connection: local
    gather_facts: no

    tasks:
      - name: DEPLOYING AAA GROUP AND IPS 1
        ios_config:
          parents:
            - aaa group server tacacs+ TESTING
          commands:
            - server 1.2.3.4
            - server 2.1.3.4
            - server 3.2.1.4
        tags: starting_config 

      - name: DEPLOYING AAA GROUP AND IPS 2
        ios_config:
          parents:
            - aaa group server tacacs+ TESTING
          commands:
            - server 4.3.2.1
            - server 1.2.3.4
            - server 2.1.3.4
            - server 3.2.1.4
        tags: append_server 
```



##### Step 5

Execute the playbook in verbose mode using the "append_server" tag:

```
ntc@ntc:ansible$ ansible-playbook -i inventory aaa.yml --tags=append_server -v
```

Relevant task output:

```
TASK [DEPLOYING AAA GROUP AND IPS 2] **********************************************************
changed: [csr1] => {"banners": {}, "changed": true, "commands": ["aaa group server tacacs+ TESTING", "server 4.3.2.1"], "updates": ["aaa group server tacacs+ TESTING", "server 4.3.2.1"]}

```

Notice how only the new IP was deployed?

##### Step 6

Go back to the router console and check the IP address ordering:

```
csr1#show run | begin TESTING 
aaa group server tacacs+ TESTING
 server 1.2.3.4
 server 2.1.3.4
 server 3.2.1.4
 server 4.3.2.1
```

Our goal was to have `4.3.2.1` at the top of the list, but it's now showing at the bottom.

##### Step 7

Add one new task as shown below.

```yaml
  - name: CONFIGURING AAA SERVER GROUPS
    hosts: csr1
    connection: local
    gather_facts: no

    tasks:
      - name: DEPLOYING AAA GROUP AND IPS
        ios_config:
          parents:
            - aaa group server tacacs+ TESTING
          commands:
            - server 1.2.3.4
            - server 2.1.3.4
            - server 3.2.1.4
        tags: starting_config 

      - name: DEPLOYING AAA GROUP AND IPS
        ios_config:
          parents:
            - aaa group server tacacs+ TESTING
          commands:
            - server 4.3.2.1
            - server 1.2.3.4
            - server 2.1.3.4
            - server 3.2.1.4
        tags: append_server 

      - name: DEPLOYING AAA GROUP AND IPS
        ios_config:
          before: no aaa group server tacacs+ TESTING
          parents:
            - aaa group server tacacs+ TESTING
          commands:
            - server 4.1.1.1
            - server 1.2.3.4
            - server 2.1.3.4
            - server 3.2.1.5
          match: exact
        tags: replace_on_change 
```

This task introduces even more parameters for `ios_config` such as `before` and `match`.

 * `before` - commands that will get execute "before" the `parents` and `commands` _if_ a change is required
 * `match` - this dictates how matching is done against the existing running configuration.  The default is `match: line` which just ensures the commands exist.  "exact" will make sure the ordering is exactly how you define it in the playbook.

##### Step 8

Execute the playbook in verbose mode using the "replace_on_change" tag:

```
ntc@ntc:ansible$ ansible-playbook -i inventory aaa.yml --tags=replace_on_change -v
```

Relevant task output:

```
TASK [DEPLOYING AAA GROUP AND IPS] **********************************************************
changed: [csr1] => {"banners": {}, "changed": true, "commands": ["no aaa group server tacacs+ TESTING", "aaa group server tacacs+ TESTING", "server 4.1.1.1", "server 1.2.3.4", "server 2.1.3.4", "server 3.2.1.5"], "updates": ["no aaa group server tacacs+ TESTING", "aaa group server tacacs+ TESTING", "server 4.1.1.1", "server 1.2.3.4", "server 2.1.3.4", "server 3.2.1.5"]}
```

As you can see now the servers are deployed in the proper order.


##### Step 9

**MANUAL STEP**

SSH into **csr1** and enter the following commands:

```
config t
no aaa new-model
end
```


### Task 3 - Viewing Diffs and Performing a Configuration Validation

This task introduces other command line flags and parameters available when using the `config` module.

##### Step 1

Create a new playbook called `verify-config.yml`.

##### Step 2

Save the following in the new playbook.

```yaml
  - name: USING DIFF AGAINST WITH CONFIG
    hosts: csr1
    connection: local
    gather_facts: no

    tasks:

      - name: ENSURE THAT LOOPBACK222 IS CONFIGURED
        ios_config:
          parents:
            - interface Loopback222
          commands:
            - ip address 10.224.222.222 255.255.255.255
          diff_against: running
        tags: diff_me

```

##### Step 3

In prior labs, you've learned how to view the commands that are (and will) get sent using a combination of `check` mode and `verbose` mode.  This step introduces a flag called `--diff` that allows you to see the exact diffs comparing the commands in the playbook and commands in the running configuration.

Execute the playbook using the `diff_me` tag and the `--diff` flag.

```
ntc@ntc:ansible$ ansible-playbook -i inventory verify-config.yml --tags=diff_me --diff 
```

Notice now how you see the exact diffs directly on the Linux terminal when the playbook is running:

```
TASK [ENSURE THAT LOOPBACK222 IS CONFIGURED] ************************************************
--- before
+++ after
@@ -87,6 +87,8 @@
  no ip address
 interface Loopback200
  ip address 10.200.100.1 255.255.255.255
+interface Loopback222
+ ip address 10.224.222.222 255.255.255.255
 interface GigabitEthernet1
  description MANAGEMENT'
  vrf forwarding MANAGEMENT

changed: [csr1]
```

###### Step 4

Add a new task to the playbook.  This task will compare the FULL config of one previously backed up to one that is on the device.

```yaml
```yaml
  - name: USING DIFF AGAINST WITH CONFIG
    hosts: csr1
    connection: local
    gather_facts: no

    tasks:

      - name: ENSURE THAT LOOPBACK222 IS CONFIGURED
        ios_config:
          parents:
            - interface Loopback222
          commands:
            - ip address 10.224.222.222 255.255.255.255
          diff_against: running
        tags: diff_me

      - name: VERIFY GOLDEN CONFIGURATION
        ios_config:
          diff_against: intended
          intended_config: "{{ lookup('file', './backups/{{ inventory_hostname }}.cfg') }}"
        tags: verify_config
```

##### Step 5

Execute the playbook using the `verify_config` tag and the `--diff` flag.

```
ntc@ntc:ansible$ ansible-playbook -i inventory verify-config.yml --tags=verify_config --diff 
```

Just like the last task, notice now how you see the exact diffs directly on the Linux terminal when the playbook is running.  However, you should see them for the full config being proposed (intended).

```
TASK [VERIFY GOLDEN CONFIGURATION] **********************************************************
--- before
+++ after
@@ -12,7 +12,13 @@
  exit-address-family
  address-family ipv6
  exit-address-family
-no aaa new-model
+aaa new-model
+aaa group server tacacs+ TESTING
+ server 4.1.1.1
+ server 1.2.3.4
+ server 2.1.3.4
+ server 3.2.1.5
+aaa session-id common
 no ip domain lookup
 ip domain name ntc.com
 subscriber templating
@@ -79,6 +85,10 @@
  ip address 1.1.1.2 255.255.255.255
 interface Loopback101
  no ip address
+interface Loopback200
+ ip address 10.200.100.1 255.255.255.255
+interface Loopback222
+ ip address 10.224.222.222 255.255.255.255
 interface GigabitEthernet1
  description MANAGEMENT'
  vrf forwarding MANAGEMENT
@@ -138,18 +148,16 @@
  stopbits 1
 line vty 0
  privilege level 15
- login local
  transport preferred ssh
 line vty 1
- login local
+ privilege level 15
  length 0
  transport preferred ssh
 line vty 2 4
  privilege level 15
- login local
  transport preferred ssh
 line vty 5 30
- login local
+ privilege level 15
  transport preferred ssh
 wsma agent exec
 wsma agent config

changed: [csr1]
```

While this says changed, it is NOT making a change on the network. When you use `intended` as the`diff_against` value, the module does not permit changes on the network.

