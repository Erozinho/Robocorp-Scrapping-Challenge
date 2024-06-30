from os import makedirs, path
from datetime import datetime as dt
from requests import get
from re import search, sub
from openpyxl import Workbook
from random import choice
from string import ascii_letters, digits


def check_date(data: str) -> str:
    if "minutes" in data:
        today = dt.now
        return today.strftime("%B %d, %Y")
    return data


def write_xls_data(data: list) -> None:
    file_path = "./output/News data.xlsx"
    makedirs(path.dirname(file_path), exist_ok=True)
    wb = Workbook()
    ws = wb.active

    for line in data:
        ws.append(line)

    wb.save(file_path)


def generate_name(extension="jpg", nchar=8) -> str:
    characters = ascii_letters + digits
    filename = ''.join(choice(characters) for _ in range(nchar))
    return f"{filename}.{extension}"


def count_phrase(phrase: str, text: str) -> int:
    text = sub(r'[^\w\s]', '', text.lower())
    phrase = phrase.lower()
    return text.split().count(phrase)


def check_dollar(text: str) -> bool:
    patterns = [
        r'\$\d+',
        r'\d+\s*dollars',
        r'\d+\s*usd',
        r'\d+\s*dollar',
    ]
    text_lower = text.lower()
    return any(search(pattern, text_lower) for pattern in patterns)


def save_img(image_url: str) -> str:
    file_path = "./output/images/"
    image_name = generate_name()
    makedirs(path.dirname(file_path), exist_ok=True)

    if image_url == "":
        return ""

    img_data = get(image_url).content
    with open(f"{file_path+image_name}", "wb") as handler:
        handler.write(img_data)

    return image_name
