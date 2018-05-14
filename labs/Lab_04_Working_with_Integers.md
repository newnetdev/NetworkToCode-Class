## Lab 4 - Working with Integers

This lab provides an introduction to working with integers in Python.  While integers aren't used much in the course, it's still worth understanding some basics of integers.

##### Step 1

Create the variable `vlan_id` and assign it the value of 10. 

```python
>>>
>>> vlan_id = 10
>>> 
```

##### Step 2

Check the data type of `vlan_id`:

```python
>>> type(vlan_id)
<type 'int'>
>>> 
```

##### Step 3

Using the `dir(vlan_id)` or `dir(list)` statement, view all built-in methods for integers:

```python
>>> dir(vlan_id)
['__abs__', '__add__', '__and__', '__class__', '__cmp__', '__coerce__', '__delattr__',
'__div__', '__divmod__', '__doc__', '__float__', '__floordiv__', '__format__',
'__getattribute__', '__getnewargs__', '__hash__', '__hex__', '__index__', '__init__',
'__int__', '__invert__', '__long__', '__lshift__', '__mod__', '__mul__', '__neg__',
'__new__', '__nonzero__', '__oct__', '__or__', '__pos__', '__pow__', '__radd__',
'__rand__', '__rdiv__', '__rdivmod__', '__reduce__', '__reduce_ex__', '__repr__',
'__rfloordiv__', '__rlshift__', '__rmod__', '__rmul__', '__ror__', '__rpow__',
'__rrshift__', '__rshift__', '__rsub__', '__rtruediv__', '__rxor__', '__setattr__',
'__sizeof__', '__str__', '__sub__', '__subclasshook__', '__truediv__', '__trunc__',
'__xor__', 'bit_length', 'conjugate', 'denominator', 'imag', 'numerator', 'real']
>>>
```

You'll notice there are not very many relevant methods for integers.

##### Step 4

Create a new variable called `vid` and assign it the value of "100" using quotes:

```python
>>> vid = "100"
>>> 
```

##### Step 5

Print both `vlan_id` and `vid` using the print statement:

```python
>>> print(vlan_id)
10
>>> 
>>> print(vid)
100
>>>
```

Notice how you cannot tell the data type from a print statement.  Be careful and be consistent with the data types you choose!

##### Step 6

Print them both again without using the print statement:

```python
>>> vlan_id
10
>>> 
>>> vid
'100'
>>> 
```

Here you can see which one the string is by noticing the quotes wrapped around the value.

##### Step 7

Let's now take a look at a concept called "casting" converting one data type to another.

Create a variable called `ipaddr` and assign it the value of "10.2.9.1" and also create another variable called `mask` assigning it a value of 24:

```python
>>> ipaddr = "10.2.9.1"
>>> 
>>> mask = 24
>>> 
```

##### Step 8

Now try concatenating `ipaddr` and `mask` while inserting a "/" in between both:

```python
>>> ipaddr + "/" + mask
```

You should see this error message:

```python
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: cannot concatenate 'str' and 'int' objects
>>> 
```

Note that you cannot concatenate a string and an integer.  You must convert the integer to a string.

##### Step 9

You can convert the integer to a string using the `str()` function:

```python
>>> ipaddr + "/" + str(mask)
'10.2.9.1/24'
>>> 
```

##### Step 10

Here are a few more examples looking at using `str()` and `int()`. 

Ensure you still have `vlan_id` with an integer value of 10.

Walk through the process of converting this to a new variable that is a string equivalent. 

```python
>>> type(vlan_id)
<type 'int'>
>>> 
>>> vlan_id_string = str(vlan_id)
>>> 
>>> type(vlan_id_string)
<type 'str'>
>>> 
```


