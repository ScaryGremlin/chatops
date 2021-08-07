import paramiko
from smb.SMBConnection import SMBConnection
import miscellaneous as misc

import credentials as creds

with paramiko.SSHClient() as ssh_client:
    id_rsa = paramiko.RSAKey.from_private_key_file("/home/member/.ssh/id_rsa")
    ssh_client.load_system_host_keys()
    ssh_client.connect("192.168.213.237", username="user", pkey=id_rsa)
    stdin, stdout, stderr = ssh_client.exec_command("dir")
    print(stdout.read().decode("cp1252"))

del ssh_client, stdin, stdout, stderr


smb_connection = SMBConnection(username=creds.SMB_SERVER_LOGIN,
                               password=creds.AD_PASSWORD,
                               my_name="python_script",
                               remote_name=creds.SMB_SERVER_NAME,
                               domain=creds.DOMAIN,
                               use_ntlm_v2=True)
smb_connection.connect(creds.SMB_SERVER_IP, timeout=20)





