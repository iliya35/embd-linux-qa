#!/bin/bash

remote_password="root"
remote_user="root"
remote_host="$1"

# Function to display results
display_result() {
    if [ "$1" -eq 0 ]; then
        echo "[PASS] $2"
    else
        echo "[FAIL] $2"
    fi
}


test_file_path="/tmp/bigfile"
test_file_size=64 # in Mb
local_directory=".tmp_tests/test_SSH_01"

dd_cmd="dd if=/dev/urandom of=${test_file_path} bs=1M count=${test_file_size}"
md5_cmd="md5sum ${test_file_path}"

sshpass -p $remote_password ssh ${remote_user}@${remote_host} "$dd_cmd"
display_result $(($?)) "Remote DD command completed"

remote_md5=$(sshpass -p $remote_password ssh ${remote_user}@${remote_host} "$md5_cmd")
display_result $(($?)) "Remote MD5 command completed"

# Download remote files
mkdir -p "$local_directory"
sshpass -p $remote_password scp ${remote_user}@${remote_host}:"$test_file_path" "$local_directory"
echo "$test_file_path downloaded successfully."

# Calculate local MD5
local_md5=$(md5sum "$local_directory/$(basename $test_file_path)" | awk '{print $1}')
remote_md5="$(echo "$remote_md5"  | awk '{print $1}')"

# Compare MD5
if [ "$remote_md5" == "$local_md5" ]; then
    echo "MD5 matches."
    md5_match=0
else
    echo "MD5 does not match."
    md5_match=1
fi
display_result $(($md5_match && $?)) "Match MD5 sum of generated files"
