## Lab 6 - Working with Booleans

### Task 1 - Working with Booleans Part 1

You've already seen booleans after learning and using string methods such as `startswith` and `isdigit`.  This lab will introduce more concepts as they relate to working with boolean values, expressions, and operators.

##### Step 1

Create a new variable called `is_layer3` and assign it the value of `True` (do not use quotes):

```python
>>> is_layer3 = True
>>>
```

> If you use quotes, it will be a string.

##### Step 2

Perform a type check on the variable:

```python
>>> type(is_layer3)
<type 'bool'>
>>>
```

##### Step 3

Create another variable called `needs_bgp` and assign it the value of `False`. Then print it out.

```python
>>> needs_bgp = False
>>>
>>> print(needs_bgp)
False
>>>
```

Note that True and False using capital T and F without quotes are the only two boolean values.  Every object in Python always evaluates to either True or False.

Let's take a look at a few boolean expressions.


##### Step 4

Create 3 variables called `hostname`, `vendor` and `interfaces`.


```python
>>> hostname = 'nxos-spine1'
>>> vendor = 'cisco'
>>> interfaces = ['Ethernet2/1', 'Ethernet2/2', 'Ethernet2/3']
>>>
```

We will use these to practice using boolean operators.

##### Step 5

Use the `==` operator to evaluate `hostname` with the `nxos-spine2` string and `vendor` with the `cisco` string.

The `==` operator is used to see if one object _is equal_ to another object.

```python
>>> hostname == 'nxos-spine2'
False
>>>
>>> vendor == 'cisco'
True
>>>
```

##### Step 6

Use the `>` and `!=` operators to evaluate `interfaces`'s length with the `3` number.

```python
>>> len(interfaces) > 3
False
>>>
>>> len(interfaces) != 3
False
```

##### Step 7

Note that `!=` says "does not equal", so you can also use this for the hostname check too:

```python
>>> hostname != 'nxos-spine2'
True
>>>
```

##### Step 8

Now use the `in` "containment" keyword to evaluate if "Ethernet2/4" is a defined interface.  You're checking to see if "Ethernet2/4" is in the `interfaces` list:

```python
>>> 'Ethernet2/4' in interfaces
False
>>>
```

In short, this is checking to see if an element exists in a list.

##### Step 9

You can also see if a sub-string exists in a string:

```python
>>> "Eth" in "Ethernet2/4"
True
>>>
```

This checked to see if the string "Eth" exists in the larger string "Ethernet2/4".

Note that it's case-sensitive:

```python
>>> "eth" in "Ethernet2/4"
False
>>>
```

##### Step 10

It's often good practice to normalize (if possible) before doing the comparison or logic check.

```python
>>> "eth" in "Ethernet2/4".lower()
True
>>>
```

##### Step 11

Use the `and` operator to evaluate if `Ethernet2/2` is a defined interface and `vendor` equals to `cisco`.

```python
>>> 'Ethernet2/2' in interfaces and vendor == 'cisco'
True
>>>
```

When using `and`, everything must be True for the expression to evaluate to True.

You can do a quick test to prove this:

```python
>>> True and True and True and False
False
>>>
>>> True and True and True
True
>>>
```

##### Step 12

When you use "or" only ONE element has to be True for the expression to be True:

```python
>>> hostname == "nxos-spine2" or hostname == "nxos-spine10"
False
>>>
```

```python
>>> vendor == "cisco" or hostname == "nxos-spine10"
True
>>>
```

### Task 2 - Working with Booleans Part 2

In this task, we'll explore the boolean value of a single variable.  This will be used heavily when you start using `if` statements in Python.

In Python, a variable can evaluate to either True or False.

##### Step 1

Create a new variable called `hostname` and assign it the value of "r1":

```python
>>> hostname = "r1"
>>>
```

Perform a boolean check on this varible using the `bool()` statement:

```python
>>> bool(hostname)
True
>>>
```

You may be wondering what's actually happening.  Yes, `hostname` is a string, but when used in a boolean expression, it would evaluate to True.

Why?  Because it has a value of one or more characters.

##### Step 2

Create a new variable called `vendor` and assign it the value of a null/empty string:

```python
>>> vendor = ""
>>>
```

Perform the same boolean check:

```python
>>> bool(vendor)
False
>>>
```

See the difference?  As long as a "value" is assigned, it would evaluate to True when used in an expression.

The same is true for other data types such as lists.

##### Step 3

Create a variable called `vendors` and assign it the value of `['cisco']`.  After it's created, do a boolean check:

```python
>>> vendors = ['cisco']
>>>
>>> bool(vendors)
True
>>>
```

##### Step 4

Perform the same excercise by using an empty list as the value:

```python
>>> vendors = []
>>>
>>> bool(vendors)
False
>>>
```

With this logic, you'll be able to know if there is some value assigned to your variable when we start using conditional logic (if statements) in Python.
