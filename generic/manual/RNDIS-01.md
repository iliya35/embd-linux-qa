
### RNDIS-01

1. Test objective:
   - Checking the operation of Embedded device when connected to the host as an OTG slave device in the USB network adapter mode using the RNDIS protocol
2. Preconditions: 
   - Connect the device device to the Linux host via **USB-OTG**
3. Test Execution:

   * Step **#1**:
     - On a Linux host, check if device is recognized as an **RNDIS** network device by running the command:
       ```
       $ dmesg  | grep -i rndis
       ```
     - **[RESULT]:**
       - The output contains information about registering the device and assigning it the name of a network adapter. For example:
         ```lua
         > rndis_host 3-7.4:1.0 usb0: register 'rndis_host' at usb-0000:00:14.0-7.4, RNDIS device, 46:d2:8f:17:0a:eb
         > rndis_host 3-7.4:1.0 enp0s20f0u7u4: renamed from usb0
         ```
   * Step **#2**:
     - On the device, check if the `usb0` network adapter appears:
       ```
       # dmesg | grep -i usb0
       # ip a show dev usb0
       ```
     - **[RESULT]:**
       - The output of the commands contains information without errors about the network adapter `usb0`
       - The IP address of the `usb0` adapter is `169.254.0.1/16`
   * Step **#3**:
     - On the Host, check if an IP address has been automatically obtained from device's `DHCP` server
       ```lua
       $ ip a show dev <rndis_adapter>
       ```
       , where <`rndis_adapter`> - name of the `RNDIS` USB network adapter recieved by **step 1**.
     - **[RESULT]:**
       - The command displayed the network parameters of the **RNDIS** network adapter without errors.
       - The output of the `ip` command shows that the RNDIS network adapter has been assigned an IP address on the network `169.254.0.0/16`
     - **[RESULT]:**
       - The output contains information about the leased IP addresses, while the first value of the MAC address must match the MAC address obtained by the `ip` command in the `2 step`.
   * Step **#4**:
     - On the host, try to SSH into the device via SSH using device's DHCP server IP address:
       ```lua
       $ ssh user@<rndis_client_ip>
       ```
     - **[RESULT]:**
       - The connection **to the device** was successfully established using SSH through the USB network adapter.
   * Step **#5**:
     - On the device, try to SSH into the host via SSH using the DHCP client IP address obtained in `step 2 or 4`:
       ```lua
        # ssh <user>@<rndis_host_ip>
       ```
     - **[RESULT]:**
       - The connection **to the host** was successfully established using SSH through the USB network adapter.
  
4. Test Cleanup: None