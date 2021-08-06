import paramiko

with paramiko.SSHClient() as ssh_client:
    id_rsa = paramiko.RSAKey.from_private_key_file("/home/member/.ssh/id_rsa")
    ssh_client.load_system_host_keys()
    ssh_client.connect("192.168.213.237", username="user", pkey=id_rsa)
    stdin, stdout, stderr = ssh_client.exec_command("dir")
    print(stdout.read().decode("cp1252"))

del ssh_client, stdin, stdout, stderr
