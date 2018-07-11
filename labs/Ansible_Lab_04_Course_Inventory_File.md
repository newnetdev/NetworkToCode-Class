## Lab 4 - Ansible Inventory File

This lab builds on previous labs and shows how to build a more robust Ansible inventory file.  You'll learn how to create groups, nested groups, and group based variables all within the inventory file.

> **Note:** This is the master inventory file used for this course.  It is critical this step is performed so that all other tasks work as expected.

> If there are certain devices that are not in your course, please do not include them in your inventory file.

### Task 1 - Create Inventory Device Groups

##### Step 1

Navigate to the Ansible directory.

```
ntc@ntc:~$ cd ansible
ntc@ntc:ansible$
```

##### Step 2

Open the inventory file in your text editor.


##### Step 3

Create the following groups with the proper devices in them in your inventory file.  Each parent bullet is a group name and the sub-bullets are the devices in that particular group.

* eos-leaves
  * eos-leaf1
  * eos-leaf2
* eos-spines
  * eos-spine1
  * eos-spine2
* iosxe
  * csr1
  * csr2
  * csr3
* nxos-spines
  * nxos-spine1
  * nxos-spine2
* vmx
  * vmx7
  * vmx8
  * vmx9


All devices names are pre-set in your `/etc/hosts` file.  You should be able to ping all of these devices by name from your Ubuntu jump host.

One example group is **vmx**, which will look like this:

```

[vmx]
vmx7
vmx8
vmx9

```

This methodology can be quite tedious for a large number of devices.

The file can be optimized by using patterns in the inventory file.  For example, there are currently 3 *vmx* devices with the same name except having a different number appended.  When you have this pattern, you can list individual devices like *vmx7*, *vmx8*, and *vmx9* **or** you can use this syntax:

```
vmx[7:9]
```

We'll only do this for the vmx devices, but feel free to do this for the other devices too.  Note: patterns *do not* have to be at the end of the device name.

The new inventory file looks like this:

```
[eos-spines]
eos-spine1
eos-spine2

[eos-leaves]
eos-leaf1
eos-leaf2

[iosxe]
csr1
csr2
csr3

[nxos-spines]
nxos-spine1
nxos-spine2

[vmx]
vmx[7:9]


```


### Task 2 - Create Parent/Child (Nested) Groups

##### Step 1

You may have noticed we didn't create a group that has **all** Nexus switches or **all** Arista switches.  We can list the same device in two groups, but that is a bit redundant.  Another option is to use child groups in the inventory file.

For example, you can create a group called *eos* and include the *eos-spines* and *eos-leaves* groups as children of the new group.  This can be done as follows:

```
[eos:children]
eos-spines
eos-leaves
```

**Do this for both Arista EOS and Cisco NXOS groups.**  Note that there are Arista Spines and Leaves, but only Cisco Nexus Spines.

##### Step 2

Additionally create a group called `AMER` that contains all the csrs and a group called `EMEA` that contains all the vmxs

The updated inventory file should look like this:

```

[eos:children]
eos-spines
eos-leaves

[eos-spines]
eos-spine1
eos-spine2

[eos-leaves]
eos-leaf1
eos-leaf2

[iosxe]
csr1
csr2
csr3

[nxos:children]
nxos-spines

[nxos-spines]
nxos-spine1
nxos-spine2

[vmx]
vmx[7:9]

[AMER:children]
iosxe

[EMEA:children]
vmx

```

> In this case, the group *nxos* is basically the same as *nxos-spines*.


### Task 3 - Create Group Based Variables for the *all* group

In this task, you'll create group based variables that will be used throughout the course.  Do NOT forget there is an implicit group that always exists called **all**.

Ensure you have three group variables in the **all** group that are used for authentication:

```
[all:vars]
ansible_user=ntc
ansible_ssh_pass=ntc123
ansible_connection=network_cli
```

All devices in the course use these credentials and connection type.

### Task 4 - Create Group Based Variables for the *eos* group

Create the variables required in the **eos** group:

```
[eos:vars]
ansible_network_os=eos
ntc_api=eapi
ntc_vendor=arista
```

We'll use these variables in a variety of ways throughout the course.

### Task 5 - Create Group Variables for the *nxos* group


Create the variables required in the **nxos** group:

* Set `ansible_network_os` to **nxos**
* Set `ntc_api` equal to **nxapi**
* Set `ntc_vendor` equal to **cisco**

We'll use these variables in a variety of ways throughout the course.

### Task 6 - Create Group Variables for the *iosxe* group


Create the variables required in the **iosxe** group:

* Set `ansible_network_os` to **ios**
* Set `ntc_api` equal to **ssh**
* Set `ntc_vendor` equal to **cisco**

We'll use these variables in a variety of ways throughout the course as well.


### Task 7 - Create Group Variables for the *vmx* group

Create the variables required in the **vmx** group:

* Set `ansible_connection` to **netconf**
* Set `ansible_network_os` to **junos**
* Set `ntc_api` equal to **netconf**
* Set `ntc_vendor` equal to **juniper**


We'll use these variables in a variety of ways throughout the course.

### Task 8 - Status Check

After adding all group variables, your inventory file should look like this (note that order doesn't matter):

> Note: if there isn't a particular device in your topology, there is no need to have it in the inventory file.

```
[all:vars]
ansible_user=ntc
ansible_ssh_pass=ntc123
ansible_connection=network_cli

[eos:children]
eos-spines
eos-leaves

[eos-spines]
eos-spine1
eos-spine2

[eos-leaves]
eos-leaf1
eos-leaf2

[eos:vars]
ansible_network_os=eos
ntc_api=eapi
ntc_vendor=arista

[iosxe]
csr1
csr2
csr3

[iosxe:vars]
ansible_network_os=ios
ntc_api=ssh
ntc_vendor=cisco

[nxos:children]
nxos-spines

[nxos-spines]
nxos-spine1
nxos-spine2

[nxos:vars]
ansible_network_os=nxos
ntc_api=nxapi
ntc_vendor=cisco

[vmx]
vmx[7:9]

[vmx:vars]
ansible_connection=netconf
ansible_network_os=junos
ntc_api=netconf
ntc_vendor=juniper

[AMER:children]
iosxe

[EMEA:children]
vmx

```
