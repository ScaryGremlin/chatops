import paramiko
from smb.SMBConnection import SMBConnection

import miscellaneous as misc


class SMBConnector:
    """
    Класс взаимодействия с smb-сервером
    """
    def __init__(self, smb_server_ip: str, username: str, password: str, domain: str, remote_name: str):
        """
        Конструктор
        :param smb_server_ip: IP-адрес smb-сервера
        :param username: Пользователь для подключения к smb-шаре
        :param password: Пароль пользователя для подключения к smb-шаре
        """
        self.__smb_connection = SMBConnection(username=username,
                                              password=password,
                                              my_name="python_script",
                                              remote_name=remote_name,
                                              domain=domain,
                                              use_ntlm_v2=True)
        self.__smb_connection.connect(smb_server_ip, timeout=20)

    def create_directory(self, share: str, directory_name: str) -> None:
        """
        Создать директорию на smb-шаре
        :param share: Имя smb-шары
        :param directory_name: Имя директории внутри smb-шары
        :return:
        """
        self.__smb_connection.createDirectory(share, directory_name)

    def create_password_file(self, share: str, directory_name: str) -> None:
        """
        Создать файл с паролем пользователя по умолчанию
        :param share: Имя smb-шары
        :param directory_name: Имя директории внутри smb-шары
        :return:
        """
        # Создать локальную копию файла с паролем
        password = misc.get_password(password_length=8, by_chance=True)
        with open("pass.txt", "w") as pass_file:
            pass_file.write(password)
        # Создать файл с паролем на smb-шаре
        with open("pass.txt", 'rb') as pass_file:
            uploaded_file = self.__smb_connection.storeFile(share, f"{directory_name}/pass.txt", pass_file)

    @staticmethod
    def set_permissions(rsat_desktop_ip: str, rsat_desktop_username: str, account_directory: str) -> str:
        """
        Установить права на директорию пользователя и файл с паролем
        :param rsat_desktop_ip: IP-адрес RSAT-компьютера
        :param rsat_desktop_username: Имя пользователя для подключения по ssh
        :param account_directory: Название директории пользователя. Оно же и название учётной записи.
        :return:
        """
        with paramiko.SSHClient() as ssh_client:
            id_rsa = paramiko.RSAKey.from_private_key_file("/home/member/.ssh/id_rsa")
            ssh_client.load_system_host_keys()
            ssh_client.connect(rsat_desktop_ip, username=rsat_desktop_username, pkey=id_rsa)
            stdin, stdout, stderr = ssh_client.exec_command(f'c:/scripts/set_permissions.ps1 "{account_directory}"')
            ssh_command_output = stdout.read().decode("cp866")
        del ssh_client, stdin, stdout, stderr
        return ssh_command_output
