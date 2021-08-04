import emoji
from ldap3 import Connection, Server, ALL, MODIFY_REPLACE

import miscellaneous as misc
from credentials import DOMAIN


class ADConnector:
    """
    Класс подключения к серверу Active Directory
    """
    ACCOUNT_ADDED = emoji.emojize(":check_mark: Учётная запись пользователя добавлена.\n")
    DEFAULT_PASSWORD_SET = emoji.emojize(":check_mark: Пароль учётной записи по умолчанию установлен.\n")
    ACCOUNT_ATTRIBUTES_CHANGED = emoji.emojize(":check_mark: Атрибуты учётной записи изменены.\n")
    ERROR_ADDING_ACCOUNT = emoji.emojize(":cross_mark: Ошибка добавления учётной записи пользователя.\n")
    PASSWORD_SETTING_ERROR = emoji.emojize(":cross_mark: Ошибка установки пароля учётной записи.\n")
    ERROR_CHANGING_ATTRIBUTES = emoji.emojize(":cross_mark: Ошибка изменения арибутов учётной записи.\n")

    def __init__(self, server: str, login: str, password: str):
        """
        Конструктор
        :param server: Адрес сервера Active Directory. DNS-имя или IP.
        :param login: NetBIOS-имя домена\логин - CO\Administrator
        :param password: Пароль
        """
        ldap_server = Server(server, get_info=ALL)
        self.__connection = Connection(ldap_server, login, password, auto_bind=True)

    def add_account(self, fio: str, org_unit: str, mobile: str) -> tuple:
        """
        Добавить пользователя
        :param fio: Фамилия, имя, отчество пользователя
        :param org_unit: Организационная еденица домена. Подразделение, в которое добавить пользователя.
        :param mobile: Мобильный телефон пользователя
        :return: Список ошибок или успешных выполнений команд
        """
        # Получить фамилию, имя и отчетство пользователя
        requisites = misc.requisites_to_data(fio)

        # Сгенерировать строку dn
        surname = requisites[0]
        name = requisites[1]
        login = requisites[3]
        cn = "CN=" + name + " " + surname + ","
        ou = "OU=" + org_unit + ","
        dc = ""
        for element in DOMAIN.split("."):
            dc += "DC=" + element + ","
        dn = cn + ou + dc.strip(",")

        #
        object_class = ["top", "person", "organizationalPerson", "user"]

        # Установить атрибуты учётной записи.
        # Фамилия, имя, логин для входа - Фамилия_ИО, отображаемое имя и мобильный телефон.
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

        # Сгенерировать пароль по умолчанию - месяц и год, например, август2021
        password = misc.get_password()

        # Список возвращаемых ошибок или успешных выполнений команд
        return_codes = []
        error = True
        if self.__connection.add(dn, object_class, attributes):
            # Учётная запись пользователя добавлена
            return_codes.append(self.ACCOUNT_ADDED)
            if self.__connection.extend.microsoft.modify_password(dn, password):
                # Пароль учётной записи по умолчанию установлен
                return_codes.append(self.DEFAULT_PASSWORD_SET)
                if self.__connection.modify(dn, uac_attributes):
                    # Атрибуты учётной записи изменены
                    return_codes.append(self.ACCOUNT_ATTRIBUTES_CHANGED)
                    error = False
                else:
                    # Ошибка изменения арибутов учётной записи
                    return_codes.append(self.ERROR_CHANGING_ATTRIBUTES)
            else:
                # Ошибка установки пароля учётной записи
                return_codes.append(self.PASSWORD_SETTING_ERROR)
        else:
            # Ошибка добавления учётной записи пользователя
            return_codes.append(self.ERROR_ADDING_ACCOUNT)

        self.__connection.unbind()
        # Вернуть True, если была ошибка, иначе - False и список с пояснениями выполнения операций
        return error, return_codes
