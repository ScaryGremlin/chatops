from smb.SMBConnection import SMBConnection


class SMBConnector:
    """
    Класс взаимодействия с smb-сервером
    """
    def __init__(self, ip_address: str, domain: str, username: str, password: str, my_name: str, remote_name: str):
        """
        Конструктор
        """
        self.__connection = SMBConnection(username=username,
                                          password=password,
                                          my_name=my_name,
                                          remote_name=remote_name,
                                          domain=domain,
                                          use_ntlm_v2=True)
        self.__connection.connect(ip_address)
