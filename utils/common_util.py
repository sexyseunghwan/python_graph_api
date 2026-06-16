import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import cv2
from telegram.error import TelegramError

from config import logger


def read_file_to_json(file_path: str) -> dict | None:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        logger.error(str(e), exc_info=True)
        return None


def is_date(string_date: str, date_format: str) -> bool:
    try:
        datetime.strptime(string_date, date_format)
        return True
    except ValueError:
        return False


def exchange_rate(query: str) -> dict:
    currency_dict = {}

    logger.info(f'{query} query executed')
    url = f"https://www.google.com/search?q={query}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(str(e))
        return currency_dict

    soup = BeautifulSoup(response.text, "html.parser")
    target_currency = soup.find("span", {"class": "r0bn4c rQMQod"})
    korea_won = soup.find("div", {"class": "BNeawe iBp4i AP7Wnd"})

    if target_currency is None or korea_won is None:
        logger.error(f'Unable to parse exchange rate from query: {query}')
        return currency_dict

    currency_dict['target_currency'] = target_currency.get_text()
    currency_dict['korea_won'] = korea_won.get_text()
    return currency_dict


def send_image(update, context, file_path: str) -> None:
    img = cv2.imread(file_path)
    if img is None:
        logger.error(f'Unable to read image file: {file_path}')
        return

    try:
        ok, encoded_img = cv2.imencode(".jpg", img)
    except cv2.error as e:
        logger.error(str(e))
        return

    if not ok:
        logger.error(f'Unable to encode image file: {file_path}')
        return

    try:
        img_bytes = encoded_img.tobytes()
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=img_bytes)
    except TelegramError as e:
        logger.error(str(e))
        return

    logger.info(f'A picture of {file_path} has been sent.')
