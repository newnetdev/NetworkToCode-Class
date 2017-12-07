## BONUS Lab 15 - Using Ansible Vault for encrypted data

This lab will walk you through the Ansible Vault functionality, allowing you to store sensitive data as a one-way hash on the filesystem, that can be unecrypted on the fly during a playbook execution.


### Task 1 - Collect the Serial Number from the CSR devices

##### Step 1

From the inventory file, remove the the `un` and `pwd` variables, currently under the `[all:vars]` group vars.


##### Step 2

Within the `group_vars` directory, create a subdirectory called `all` and move the `group_vars/all.yml` file to the new `all` subdirectory


```
ntc@ntc:ansible$ cd group_vars
ntc@ntc:group_vars$ mkdir all
ntc@ntc:group_vars$ mv all.yml all/
ntc@ntc:group_vars$ 
```

##### Step 3

Open the `group_vars/all/all.yml`  file using a text editor. Here, we will add our `un` and `pwd` variables. However, rather than assign them the value `ntc` and `ntc123`, we will point them to new variables `user` and `pass`.

``` yaml
un: "{{ user }}"
pwd: "{{ pass }}"

provider:
  username: "{{ un }}"
  password: "{{ pwd }}"
  host: "{{ inventory_hostname }}"


```

##### Step 4

Using the `ansible-vault` command, create a new file in the `all` directory called `vaultfile.yml`

> Enter a password when prompted. This will be used to decrypt/edit this file in the future.

```
ntc@ntc:all$ ansible-vault create vaultfile.yml
New Vault password: 
Confirm New Vault password: 
```

##### Step 5

This will open a text editor where you can create the new variables whose data is sensitive.


``` yaml
user: ntc
pass: ntc123
```

Save an exit this file. Now if you try and view the `vaultfile.yml` it will contain an encrypted oneway hash of the username and password.

```
ntc@ntc:all$ ls
vaultfile.yml
ntc@ntc:all$ cat vaultfile.yml 
$ANSIBLE_VAULT;1.1;AES256
38353863306139626235623263313439653437646261393562323036356531336432323736646534
3161333737316430396431313931633863646535303432660a353461636464303238353765343162
31346366353766663063303636386265326665643331326632613536363831346364663065316462
6365646337363838650a326563386465383662643733633930323264333065633034363338643735
33323566656238633436623732623062313562386465666664333961386161313034

```
##### Step 6

Navigate back to the `ansible` directory, where we will write a playbook that will use the encrypted data. Create a playbook called `use_vault.yml`.


``` yaml
---
- name: USE ENCRYPTED LOGIN
  hosts: iosxe
  gather_facts: no
  connection: local


  tasks:

    - name: COLLECT THE SERIAL NUMBER
      ios_facts:
        provider: "{{ provider }}"


    - name: DISPLAY SERIAL NUMBER ON TERMINAL
      debug:
        msg: "{{ ansible_net_serialnum }}"
      

```


`ios_facts` module is using the `provider` variable. The `provider` variable as defined in the `all.yml`  references `un` and `pwd`. 

``` yaml
provider:
  username: "{{ un }}"
  password: "{{ pwd }}"
  host: "{{ inventory_hostname }}"

```


The `un` and `pwd` variables in the `all.yml` references the encrypted variables `user` and `pass` stored inside the `vaultfile.yml`


> Using a multi-stage variable like this is a best practice recommendation. This allows you to know what variables were defined inside your vault file without having to explicitly decrypting it.

##### Step 7

Finally save and run the playbook. You will need to use the `--ask-vault-pass` flag while invoking the playbook. This will prompt you to enter the password used to encrypt the vault file.


```
ntc@ntc:ansible$ ansible-playbook -i inventory use_vault.yml --ask-vault-pass
Vault password: 

PLAY [USE ENCRYPTED LOGIN] *******************************************************************************************************

TASK [COLLECT THE SERIAL NUMBER] ******************************************************************************************************
ok: [csr1]
ok: [csr2]
ok: [csr3]


TASK [DISPLAY SERIAL NUMBER ON TERMINAL] **********************************************************************************************
ok: [csr1] => {
    "msg": "9KXI0D7TVFI"
}
ok: [csr2] => {
    "msg": "LMXI0D7TV09"
}
ok: [csr3] => {
    "msg": "69DI033TVFF"
}

PLAY RECAP ***********************************************************************************************************************
csr1                       : ok=2    changed=0    unreachable=0    failed=0   
csr2                       : ok=2    changed=0    unreachable=0    failed=0   
csr3                       : ok=2    changed=0    unreachable=0    failed=0   


```

