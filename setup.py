import os, sys
from getpass import getpass
from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient

if getattr(sys, 'frozen', False):
    current_path = os.path.dirname(sys.executable)
else:
    current_path = os.path.abspath(os.path.dirname(__file__))

username = input("Username: ")
password = getpass("Password: ")

remote_host = input("Remote host: ")
remote_port = input("Port: ")
rsa_path = f"/home/{username}/.ssh/id_rsa"
remote_path = f"/data/ProtonTherapy_data/data"

print("Connect to remote host...", end='')
try:
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    ssh.connect(remote_host, port=remote_port, username=username, password=password)
    print("Done.")
except:
    print("Failed.")
    print("Terminate setup.")
    sys.exit(0)

with SCPClient(ssh.get_transport()) as scp:
    print("Get rsa key file...", end='')
    try:
        scp.get(rsa_path, current_path)
        print("Done.")
    except:
        print("Failed.")
    print("Get NCC gantry structure...", end='')
    try:
        scp.get(remote_path, current_path, recursive=True)
        print("Done.")
    except:
        print("Failed.")
    
ssh.close()

data_path = os.path.join(current_path, 'data')
component_path = os.path.join(data_path, 'components')

def rewrite(fname, cpath):
    lines = []
    with open(fname, 'r') as f:
        lines = f.readlines()
    for idx, line in enumerate(lines):
        if "includeFile" in line:
            tmp = line.split(" = ")
            new = tmp[0] + " = " +os.path.join(cpath, 'NCC', tmp[-1].split("/")[-1])
            lines[idx] = new
    with open(fname, 'w') as f:
        f.writelines(lines)

for i in os.listdir(data_path):
    if i.endswith('nzl'):
        fname = os.path.join(data_path, i)
        rewrite(fname, component_path)
    elif os.path.isdir(os.path.join(data_path, i)):
        for j in os.listdir(os.path.join(component_path)):
            for file in os.listdir(os.path.join(component_path, j)):
                fname = os.path.join(component_path, j, file)
                rewrite(fname, component_path)

print("Setup is complete.")
input("Press Enter to exit.")
