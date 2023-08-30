### JOURNALD-01

1. Test objective: Checking if systemd's automatic journals cleaning works
2. Preconditions: None
3. Test Execution:

   * Step **#1**:
      - Execute the following commands to get current used space by systemd journals:
        ```tex
        # du -hsc /var/log/journal/   (for EB and VM)
        # du -hsc /run/log/journal/   (for NZ)
        # journalctl --disk-usage
        ```
      - Run the following command to get the maximum allowed size of journals that can be stored on disk or in RAM, as specified in the `journald.conf` setting:
        ```lua
        # grep -E '^SystemMaxUse=' /etc/systemd/journald.conf  (for EB and VM)
        # grep -E '^RuntimeMaxUse=' /etc/systemd/journald.conf (for NZ)
        ```
      - **[RESULT]:**
        - The `du` and `journalctl` commands show the same disk space usage by systemd journals.
        - Ensure that the used space does not exceed the value specified in the configuration.\
          ***Note:*** It is acceptable to exceed the size by about *10%*, since the current session also accumulates logs or journald has not yet performed log rotation and deletion of older entries, or due to the dynamic nature of logging.
        - If the output of the command is missing, then this means that the *default* value is used:
          - For **SystemMaxUse=** and **RuntimeMaxUse=** the default is *10%* of the corresponding file system size, but the value is limited to *4G*.
   * Step **#2**:
     - Put [spam.service](uploads/71691fb07ac6d659f5dc9d41783b1859/spam.service) service file on the system, which will artificially clog systemd journals:
       ```
       $ scp spam.service <device_user>@<device_ip>:/etc/systemd/system/spam.service
       ```
     - Reset all current logs:
       ```
       # journalctl --rotate --vacuum-size=8M
       ```
     - Start the "**spam**" systemd service:
       ```lua
       # systemctl start spam
       ```
     - **[RESULT]:**
       - All old systemd journals cleared.
       - Service "**spam**" started without errors
   * Step **#3**:
     - Start watching disk space usage by systemd journals:
       ```lua
       # watch -n 1 " \
          journalctl  --flush; \
          journalctl --disk-usage; echo; \
          du -hs /var/log/journal/; echo; \
          ls -hla /var/log/journal/$(cat /etc/machine-id); \
        "
       ```
       ***Note:*** It may take approximately *15 minutes* for the space to fill up to the set disk space usage limit
     - **[RESULT]:**
       - The size of the logs will gradually increase, but it should periodically reset to the limit values from the first step (with an error of approximately *10%*)
       - The current journal file `system.journal` when reaching *1/8* of the detected limit from the first step (or reaching the **SystemMaxFileSize** value specified in the `journald.conf` file) should be archived and moved as `system@<journal_hash>.journal`, thereby performing **rotation** of systemd journals.
4. Test Cleanup: 
   - Remove test "spam" service and reboot system:
     ```
     # systemctl stop spam 
     # rm /etc/systemd/system/spam.service
     # remoot
     ```
