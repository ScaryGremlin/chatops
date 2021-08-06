from smb.SMBConnection import SMBConnection

import credentials as creds


class SMBConnector:
    """
    Класс взаимодействия с smb-сервером
    """
    def __init__(self, smb_server_ip: str, username: str, password: str, domain: str, remote_name: str):
        """
        Конструктор
        :param smb_server_ip:
        :param username:
        :param password:
        """
        self.__smb_connection = SMBConnection(username=username,
                                              password=password,
                                              my_name="python_script",
                                              remote_name=remote_name,
                                              domain=domain,
                                              use_ntlm_v2=True)
        self.__smb_connection.connect(smb_server_ip)

    def create_directory(self, share, directory_name):
        for element in self.__smb_connection.listPath(share, directory_name):
            print(element.filename)

    def set_directory_permissions(self, account_directory):
        """

        :param account_directory:
        :return:
        """
        pass

    def create_password_file(self, account_directory):
        pass


def main():
    smb_connector = SMBConnector(smb_server_ip=creds.SMB_SERVER_IP,
                                 username=creds.SMB_SERVER_LOGIN,
                                 password=creds.AD_PASSWORD,
                                 domain=creds.DOMAIN,
                                 remote_name=creds.SMB_SERVER_NAME
                                 )
    smb_connector.create_directory(creds.SHARE, "/")


if __name__ == '__main__':
    main()
