import os
from datetime import datetime
import requests
import glob
from collections import Counter
from openpyxl import Workbook
from random import choice
from string import ascii_letters, digits


def create_image_folder() -> None:
    dir = "./output/images"
    if not os.path.exists(dir):
        os.makedirs(dir)


def check_date(data: str) -> str:
    if "minutes" in data:
        today = datetime.now.strftime("%B %d, %Y")
        return today
    return data


def write_xls_data(data: list) -> None:
    file_path = "./output/News data.xlsx"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
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
    c = 0
    txt = text.split()

    for word in txt:
        if word.strip(",.;:-?!+=*%$#@[]") == phrase:
            c += 1

    return c


def check_dollar(text: str) -> bool:
    pattern = ["$", "dollars", "usd", "dollar"]
    count = Counter(text.lower())
    number = {char: count[char] for char in pattern}

    if number != 0:
        return True
    return False


def save_img(image_url: str) -> str:
    image_name = generate_name()

    if image_url == "":
        return ""

    img_data = requests.get(image_url).content
    with open(f"./output/images/{image_name}", "wb") as handler:
        handler.write(img_data)

    return image_name


def get_img_names(path="./output/images/*.jpg"):
    files = glob.glob(path)
    return files
