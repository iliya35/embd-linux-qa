### SSH-01

1. Test objective: Check if remote access via SSH is functional
2. Preconditions:

   * On device prepare a test file:
     ```lua
     # dd if=/dev/urandom of=/data/testfile bs=1M count=512
     ```
3. Test Execution:

   - Step **#1**:
     - Check if the device can be accessed remotely via SSH *from the host*, and then copy the file *from the device* *to the host*:
        ```lua
        $ ssh <user>@<device_ip> 
        > # scp /data/testfile <user>@<host_ip>:/tmp
        ```
     - **[RESULT]:** 
       - Remote access to the device is possible. 
       - File is copied successfully.
       - The password change offer for the user should **not** be prompted
   - Step **#2**:
     - Check if you can remotely access *the host* via SSH *from the device*, and then copy the file *from the host* back *to the device* under a different name:
        ```lua
        # ssh <user>@<host_ip>
        > $ scp /tmp/testfile <user>@<device_ip>:/data/testfile1
        ```
     - Then log out of the host's remote console to return to the device's console
       ```lua
       $ exit
       ```
     - **[RESULT]:** 
       - Remote access from the device is possible. 
       - File is copied from host to the device successfully.
   - Step **#3**:
     - On device check if files were copied correctly:
        ```lua
        # md5sum /data/testfile*
        ```
     - Then log out of the device's remote console to return to the initial host's terminal:
       ```lua
       # exit
       ```
     - **[RESULT]:** _`md5sum`_ hashes of files copied to device are identical
   - Step **#4**:
     - On host check if file was copied correctly:
        ```lua
        $ md5sum /tmp/testfile
        ```
     - **[RESULT]:** _`md5sum`_ hashes of files copied from device are identical

4. Test Cleanup: None