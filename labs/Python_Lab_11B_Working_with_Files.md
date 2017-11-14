## Lab 11B - Working with Files

### Task 1 - Reading Data from YAML Files

In this task, we're going to introduce how a YAML file is rendered in Python seeing how YAML files map 1 to 1 to specific Python objects such as strings, lists, and dictionaries.

> Note: we will spend much more time on YAML later in the course.  This is just a light introduction to see how a YAML file maps to Python objects.

##### Step 1

Navigate to the `scripts` directory within your home directory.:

```
ntc@ntc:~$ cd scripts
ntc@ntc:~/scripts$
```

##### Step 2

Create a new file named `data.yml`. This will contain YAML data that we'll print in Python.

```
ntc@ntc:~/scripts$ touch data.yml
ntc@ntc:~/scripts$
```

##### Step 3

Open the file in Sublime (or text editor of your choice).

##### Step 4

Copy and paste the following into `data.yml`.

``` yaml
---

hostname: nycr01
snmp_ro: public
snmp_rw: private


```

We've defined three key-value pairs in a YAML file.  Let's see what that looks like in Python


##### Step 5

To visualize how to work with a YAML file within our code, we can first explore it within the Python interpreter shell.

From the command prompt, enter the Python interpreter shell.

``` python
ntc@ntc:~/scripts$ python
Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
[GCC 5.4.0 20160609] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> 
>>> 
```

##### Step 6

Import the `yaml` module - this is needed to easily translate YAML encoded data to standard Python datatypes.

``` python
>>> import yaml
>>> 

```

##### Step 7

Next, read the YAML file, and load it's contents as a standard python dictionary variable.

``` python
>>> yaml_file = open('data.yml', 'r')
>>> data = yaml.load(yaml_file)
>>> 
>>> type(data)
<type 'dict'>
>>>
```

##### Step 8

Print out the `data` variable

``` shell
>>> print(data)
{'hostname': 'nycr01', 'snmp_ro': 'public', 'snmp_rw': 'private'}
>>>
```

Notice how the full YAML file is a dictionary and each key-value pair in the file is a key-value pair in the dictionary.

##### Step 9

You can additionally pretty print the data:

```python
>>> print json.dumps(data, indent=4)
{
    "hostname": "nycr01", 
    "snmp_ro": "public", 
    "snmp_rw": "private"
}
>>> 
```


##### Step 10

Now make the following changes to open and load the file in one step.  This will simplify the process as you continue to add data to the YAML file.

```python
>>> data = yaml.load(open('data.yml', 'r'))
>>> 
```

##### Step 11

Update the data YAML file to have the VLANs as shown below:

```yaml
---

hostname: nycr01
snmp_ro: public
snmp_rw: private

vlans_list:
  - 1
  - 2
  - 3
  - 100
```

##### Step 12

Re-load and print the data in the YAML.

```python
>>> data = yaml.load(open('data.yml', 'r'))
>>> 
```

```python
>>> print(data)
{'snmp_rw': 'private', 'hostname': 'nycr01', 'snmp_ro': 'public', 'vlans_list': [1, 2, 3, 100]}
>>>
```

Note: whenever you see a hyphen `-` in a YAML file, that denotes a `list` object in Python.

##### Step 13

Remember to pretty print it to make it easier to read:

```python
>>> print json.dumps(data, indent=4)       
{
    "snmp_rw": "private", 
    "hostname": "nycr01", 
    "snmp_ro": "public", 
    "vlans_list": [
        1, 
        2, 
        3, 
        100
    ]
}
>>> 
```

##### Step 14

Update the data YAML file to have the VLANs as shown below:

```yaml
---

hostname: nycr01
snmp_ro: public
snmp_rw: private

vlans_list:
  - 1
  - 2
  - 3
  - 100

snmp:
  ro: public
  rw: private
  contact: JOHN SMITH
  location: AMERS

```


##### Step 15

Re-load and print the data in the YAML.

```python
>>> data = yaml.load(open('data.yml', 'r'))
>>> 
```

```python
>>> print(data)
{'snmp_rw': 'private', 'hostname': 'nycr01', 'snmp': {'rw': 'private', 'ro': 'public', 'location': 'AMERS', 'contact': 'JOHN SMITH'}, 'snmp_ro': 'public', 'vlans_list': [1, 2, 3, 100]}
>>> 

```

Whenever you use an indentation under a key in a YAML file, that'll map back and be a dictionary while in Python:

```python
>>> print json.dumps(data, indent=4)
{
    "snmp_rw": "private", 
    "hostname": "nycr01", 
    "snmp": {
        "rw": "private", 
        "ro": "public", 
        "location": "AMERS", 
        "contact": "JOHN SMITH"
    }, 
    "snmp_ro": "public", 
    "vlans_list": [
        1, 
        2, 
        3, 
        100
    ]
}
>>>
```

Feel free to access these elements while on the Python shell or add more objects in your YAML file and continue this process.