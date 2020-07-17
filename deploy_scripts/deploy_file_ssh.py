#!/usr/bin/python
import paramiko
from pathlib import Path

# auth_method: if 0, use the private key located at 'pwd', else use the password 'pwd'

def put_file(host, user, local_path, remote_path, auth_method, pwd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    if auth_method == 0:
        key = paramiko.RSAKey.from_private_key_file(pwd)
        ssh.connect(hostname=host, username=user, pkey=key)
    else:
        ssh.connect(hostname=host, username=user, password=pwd)

    sftp = ssh.open_sftp()

    sftp.put(local_path, remote_path)
    sftp.close()
    ssh.close()

    print("File deployed to server successfully!")


host = "192.168.1.1"
user = "USERNAME"
auth = 0
key_path = "//wsl$/Ubuntu/home/USERNAME/.ssh/id_rsa"

local_path = str(Path("c:/path/to/file/to/upload.toml"))
remote_path = "/home/USERNAME/path/to/upload.toml"

put_file(host, user, local_path, remote_path, auth, key_path)
