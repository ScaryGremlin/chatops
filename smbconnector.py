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



from smb.SMBConnection import SMBConnection
import credentials as creds


class SMBConnector:
    """
    Класс взаимодействия с smb-сервером
    """
    def __init__(self, ip_address: str, domain: str, username: str, password: str, my_name: str, remote_name: str):
        """

        :param ip_address:
        :param domain:
        :param username:
        :param password:
        :param my_name:
        :param remote_name:
        """
        connection = Connection(uuid.uuid4(), server, port)
        connection.connect()

        session = Session(connection, username, password)
        session.connect()

        tree = TreeConnect(session, share)
        tree.connect()
        dir_open = Open(tree, dir_name)
        dir_open.create(
            ImpersonationLevel.Impersonation,
            DirectoryAccessMask.GENERIC_READ | DirectoryAccessMask.GENERIC_WRITE,
            FileAttributes.FILE_ATTRIBUTE_DIRECTORY,
            ShareAccess.FILE_SHARE_READ | ShareAccess.FILE_SHARE_WRITE,
            CreateDisposition.FILE_OPEN_IF,
            CreateOptions.FILE_DIRECTORY_FILE
        )

        self.__connection = SMBConnection(username=username,
                                          password=password,
                                          my_name=my_name,
                                          remote_name=remote_name,
                                          domain=domain,
                                          use_ntlm_v2=True)
        self.__connection.connect(ip_address)

    def create_directory(self, directory_name):
        pass

    def get_directories(self):
        for path in self.__connection.listPath("exchange", "/"):
            print(path.filename)

    def set_directory_permissions(self, account_directory):
        """

        :param account_directory:
        :return:
        """
        attrs = self.__connection.getSecurity("exchange", "text.txt")
        print(attrs.group)











def main():
    smb_connector = SMBConnector(ip_address=creds.SMB_SERVER_IP,
                                 domain=creds.DOMAIN,
                                 username=creds.SMB_SERVER_LOGIN,
                                 password=creds.AD_PASSWORD,
                                 my_name="python_script",
                                 remote_name=creds.SMB_SERVER_NAME
                                 )
    # smb_connector.get_directories()
    smb_connector.set_directory_permissions("")


if __name__ == '__main__':
    main()
