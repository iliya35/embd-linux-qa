### RDP-01

1. Test objective:
   - Check if remote access via RDP is functionalS
2. Preconditions:
   - Make sure you have packages installed on the host:
      - `freerdp2-x11`
3. Test Execution:

   * Step **#1**:
     - On host, check if remote access to the device via RDP is possible. Open RDP client on the host using for example the `xfreerdp` application
       ```lua
       $ xfreerdp -sec-tls /sec:rdp /v:<device_ip> /u:user /p:password /w:1920 /h:1080
       ```
     - **[RESULT]:**
       - Remote access to the device is possible.
       - Access to the GUI and desktop of the Embedded device works
   * Step **#2**:
     - Check the display resolution of the RDP session. While on your desktop in a remote session, open the "`Terminal Emulator`" application and enter the following commands:
       ```
       # export XAUTHORITY="/home/<user_name>/.Xauthority"
       # xrandr --current
       ```
     - **[RESULT]:**
       - The remote session screen resolution must be set to the correct resolution.
       - So the command output should contain the following information:
         ```py
         rdp0 connected 800x600+0+0 0mm x 0mm
         800x600       50.00* 
         ```
   * Step **#3**:
     - Check that clipboard copying works from the host to the device and back.
     - **[RESULT]:**
       - Clipboard copying  works from the host to the device and in opposite direction.
   * Step **#4**:
     - Check the ability to switch from the EN layout (**QWERTY**) of the keyboard to the other layout and vice versa using the key combination `Shift` + `Alt`
     - To do this, you can use any application where you can enter text, such as **GVim**
     - **[RESULT]:**
       - Switching the layout to German and vice versa works
   * Step **#5**:
     - On host, check that RDP connection does **not** use TLS encryption by forcing the security protocol to be **TLS**: 
       ```lua
       $ xfreerdp /sec:tls  /v:192.168.1.151 /u:<user_name> /p:<user_name> /w:800 /h:600
       ``` 
     - **[RESULT]:**
       - Connection should be failed.

4. Test Cleanup: None
