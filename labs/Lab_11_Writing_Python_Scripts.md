## Lab 11 - Writing Scripts

This lab helps make the transition from writing on the Python Interpreter to actually writing Python standalone scripts.

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

> Note: An alternative option is to use a program called Cyberduck (or equivalent) that allows you to connect to the jump host via SFTP and edit files locally on your laptop.  As soon as you save them, they are SFTP'd back to the jump host.  


##### Step 5

Create a *Hello World* script that just prints *Hello Network Automation!*

```python
#! /usr/bin/env python

print('Hello Network Automation!')

```

> Note: we've also included the optional shebang that instructions the system which version of Python to use when running this script.  That is the first line of the script. You could also do `#! /usr/bin/python3.4`, but then you'd need to change the line in all of your scripts vs. using your environment should you want to test different versions of Python.  Using the recommended shebang, you just need to change the Python version in your environment.


_Finally, there is another optional line that's left out of this script, which is an entry point conditional, e.g. `if __name__ == "__main__":`.  We state it here for completeness, but we'll re-visit it again once we get to cover `if` statements in the course._


##### Step 6

Save the file and execute it from the command line:

```
ntc@ntc:~/scripts$ python networkauto.py
Hello Network Automation!
ntc@ntc:~/scripts$
```

As you can see, it was quite simple to write a Python script.  It's technically no different than typing on the Python shell.

### Task 2 - Printing Data

In this task, you will create a script that replicates what you did in previous labs.  This script will print the facts for three devices.

##### Step 1

Create a new script called `print_facts.py`.  Save it in the `scripts` directory.

##### Step 2

Take the code below and save it in `print_facts.py`.


```python
#! /usr/bin/env python

import json 

facts1 = {'vendor': 'cisco', 'os': 'nxos', 'ipaddr': '10.1.1.1'}
facts2 = {'vendor': 'cisco', 'os': 'ios', 'ipaddr': '10.2.1.1'}
facts3 = {'vendor': 'arista', 'os': 'eos', 'ipaddr': '10.1.1.2'}

devices = [facts1, facts2, facts3]

print json.dumps(devices, indent=4)

```

##### Step 3

Execute the script.

```
ntc@ntc:~/scripts$ python print_facts.py
[
    {
        "os": "nxos", 
        "ipaddr": "10.1.1.1", 
        "vendor": "cisco"
    }, 
    {
        "os": "ios", 
        "ipaddr": "10.2.1.1", 
        "vendor": "cisco"
    }, 
    {
        "os": "eos", 
        "ipaddr": "10.1.1.2", 
        "vendor": "arista"
    }
]
ntc@ntc:~/scripts$
```

The point in this lab is to showcase the transition going from learning to write code on the Python shell.

We'll now move onto more useful scripts.


