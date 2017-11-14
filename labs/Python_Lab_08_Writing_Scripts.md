## Lab 8 - Writing Scripts

### Task 1 - Hello Network Automation

##### Step 1

Within your home directory, create a new directory called `scripts`:

```
ntc@ntc:~$ mkdir scripts
ntc@ntc:~$
```

##### Step 2

Navigate to the `scripts` directory.

```
ntc@ntc:~$ cd scripts
ntc@ntc:~/scripts$
```

##### Step 3

Create a new file called `networkauto.py`

```
ntc@ntc:~/scripts$ touch networkauto.py
ntc@ntc:~/scripts$
```

##### Step 4

Open the file in the text editor of your choice.

  * If you've RDP'd into the jump host, you can use Sublime Text on the desktop.
  * If you've SSH'd into the jump host, you can use nano, vi/vim, gedit, or any other text-based editor of your choosing.

> Note: An alternative option is to use a program called Cyberduck (or equivalent) that allows you to connect to the jump host via SFTP and edit files locally on your laptop.  As soon as you save them, they are SFTP'd back to the jump host.  This could improve latency for particular labs.


##### Step 5

Create a *Hello World* script that just prints *Hello Network Automation!*

```python
#! /usr/bin/env python

if __name__ == "__main__":

    print('Hello Network Automation!')

```

##### Step 6

Save the file and execute it from the command line:

```
ntc@ntc:~/scripts$ python networkauto.py
Hello Network Automation!
ntc@ntc:~/scripts$
```

As you can see, it was quite simple to write a Python script.  In fact, everything under `if __name__ == "__main__": ` is the same as if you were using the Python shell.

### Task 2 - Printing Data

In this task, you will create a script that replicates what you did in the last lab.  This script will print the facts for three devices.

##### Step 1

Create a new script called `print_facts.py`.  Save it in the `scripts` directory.

##### Step 2

Take the code below and save it in `print_facts.py`.


```python
#! /usr/bin/env python

if __name__ == "__main__":

    facts1 = {'vendor': 'cisco', 'os': 'nxos', 'ipaddr': '10.1.1.1'}
    facts2 = {'vendor': 'cisco', 'os': 'ios', 'ipaddr': '10.2.1.1'}
    facts3 = {'vendor': 'arista', 'os': 'eos', 'ipaddr': '10.1.1.2'}

    devices = [facts1, facts2, facts3]

    for item in devices:
        print("VENDOR: {}".format(item['vendor']))
        print("OS: {}".format(item['os']))
        print("IP ADDRESS: {}".format(item['ipaddr']))
        print("-" * 10)

```

##### Step 3

Execute the script.

```
ntc@ntc:~/scripts$ python print_facts.py
VENDOR: cisco
OS: nxos
IP ADDRESS: 10.1.1.1
----------
VENDOR: cisco
OS: ios
IP ADDRESS: 10.2.1.1
----------
VENDOR: arista
OS: eos
IP ADDRESS: 10.1.1.2
----------
ntc@ntc:~/scripts$
```

The point in this lab is to showcase the transition going from learning to write code on the Python shell.

We'll now move onto more useful scripts


