import paramiko
from smb.SMBConnection import SMBConnection
import miscellaneous as misc

import credentials as creds

# with paramiko.SSHClient() as ssh_client:
#     id_rsa = paramiko.RSAKey.from_private_key_file("/home/member/.ssh/id_rsa")
#     ssh_client.load_system_host_keys()
#     ssh_client.connect("192.168.213.237", username="user", pkey=id_rsa)
#     stdin, stdout, stderr = ssh_client.exec_command("")
#     print(stdout.read().decode("cp1252"))
#
# del ssh_client, stdin, stdout, stderr


def set_permissions(rsat_desktop_ip: str, rsat_desktop_username: str, account_directory: str) -> None:
    """
    Установить права на директорию пользователя и файл с паролем
    :param rsat_desktop_ip: IP-адрес RSAT-компьютера
    :param rsat_desktop_username: Имя пользователя для подключения по ssh
    :param account_directory: Название директории пользователя
    :return:
    """
    with paramiko.SSHClient() as ssh_client:
        id_rsa = paramiko.RSAKey.from_private_key_file("/home/member/.ssh/id_rsa")
        ssh_client.load_system_host_keys()
        ssh_client.connect(rsat_desktop_ip, username=rsat_desktop_username, pkey=id_rsa)
        stdin, stdout, stderr = ssh_client.exec_command(f'c:/scripts/set_permissions.ps1 "{account_directory}"')
        print(stdout.read().decode("cp866"))
    del ssh_client, stdin, stdout, stderr






def create_password_file(share: str, directory_name: str) -> None:
    """
    Создать файл с паролем пользователя по умолчанию
    :param share: Имя smb-шары
    :param directory_name: Имя директории внутри smb-шары
    :return:
    """
    smb_connection = SMBConnection(username=creds.SMB_SERVER_LOGIN,
                                   password=creds.AD_PASSWORD,
                                   my_name="python_script",
                                   remote_name=creds.SMB_SERVER_NAME,
                                   domain=creds.DOMAIN,
                                   use_ntlm_v2=True)
    smb_connection.connect(creds.SMB_SERVER_IP, timeout=20)
    # Создать локальную копию файла с паролем
    password = misc.get_password(password_length=8, by_chance=True)
    with open("pass.txt", "w") as pass_file:
        pass_file.write(password)
    # Создать файл с паролем на smb-шаре
    with open("pass.txt", 'rb') as pass_file:
        uploaded_file = smb_connection.storeFile(share, f"{directory_name}/pass.txt", pass_file)


# create_password_file(creds.SHARE, "soft")
set_permissions(creds.RSAT_DESKTOP_IP, creds.RSAT_DESKTOP_USERNAME, "Петушаркин_ПП")
