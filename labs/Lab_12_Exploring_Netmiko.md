## Lab 12 - Exploring Netmiko

In this lab, we will explore using Netmiko for network automation.  Recall that Netmiko is an SSH client for Python and in this lab you'll be SSH'ing and automating Cisco IOS devices. Even in a world where there are only APIs on network devices, you may still need to automate _turning on the API_.  And to do that, Netmiko is stil a great choice.

### Task 1 - Using Netmiko in Exec Mode

This task will show you how to establish an interactive SSH session to a Cisco router running IOS using Netmiko.  

> Note: More specifically, this lab uses the CSR 1000V running IOS XE.

##### Step 1

**Make sure you can ping csr1 from the Linux terminal.**

```
ntc@ntc:~$ ping csr1
PING csr1 (10.0.0.51) 56(84) bytes of data.
64 bytes from csr1 (10.0.0.51): icmp_seq=1 ttl=231 time=9.9 ms
64 bytes from csr1 (10.0.0.51): icmp_seq=2 ttl=231 time=8.8 ms
64 bytes from csr1 (10.0.0.51): icmp_seq=3 ttl=231 time=8.9 ms
```

##### Step 2

Navigate to the `files` directory and enter the Python Dynamic Interactive Interpreter.

```
ntc@ntc:~$ cd files
ntc@ntc:files$ 
```

```
ntc@ntc:files$ python
Python 2.7.6 (default, Oct 26 2016, 20:32:47) 
[GCC 4.8.4] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```


##### Step 3

Import the netmiko `ConnectHandler` object and establish an SSH session to the Cloud Services Router device switch with the following details:

* hostname: csr1
* Username: ntc
* Password: ntc123
* SSH port: 22



```python
>>> from netmiko import ConnectHandler
>>> 
>>> platform = 'cisco_ios'
>>> host = 'csr1'
>>> username = 'ntc'
>>> password = 'ntc123'
>>> 
>>> device = ConnectHandler(device_type=platform, ip=host, username=username, password=password)
>>>
>>> 
```

##### Step 4

Issue a `dir()` on `device` to see available methods that can be called.

```python
>>> dir(device)
['__class__', '__delattr__', '__dict__', '__doc__', '__enter__', '__exit__', 
'__format__', '__getattribute__', '__hash__', '__init__', '__module__', 
__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_autodetect_fs', 
'_build_ssh_client', '_connect_params_dict', '_lock_netmiko_session', 
'_modify_connection_params', '_read_channel', '_read_channel_expect', 
'_read_channel_timing', '_sanitize_output', '_session_locker', 
'_test_channel_read', '_timeout_exceeded', '_unlock_netmiko_session',
'_use_ssh_config', '_write_channel', 'allow_agent', 'alt_host_keys', 
'alt_key_file', 'ansi_escape_codes', 'base_prompt', 'check_config_mode', 
'check_enable_mode', 'cleanup', 'clear_buffer', 'commit', 'config_mode', 
'device_type', 'disable_paging', 'disconnect', 'enable', 'establish_connection'
, 'exit_config_mode', 'exit_enable_mode', 'find_prompt', 'global_delay_factor',
 'host', 'is_alive', 'keepalive', 'key_file', 'key_policy', 'normalize_cmd', 
 'normalize_linefeeds', 'password', 'port', 'protocol', 'read_channel', '
'read_until_pattern', 'read_until_prompt', 'read_until_prompt_or_pattern', 
 'remote_conn', 'remote_conn_pre', 'secret', 'select_delay_factor', 
 'send_command', 'send_command_expect', 'send_command_timing', 
 'send_config_from_file', 'send_config_set', 'session_preparation', 
 'session_timeout', 'set_base_prompt', 'set_terminal_width', 
 'special_login_handler', 'ssh_config_file', 'strip_ansi_escape_codes', 
 'strip_backspaces', 'strip_command', 'strip_prompt', 'system_host_keys', 
 'telnet_login', 'timeout', 'use_keys', 'username', 'verbose', 'write_channel']
>>> 
```


##### Step 5

Verify there is an active connection to the device.  Verify it is _alive_.

```python
>>> device.is_alive()
True
>>>
```

You could also view the help menu for this method too:

```python
>>> help(device.is_alive)
Help on method is_alive in module netmiko.base_connection:

is_alive(self) method of netmiko.cisco.cisco_ios.CiscoIosBase instance
    Returns a boolean flag with the state of the connection.
(END)
```

##### Step 6

Now we can send a few "show" or "exec" level commands.  To do this, use the `send_command` method.

Execute the command `show version` and save the response as a variable:

```python
>>> output = device.send_command('show version')
>>> 
>>> print output
Cisco IOS XE Software, Version 16.06.02
Cisco IOS Software [Everest], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.6.2, RELEASE SOFTWARE (fc2)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2017 by Cisco Systems, Inc.
Compiled Wed 01-Nov-17 07:24 by mcpre


Cisco IOS-XE software, Copyright (c) 2005-2017 by cisco Systems, Inc.
All rights reserved.  Certain components of Cisco IOS-XE software are
licensed under the GNU General Public License ("GPL") Version 2.0.  The
software code licensed under GPL Version 2.0 is free software that comes
with ABSOLUTELY NO WARRANTY.  You can redistribute and/or modify such
GPL code under the terms of GPL Version 2.0.  For more details, see the
documentation or "License Notice" file accompanying the IOS-XE software,
or the applicable URL provided on the flyer accompanying the IOS-XE
software.


ROM: IOS-XE ROMMON

csr1 uptime is 27 minutes
Uptime for this control processor is 32 minutes
System returned to ROM by reload
System image file is "bootflash:packages.conf"
Last reload reason: reload



This product contains cryptographic features and is subject to United
States and local country laws governing import, export, transfer and
use. Delivery of Cisco cryptographic products does not imply
third-party authority to import, export, distribute or use encryption.
Importers, exporters, distributors and users are responsible for
compliance with U.S. and local country laws. By using this product you
agree to comply with applicable laws and regulations. If you are unable
to comply with U.S. and local laws, return this product immediately.

A summary of U.S. laws governing Cisco cryptographic products may be found at:
http://www.cisco.com/wwl/export/crypto/tool/stqrg.html

If you require further assistance please contact us by sending email to
export@cisco.com.

License Level: ax
License Type: Default. No valid license found.
Next reload license Level: ax

cisco CSR1000V (VXE) processor (revision VXE) with 2190795K/3075K bytes of memory.
Processor board ID 9KIBQAQ3OPE
4 Gigabit Ethernet interfaces
32768K bytes of non-volatile configuration memory.
3984708K bytes of physical memory.
7774207K bytes of virtual hard disk at bootflash:.
0K bytes of WebUI ODM Files at webui:.

Configuration register is 0x2102

>>> 
```

##### Step 7

Re-issue the same command using a _pipe include_ to only return the Configuration register:

```python
>>> output = device.send_command('show version | include register')
>>> 
>>> print output
Configuration register is 0x2102
>>>
```

If you were doing a check to ensure all config registers were correct, you can this use the `in` containment keyword we covered in the booleans lab like so:

```python
>>> '0x2102' in output 
True
>>> 
```

Maybe it's more important the device just doesn't boot into ROMMON mode: 

```python
>>> '0x2142' not in output 
True
>>> 
```

##### Step 8

Save the configuration using the `wr mem` command.

```python
>>> output = device.send_command('wr mem')  
>>> 
>>> print(output)
Building configuration...
[OK]
>>>
```

You can always view the output coming back from the device saving it to a variable.

##### Step 9

Let's try checking connectivity to Google's DNS server.  Note our management interface is in the **MANAGEMENT** VRF.

```python
>>> output = device.send_command('ping vrf MANAGEMENT 8.8.8.8')
>>> 
>>> print(output)
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 8.8.8.8, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 2/2/2 ms
>>> 
```


### Task 2 - Issuing Configuration Commands with Netmiko

In this task, we'll explore two methods to send configuration commands to the device.

**Option 1:** - send a list of commands to the device.
**Option 2:** - send commands from a file.

While you can use the `send_command` method, it's much cleaner to use the methods shown in this task, e.g. `send_config_set` and `send_config_from_file`.


##### Step 1

Add a new loopback to the device by first creating a list of commands you want to send:

```python
>>> commands = ['interface Loopback100', 'ip address 10.200.1.20 255.255.255.0']
>>> 
```


##### Step 2

Use the `send_config_set` method takes a list as a parameter:

```python
>>> output = device.send_config_set(commands)
>>> 
```

You can optionally print the response seeing what Netmiko is doing under the covers.  Notice how it is automatically going into and exiting configuration mode.

```python
>>> print (output)
config term
Enter configuration commands, one per line.  End with CNTL/Z.
csr1(config)#interface Loopback100
csr1(config-if)#ip address 10.200.1.20 255.255.255.0
csr1(config-if)#end
csr1#
>>> 
```

##### Step 3

You can also use `help()` to learn more about each method just like you saw with the built-in Python data types.

For example, here is the help on `send_config_set`:

```python
>>> help(device.send_config_set)

Help on method send_config_set in module netmiko.base_connection:

send_config_set(self, config_commands=None, exit_config_mode=True, **kwargs) method of netmiko.cisco.cisco_nxos_ssh.CiscoNxosSSH instance
    Send group of configuration commands down the SSH channel.
    
    config_commands is an iterable containing all of the configuration commands.
    The commands will be executed one after the other.
    
    Automatically exits/enters configuration mode.
    
    **kwargs will allow passing of all the arguments to send_command
    strip_prompt and strip_command will be set to False if not explicitly set in
    the method call.
(END)
```

##### Step 4

Add two community strings and verify they're configured.  

```python
>>> snmp_commands = ['snmp-server community ntclab RO', 'snmp-server community ntcrw RW'] 
>>> 
>>> response = device.send_config_set(snmp_commands)
>>> 
>>> verify = device.send_command('show run | inc snmp-server community')
>>> 
>>> print verify
snmp-server community networktocode RO
snmp-server community public RO
snmp-server community ntclab RO
snmp-server community ntcrw RW
>>> 
```


##### Step 5

Let's try to send commands from a file now.

In a separate terminal window, navigate to the `files` directory and create a new file called `config.txt`

If you're unsure of where you entered the shell, remember you can do the following to check your current working directory:

```python
>>> import os
>>> 
>>> os.getcwd()
'/home/ntc/files'
>>> 
```

##### Step 6

Put the following commands into `config.txt`:

```bash
!
snmp-server community supersecret RW
snmp-server community notprivate RO
!
interface Loopback101
 ip address 10.9.88.1 255.255.255.0
!
```

##### Step 7

Deploy the commands from the config file using the Netmiko method called `send_config_from_file`:

```python
>>> output = device.send_config_from_file('config.txt')
>>> 
```

##### Step 8

Verify `output` has the commands without any errors being received from the device:

```python
>>> print output
config term
Enter configuration commands, one per line.  End with CNTL/Z.
csr1(config)#!
csr1(config)#snmp-server community supersecret RW
csr1(config)#snmp-server community notprivate RO
csr1(config)#!
csr1(config)#interface Loopback101
csr1(config-if)# ip address 10.9.88.1 255.255.255.0
csr1(config-if)#!
csr1(config-if)#
csr1(config-if)#end
csr1#
>>> 
```


### Task 3

In this task, you'll get to see a few more built-in methods.

##### Step 1

Enter Config Mode:

```python
>>> device.config_mode()
u'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\ncsr1(config)#'
>>> 
```

##### Step 2

By default `send_command` waits for the device "prompt string" to return to what it was.  If you're choosing to send non-global config commands using `send_command`, the prompt will change.  Therefore, you should be aware of `send_command_timing`:

```python 
>>> data =  device.config_mode()
>>> data = device.send_command_timing('interface Gigabit3')
>>>
```

However, to keep things simple, you should use `send_config_set` and `send_config_from_file` when sending configuration commmands.

##### Step 3

You can always view your prompt string:

```python
>>> print device.find_prompt()           
csr1(config-if)#
>>> 
```

##### Step 4

Exit configuration mode:

```python
>>> device.exit_config_mode()
u'end\ncsr1#'
>>>
```

##### Step 5

Disconnect from the device

```python
>>> device.disconnect()
>>> 
```

##### Step 6

Validate the SSH connection is no longer active:

```python
>>> device.is_alive()
False
>>> 
```

##### Step 7

Re-establish connection back to the device:

```python
>>> device.establish_connection()
u''
>>> 
```

##### Step 8

Finally, disconnect one final time.

```python
>>> device.disconnect()
>>> 
```
