import pytest
import logging

def pytest_addoption(parser):
    parser.addoption(
        '--device',
        action='store',
        default="Customer1", 
        help='Device name for testing',
        dest='device_name', 
        choices=("Customer1", "Customer2", "Customer3"),
    )

@pytest.fixture
def device_name(request):
    return request.config.getoption("--device")

@pytest.fixture(scope='function', autouse=True)
def test_log(request):
    logging.info("Test '{}' STARTED".format(request.node.nodeid)) # Here logging is used, you can use whatever you want to use for logs
    def fin():
        logging.info("Test '{}' COMPLETED".format(request.node.nodeid))
    request.addfinalizer(fin)

def pytest_configure(config):
    device_name_value = config.getoption("--device")
    if device_name_value == "Customer1":
        print("The Generic test plan for {} board in progress".format(device_name_value))
    elif device_name_value == "Customer2":
        print("The Generic test plan for {} board in progress".format(device_name_value))
    elif device_name_value == "Customer3":
        print("The Generic test plan for {} board in progress".format(device_name_value))
    else: assert 0

# def pytest_generate_tests(metafunc):
#     if 'device' in metafunc.fixturenames:
#         metafunc.parametrize('device',  metafunc.config.getoption("device"))

# --- Remote command execution --- 
# command = f'ls -la {command_part}'
# stdin, stdout, stderr = ssh_client.exec_command(command)
# result = stdout.read().decode().strip()
# assert result.startswith("Linux")

# --- root access via Channel invoke_shell() method ---
# channel:Channel = ssh_client.invoke_shell()
# print(type(channel))
# channel_data = str()
# while True:
#     if channel.recv_ready():
#         time.sleep(1)
#         channel_data += str(channel.recv(999))
#     else:
#         continue
#     channel.send("su\n")
#     time.sleep(1)
#     channel_data += str(channel.recv(999))
#     channel.send("root\n")
#     time.sleep(1)
#     channel_data += str(channel.recv(999))
#     break  
# output_lines = channel_data.split('\n')
# for line in output_lines:
#     print(line)    

# --- root access via exec_command() method ---
# stdin, stdout, stderr = ssh_client.exec_command('sudo su -')
# stdin.write('password\n')
# stdin.flush()