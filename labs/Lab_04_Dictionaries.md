## Lab 4 - Dictionaries

### Task 1 - Working with Dictionaries

##### Step 1

Ensure you are back at the Python shell.

##### Step 2

Create three dictionaries called `facts_1`, `facts_2`, and `facts_3`.  Each of these dictionaries will store information about a particular network device.

Use a different approach for creating each of the dictionaries as shown below.

*Method 1*

```python
>>>
>>> facts_1 = dict(hostname='APAC1', vendor='arista', location='Sydney', model='7050')
>>> facts_1
{'model': '7050', 'hostname': 'APAC1', 'vendor': 'arista', 'location': 'Sydney'}
```

*Method 2*

```python
>>> facts_2 = {}
>>> facts_2['hostname'] = 'EMEA1'
>>> facts_2['vendor'] = 'cisco'
>>> facts_2['location'] = 'London'
>>> facts_2['model'] = '9396'
>>>
>>> facts_2
{'model': '9396', 'hostname': 'EMEA1', 'vendor': 'cisco', 'location': 'London'}
```


*Method 3*

```python
>>> facts_3 = {'model': 'catalyst', 'hostname': 'NAUS2', 'vendor': 'cisco', 'location': 'new_york'}
>>>
>>> facts_3
{'model': 'catalyst', 'hostname': 'NAUS2', 'vendor': 'cisco', 'location': 'new_york'}
```


##### Step 3

Update the `vendor` for `facts_2` to be **juniper** and the `model` to be **mx**.

```python
>>> facts_2['model'] = 'mx'
>>> facts_2['vendor'] = 'juniper'
>>> 
>>> print(facts_2)
{'model': 'mx', 'hostname': 'EMEA1', 'vendor': 'juniper', 'location': 'London'}
>>> 
```

Each of the values are easily over written if they already exist.

##### Step 4

Add a new key called `os` to each of the facts dictionaries.  

For each of `facts_1`, `facts_2`, `facts_3`, the key should be set to **eos**, **junos**, and **ios**, respectively.

`facts_1`:

```python
>>> facts_1['os'] = 'eos'
>>> 
>>> print(facts_1)
{'os': 'eos', 'model': '7050', 'hostname': 'APAC1', 'vendor': 'arista', 'location': 'Sydney'}
>>> 
```

`facts_2`:


```python
>>> facts_2['os'] = 'junos'
>>> 
>>> print(facts_2)
{'os': 'junos', 'model': 'mx', 'hostname': 'EMEA1', 'vendor': 'juniper', 'location': 'London'}
>>> 
```

`facts_3`:

```python
>>> facts_3['os'] = 'ios'
>>> 
>>> print(facts_3)
{'os': 'ios', 'model': 'catalyst', 'hostname': 'NAUS2', 'vendor': 'cisco', 'location': 'new_york'}
>>> 
```


This important piece here is realize it's the same process to add new _items_ (key-value pairs) or over-write them.


##### Step 5

Review the built-in methods for dictionaries using the `dir()` function on `facts_2`

```python
>>> dir(facts_2)
['clear', 'copy', 'fromkeys', 'get', 'has_key', 'items', 'iteritems', 'iterkeys', 'itervalues',
'keys', 'pop', 'popitem', 'setdefault', 'update', 'values', 'viewitems', 'viewkeys',
'viewvalues']
>>> # shorterned for brevity
```

##### Step 6

Print the keys for `facts_1`:

```python
>>> print(facts_1.keys())
['os', 'model', 'hostname', 'vendor', 'location']
>>> 
```

##### Step 7

Print the values for `facts_1`:

```python
>>> print(facts_1.values())
['eos', '7050', 'APAC1', 'arista', 'Sydney']
>>> 
```


##### Step 8

Now print the keys and the values for `facts_2`.

```python
>>> print(facts_2.keys())
['os', 'model', 'hostname', 'vendor', 'location']
>>> 
>>> print(facts_2.values())
['junos', 'mx', 'EMEA1', 'juniper', 'London']
>>> 
```


##### Step 9

Print the value for `hostname` in `facts_3`:

```python
>>> print(facts_3['hostname'])
NAUS2
>>>
```

##### Step 10

Print the value for key called `os` in `facts_3`.


```python
>>> print(facts_3['os'])
ios
>>> 
```

##### Step 11

Try print the value for a key called `os_version` in `facts_3`:

```python
>>> print(facts_3['os_version'])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 'os_version'
>>> 
```

As expected, an error is thrown since the key DOES NOT exist.

##### Step 12

Now use the `get` method to return the string **unknown** when trying to print the value for `os_version`.

```python
>>> print(facts_3.get('os_version', 'unknown'))
unknown
>>>
```

##### Step 13

Store the return value in a variable.

```python
>>> os_ver = facts_3.get('os_version', 'unknown')
>>>
>>> print(os_ver)
unknown
>>>
```

##### Step 14

Repeat the same step, but do not return "unknown":

```python
>>> os_ver = facts_3.get('os_version')
>>>
>>> print(os_ver)
None
>>>
```

This is common when you just want to check to see if the key has **any** value assigned to it.  We haven't covered conditionals yet, but we would now be able to do `if os_ver:` and it would return `True` if there is any non null value assigned to it.

Using `get` is safe approach that allows you to check to see if there is a value assigned without knowing if the key exists (and without needing try/except error handling).


##### Step 15

Remove the `hostname` key-value pair from `facts_3` using the `pop` method.

> Remember to print the dictionary as much you want in between modifications, to see how the dictionary is being modified by the methods you are executing.

```python
>>> facts_3.pop('hostname')
'NAUS2'
>>>
```

##### Step 16

Update the hostname of **facts_3** to be **nycr01**:

```python
>>> facts_3['hostname'] = 'nycr01'
>>> 
>>> print(facts_3)
{'os': 'ios', 'model': 'catalyst', 'hostname': 'nycr01', 'vendor': 'cisco', 'location': 'new_york'}
>>> 
```

##### Step 17

Create a new dictionary called `static_facts`.  It should have two key value pairs.

* customer: **acme**
* device_type: **switch**

```python
>>> static_facts = {'customer': 'acme', 'device_type': 'switch'}
>>> 
```

##### Step 18

The facts in the `static_facts` dictionary pertinent for all 3 other devices that already have their own facts dictionaries: `facts_1`, `facts_2`, `facts_3`.

Use the `update` method to _combine_ `static_facts` with all 3 other dictionaries.

```python
>>> facts_1.update(static_facts)
>>> 
>>> facts_2.update(static_facts)
>>> 
>>> facts_3.update(static_facts)
>>> 
```

Verify the updated dictionaries:

```python
>>> print(facts_1)
{'customer': 'acme', 'vendor': 'arista', 'location': 'Sydney', 'device_type': 'switch', 'model': '7050', 'hostname': 'APAC1', 'os': 'eos'}
>>> 
>>> print(facts_2)
{'customer': 'acme', 'vendor': 'juniper', 'location': 'London', 'device_type': 'switch', 'model': 'mx', 'hostname': 'EMEA1', 'os': 'junos'}
>>> 
>>> print(facts_3)
{'customer': 'acme', 'vendor': 'cisco', 'location': 'new_york', 'device_type': 'switch', 'model': 'catalyst', 'hostname': 'nycr01', 'os': 'ios'}
>>> 
```

Do not exit the Python shell.


### Task 2 - Introduction to a List of Dictionaries

##### Step 1

Create a list of dictionaries using the three dictionaries from the previous task.  The name of the list should be `facts_list`.  After the list is created, print the new list.

```python
>>> facts_list = [facts_1, facts_2, facts_3]
>>> 
>>> print(facts_list)
[{'customer': 'acme', 'vendor': 'arista', 'location': 'Sydney', 'device_type': 'switch', 'model': '7050', 'hostname': 'APAC1', 'os': 'eos'}, {'customer': 'acme', 'vendor': 'juniper', 'location': 'London', 'device_type': 'switch', 'model': 'mx', 'hostname': 'EMEA1', 'os': 'junos'}, {'customer': 'acme', 'vendor': 'cisco', 'location': 'new_york', 'device_type': 'switch', 'model': 'catalyst', 'hostname': 'nycr01', 'os': 'ios'}]
>>> 

```

##### Step 2

Pretty print `facts_list` by using the `dumps` function in the `json`

You first need to import the `json` module:

```python
>>> import json
>>> 
```

Once you import it, use the `dumps` function to pretty print the list of dictionaries with an indentation of 4 spaces.

This will make the object much easier to read.

```python
>>> print(json.dumps(facts_list, indent=4))
[
    {
        "customer": "acme", 
        "vendor": "arista", 
        "location": "Sydney", 
        "device_type": "switch", 
        "model": "7050", 
        "hostname": "APAC1", 
        "os": "eos"
    }, 
    {
        "customer": "acme", 
        "vendor": "juniper", 
        "location": "London", 
        "device_type": "switch", 
        "model": "mx", 
        "hostname": "EMEA1", 
        "os": "junos"
    }, 
    {
        "customer": "acme", 
        "vendor": "cisco", 
        "location": "new_york", 
        "device_type": "switch", 
        "model": "catalyst", 
        "hostname": "nycr01", 
        "os": "ios"
    }
]
>>> 
```


#### Step 3

Print the hostname of the second device (from `facts_2`).

```python
>>> print(facts_list[1]['hostname'])
EMEA1
>>>
```

Notice the syntax.

You first need to access the second element with the index of `1`.  This *returns* the full dictionary of what was `facts_2`.  You then access and use the `hostname` key of the dictionary.

Take a few more minutes to explore `facts_list`.  

Try the following:
  * Print the facts_2 hostname
  * Print the facts_1 model
  * Print the facts_3 os type

You can also break each up into two steps instead of one step too.  For example: 

```python
>>> f1 = facts_list[1]
>>> f1hn = f1['hostname']
>>> print(f1hn)
EMEA1
>>> 
```


