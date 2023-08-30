import json
import paramiko
import pytest
import time
import os
import re
from scp import SCPClient
import hashlib

reference_configs_path = "reference_configs/configs"

def calculate_md5(file_path):
    md5_hash = hashlib.md5()  
    
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
    
    return md5_hash.hexdigest()


# Загрузка данных из JSON файла
def load_device_data(device_name):
    with open('tests_config.json', 'r') as file:
        data = json.load(file)
        all_devices_data = data.get('devices', {})
        devices_data = all_devices_data.get(device_name, None)
        if not devices_data:
            print(f"Device '{device_name}' not found in the device list.")
            return
        return devices_data

def load_config_data(device_name):
    with open('tests_config.json', 'r') as file:
        data = json.load(file)
        all_config_data = data.get('configs', {})
        config_data = all_config_data.get(device_name, None)
        if not config_data:
            print(f"Device '{device_name}' not found in the device list.")
            return
        return config_data

@pytest.fixture(scope="module")
def ssh_client(request):
    device_name = request.config.getoption("--device")
    device_data = load_device_data(device_name)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(
            device_data['device_ip'],
            username=device_data['device_username'],
            password=device_data['device_password']
        )
    except paramiko.AuthenticationException:
        print(f"Authentication failed for {device_name}.")
    except paramiko.SSHException as e:
        print(f"SSH Exception occurred for {device_name}: {e}")
    yield client
    client.close()


def download_remote_files(ssh_client, remote_paths, local_directory):
    scp = SCPClient(ssh_client.get_transport())
    for remote_path in remote_paths:
        remote_filename = remote_path.split("/")[-1]
        # local_path = local_directory + "/" + remote_filename
        if not os.path.exists(local_directory):
            os.makedirs(local_directory)
        local_path = os.path.join(local_directory, remote_filename)
        scp.get(remote_path, local_path)
    scp.close()

def read_remote_json(ssh_client, remote_path):
    # sftp = ssh_client.open_sftp(
    # with sftp.file(remote_path, 'r') as remote_file:
    #     json_data = remote_file.read()
    #     return json.loads(json_data)
    # sftp.close()
    read_remote_json_cmd=f'cat {remote_path} | jq'
    stdin, stdout, stderr = ssh_client.exec_command(read_remote_json_cmd)
    json_output = stdout.read().decode('utf-8').replace("'", "\"")
    try:
        json_object = json.loads(json_output)
        return json_object
    except json.JSONDecodeError as e:
        print("Error JSON decoding:", str(e))
        return None


def reboot_remote_host(ssh_client, wait_time=60, max_retries=3):
    hostname = ssh_client.get_transport().getpeername()[0]
    
    retries = 0
    while retries < max_retries:
        try:
            print(f"Rebooting {hostname}...")
            stdin, stdout, stderr = ssh_client.exec_command("/sbin/reboot -f > /dev/null 2>&1 &")
            stdout.channel.recv_exit_status()

            print(f"Waiting for {wait_time} seconds after reboot...")
            time.sleep(wait_time)

            print(f"Reconnection attempt {retries + 1} successful.")
            break

        except Exception as e:
            print(f"Error during reboot: {e}")
            retries += 1
            if retries < max_retries:
                print(f"Retrying in 10 seconds...")
                time.sleep(10)
            else:
                print("Max retries reached. Exiting.")

def test_SSH_01(ssh_client):
    test_file_path = "/tmp/bigfile"
    test_file_size = 64 # in Mb
    local_directory = ".tmp_tests/" + test_SSH_01.__name__
    try:
        dd_cmd = f'dd if=/dev/urandom of={test_file_path} bs=1M count={test_file_size}'
        md5_cmd = f"md5sum {test_file_path} | awk '{{print $1}}'"

        stdin, stdout, stderr = ssh_client.exec_command(dd_cmd)
        dd_code = stdout.channel.recv_exit_status()
        if dd_code == 0:
            print("Command 'dd' completed successfully.")
        else:
            print(f"Command 'dd' failed with return code {returncode}")
            pytest.fail("Command 'dd' failed")  
        stdin, stdout, stderr = ssh_client.exec_command(md5_cmd)
        remote_md5 = stdout.read().decode().strip()

        download_remote_files(ssh_client, test_file_path.split(), local_directory)
        print("{} file downloaded successfully.".format(test_file_path))
        local_md5 = calculate_md5(os.path.join(local_directory, os.path.basename(test_file_path)))

        assert remote_md5 == local_md5

    except Exception as e:
        print("download_Error:", e)
        pytest.fail("Error downloading file via ssh")


def test_CONF_01(ssh_client, device_name):
    if device_name == "Customer1":
        print("The CONF_01 test case for {} board in progress".format(device_name))
    elif device_name == "Customer2":
        print("The CONF_01 test case for {}board in progress".format(device_name))
    elif device_name == "Customer3":
        print("The CONF_01 test case for {} board in progress".format(device_name))
    else: assert 1

    remote_keys_files = [
        "/root/.ssh/id_rsa",
        "/root/.ssh/id_rsa.pub",
        "/root/.ssh/known_hosts"
    ]
    remote_json_config = "/root/device.json"
    remote_config = "/etc/foo-conf/Customer.conf"

    local_directory = ".tmp_tests/" + test_CONF_01.__name__
    
    ref_remote_json_config = '''{
        "foo-id": 12345,
        "foo-2": "boo-a",
        "foo-3": false
    }'''
    ref_remote_json_config = json.loads(ref_remote_json_config.lower().replace("'", "\""))
    stdin, stdout, stderr = ssh_client.exec_command("whoami; uname -a")
    print (stdout.readlines())
    try:
        json_content = read_remote_json(ssh_client, remote_json_config)
        print(json_content['foo-id'])
        if 'foo-id' in json_content:
            id_value = json_content['foo-id']
            if not  re.match(r'^[0-9a-fA-F]{32}$', id_value):
                pytest.fail("ID format is incorrect.")

        if device_name == "Customer1":
            _, stdout, _ = ssh_client.exec_command('/bin/hostname')
            remote_hostname = stdout.read()
            if isinstance(remote_hostname, bytes):
                remote_hostname = remote_hostname.decode('utf-8')
                # 
                # Add Customer1 hostname handler here
                # 
        elif device_name == "Customer2":
            _, stdout, _ = ssh_client.exec_command('/bin/hostname')
            remote_hostname = stdout.read()
            if isinstance(remote_hostname, bytes):
                remote_hostname = remote_hostname.decode('utf-8')
                # 
                # Add Customer2 hostname handler here
                #
        elif device_name == "Customer3":
            _, stdout, _ = ssh_client.exec_command('/bin/hostname')
            remote_hostname = stdout.read()
            if isinstance(remote_hostname, bytes):
                remote_hostname = remote_hostname.decode('utf-8')
                # 
                # Add Customer3 hostname handler here
                #  
    except Exception as e:
        print("Error:", e)
   
    if device_name == "Customer1" or device_name == "Customer2":
        try:
            json_content = read_remote_json(ssh_client, remote_json_config)
            rem_json_conf_content = json.dumps(json_content, sort_keys=True).lower()
            ref_remote_json_config = json.dumps(ref_remote_json_config, sort_keys=True).lower()
            if rem_json_conf_content == ref_remote_json_config:
                print("JSON Config identical with reference.")
            else:
                pytest.fail("JSON objects are not identical.")
        except Exception as e:
            print("Error:", e)

    try:
        download_remote_files(ssh_client, remote_keys_files, local_directory)
        print("Keys files downloaded successfully.")
    except Exception as e:
        print("download_Error:", e)

    try:
        download_remote_files(ssh_client, remote_config.split(), local_directory)
        print("Config file downloaded successfully.")
        ref_conf_name = load_config_data(device_name)["ref_conf_name"]
        with open(os.path.join(local_directory, os.path.basename(remote_config)), 'rb') as file1, 
            open(os.path.join(reference_configs_path, ref_conf_name), 'rb') as file2:
            content1 = file1.read()
            content2 = file2.read()
            if content1 == content2:
                print ("The Config file is correct")
            else:
                pytest.fail("The Config file does not match the reference")
    except Exception as e:
        print("download_Error:", e)

    while True:
        # reboot_remote_host(ssh_client)
        # ssh_client.exec_command('/sbin/reboot -f > /dev/null 2>&1 &')
        # time.sleep(5)
        try:
            id_value_reb = read_remote_json(ssh_client, remote_json_config)['foo-id']
            print(id_value_reb)
            break
        except paramiko.SSHException:
            time.sleep(60)

    ssh_client.close()


