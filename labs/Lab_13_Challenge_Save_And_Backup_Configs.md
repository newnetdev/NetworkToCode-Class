## Lab 13 - Challenge

Using only what has been covered in previous labs, use Netmiko to:

* Save the configurations for each **csr1** and **csr2**: `write memory`
* Backup the configuration for each **csr1** and **csr2** to your jump host saving them in `/home/ntc/scripts/configs`.  
* Each file should be saved as `csr1.cfg` and `csr2.cfg`
* Add a print statement when each of the four actions are occuring:
  * Connecting to the device
  * Saving the configuration
  * Backing up configuration
  * Writing configuration to file

Save this script in the `scripts` directory and call it `backup.py`

[Solution](challenges/challenge_13_solution.py)
