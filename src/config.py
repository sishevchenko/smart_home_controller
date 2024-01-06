import os
from dotenv import load_dotenv

load_dotenv(".env")

DEBUG = True
BOT_START = True

APP_HOST = os.getenv("APP_HOST")
APP_PORT = os.getenv("APP_PORT")
SECRET_KEY = os.getenv("SECRET_KEY")
API_KEY = os.getenv("API_KEY")
BOT_URL = os.getenv("BOT_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN")
REGISTER_KEY = os.getenv("REGISTER_KEY")

OWNERS_IDS = {
	344797426: "Sergey",
	451773711: "Igor",
	408042394: "Alya",
	124965654: "Matvey",
}
