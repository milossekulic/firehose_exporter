# app/config.py
import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")


def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


config = load_config()

DIRECTORY_PATH = config["DIRECTORY_PATH"]
REGION_NAME = config["REGION_NAME"]
AWS_ACCESS_KEY_ID = config["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = config["AWS_SECRET_ACCESS_KEY"]
DELIVERY_STREAM_NAME = config["DELIVERY_STREAM_NAME"]
POSITION_FILE = "file_positions.json"
MAX_RETRIES = config.get("MAX_RETRIES", 3)
RETRY_DELAY = config.get("RETRY_DELAY", 5)  # seconds
