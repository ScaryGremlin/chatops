from ldap3 import Connection, Server, ALL

from credentials import DOMAIN
from datetime import datetime
import locale


class ADConnector:
    """
    Класс подключения к серверу Active Directory
    """
    def __init__(self, server: str, login: str, password: str):
        """
        Конструктор
        :param server: Адрес сервера Active Directory. DNS имя или IP.
        :param login: Домен\логин - CO\Administrator
        :param password: Пароль
        """
        ldap_server = Server(server, get_info=ALL)
        self.__connection = Connection(ldap_server, login, password, auto_bind=True)

    @staticmethod
    def get_password(password_length=0, random=None) -> str:
        """
        Генерация пароля пользователя. Если random=True, то пароль - набор случайных символов, длинной password_length
        Если random=None, то пароль - текщий месяц плюс год со строчной буквы, например, май2021
        :return: Пароль пользователя
        """
        if random:
            pass
        else:
            list_of_months = ["январь", "февраль", "март", "апрель", "май", "июнь",
                              "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"]
            date = datetime.now()
            month = date.month
            year = date.year
            return list_of_months[month-1] + str(year)

    def add_user(self, fio: str, org_unit: str):
        """
        Добавление пользователя
        :param fio: Фамилия, имя, отчество.
        :param org_unit: Организационная еденица домена. Подразделение, в которое добавить пользователя
        """
        surname, name, middle_name = [element.strip().capitalize() for element in fio.split()]
        login = surname + "_" + name[0] + middle_name[0]
        cn = "CN=" + name + " " + surname + ","
        ou = "OU=" + org_unit + ","
        dc = ""
        for element in DOMAIN.split("."):
            dc += "DC=" + element + ","
        dn = cn + ou + dc.strip(",")
        object_class = ["top", "person", "organizationalPerson", "user"]
        attributes = {'sn': surname, "givenName": name, "sAMAccountName": login}
        print(self.get_password())
        # self.__connection.add(dn, object_class, attributes)
        # print(self.__connection.result)
        print(login)
