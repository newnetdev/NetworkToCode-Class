## Dev Environment for Network to Coders

Sample Vagrantfile install and setup to get a host that closely replicates the jump host for the course.

### Step 1

Install Vagrant (Windows or MAC) install Virtualbox.


### Step 2

Clone this repo and navigate into the repo

### Step 3

Use the command `vagrant up` in the directory where `Vagrantfile` is.

The first time, it'll download the vagrant "box" (VM).

### Step 4

Once you see the login process fail b/c Vagrant is trying to use a default key.  You'll see this message:

```
default: Warning: Authentication failure. Retrying...
```

Let it time out or just control+C.

### Step 5

Copy your public key to the new VM.

```
ssh-copy-id vagrant@localhost -p 2222
```

Yes, it uses 2222 instead of 22.


### Step 6

We'll reload so we can continue the provisioning process (now the provisioner will automatically login)


```
vagrant reload
```

This will continue through the Vagrant file and run the Ansiblie provisioner.


### Step 6

This is just because we added a user called **ntc** in the provisioner with the creds ntc/ntc123.


```
ssh-copy-id ntc@localhost -p 2222
```


Then you can `ssh ntc@localhost -p 2222` without a password.


Note: At this point, `vagrant ssh` still uses the vagrant username, but you can add (uncomment) `config.vm.host_name = "ntc"` in Vagrantfile to make it such that `vagrant ssh` uses the `ntc username.




### Common Commands

* vagrant up
* vagrant ssh
* vagrant halt
* vagrant reload
* vagrant destroy
* vagrant provision - if just the playbook changes, use this as an option


Whenever you **destroy** and then `vagrant up` again, you'll have a fresh clean install (in a few minutes).  Can do multiple using different directories and same Vagrantfile.


### Sharing Data

* `.` (on your host, where the Vagrantfile is) automatically synch'd with `/vagrant` in the vagrant box so you can easily use client applications such as text editors and run scripts seamlessly in the VM.
* `~/ntc-data` (on your host) automatically synch'd with `/ntc-data` in the vagrant box so you can easily use client applications such as text editors and run scripts seamlessly in the VM.


### Accessing the VM

Currently, we have these ports mapped:

| On your local machine | VM Port |
|--------------------------|---------|
|    2222 | 22 |
|    8080 | 80 |
|    8443 | 443 |
|    4001 | 4000 |
|    5001 | 5000 |
|    8001 | 8000 |



### NOTES

* You can nest 64 bit VMs in Virtual Box right now, i.e. you can't use Vagrant within your existing Ubuntu VM in VBox
* If you do not want to use Windows as your client machine, you can VMware Workstation (expense it if needed)
* You can uncomment `config.vm.host_name = "ntc"` after the process is complete so that `vagrant ssh` natively uses the "ntc" user
* This has a modified prompt string - feedback welcome.  We don't need to stanardize on this, but we can try.




