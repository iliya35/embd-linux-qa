#! /bin/bash

log_path="/data"

# Function to display results
display_result() {
    if [ "$1" -eq 0 ]; then
        echo "[PASS] $2"
    else
        echo "[FAIL] $2"
    fi
}

# Step 1: Check file system usage and largest objects
echo "Step 1: Checking file system usage and largest objects..."
df_output=$(df -h)
du_output=$(du -chs /data/* /var/* /home/* /etc/* 2>/dev/null | sort -h)

echo "=== df Output ===" > ${log_path}/overflow_01_results.log
echo "$df_output" >> ${log_path}/overflow_01_results.log
echo "" >> ${log_path}/overflow_01_results.log
echo "=== du Output ===" >> ${log_path}/overflow_01_results.log
echo "$du_output" >> ${log_path}/overflow_01_results.log

display_result $? "Checking file system usage and largest objects"

echo "Results saved to ${log_path}/overflow_01_results.log"
echo "Please note down the initial results and proceed to Step 2."

# Step 2: Wait for 48 hours and repeat Step 1
echo "Step 2: Waiting for 48 hours..."
sleep 172800  

echo "Step 2: Checking file system usage and largest objects after 48 hours..."
df_output_after=$(df -h)
du_output_after=$(du -chs /data/* /var/* /home/* /etc/* 2>/dev/null | sort -h)

echo "" >> ${log_path}/overflow_01_results.log
echo "=== df Output after 48 hours ===" >> ${log_path}/overflow_01_results.log
echo "$df_output_after" >> ${log_path}/overflow_01_results.log
echo "" >> ${log_path}/overflow_01_results.log
echo "=== du Output after 48 hours ===" >> ${log_path}/overflow_01_results.log
echo "$du_output_after" >> ${log_path}/overflow_01_results.log

display_result $? "Checking file system usage and largest objects after 48 hours"
