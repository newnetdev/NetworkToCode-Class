## Lab 16 - Performing a Conditional Traceroute Based on Ping Failures

In the previous lab, you learned how to use TextFSM templates and custom Ansible RegEx spec files to parse data.

In this lab, you'll use more built-in filters to parse data, but also conditionally perform another task, based on the response coming back from the device.

### Task 1 - Pinging Remote IPs from the Device

The first task will setup the foundation by just getting a ping response back to Ansible, but now also parsing the data too.

##### Step 1

Create a new playbook called `test-reachability.yml`.  Use the following to get started.  There is nothing new in this playbook that we haven't already covered.

```yaml
---

  - name: PING TEST AND TRACEROUTE
    hosts: csr1
    connection: local
    gather_facts: no

    vars:
      dest: "8.8.8.8"

    tasks:

    - name: ISSUE PING
      ios_command:
        commands: "ping vrf MANAGEMENT {{ dest }} repeat 2"
      register: output
```



##### Step 2

Add two new tasks:

  * One that will _parse_ the "show version" response using the pre-built `regex_filter` filter and save it as a new variable using the `set_fact` module.
  * One that will debug the new variable.

```yaml
---

  - name: PING TEST AND TRACEROUTE
    hosts: csr1
    connection: local
    gather_facts: no

    vars:
      dest: "8.8.8.8"

    tasks:

    - name: ISSUE PING
      ios_command:
        commands: "ping vrf MANAGEMENT {{ dest }} repeat 2"
      register: output

    - name: PARSE PING RESPONSE TO OBTAIN % OF SUCCESS
      set_fact:
        ping_pct: "{{ output.stdout.0 | regex_search('Success rate is (\\d+)\\s+percent') | regex_search('(\\d+)') }}"

    - debug:
        var: ping_pct 
```

This example is _chaining_ `regex_search()` calls together because the first one returns "Success rate is 80 percent" and when passing it to the seconf filter, it then only returns "80".

> Note: keep in mind the extra `\` for RegEx when writing RegEx in Ansible as compared to Python where it wasn't used.

##### Step 3

Save and Execute the playbook.

##### Step 4 (Optional)

This step is optional or read-only as it shows another way to parse the ping response coming back from the device.  This time withthe `regex_findall` filter.  Because it's a `find_all` filter, it always returns a list.  Since we know this match would only ever occur once, we're combinging this with the `first` filter to return the first element in the list.

>Note: the `regex_findall` only returns the data in the RegEx capture group.

```yaml

    - name: ALTERNATE OPTION FOR PARSING WITH REGEX
      set_fact:
        ping_data2: "{{ output.stdout.0 | regex_findall('Success rate is (\\d+)\\s+percent') | first }}"

    - name: ALTERNATE DEBUG
      debug:
        var: ping_data2 


```

If you've chosen to do this step, save and execute the playbook.

##### Step 4

Let's now add a task to traceroute to the same target IP address.  We're also using a timeout of "1" and a max TTL of "5" to speed things up for the lab.

```yaml
    - name: ISSUE TRACEROUTE
      ios_command:
        commands: "traceroute vrf MANAGEMENT {{ dest }} timeout 1 ttl 1 5"
      register: traceroute

    - name: DEBUG TRACEROUTE
      debug:
        var: traceroute  
```

##### Step 5

Save and execute the playbook.

##### Step 6

Add conditional logic using the `when` task attribute to only perform the traceroute if the ping response percentage is less than 81%.

In this task, we're also using a Jinja2 filter called `int` to convert `ping_pct` from a string to an integer so can perform comparisons on it.

```yaml
    - name: ISSUE TRACEROUTE
      ios_command:
        commands: "traceroute vrf MANAGEMENT {{ dest }} timeout 1 ttl 1 5"
      register: traceroute
      when: ping_pct|int < 81

    - name: DEBUG TRACEROUTE
      debug:
        var: traceroute  
```

##### Step 7

Save and execute the playbook.

Note: the traceroute task should NOT run.

##### Step 8

Execute the playbook using extra vars passing in a new `dest` IP address to test against.

```

ntc@ntc:ansible$ ansible-playbook -i inventory test-reachability.yml --extra-vars="dest=4.4.4.4"
```

You could also simply just change the value inside the playbook.  

Feel free to change `hosts: csr1` to all devices or also make that a variable and use another extra variable.

**The final playbook should look like this:**


```yaml
  - name: PING TEST AND TRACEROUTE
    hosts: csr1
    connection: local
    gather_facts: no

    vars:
      dest: "8.8.8.8"

    tasks:

    - name: ISSUE PING
      ios_command:
        commands: "ping vrf MANAGEMENT {{ dest }} repeat 2"
      register: output

    - name: PARSE PING RESPONSE TO OBTAIN % OF SUCCESS
      set_fact:
        ping_pct: "{{ output.stdout.0 | regex_search('Success rate is (\\d+)\\s+percent') | regex_search('(\\d+)') }}"

    - debug:
        var: ping_pct 

    - name: ALTERNATE OPTION FOR PARSING WITH REGEX
      set_fact:
        ping_data2: "{{ output.stdout.0 | regex_findall('Success rate is (\\d+)\\s+percent') | first }}"

    - name: ISSUE TRACEROUTE
      ios_command:
        commands: "traceroute vrf MANAGEMENT {{ dest }} timeout 1 ttl 1 5"
      register: traceroute
      when: ping_pct|int < 81

    - name: DEBUG TRACEROUTE
      debug:
        var: traceroute  
```


