## Lab 12 - Network Automation with Netmiko 

In this lab, we will explore using netmiko for network automation on the Juniper VMX devices.

### Task 1 - Using Netmiko

This task will show you how to establish an interactive SSH session to a Junuper VMX router running JUNOS using Netmiko.  

> Note: More specifically, this lab uses the Juniper VMX  running 15.1F4.15.

##### Step 1

Enter the Python Dynamic Interactive Interpreter.

##### Step 2

Import the netmiko `ConnectHandler` object and establish an SSH session to the Virtual MX router with the following details:

* hostname: vmx7
* Username: ntc
* Password: ntc123
* SSH port: 22

```python
>>> from netmiko import ConnectHandler
>>> 
>>> platform = 'juniper_junos'
>>> host = 'vmx7'
>>> username = 'ntc'
>>> password = 'ntc123'
>>> 
>>> device = ConnectHandler(device_type=platform, ip=host, username=username, password=password)
>>>
>>> 
```

##### Step 3

Issue a `dir()` on `device` to see available methods that can be called.

```python
>>> dir(device)
['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_autodetect_fs', '_connect_params_dict', '_read_channel_expect', '_read_channel_timing', '_sanitize_output', '_use_ssh_config', 'alt_host_keys', 'alt_key_file', 'ansi_escape_codes', 'base_prompt', 'check_config_mode', 'check_enable_mode', 'cleanup', 'clear_buffer', 'commit', 'config_mode', 'device_type', 'disable_paging', 'disconnect', 'enable', 'establish_connection', 'exit_config_mode', 'exit_enable_mode', 'find_prompt', 'global_delay_factor', 'host', 'ip', 'key_file', 'key_policy', 'normalize_cmd', 'normalize_linefeeds', 'password', 'port', 'protocol', 'read_channel', 'read_until_pattern', 'read_until_prompt', 'read_until_prompt_or_pattern', 'remote_conn', 'remote_conn_pre', 'secret', 'select_delay_factor', 'send_command', 'send_command_expect', 'send_command_timing', 'send_config_from_file', 'send_config_set', 'session_preparation', 'set_base_prompt', 'set_terminal_width', 'special_login_handler', 'ssh_config_file', 'strip_ansi_escape_codes', 'strip_backspaces', 'strip_command', 'strip_prompt', 'system_host_keys', 'telnet_login', 'timeout', 'use_keys', 'username', 'verbose', 'write_channel']
>>> 
```

##### Step 4

Execute the command `show version` using netmiko:

```python
>>> output = device.send_command('show version')
>>> 
>>> print(output)

Hostname: vmx7
Model: vmx
Junos: 15.1F4.15
JUNOS Base OS boot [15.1F4.15]
JUNOS Base OS Software Suite [15.1F4.15]
JUNOS Crypto Software Suite [15.1F4.15]
JUNOS Online Documentation [15.1F4.15]
JUNOS 64-bit Kernel Software Suite [15.1F4.15]
JUNOS Routing Software Suite [15.1F4.15]
JUNOS Runtime Software Suite [15.1F4.15]
JUNOS 64-bit Runtime Software Suite [15.1F4.15]
JUNOS Services AACL PIC package [15.1F4.15]
JUNOS Services Application Level Gateway (xlp64) [15.1F4.15]
JUNOS Services Application Level Gateway [15.1F4.15]
JUNOS Services Application Level Gateway (xlr64) [15.1F4.15]
JUNOS Services AppId PIC package (xlr64) [15.1F4.15]
JUNOS AppId Services PIC Package [15.1F4.15]
JUNOS Services Captive Portal and Content Delivery PIC package [15.1F4.15]
JUNOS Border Gateway Function PIC package [15.1F4.15]
JUNOS Services HTTP Content Management PIC package [15.1F4.15]
JUNOS Services Captive Portal and Content Delivery (xlp64) [15.1F4.15]
JUNOS IDP Services PIC Package [15.1F4.15]
JUNOS Services HTTP Content Management PIC package (xlr64) [15.1F4.15]
JUNOS Services JFLOW PIC package (xlp64) [15.1F4.15]
JUNOS Services JFLOW PIC package [15.1F4.15]
JUNOS Services LL-PDF PIC package [15.1F4.15]
JUNOS MobileNext PIC package [15.1F4.15]
JUNOS Services Mobile Subscriber Service PIC package (xlr64) [15.1F4.15]
JUNOS Services Mobile Subscriber Service Container package [15.1F4.15]
JUNOS MobileNext PIC package (xlr64) [15.1F4.15]
JUNOS Services PTSP PIC package [15.1F4.15]
JUNOS Services NAT PIC package (xlr64) [15.1F4.15]
JUNOS Services NAT PIC package (xlp64) [15.1F4.15]
JUNOS Services NAT PIC package [15.1F4.15]
JUNOS Services RPM PIC package (xlp64) [15.1F4.15]
JUNOS Services RPM PIC package [15.1F4.15]
JUNOS Services Stateful Firewall PIC package (xlr64) [15.1F4.15]
JUNOS Services Stateful Firewall PIC package (xlp64) [15.1F4.15]
JUNOS Services Stateful Firewall PIC package [15.1F4.15]
JUNOS BSG PIC package [15.1F4.15]
JUNOS Services Crypto Base PIC package [15.1F4.15]
JUNOS Services Crypto Base PIC package [15.1F4.15]
JUNOS Services Crypto Base PIC package(xlr64) [15.1F4.15]
JUNOS Services IPSec PIC(xlr64) package [15.1F4.15]
JUNOS Services IPSec PIC package [15.1F4.15]
JUNOS Services IPSec PIC package [15.1F4.15]
JUNOS Services SSL PIC package [15.1F4.15]
JUNOS Packet Forwarding Engine Simulation Package [15.1F4.15]

>>>
```


##### Step 5

Shutdown interface `ge-0/0/3` sending one command at a time.

```python
>>> device.config_mode()
u'configure \r\nEntering configuration mode\r\n\r\n[edit]\r\nntc@vmx7# '
>>> 
>>> device.send_command('set interfaces ge-0/0/3 disable')
u'\n'
>>> device.commit()
u'commit \ncommit complete\n\n[edit]\nntc@vmx7# '
>>> 
```

To absorb the output for each command and not see the returning prompts, you can simply do the following (or use different variables):

```python 
>>> data =  device.config_mode()
>>> data = device.send_command('set interfaces ge-0/0/3 disable')
>>> data = device.commit()
>>>
```
> Log in to the vmx7 from another terminal to validate changes.

Exit configuration mode:

```python
>>> device.exit_config_mode()
u'exit configuration-mode \nExiting configuration mode\n\nntc@vmx7> '
>>>
```


##### Step 6

Re-enable interface `ge-0/0/3` *sending a list of commands*.

```python
>>> commands = ['set interfaces ge-0/0/3 enable', 'commit']
>>> 
>>> device.send_config_set(commands)
u'configure \nEntering configuration mode\n\n[edit]\nntc@vmx7# set interfaces ge-0/0/3 enable \n\n[edit]\nntc@vmx7# commit \ncommit complete\n\n[edit]\nntc@vmx7# exit configuration-mode \nExiting configuration mode\n\nntc@vmx7> '
>>> 
>>>
```

If you save the output in a variable and use the print command, you will see a cleaner output:

```python
>>> response = device.send_config_set(commands)
>>> 
>>> print(response)
configure 
Entering configuration mode

[edit]
ntc@vmx7# set interfaces ge-0/0/3 enable 

[edit]
ntc@vmx7# commit 
commit complete

[edit]
ntc@vmx7# exit configuration-mode 
Exiting configuration mode

ntc@vmx7> 

>>>
```
> Log in to the vmx7 from another terminal to validate changes.

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

##### Step 7

Continue to try other Netmiko methods as you saw in Step 3.

##### Step 8

Disconnect from the device

```python
>>> device.disconnect()
>>> 
```

Exit the Python shell.


