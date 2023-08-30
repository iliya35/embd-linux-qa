### NTP-01

1. Test objective:
   - Check that synchronization of time with external NTP over Internet is enabled and works
2. Preconditions: None
3. Test Execution:

   * Step **#1**:
     - Execute the following command to check the status of the NTP service controlled by systemd:
       ```lua
       # systemctl status systemd-timesyncd
       ```
     - Verify that the output indicates that the NTP service is active and running.
     - **[RESULT]:**
       - The `timesyncd` daemon service controlled by systemd should be active and running.
   * Step **#2**:
     - List the NTP servers that the device is synchronizing bu using the following command:
       ```lua
       # echo "NTP Servers: $(timedatectl show-timesync --property=FallbackNTPServers  --value)"
       ```
     - **[RESULT]:**
       - The command output contains a list of NTP servers with *one* or *more* NTP server addresses.
   * Step **#3**:
     - Disable NTP synchronization and set the wrong datetime:
       ```
        # timedatectl set-ntp false
        # date -s "1971-01-01 01:01"        
       ```
     - Check that the date and time is set to the wrong one (to the past):
       ```
       # date
       ```
     - **[RESULT]:**
       - Wrong date (in the past) set manually is displayed correctly in the system when calling the `date` command
   * Step **#4**:
     - Enable synchronization with the NTP server again and check that the date now contains the correct value with the current date:
       ```
        # timedatectl set-ntp true
        # date       
       ```
     - **[RESULT]:**
       - The output of the `date` command displays the correct *current date* and time in *UTC*
   * Step **#5**:
     - Check that after a reboot, NTP synchronization remains enabled and the date is displayed as current:
       - Check datetime and NTP settings:
         ```
         # timedatectl status
         ```
       - Reboot device:
         ```
         # reboot
         ```
       - Check datetime and NTP settings again:
         ```
         # timedatectl status
         ```
      - **[RESULT]:**
        - Date and time is showing correctly after reboot
        - NTP sync stays enabled after reboot

4. Test Cleanup: None
