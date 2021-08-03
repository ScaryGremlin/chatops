from pathlib import Path

from errbot import BotPlugin, arg_botcmd

import credentials as creds
import miscellaneous as misc
from adconnector import ADConnector


class AdAccounts(BotPlugin):
    """
    Класс errbot
    """
    trigger_messages = [
        "как добавить учетку",
        "как добавить учетную запись"
    ]

    @arg_botcmd("--fio", dest="fio", type=str)
    @arg_botcmd("--ou", dest="org_unit", type=str)
    @arg_botcmd("--mobile", dest="mobile", type=str)
    def add_account(self, _, fio, org_unit, mobile):
        """
        Обработчик команды add_account
        :param _:
        :param fio: Фамилия, имя, отчество пользователя
        :param org_unit: Организационная еденица домена. Подразделение, в которое добавить пользователя.
        :param mobile: Мобильный телефон пользователя
        :return: Сообщение об ошибке или об успешном выполнении команд
        """
        # Подключиться к серверу Active Directory
        try:
            active_directory = ADConnector(server=creds.AD_SERVER, login=creds.AD_LOGIN, password=creds.AD_PASSWORD)
        except Exception:
            return "<code>Ошибка подключения к серверу AD</code>"
        else:
            # Добавить учётную запись пользователя
            error, error_codes = active_directory.add_account(fio, org_unit, mobile)
            if not error:
                # Сгенерировать путь к директории пользователя
                account_directory = Path(creds.EXCHANGE_FOLDER) / Path(misc.requisites_to_data(fio)[3])
                # Создать директорию пользователя
                try:
                    account_directory.mkdir()
                except Exception:
                    return "Ошибка создания директории пользователя"
                else:
                    # Установить права на директорию пользователя
                    misc.set_directory_permissions(account_directory)
            # Оповестить об ошибках добавления учётной записи пользователя или об успешном завершении команд
            reply_message = ""
            for error_code in error_codes:
                reply_message += error_code + "\n"
        return reply_message

    def callback_message(self, message) -> None:
        if any(trigger in message.body.lower() for trigger in self.trigger_messages):
            self.send(message.frm, "Воспользуйтесь командой !add_account")
        if message.body == "help":
            self.send(message.frm, '!add_account --fio "Фамилия Имя Отчество" '
                                   '--ou "OrganizationUnit" --mobile "+79995556677"')
