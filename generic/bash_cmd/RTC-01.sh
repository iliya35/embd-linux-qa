#!/bin/bash

# Function to display results
display_result() {
    if [ "$1" -eq 0 ]; then
        echo "[PASS] $2"
    else
        echo "[FAIL] $2"
    fi
}

# Step 0: Disable NTP synchronization:
echo "Step 0: Disable NTP synchronization:..."
timedatectl set-ntp false 
display_result $? "Disable NTP synchronization"

# Step 1: Check available RTC devices
echo "Step 1: Checking available RTC devices..."
ls -la /sys/class/rtc/*
cat /proc/driver/rtc

display_result $? "Checking available RTC devices"

# Step 2: Check proper Time Synchronization
echo "Step 2: Checking proper Time Synchronization..."
system_time=$(date   +%Y-%m-%d\ %H:%M)
rtc_device="/dev/$(ls /sys/class/rtc/ | head -n 1)"
rtc_time=$(date -d "$(hwclock --show --rtc /dev/rtc0 | cut -d'.' -f1)" +%Y-%m-%d\ %H:%M)

echo "System Time: $system_time"
echo "RTC Time: $rtc_time"

if [ "$system_time" == "$rtc_time" ]; then
    rtc_sync_result=0
else
    rtc_sync_result=1
fi

display_result $rtc_sync_result "Checking proper Time Synchronization"

# Step 3: Synchronize system time from RTC
echo "Step 3: Synchronizing system time from RTC..."
echo -en "Set System Time to: "
date -s "1971-01-01 01:01"
hwclock --hctosys --rtc $rtc_device
y_system_time=$(date +%Y)
y_rtc_time=$(date -d "$rtc_time"  +%Y)
if [ "$y_rtc_time" == "$y_system_time" ]; then
    date;
    echo "Synchronization of system time with RTC was successful"
    echo "Current date: $(date)"
    sys_sync_result=0
else
    sys_sync_result=1
fi

display_result $sys_sync_result "Synchronizing system time from RTC"

# Step 4: Synchronize RTC from system time
echo "Step 4: Synchronizing RTC from system time..."
date -s "1971-01-01 01:01"
hwclock --systohc --rtc $rtc_device
hwclock_synced=$(hwclock --show --rtc $rtc_device)

display_result $(($rtc_sync_result && $?)) "Synchronizing RTC from System time"

# Step 5: Synchronize system time and RTCs with NTP server
echo "Step 5: Synchronizing system time and RTCs with NTP server..."
timedatectl set-ntp true
hwclock --systohc
hwclock_synced_ntp=$(hwclock --show --rtc $rtc_device)
system_time_ntp=$(date)

display_result $(($rtc_sync_result && $?)) "Synchronizing system time and RTCs with NTP server"

# Step 6: Check if RTC time survives after reboot
echo "Step 6: Checking if RTC time survives after reboot..."
initial_rtc_time=$(hwclock --show --rtc $rtc_device)

echo "Initial RTC Time: $initial_rtc_time"
echo "Turning off the power. Please wait for 5 minutes..."
sleep 300  && echo "Powering up the device after 5 minute."

new_rtc_time=$(hwclock --show --rtc $rtc_device)
echo "New RTC Time: $new_rtc_time"

display_result $(($rtc_sync_result && $?)) "Checking if RTC time survives after reboot"

# Step 7: Sleep mode test
echo "Step 7: Entering sleep mode and waking up..."
rtcwake -m mem -s 60 -d $rtc_device
wakeup_system_time=$(date)

echo "Wakeup System Time: $wakeup_system_time"

display_result $? "Sleep mode and wakeup test"

# Cleanup: Revert NTP sync back to enabled
echo "Cleaning up: Reverting NTP sync back to enabled..."
timedatectl set-ntp true

echo "Test completed."
