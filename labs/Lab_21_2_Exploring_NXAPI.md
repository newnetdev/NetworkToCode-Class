## Lab 21.2 - Cisco NX-API

### Task 1 - NX-API Developer Sandbox

This tasks introduces you to the Developer Sandbox environment that exists on each Nexus switch (assuming it supports NX-API).  The NX-API is a great tool for beginners and experts alike, as it gives you direct insight with how the switch will respond to API calls.  This allows you to verify what key-value pairs and response you should be getting back as you are writing and testing your code.

##### Step 1

Open a Web Browser and connect to the switch using _http://nxos-spine1_. 

Ensure you are using **http**.

Login with the credentials ntc/ntc123.

![NX-API Sandbox Logon](images/cisco_sandbox_logon.png)

You will then see the NX-API Developer Sandbox.

![NX-API Sandbox 4](images/cisco_04.png)

##### Step 2

Enter the command "show version" in the large text box on the left hand side. Keep all other settings as default for now.

##### Step 3

Click the blue **POST** button.

You will see the response in the bottom right pane.

![NX-API Sandbox 5](images/cisco_05.png)

Notice the JSON data that came back. It has several key-value pairs including `jsonrpc`, `result`, and `id`.  Notably, the main response is in under its own key called `body` as the value for the key `result`.

##### Step 4

In the command text box, now enter the following command:

"show interface Eth2/1"

![NX-API Sandbox 6](images/cisco-show-int.png)

##### Step 5

Choose the Message format **XML** and choose the command type **cli_show_ascii**

>> Note: **cli_show_ascii** is used when you want to receive raw text back from the device as opposed to structured data that is returned when you use **cli_show**.

![NX-API Sandbox 7](images/cisco_07.png)

##### Step 6

Click the blue **POST** button.

You will see the raw text response just like you'd see if you were on the switch locally.

![NX-API Sandbox 8](images/cisco-show-int-rsp.png)

##### Step 7

Now keep the same command "show interface Eth2/1", but change the command type back to **cli_show**.

![NX-API Sandbox 12](images/cisco_12.png)

##### Step 8

Click the blue **POST** button.

Notice the difference from the previous task comparing and contrasting receiving structured data (XML) vs. raw text.  Feel free to try the same command using JSON-RPC.

![NX-API Sandbox 13](images/cisco-show-int-rsp2.png)

##### Step 9

Now Go back to the command text box and enter the following string:

```
interface Ethernet2/1 ; no shutdown
```

![NX-API Sandbox 9](images/cisco-config-int.png)

##### Step 10

Change the command type to be **cli_conf**.

**cli_conf** is used when you want to configure the device from within "configuration" mode on the switch.

![NX-API Sandbox 10](images/cisco_10.png)

##### Step 11

Click the blue **POST** button.

You will see the response in the bottom left.  Notice that a status code for each command returned.

![NX-API Sandbox 11](images/cisco_11.png)


Take a few more minutes and continue to explore the Cisco NX-API Developer Sandbox.

