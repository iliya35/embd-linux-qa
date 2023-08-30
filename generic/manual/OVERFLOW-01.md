### OVERFLOW-01

1. Test objective: 
   - Checking that the file system does not grow over time
2. Preconditions: None.
3. Test Execution:

   * Step **#1**:
     - Run the following commands to find out the current file system usage and the largest objects at 1st depth level
       ```
       # df -h
       # { du -chs /data/* /var/* /home/* /etc/ | sort -h; }
       ```
     - Write down the results
     - **[RESULT]:**
       - The output of the `df` command contains information on the use of the main storages mounted on the device
       - The output of the `du` command contains information about the sizes of all files and directories of the first level of depth for all major mount points on the root file system
   * Step **#2**:
     - Leave the system for *48 hours* and then check that the fullness of the file system and the largest files have not changed (or have not changed much) by repeating **step 1**
     - **[RESULT]:**
       - After *48 hours*, the population of the main filesystem mount points has not changed much

4. Test Cleanup: None