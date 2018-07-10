## Lab 6 - Prompting the User for Input


### Task 2 - Using vars_prompt

In Ansible, you have the ability to prompt for user input while running a playbook using the `vars_prompt` directive.

##### Step 1

Create a new playbook in the `ansible` directory called `user_input.yml`:

```
ntc@ntc:ansible$ touch user_input.yml
ntc@ntc:ansible$ 

```

##### Step 2

Open this file with a text editor and input the play definition as follows:

``` yaml
---
- name: COLLECT USERNAME AND PASSWORD
  hosts: csr1
  gather_facts: no
  connection: network_cli
  
```


##### Step 3

Add a `vars_prompt` directive that allows you to collect user input data.

``` yaml
---
- name: COLLECT USERNAME AND PASSWORD
  hosts: csr1
  gather_facts: no
  connection: network_cli

  vars_prompt:
    - name: un
      prompt: "Please enter the username"
      private: no
      
    - name: pwd
      prompt: "Please enter the password"
      private: no
      
  tasks:

    - name: DISPLAY THE USERNAME AND PASSWORD
      debug:
        msg: "The Username is {{ un }} and password is {{ pwd }}"

```

##### Step 4

Now run the playbook as follows:

```
ntc@ntc:ansible$ ansible-playbook -i inventory user_input.yml
Please enter the username: ntc
Please enter the password: ntc123

PLAY [COLLECT USERNAME AND PASSWORD] ************************************************************************************

TASK [DISPLAY THE USERNAME AND PASSWORD] ********************************************************************************
ok: [localhost] => {
    "msg": "The Username is ntc and password is ntc123"
}

PLAY RECAP **************************************************************************************************************
localhost                  : ok=1    changed=0    unreachable=0    failed=0   


```

The playbook prompts you to enter a username and password which is stored into the variables `un` and `pwd`. The debug statement finally prints this to the terminal

##### Step 5

For sensitive information, such as the password, we do not want the user input to be echoed on the terminal. This can be avoided by setting the `private` parameter to `yes` (The default is `yes`. So you can effectively achieve this by not having that private directive in your playbook at all, for password)


Update the playbook as follows:

``` yaml
---
- name: COLLECT USERNAME AND PASSWORD
  hosts: csr1
  gather_facts: no
  connection: network_cli

  vars_prompt:
    - name: un
      prompt: "Please enter the username"
      private: no
      
    - name: pwd
      prompt: "Please enter the password"
      private: yes
      
  tasks:

    - name: DISPLAY THE USERNAME AND PASSWORD
      debug:
        msg: "The Username is {{ un }} and password is {{ pwd }}"

```


##### Step 6

Run the playbook.

```
ntc@ntc:ansible$ ansible-playbook -i inventory user_input.yml
Please enter the username: ntc
Please enter the password: 

PLAY [COLLECT USERNAME AND PASSWORD] ************************************************************************************

TASK [DISPLAY THE USERNAME AND PASSWORD] ********************************************************************************
ok: [localhost] => {
    "msg": "The Username is ntc and password is ntc123"
}

PLAY RECAP **************************************************************************************************************
localhost                  : ok=1    changed=0    unreachable=0    failed=0   


```

Notice how the password is no longer echoed back on the screen.


##### Step 7

Finally, the `var_prompt` directive can also be set up to take a default value that can be overridden. Update the playbook as follows:


``` yaml
---
- name: COLLECT USERNAME AND PASSWORD
  hosts: csr1
  gather_facts: no
  connection: network_cli

  vars_prompt:
    - name: un
      prompt: "Please enter the username"
      private: no
      default: ntc
      
    - name: pwd
      prompt: "Please enter the password"
      
  tasks:

    - name: DISPLAY THE USERNAME AND PASSWORD
      debug:
        msg: "The Username is {{ un }} and password is {{ pwd }}"

```


##### Step 8


Run the playbook again.

```
ntc@ntc:ansible$ ansible-playbook -i inventory user_input.yml
Please enter the username [ntc]: 
Please enter the password: 

PLAY [COLLECT USERNAME AND PASSWORD] ************************************************************************************

TASK [DISPLAY THE USERNAME AND PASSWORD] ********************************************************************************
ok: [localhost] => {
    "msg": "The Username is ntc and password is ntc123"
}

PLAY RECAP **************************************************************************************************************
localhost                  : ok=1    changed=0    unreachable=0    failed=0   


```

This time, notice how you are prompted for the username, with the default value populated. If you run the playbook without any input to username, the value `ntc` is taken.

Feel free to continue to explore using `vars_prompt` and debugging variables.  This could also be used for passing in configuration data or anything else needed to execute a playbook.


