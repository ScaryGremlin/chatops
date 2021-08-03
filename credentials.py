from os import getenv

from dotenv import load_dotenv

load_dotenv()
AD_SERVER = getenv("AD_SERVER")
SMB_SERVER_IP = getenv("SMB_SERVER_IP")
SMB_SERVER_NAME = getenv("SMB_SERVER_NAME")
AD_LOGIN = getenv("AD_LOGIN")
AD_PASSWORD = getenv("AD_PASSWORD")
DOMAIN = getenv("DOMAIN")
EXCHANGE_FOLDER = getenv("EXCHANGE_FOLDER")
