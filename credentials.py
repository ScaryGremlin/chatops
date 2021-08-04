from os import getenv

from dotenv import load_dotenv

load_dotenv()

AD_SERVER_IP = getenv("AD_SERVER_IP")
AD_LOGIN = getenv("AD_LOGIN")
AD_PASSWORD = getenv("AD_PASSWORD")
DOMAIN = getenv("DOMAIN")

SMB_SERVER_IP = getenv("SMB_SERVER_IP")
SMB_SERVER_PORT = int(getenv("SMB_SERVER_PORT"))

SHARE = getenv("SHARE")
