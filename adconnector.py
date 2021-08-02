from ldap3 import Connection, Server, ALL, MODIFY_REPLACE

from credentials import DOMAIN
from misc import get_password


class ADConnector:
    """
    Класс подключения к серверу Active Directory
    """
    def __init__(self, server: str, login: str, password: str):
        """
        Конструктор
        :param server: Адрес сервера Active Directory. DNS-имя или IP.
        :param login: Домен\логин - CO\Administrator
        :param password: Пароль
        """
        ldap_server = Server(server, get_info=ALL)
        self.__connection = Connection(ldap_server, login, password, auto_bind=True)

    def add_account(self, fio: str, org_unit: str, mobile: str):
        """
        Добавить пользователя
        :param fio: Фамилия, имя, отчество пользователя
        :param org_unit: Организационная еденица домена. Подразделение, в которое добавить пользователя
        :param mobile: Мобильный телефон пользователя
        """
        # Получить фамилию, имя и отчетство пользователя
        surname, name, middle_name = [element.strip().capitalize() for element in fio.split()]
        login = surname + "_" + name[0] + middle_name[0]

        # Сгенерировать строку dn
        cn = "CN=" + name + " " + surname + ","
        ou = "OU=" + org_unit + ","
        dc = ""
        for element in DOMAIN.split("."):
            dc += "DC=" + element + ","
        dn = cn + ou + dc.strip(",")

        #
        object_class = ["top", "person", "organizationalPerson", "user"]

        # Установить атрибуты учётной записи.
        # Фамилия, имя, логин для входа - Фамилия_ИО, отображаемое имя и мобильный телефон
        attributes = {
            'sn': surname,
            "givenName": name,
            "sAMAccountName": login,
            "displayName": name + " " + surname,
            "mobile": mobile
        }

        # Установить дополнителные атрибуты учётной записи.
        # userAccountControl: 512 - включенная учётная запись,
        # pwdLastSet: 0 - требовать смену пароля при первом входе.
        uac_attributes = {
            "userAccountControl": (MODIFY_REPLACE, [512]),
            "pwdLastSet": (MODIFY_REPLACE, [0])
        }

        # Сгенерировать пароль по умолчанию
        password = get_password()

        if self.__connection.add(dn, object_class, attributes):
            print("Учётная запись пользователя добавлена.")
            if self.__connection.extend.microsoft.modify_password(dn, password):
                print("Пароль учётной записи по умолчанию установлен.")
                if self.__connection.modify(dn, uac_attributes):
                    print("Атрибуты учётной записи изменены.")
                else:
                    print("Ошибка изменения арибутов учётной записи.")
            else:
                print("Ошибка установки пароля учётной записи.")
        else:
            print("Ошибка добавления учётной записи пользователя.")

        self.__connection.unbind()
