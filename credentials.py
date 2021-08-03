from os import getenv

from dotenv import load_dotenv

load_dotenv()
AD_SERVER = getenv("AD_SERVER")
AD_LOGIN = getenv("AD_LOGIN")
AD_PASSWORD = getenv("AD_PASSWORD")
DOMAIN = getenv("DOMAIN")
EXCHANGE_FOLDER = getenv("EXCHANGE_FOLDER")
