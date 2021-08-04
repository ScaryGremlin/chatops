import uuid

from smbprotocol.connection import Connection
from smbprotocol.open import (
    CreateDisposition,
    CreateOptions,
    DirectoryAccessMask,
    FileAttributes,
    ImpersonationLevel,
    Open,
    ShareAccess
)
from smbprotocol.session import Session
from smbprotocol.tree import TreeConnect

import credentials as creds


class SMBConnector:
    """
    Класс взаимодействия с smb-сервером
    """
    def __init__(self, smb_server_ip: str, port: int, username: str, password: str):
        """
        Конструктор
        :param smb_server_ip:
        :param username:
        :param password:
        """
        self.__smb_connection = Connection(uuid.uuid4(), smb_server_ip, port)
        self.__smb_connection.connect()
        self.__smb_session = Session(self.__smb_connection, username, password)
        self.__smb_session.connect()

    def create_directory(self, share, directory_name):
        smb_tree = TreeConnect(self.__smb_session, share)
        smb_tree.connect()
        dir_open = Open(smb_tree, directory_name)
        dir_open.create(
            ImpersonationLevel.Impersonation,
            DirectoryAccessMask.GENERIC_READ | DirectoryAccessMask.GENERIC_WRITE,
            FileAttributes.FILE_ATTRIBUTE_DIRECTORY,
            ShareAccess.FILE_SHARE_READ | ShareAccess.FILE_SHARE_WRITE,
            CreateDisposition.FILE_OPEN_IF,
            CreateOptions.FILE_DIRECTORY_FILE
        )

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
                                 port=creds.SMB_SERVER_PORT,
                                 username=creds.AD_LOGIN,
                                 password=creds.AD_PASSWORD,
                                 )
    smb_connector.create_directory(creds.SHARE, "123")
    smb_connector.set_directory_permissions("")


if __name__ == '__main__':
    main()
