### SYSTEM-01

1. Test objective:
   - Test of specific Embedded Linux features on the Embedded board, such as:
     - read-only root file system and enabled *dm-verity*
     - no redundant logs
2. Preconditions: None
3. Test Execution:
    * Step **#1**: 
      - Enter the following command to check the list of active Device Mapper devices and take note of the ID of the device (for example, `/dev/mapper/<device>`) that you want to check.:
        ```
        # dmsetup info 
        ```
      - Check if *dm-verity* is enabled for the specified device
        ```
        # dmsetup table /dev/mapper/rootfs
        ```
      - **[RESULT]:** 
        - The commands completed without errors.
        - The output of the `dmsetup` table command will contain a line with "verity".
    * Step **#2**: 
      - Attempt to write to the root file system. At the command prompt, run the following command, which will attempt to create a file on the root file system:
        ```
        # touch /test_file
        ```
      - Try to modify an existing file on the root file system. At the command prompt, run the following command, which will attempt to modify an existing file on the root file system:
        ```
        # echo "Test content" >> /etc/hosts
        ```
      - **[RESULT]:** The system should return an error stating that the file system is read-only.
    * Step **#3**:
      - Run the following command to get the current `machine-id`:
        ```
        # cat /etc/machine-id
        ```
      - Get the current `machine-id` values that systemd uses to store logs by running the following command:
        ```
        # journalctl --header | grep "Machine ID"
        ```
      - Reboot the device and make sure the `machine-id` does not change after that by running the commands above again
      - **[RESULT]:**
        - The `machine-id` values should be the same in the output of both commands, and also after reboot.
    * Step **#5**:
      - Verify that the amount of memory used by the system matches the actual amount installed on the SBC
        ```
        # free -h
        ```
      - **[RESULT]:** The value of memory in the system is displayed correctly

4. Test Cleanup: None