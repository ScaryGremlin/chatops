import emoji
from errbot import BotPlugin, arg_botcmd
from errbot.templating import tenv

import credentials as creds
import miscellaneous as misc
from adconnector import ADConnector
from smbconnector import SMBConnector


class AdAccounts(BotPlugin):
    """
    Класс errbot
    """
    trigger_messages = [
        "как добавить учетку",
        "как добавить учётку",
        "как добавить учетную запись",
        "как добавить учётную запись",
        "как создать учетку",
        "как создать учётку",
        "как создать учетную запись",
        "как создать учётную запись"
    ]

    DIRECTORY_AND_PASSFILE_CREATED = emoji.emojize(":check_mark: Директория пользователя и файл "
                                                   "с паролем созданы. \n")
    PERMISSIONS_SET = emoji.emojize(":check_mark: Права на директорию пользователя и на файл с паролем установлены. \n")
    ERROR_CONNECTING_AD = emoji.emojize(":cross_mark: Ошибка подключения к серверу AD.\n")
    ERROR_CONNECTING_SMB = emoji.emojize(":cross_mark: Ошибка подключения к SMB-серверу.\n")
    ERROR_CREATING_USER_DIRECTORY_OR_FILE = emoji.emojize(":cross_mark: Ошибка создания директории пользователя "
                                                          "или файла с паролем.\n")
    ERROR_SET_PERMISSION = emoji.emojize(":cross_mark: Ошибка установки прав директории пользователя.\n"
                                         "Функция выполнилась с прерыванием!\n")

    @arg_botcmd("-fio", dest="fio", type=str)
    @arg_botcmd("-ou", dest="org_unit", type=str)
    @arg_botcmd("-mobile", dest="mobile", type=str)
    def add_account(self, _, fio, org_unit, mobile):
        """
        Обработчик команды add_account
        :param _:
        :param fio: Фамилия, имя, отчество пользователя
        :param org_unit: Организационная еденица домена. Подразделение, в которое добавить пользователя.
        :param mobile: Мобильный телефон пользователя
        :return: Сообщение об ошибке или об успешном выполнении команд
        """
        result_set_permissions = "" # Вывод ssh
        # Подключиться к серверу Active Directory
        try:
            active_directory = ADConnector(server=creds.AD_SERVER_IP,
                                           login=creds.AD_LOGIN,
                                           password=creds.AD_PASSWORD)
        except Exception:
            return self.ERROR_CONNECTING_AD
        else:
            # Добавить учётную запись пользователя
            error, command_results = active_directory.add_account(fio, org_unit, mobile)
            # Если добавление учётное записи завершилось без ошибок...
            if not error:
                # Сгенерировать имя директории пользователя
                account_directory = misc.requisites_to_data(fio)[3]
                # Подключиться к SMB-серверу и создать директорию пользователя с необходимым набором прав
                try:
                    smb_connector = SMBConnector(smb_server_ip=creds.SMB_SERVER_IP,
                                                 username=creds.SMB_SERVER_LOGIN,
                                                 password=creds.AD_PASSWORD,
                                                 domain=creds.DOMAIN,
                                                 remote_name=creds.SMB_SERVER_NAME
                                                 )
                except Exception:
                    command_results.append(self.ERROR_CONNECTING_SMB)
                else:
                    # Создать директорию пользователя и файл с паролем с необходимым набором прав
                    try:
                        smb_connector.create_directory(creds.SHARE, account_directory)
                        smb_connector.create_password_file(creds.SHARE, account_directory)
                    except Exception:
                        command_results.append(self.ERROR_CREATING_USER_DIRECTORY_OR_FILE)
                    else:
                        command_results.append(self.DIRECTORY_AND_PASSFILE_CREATED)
                        # Установить права на директорию пользователя и на файл с паролем
                        try:
                            result_set_permissions = smb_connector.set_permissions(rsat_desktop_ip=creds.RSAT_DESKTOP_IP,
                                                                                  rsat_desktop_username=creds.RSAT_DESKTOP_USERNAME,
                                                                                  account_directory=account_directory)
                        except Exception:
                            command_results.append(self.ERROR_SET_PERMISSION)
            # Оповестить об ошибках добавления учётной записи пользователя или об успешном завершении команд
            reply_message = ""
            for command_result in command_results:
                reply_message += command_result
            return reply_message + "```Вывод ssh:```\n" + f"```{result_set_permissions}```"

    def callback_message(self, message) -> None:
        if any(trigger in message.body.lower() for trigger in self.trigger_messages):
            self.send(message.frm, emoji.emojize(":information: Воспользуйтесь командой !add_account. \n "
                                                 "Для подробностей наберите help"))
        if message.body == "help":
            help_message = tenv().get_template("help.md").render()
            print(help_message)
            msg = "__help message__"
            print(msg)
            self.send(message.frm, msg)
