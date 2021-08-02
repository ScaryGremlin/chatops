import credentials as creds
from adconnector import ADConnector


def main():
    active_directory = ADConnector(server=creds.AD_SERVER, login=creds.AD_LOGIN, password=creds.AD_PASSWORD)
    active_directory.add_account("Лепшоков Дахир Ахматович", "frontoffice", "+79994970133")


if __name__ == '__main__':
    main()
