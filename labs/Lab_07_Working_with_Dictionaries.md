## Lab 7 - Working with Dictionaries

### Task 1 - Working with Dictionaries Part 1

##### Step 1

Create a variable called `facts` and assign the it value of "{}" that will make it an empty dictionary:

```python
>>> facts = {}
>>> 
```

##### Step 2

Perform a type check on `facts` to prove it's a dictoinary:

```python
>>> type(facts)
<type 'dict'>
>>>
```

##### Step 3

Add a single key-value pair to the `facts` dictionary.  The key should be "vendor" and the value should be "cisco":

```python
>>> facts['vendor'] = 'cisco'
>>> 
```

##### Step 4

Print the dictionary after adding the key-value pair:

```python
>>> print(facts)
{'vendor': 'cisco'}
>>> 
```

##### Step 5

Perform a `len()` check on `facts`:

```python
>>> len(facts)
1
>>> 
```

`facts` has a length of 1 because there is one "item" in the dictionary--ONE key-value pair.

##### Step 6

Add a few more key-value pairs as shown below and when done, print the updated `facts` dictionary:

```python
>>> facts['os'] = 'nxos'
>>> facts['version'] = '7.1'
>>> facts['platform'] = 'nexus'
>>> 
>>> print(facts)
{'os': 'nxos', 'version': '7.1', 'vendor': 'cisco', 'platform': 'nexus'}
>>> 
```

##### Step 7

Update the version from "7.1" to "7.3" and print the dictionary to verify it:

```python
>>> facts['version'] = "7.3"
>>> 
>>> facts
{'os': 'nxos', 'version': '7.3', 'vendor': 'cisco', 'platform': 'nexus'}
>>> 
```

##### Step 8

You can also create a dictionary using the same notation you see when you print it.  In the first few steps, you gradually added key-value pairs.  However, you could just assign a new dictionary a value when it's created too:

```python
>>> facts_2 = {'os': 'ios', 'version': '16.6', 'vendor': 'cisco', 'platform': 'catalyst'}
>>> 
```

##### Step 9

Another option is to use the built-in `dict()` function when creating dictionaries:

```python
>>>
>>> facts_3 = dict(hostname='APAC1', vendor='arista', location='Sydney', model='7050')
>>> facts_3
{'model': '7050', 'hostname': 'APAC1', 'vendor': 'arista', 'location': 'Sydney'}
```

When you print it, it looks the exact same as the previous methods.

In this syntax, you can also create an empty dictionary like this too:

```python
>>> facts_4 = dict()
>>> 
```


### Task 2 - Working with Dictionaries Part 2

##### Step 1

Review the built-in methods for dictionaries using the `dir()` function on `facts`:

```python
>>> dir(facts)
['clear', 'copy', 'fromkeys', 'get', 'has_key', 'items', 'iteritems', 'iterkeys', 'itervalues',
'keys', 'pop', 'popitem', 'setdefault', 'update', 'values', 'viewitems', 'viewkeys',
'viewvalues']
>>> # shorterned for brevity
```

##### Step 2

Print the keys for `facts`:

```python
>>> print(facts.keys())
['os', 'version', 'vendor', 'platform']
>>> 
```

##### Step 3

Print the values for `facts`:

```python
>>> print(facts.values())
['nxos', '7.3', 'cisco', 'nexus']
>>>  
```


##### Step 4

Now print the keys and the values for `facts_2`:

```python
>>> print(facts_2.keys())
['vendor', 'version', 'os', 'platform']
>>> 
>>> print(facts_2.values())
['cisco', '16.6', 'ios', 'catalyst']
>>> 
```


##### Step 5

Print the value for `hostname` in `facts_3`:

```python
>>> facts_3['hostname']
'APAC1'
>>>
```

##### Step 6

Print the value for the key called `os` in `facts`:

```python
>>> print(facts['os'])
nxos
>>> 
```

##### Step 7

Try to print the value for a key called `os_version` in `facts`:

```python
>>> print(facts['os_version'])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 'os_version'
>>> 
```

As expected, an error is thrown since the key DOES NOT exist.

##### Step 8

Now use the `get` method to try and return the value assigned to the `os_version` key:

```python
>>> facts.get('os_version')
>>> 
```

Notice there is no error - it's a bit cleaner to use.

##### Step 9

Not only is `get` cleaner, but you can return a designated value if the desired key doesn't exist:

```python
>>> facts.get('os_version', 'ERROR')
'ERROR'
>>>
```

##### Step 10

Repeat the same step, but do not return "unknown":

```python
>>> os_ver = facts.get('os_version')
>>>
>>> print(os_ver)
None
>>>
```

This is common when you just want to check to see if the key has **any** value assigned to it.  We haven't covered conditionals yet, but we would now be able to do `if os_ver:` and it would return `True` if there is any non null value assigned to it.  This is what we alluded at the end of the Booleans Lab.

Using `get` is safe approach that allows you to check to see if there is a value assigned without knowing if the key exists (and without needing try/except error handling).

Let's continue looking at other methods.

##### Step 11

Remove the `hostname` key-value pair from `facts_3` using the `pop` method.

> Remember to print the dictionary as much you want in between modifications, to see how the dictionary is being modified by the methods you are executing.

```python
>>> facts_3
{'model': '7050', 'hostname': 'APAC1', 'vendor': 'arista', 'location': 'Sydney'}
>>> 
```


```python
>>> facts_3.pop('hostname')
'APAC1'
>>>
```

##### Step 12

Update the hostname of **facts_3** to be **nycr01**:

```python
>>> facts_3['hostname'] = 'nycr01'
>>> 
>>> facts_3
{'model': '7050', 'hostname': 'nycr01', 'vendor': 'arista', 'location': 'Sydney'}
>>> 
```

##### Step 13

Create a new dictionary called `static_facts`.  It should have two key value pairs.

* customer: **acme**
* device_type: **switch**

```python
>>> static_facts = {'customer': 'acme', 'device_type': 'switch'}
>>> 
```

##### Step 14

The facts in the `static_facts` dictionary pertinent for all 3 other devices that already have their own facts dictionaries: `facts`, `facts_2`, `facts_3`.

Use the `update` method to _combine_ `static_facts` with all 3 other dictionaries.

```python
>>> facts.update(static_facts)
>>> 
>>> facts_2.update(static_facts)
>>> 
>>> facts_3.update(static_facts)
>>> 
```

Verify the updated dictionaries:

```python
>>> facts
{'customer': 'acme', 'platform': 'nexus', 'version': '7.3', 'vendor': 'cisco', 'device_type': 'switch', 'os': 'nxos'}
>>> 
>>> facts_2
{'customer': 'acme', 'platform': 'catalyst', 'version': '16.6', 'vendor': 'cisco', 'device_type': 'switch', 'os': 'ios'}
>>> 
>>> facts_3
{'customer': 'acme', 'vendor': 'arista', 'location': 'Sydney', 'device_type': 'switch', 'model': '7050', 'hostname': 'nycr01'}
>>> 
```

