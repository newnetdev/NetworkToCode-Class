## Lab 6 - Conditionals

### Task 1 - if

##### Step 1

Create a new dictionary that will depict a VLAN to configure on a device.

The three keys you should use for modeling the VLAN in this example are `id`, `name`, and `state`.  `state` refers to up/down state.

```python
>>> vlan = dict(id='100', name='app_vlan')
>>> 
```

>Note: don't worry that you didn't create a `state` key.

The goal is to prepare a list of commands to send to a device based on this dictionary.  And we need to check to make sure each value is not `None` within the dictionary before we build a list of commands.

##### Step 2

First, create a new variable called `commands` and extract the values we want from the dictionary.  Use the `get` method to do this.

```python
>>> commands = []
>>>
>>> vlan_id = vlan.get('id')
>>> name = vlan.get('name')
>>> state = vlan.get('state')
```

What would happen if we didn't use the `get` method here?


##### Step 3

Write a conditional if statement for each variable to check to ensure that some value exists for each parameter.  You should remember from the dictionary lab, that if the key doesn't exist, `None` is returned when using the `get` method.

> Note: you'll need to hit enter one extra time to exit the conditional block.  Ensure you see the `>>>` as depicted below and throughout this lab.


```python
>>> if vlan_id:
...     commands.append('vlan {}'.format(vlan_id))
...     
>>> if name:
...     commands.append('name {}'.format(name))
...
>>>
```

Notice how we are able to chain methods together.  Remember to read them inside out.

First, `'name {}'.format(name)` is executed and returns a string such as "name app_vlan".  Then "app_vlan" is appended to the `commands` variable.

##### Step 4

Add another conditional to check to see if `state` is up or down to generate the proper command.

```python
>>> if state:
...   if state == 'up':
...       commands.append('no shutdown')
...   if state == 'down':
...       commands.append('shutdown')
...
>>>
```

For validation, print the `state` variable.  What value does it have?

##### Step 5

Print the `commands` object that was generated.

```python
>>> print(commands)
['vlan 100', 'name app_vlan']
>>>
```


### Task 2 - if-elif

You may have realized that when you checked `state` there are two `if` statements, but they should never be executed one after the other because the **state** is EITHER up **or** down.  It makes much more sense to use `elif` and replace the second `if` statement.

##### Step 1

Update the `state` variable to be equal to "down".

```python
>>> state = 'down'
>>> 
```

##### Step 2

Re-enter the conditional for state.

```python
>>> if state:
...   if state == 'up':
...       commands.append('no shutdown')
...   elif state == 'down':
...       commands.append('shutdown')
...
>>>
```

##### Step 3

Print the `commands` object that was generated.

```python
>>> print(commands)
['vlan 100', 'name app_vlan', 'shutdown']
>>>
```

### Task 3 - if-elif-else

Let's re-focus on the `if state` conditional.

##### Step 1

If `state` is neither "up" or "down", print that there is an invalid entry.

```python
>>> state = 'unknown'
>>>
>>> if state:
...     if state == 'up':
...         commands.append('no shutdown')
...     elif state == 'down':
...         commands.append('shutdown')
...     else:
...         print('INVALID INPUT!!!')
...
INVALID INPUT!!!
>>>
```

### Task 4 - Containment

When there are specific values that you want to check, you can usually check them within your first conditional statement.  For example, we know that `state` should be "up" or "down".  We can use containment, using the `in` keyword to do this.  Let's examine how.

##### Step 1

Update the first conditional `if state` with an expression that checks to make sure `state` is `in ['up', 'down']`.  Otherwise, continue to print "INVALID INPUT!!!"

Notice the new indentation level for the `else` statement.

```python
>>> options = ['up', 'down']
>>>
>>> if state in options:
...     if state == 'up':
...         commands.append('no shutdown')
...     elif state == 'down':
...         commands.append('shutdown')
... else:
...     print('INVALID INPUT!!!')
...
INVALID INPUT!!!
>>>
```

You can also perform the same operation without pre-creating the list:

```python
>>>
>>> if state in ['up', 'down']:
...     if state == 'up':
...         commands.append('no shutdown')
...     elif state == 'down':
...         commands.append('shutdown')
... else:
...     print('INVALID INPUT!!!')
...
INVALID INPUT!!!
>>>
```

