import re
from typing import Union
from datetime import datetime


def text_(text: str):
    if len(text) == 0:
        return False
    points = 0
    if 2 <= len(text) <= 50:
        points += 1
    if re.fullmatch(r"[a-zA-Zа-яА-ЯёЁ\s]+", text):
        points += 1
    return True if points == 2 else False

def email_(email: str) -> bool:
    points = 0
    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}" # @(/w+).com
    result = re.search(pattern, email)
    if result:
        points += 1
        if len(result.group(1)) >= 5:
            points += 1
    if email.strip(" ") == email:
        points += 1
    return True if points == 3 else False

def password_(password) -> bool:
    points = 0
    if len(password) <= 8:
        points += 1
    if (any(char.isupper() for char in password) and
            any(char.islower() for char in password) and
            any(char.isdigit() for char in password) and
            any(char in "!@#$%^&*" for char in password)):
        points += 1
    if not " " in password:
        points += 1
    return True if points == 3 else False

def number_(number, a: int=18, b: int=100) -> bool:
    points = 0
    if not number.isdigit():
        return False
    if not " " in number:
        points += 1
    if a <= int(number) <= b:
        points += 1
    return True if points == 2 else False

def tel_(tel: str, startswith: Union[int, list[int]] = [7, 380]) -> bool:
    if isinstance(startswith, int):
        if not tel.startswith(f"+{str(startswith)}"):
            return False
    else:
        if not any(tel.startswith(f"+{str(startswith_)}") for startswith_ in startswith):
            return False
    points = 0
    if tel[1:].strip().isdigit():
        points += 1
    if 10 <= int(tel[1:].strip()) <= 15:
        points += 1
    return True if points == 2 else False


def data_(data: str, event: bool = False) -> bool:
    try:
        date = datetime.strptime(data, "%d.%m.%Y")  # Преобразуем строку в дату
    except ValueError:
        return False  # Некорректная дата (например, 30 февраля)

    today = datetime.today().date()  # Текущая дата без времени
    date = date.date()  # Убираем время у проверяемой даты

    if event:  # Если это дата события
        return date >= today  # Дата события должна быть сегодня или в будущем

    return date <= today


def time_(time: str) -> bool:
    if not re.match(r"^\d{2}:\d{2}$", time):  # Проверка формата HH:MM
        return False

    hours, minutes = map(int, time.split(":"))  # Преобразуем в числа

    if not (0 <= hours < 24 and 0 <= minutes < 60):  # Проверка границ
        return False

    return True


def url_(url: str) -> bool:
    pattern = r"^https?://[^\s/]+(\.com|\.net|\.rr)(/.*)?$"
    return bool(re.match(pattern, url))
