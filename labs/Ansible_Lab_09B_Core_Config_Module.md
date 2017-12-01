## Lab 9B - Establishing intent using the core _config module

In this lab we will work with the new parameters introduced in Ansible 2.4 core modules to establish intent.

### Task 1 - Working with the diff_against parameter

##### Step 1

Create a new playbook called `core_diff.yml` in the `ansible` directory.

##### Step 2

Add a new play. Restrict it to `csr1` and build a single task to add a new loopback interface `Loopback 222` to the device.

Note: if you already have `provider` in a `group_vars` file, you do not need it in the playbook as shown below too.

``` yaml
---
- name: VALIDATING INTENT ON IOS
  hosts: csr1
  connection: local
  gather_facts: no

  vars:
    provider:
      username: "{{ un }}"
      password: "{{ pwd }}"
      host: "{{ inventory_hostname }}"

  tasks:

    - name: ENSURE THAT LOOPBACK222 IS CONFIGURED
      ios_config:
        provider: "{{ provider }}"
        commands:
          - ip address 10.222.222.222 255.255.255.255
        parents:
          - interface loopback 222

```

##### Step 3

Add the `diff_against: running` parameter to the above task. 

``` yaml
---
- name: VALIDATING INTENT ON IOS
  hosts: csr1
  connection: local
  gather_facts: no

  vars:
    provider:
      username: "{{ un }}"
      password: "{{ pwd }}"
      host: "{{ inventory_hostname }}"

  tasks:

    - name: ENSURE THAT LOOPBACK222 IS CONFIGURED
      ios_config:
        provider: "{{ provider }}"
        commands:
          - ip address 10.222.222.222 255.255.255.255
        parents:
          - interface Loopback 222
        diff_against: running
```

##### Step 4 

Save and run the playbook as using the `--diff` flag. 
> This will also implement the configuration on the device.

```

ntc@ntc:ansible$ ansible-playbook -i inventory core_diff.yml --diff --limit csr1

PLAY [VALIDATING INTENT ON IOS] *************************************************************************************************************

TASK [ENSURE THAT LOOPBACK 222 IS CONFIGURED] ***********************************************************************************************
--- before
+++ after
@@ -63,6 +63,8 @@
 redundancy
 lldp run
 cdp run
+interface Loopback222
+ ip address 10.222.222.222 255.255.255.255
 interface GigabitEthernet1
  vrf forwarding MANAGEMENT
  ip address 10.0.0.51 255.255.255.0

changed: [csr1]

PLAY RECAP **********************************************************************************************************************************
csr1                       : ok=1    changed=1    unreachable=0    failed=0   

ntc@ntc:ansible$ 
```

Thus the `diff_against: running`, when used with a core config module, helps the operator visualize the exact change that is applied to the device.

##### Step 6

Add a new task to compare the running config, to the startup configuration on the CSR. Tag the task with `diff_startup`

``` yaml
---
- name: VALIDATING INTENT ON IOS
  hosts: csr1
  connection: local
  gather_facts: no

  vars:
    provider:
      username: "{{ un }}"
      password: "{{ pwd }}"
      host: "{{ inventory_hostname }}"

  tasks:

    - name: ENSURE THAT LOOPBACK 222 IS CONFIGURED
      ios_config:
        provider: "{{ provider }}"
        commands:
          - ip address 10.222.222.222 255.255.255.255
        parents:
          - interface loopback 222
        diff_against: running
        
    - name: COMPARE RUNNING CONFIG WITH STARTUP
      ios_config:
        provider: "{{ provider }}"
        diff_against: startup
      tags: diff_startup

```


##### Step 7

Save and run this this playbook with the `--diff` flag.


```
ntc@ntc:ansible$ ansible-playbook -i inventory core_diff.yml --diff --tags=diff_startup

PLAY [VALIDATING INTENT ON IOS] ***********************************************************************************************************************************************************************************

TASK [COMPARE RUNNING CONFIG WITH STARTUP] ************************************************************************************************************************************************************************
--- before
+++ after
@@ -22,7 +22,34 @@
  revocation-check none
  rsakeypair TP-self-signed-1692872229
 crypto pki certificate chain TP-self-signed-1692872229
- certificate self-signed 01 nvram:IOS-Self-Sig#1.cer
+ certificate self-signed 01
+  30820330 30820218 A0030201 02020101 300D0609 2A864886 F70D0101 05050030 
+  31312F30 2D060355 04031326 494F532D 53656C66 2D536967 6E65642D 43657274 
+  69666963 6174652D 31363932 38373232 3239301E 170D3136 30393137 31343532 
+  31355A17 0D323030 31303130 30303030 305A3031 312F302D 06035504 03132649 
+  4F532D53 656C662D 5369676E 65642D43 65727469 66696361 74652D31 36393238 
+  37323232 39308201 22300D06 092A8648 86F70D01 01010500 0382010F 00308201 
+  0A028201 01008C3F 8CC4110A 46D229F4 6CC98F4B B91EC0E7 14653DF4 929EFAE2 
+  735FBFB9 944BBB69 76183782 C7580776 A63E0B59 1FC59096 46083864 3BCBA45B 
+  DBBE4446 19E096CD 218C27B6 053F9ADA 3A9A442C 43028EA0 65751E97 E9AEA5AA 
+  79421470 4515CB08 B09A1546 0F2A547E 1BD79437 82000464 8675A977 0C46721B 
+  96EB64DD E69C1F5A BE21D8AE 9283BE65 F0D36816 360C71CB 266DDAF4 8E862D2F 
+  7665A0A9 1955CD7A 95B31F67 D24C4BB8 CF30E3CB 0ACA3698 0BEE3323 A2C3AF16 
+  B322FB52 BEDA9AB6 DE7B4D1A 6C89E060 0F971CC9 2192A88A E01D6B00 A7A4CBEC 
+  4EA3E233 AC213B27 6CFE403C 4ED6AF88 C48F0106 9DCB9B34 CE775B88 E22ED282 
+  98112FF5 A07B0203 010001A3 53305130 0F060355 1D130101 FF040530 030101FF 
+  301F0603 551D2304 18301680 142A6961 60B9636B 6AB03227 74EF7A25 CCEC0FCE 
+  81301D06 03551D0E 04160414 2A696160 B9636B6A B0322774 EF7A25CC EC0FCE81 
+  300D0609 2A864886 F70D0101 05050003 82010100 17DC579F D400261B 6E725759 
+  A99EE2D9 BE51F87C 00205EF4 7C647E18 C736108A E86E4C1C 5494FFA8 358D1D89 
+  B0919DBA 0C5F72DB 831C67E7 0EE7C2EB 961E0355 5FAAECC7 A946D7A0 1C401D0D 
+  FD4D1F63 C0BBCF43 DEAB63B5 11051773 172AA75D 389813A8 6080DFB6 C704A199 
+  EC8546B7 BA3C53C8 8B69DF64 5305FDEB 3A7ACA2A 1992AF6C C9D74A91 2601666D 
+  FE0AD3F3 81015D87 9721ED5B 7CAC12EC 3AB40C1C 8C51A871 C8EEB611 29B16D10 
+  A7AE1C00 4B71940E AD42D20C FD9B958D 7D353DDC 195CC910 1DDC2BE7 E971B2EA 
+  209F3F96 FBE167D6 E0E4E11F E58834D8 7FE78CB5 039297CD 113CB419 6C5F9733 
+  AF749425 129B78B2 D6BBEFA0 34F4CB8E FF9B43A7
+       quit
 license udi pid CSR1000V sn 9KXI0D7TVFI
 diagnostic bootup level minimal
 archive
@@ -36,6 +63,8 @@
 redundancy
 lldp run
 cdp run
+interface Loopback222
+ ip address 10.222.222.222 255.255.255.255
 interface GigabitEthernet1
  vrf forwarding MANAGEMENT
  ip address 10.0.0.51 255.255.255.0

changed: [csr1]

PLAY RECAP ********************************************************************************************************************************************************************************************************
csr1                       : ok=1    changed=1    unreachable=0    failed=0   

ntc@ntc:ansible$ 

```

This compares the running config of the router against the configuration stored in the NVRAM.


##### Step 8

Update the first task to save the Loopback interface configuration to the device. Also tag the task as `loopback`

> Due to an open bug in [Ansible 2.4](https://github.com/ansible/ansible/issues/32619), the `save_when` will time out. As a workaround, manually login to the device and issue a `write memory` command manually.


``` yaml
---
- name: VALIDATING INTENT ON IOS
  hosts: csr1
  connection: local
  gather_facts: no

  vars:
    provider:
      username: "{{ un }}"
      password: "{{ pwd }}"
      host: "{{ inventory_hostname }}"

  tasks:

    - name: ENSURE THAT LOOPBACK 222 IS CONFIGURED
      ios_config:
        provider: "{{ provider }}"
        commands:
          - ip address 10.222.222.222 255.255.255.255
        parents:
          - interface loopback 222
        diff_against: running
       #save_when: modified
      tags: loopback

    - name: COMPARE RUNNING CONFIG WITH STARTUP
      ios_config:
        provider: "{{ provider }}"
        diff_against: startup
      tags: diff_startup

```

##### Step 9

Run the playbook first using the tag loopback and then rerun the playbook using the `diff` flag, without any tag.

```
ntc@ntc:ansible$ ansible-playbook -i inventory core_diff.yml --tags=loopback

PLAY [VALIDATING INTENT ON IOS] *****************************************************************************************************************************************

TASK [ENSURE THAT LOOPBACK 222 IS CONFIGURED] ***************************************************************************************************************************
changed: [csr1]

PLAY RECAP **************************************************************************************************************************************************************
csr1                       : ok=1    changed=1    unreachable=0    failed=0   

ntc@ntc:ansible$ 


```

```
ntc@ntc:ansible$ ansible-playbook -i inventory core_diff.yml --diff

PLAY [VALIDATING INTENT ON IOS] *****************************************************************************************************************************************

TASK [ENSURE THAT LOOPBACK 222 IS CONFIGURED] ***************************************************************************************************************************
changed: [csr1]

TASK [COMPARE RUNNING CONFIG WITH STARTUP] ******************************************************************************************************************************
--- before
+++ after
@@ -22,7 +22,34 @@
  revocation-check none
  rsakeypair TP-self-signed-1692872229
 crypto pki certificate chain TP-self-signed-1692872229
- certificate self-signed 01 nvram:IOS-Self-Sig#1.cer
+ certificate self-signed 01
+  30820330 30820218 A0030201 02020101 300D0609 2A864886 F70D0101 05050030 
+  31312F30 2D060355 04031326 494F532D 53656C66 2D536967 6E65642D 43657274 
+  69666963 6174652D 31363932 38373232 3239301E 170D3136 30393137 31343532 
+  31355A17 0D323030 31303130 30303030 305A3031 312F302D 06035504 03132649 
+  4F532D53 656C662D 5369676E 65642D43 65727469 66696361 74652D31 36393238 
+  37323232 39308201 22300D06 092A8648 86F70D01 01010500 0382010F 00308201 
+  0A028201 01008C3F 8CC4110A 46D229F4 6CC98F4B B91EC0E7 14653DF4 929EFAE2 
+  735FBFB9 944BBB69 76183782 C7580776 A63E0B59 1FC59096 46083864 3BCBA45B 
+  DBBE4446 19E096CD 218C27B6 053F9ADA 3A9A442C 43028EA0 65751E97 E9AEA5AA 
+  79421470 4515CB08 B09A1546 0F2A547E 1BD79437 82000464 8675A977 0C46721B 
+  96EB64DD E69C1F5A BE21D8AE 9283BE65 F0D36816 360C71CB 266DDAF4 8E862D2F 
+  7665A0A9 1955CD7A 95B31F67 D24C4BB8 CF30E3CB 0ACA3698 0BEE3323 A2C3AF16 
+  B322FB52 BEDA9AB6 DE7B4D1A 6C89E060 0F971CC9 2192A88A E01D6B00 A7A4CBEC 
+  4EA3E233 AC213B27 6CFE403C 4ED6AF88 C48F0106 9DCB9B34 CE775B88 E22ED282 
+  98112FF5 A07B0203 010001A3 53305130 0F060355 1D130101 FF040530 030101FF 
+  301F0603 551D2304 18301680 142A6961 60B9636B 6AB03227 74EF7A25 CCEC0FCE 
+  81301D06 03551D0E 04160414 2A696160 B9636B6A B0322774 EF7A25CC EC0FCE81 
+  300D0609 2A864886 F70D0101 05050003 82010100 17DC579F D400261B 6E725759 
+  A99EE2D9 BE51F87C 00205EF4 7C647E18 C736108A E86E4C1C 5494FFA8 358D1D89 
+  B0919DBA 0C5F72DB 831C67E7 0EE7C2EB 961E0355 5FAAECC7 A946D7A0 1C401D0D 
+  FD4D1F63 C0BBCF43 DEAB63B5 11051773 172AA75D 389813A8 6080DFB6 C704A199 
+  EC8546B7 BA3C53C8 8B69DF64 5305FDEB 3A7ACA2A 1992AF6C C9D74A91 2601666D 
+  FE0AD3F3 81015D87 9721ED5B 7CAC12EC 3AB40C1C 8C51A871 C8EEB611 29B16D10 
+  A7AE1C00 4B71940E AD42D20C FD9B958D 7D353DDC 195CC910 1DDC2BE7 E971B2EA 
+  209F3F96 FBE167D6 E0E4E11F E58834D8 7FE78CB5 039297CD 113CB419 6C5F9733 
+  AF749425 129B78B2 D6BBEFA0 34F4CB8E FF9B43A7
+       quit
 license udi pid CSR1000V sn 9KXI0D7TVFI
 diagnostic bootup level minimal
 archive

changed: [csr1]

PLAY RECAP **************************************************************************************************************************************************************
csr1                       : ok=2    changed=2    unreachable=0    failed=0   

ntc@ntc:ansible$ 

```

> As you can see, the loopback configuration has been committed to the startup-config.


### Task 2 - Validating configuration Intent

##### Step 1

In lab 5 we had created a backup of the devices in the `backups` folder. We will use this saved configuration as our intent for `csr1`.


Create a new playbook called `core_intent.yml` and add the following task to it.

``` yaml
---
- name: VALIDATE CONFIGURATION INTENT ON DEVICES
  hosts: csr1
  gather_facts: no
  connection: local
  
  vars:
    provider: 
      username: "{{ un }}"
      password: "{{ pwd }}"
      host: "{{ inventory_hostname }}"
      
  tasks:
    - name: VALIDATE CONFIGURATION INTENT
      ios_config:
        diff_against: intended
        intended_config: "{{ lookup('file', './backups/{{ inventory_hostname }}.cfg') }}"
        provider: "{{ provider }}"

```

##### Step 2

Save and run the playbook using the `--diff` flag.

>The `intended_config` parameter is only used for compliance checking and not for modifying configuration on the devices.

```
ntc@ntc:ansible$ ansible-playbook -i inventory core_intent.yml --diff

PLAY [VALIDATE CONFIGURATION INTENT ON DEVICES] *************************************************************************************************************************

TASK [VALIDATE CONFIGURATION INTENT] ************************************************************************************************************************************
--- before
+++ after
@@ -63,6 +63,8 @@
 redundancy
 lldp run
 cdp run
+interface Loopback222
+ ip address 10.222.222.222 255.255.255.255
 interface GigabitEthernet1
  vrf forwarding MANAGEMENT
  ip address 10.0.0.51 255.255.255.0

changed: [csr1]

PLAY RECAP **************************************************************************************************************************************************************
csr1                       : ok=1    changed=1    unreachable=0    failed=0   

ntc@ntc:ansible$ 
```
