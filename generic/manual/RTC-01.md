### RTC-01

1. Test objective:
   - Check that proper RTC is used and that time is synced with it
2. Preconditions: 
   - Disable NTP synchronization: 
     ```
     # timedatectl set-ntp false
     ```
3. Test Execution:

   * Step **#1**:
     - Execute the following command to list all available RTC devices and  verify that RTC is available and recognized by the system:
       ```lua
       # ls -la /sys/class/rtc/*
       # cat /proc/driver/rtc
       ```
     - **[RESULT]:**
        - The command output displays the available RTC devices.
        - RTC devices should be listed, indicating their availability on the system.
   * Step **#2**:
     - Checking proper Time Synchronization:
       - Execute the following command to view the current system time:
         ```
         # date
         ```
       - Check if RTC could be read and ensure that the system time matches the RTC time:
          ```
          # hwclock --show --rtc rtc<X>
          ```
          , where `rtc<X>` - name of the rtc device defined on the **first step**
     - **[RESULT]:**
       - RTC time and system time should match.
   * Step **#3**:
     - Set system time to something:
        ```
        # date -s "1971-01-01 01:01"        
        ```
     - Set system time from RTC:
        ```
        # hwclock --hctosys --rtc rtc<X>
        # date
        ```
     - **[RESULT]:**
       - System time was synchronized with RTC
   * Step **#4**:  <mark>***NZ** and ***EB*** specific*</mark>:
     - Set system time to something:
        ```
        # date -s "1971-01-01 01:01"        
        ```
     - Set RTCs time from system:
        ```
        # hwclock --systohc --rtc rtc<X>
        # hwclock --show --rtc rtc<X>
        ```
     - **[RESULT]:**
       - RTC was synchronized with system time
   * Step **#5**:  <mark>***NZ** and ***EB*** specific*</mark>:
     - Synchronize system time and RTCs with NTP server:
       ```tex
       # timedatectl set-ntp true;
       # hwclock --systohc;
       # hwclock --show;
       # date
       ```
     - **[RESULT]:**
         - RTC and system time were synchronized with NTP server.
   * Step **#6**:
     - Check if RTC time survives after reboot
       - Check RTC time:
         ```
         # hwclock --show --rtc rtc<X>
         ```
       - Turn off the power of the device and wait *5 minutes*.
       - Power up the device again
       - Check RTC time again:
         ```
         # hwclock --show --rtc rtc<X>
         ```
      - **[RESULT]:**
        - The RTC time has been printed and matches the time before the reboot
   * Step **#7**:
     - Execute the following command to put the system to sleep for 1 minute using rtcwake:
       ```lua
       # rtcwake -m mem -s 60 -d rtc<X>
       ```  
     - Wait for the system to wake up.
     - After waking up, execute the date command to verify that the system time has been correctly restored:
       ```
       # date
       ```
     - Ensure that the system time is correctly updated after waking up from sleep mode.
     - **[RESULT]:**
       - The system successfully enter sleep mode using the `rtcwake` utility and wake up from sleep mode, with the system time correctly updated.

4. Test Cleanup: 
   - Revert NTP sync back to enabled:
     ```
     # timedatectl set-ntp teue
     ```
