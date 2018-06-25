## Lab 8 - Using Python Modules

In programming languages, you often need to "import" other libraries to get added functionality.  In this lab, we'll explore using a few Python libraries that come with the standard installation of Python.

Take note that a Python library may be a:

  * Python module - which is a file that has Python code
  * Python package - which is a collection of Python modules


### Task 1 - Using the json module

##### Step 1

Create a dictionary called `facts`:

```python
>>> facts = {'platform': 'nexus', 'version': '7.3', 'vendor': 'cisco', 'device_type': 'switch', 'os': 'nxos'}
>>>
```

##### Step 2

Print the dictionary:

```python
>>> print(facts)
{'platform': 'nexus', 'version': '7.3', 'vendor': 'cisco', 'device_type': 'switch', 'os': 'nxos'}
>>>
```

The larger the dictionary, the harder this will be to read.

Let's introduce a Python module that helps in pretty printing Python objects like dictionaries.

##### Step 3

First, import the `json` module using the `import` keyword:

```python
>>> import json
>>>
```

##### Step 4

Using the `dumps` function in the `json` module to pretty print the dictionary. We'll use an indent of 4.

```python
>>> print(json.dumps(facts, indent=4))
{
    "platform": "nexus",
    "version": "7.3",
    "vendor": "cisco",
    "device_type": "switch",
    "os": "nxos"
}
>>>
```

##### Step 5

We'll see 4 for every example in the course, but feel free to try 10 and 20 and see what happens:

```python
>>> print(json.dumps(facts, indent=10))
{
          "platform": "nexus",
          "version": "7.3",
          "vendor": "cisco",
          "device_type": "switch",
          "os": "nxos"
}
>>>
>>> print(json.dumps(facts, indent=20))
{
                    "platform": "nexus",
                    "version": "7.3",
                    "vendor": "cisco",
                    "device_type": "switch",
                    "os": "nxos"
}
>>>
```

Using `json.dumps` is going to help tremendously when trying to read larger dictionary objects in the next section.

### Task 2 - Using the time module

When you're writing a Python script, you may need to insert a _pause_ or delay.  This may be needed if you're performing many operations on a device, or need to give a device time to perform a calculation.

You can do this with the `time` module.  Specifically the `sleep` function.  Let's see how.

##### Step 1

Import the `time` module:

```python
>>> import time
>>>
```


##### Step 2

Insert a pause for 5 seconds using the `sleep` function:

```python
>>> time.sleep(5)
>>>
```

Notice how the keyboard hangs for 5 seconds.  This comes in handy when you're writing Python scripts (which we'll do soon).

##### Step 3

Explore printing the date and time with the `time` module.

First, do a `dir(time)`.  You'll see there are many objects within the `time` module

Here is one example of how to print the local time:

```python
>>> local_time = time.asctime()
>>>
>>> print(local_time)
Sat January 27 19:21:47 2018
>>>
```

Feel free to use the help menu on the individual objects above.


### Task 3 - Using the os module

This task shows how you can access the underlying "os" of a given device.

##### Step 1

Import the `os` module:

```python
>>> import os
>>>
```

##### Step 2

You can check to see your current working directory with the `getcwd()` function:

```python
>>> os.getcwd()
'/home/ntc'
>>>

```

##### Step 3

You can also change your working directory with `chdir()`:

```python
>>> os.chdir('/home/ntc/files')
>>>
>>> os.getcwd()
'/home/ntc/files'
>>>
```

##### Step 4

You can also access your OS ENVIRONMENT variables. Here we're accessing an environment variable called `HOME`:

```python
>>> os.getenv('HOME')
'/home/ntc'
>>>
```

In a separate Linux terminal window, you can type `env` to see other environment variables you can check from Python.

##### Step 5

You can also list the contents of a given directory from Python:

```python
>>> os.listdir('/home/ntc')
# output omitted
>>>
```

##### Step 6

You can even issue arbitrary Linux commands from Python:

```python
>>> os.system('date')    
Sat Feb 17 19:37:18 UTC 2018
0
>>>
```

```python
>>> os.system('ifconfig')
# output omitted
>>>
```

Keep in mind, this lab is just showing how to get started with Python modules.  It's not an exhaustive list of what's possible and it's not making recommendations to do things like executing Linux commands from Python.

However, you can view the standard Python docs for a module like `os` here:

https://docs.python.org/2/library/os.html


**Note: we'll continue to use even more Python modules throughout the course.**
