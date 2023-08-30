#! /bin/bash

# Function to display results
display_result() {
    if [ "$1" -eq 0 ]; then
        echo "[PASS] $2"
    else
        echo "[FAIL] $2"
    fi
}

# Step 1: Check NTP service status
echo "Step 1: Checking NTP service status..."
ntp_status=$(systemctl is-active systemd-timesyncd)
if [ "$ntp_status" == "active" ]; then
    ntp_status_result=0
else
    ntp_status_result=1
fi
display_result $ntp_status_result "NTP service status check"

# Step 2: List NTP servers
echo "Step 2: Listing NTP servers..."
ntp_servers=$(timedatectl show-timesync --property=FallbackNTPServers --value)
echo "NTP Servers: $ntp_servers"
display_result $? "NTP servers list"

# Step 3: Disable NTP synchronization and set wrong datetime
echo "Step 3: Disabling NTP synchronization and setting wrong datetime..."
timedatectl set-ntp false
date -s "1971-01-01 01:01"
set_date=$(date)
echo "Set date: $set_date"
display_result $? "Setting wrong datetime"

# Step 4: Enable NTP synchronization and check datetime
echo "Step 4: Enabling NTP synchronization and checking datetime..."
ntp_date=$(curl -Ik 'https://google.com' 2>/dev/null | grep -i '^date:' | sed 's/^[Dd]ate: //g')
ntp_date=$(date -d "$ntp_date" +"%Y-%m-%d")
timedatectl set-ntp true
sleep 5
current_date=$(date +"%Y-%m-%d")
echo "Current date: $current_date"
echo "NTP date: $ntp_date"
if [ "$ntp_date" == "$current_date" ]; then
    echo "NTP date is the same as current date"
    ntp_sync_result=0

else
    echo "NTP date is different from current date"
    ntp_sync_result=1

fi

display_result $ntp_sync_result "Enabling NTP synchronization and checking datetime"

# Step 5: Reboot the device and check settings after reboot
echo "[SKIP] Step 5: Rebooting the device... [SKIP]"
# reboot
echo "[SKIP] Rebooting device"

# Wait for the device to reboot
# sleep 120

echo "Step 6: Checking datetime and NTP settings after reboot..."
reboot_date=$(date)
reboot_only_date=$(date -d "$reboot_date" +"%Y-%m-%d")
ntp_date=$(curl -Ik 'https://google.com' 2>/dev/null | grep -i '^date:' | sed 's/^[Dd]ate: //g')
ntp_only_date=$(date -d "$ntp_date" +"%Y-%m-%d")

echo "Date after reboot: $reboot_date"

ntp_status_after=$(systemctl is-active systemd-timesyncd)
if [ "$ntp_status_after" == "active" ]; then
    ntp_status_result_after=0
else
    ntp_status_result_after=1
fi

if [ "$ntp_only_date" == "$reboot_only_date" ]; then
    echo "NTP date is the same as current date"
    reb_sync_result=0

else
    echo "NTP date is different from current date"
    reb_sync_result=1

fi
display_result $(($ntp_status_result_after && $reb_sync_result && $?)) "NTP service status after reboot"
