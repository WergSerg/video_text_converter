"""Утилиты"""

from re import findall


def get_recognized_text_in_html(recognized_text: dict) -> str:
    """Выдает распознанный текст в формате HTML"""

    return f"<div>{recognized_text}</div><br>"


async def get_minute_from_request_body(request_body: bytes) -> int:
    """Выдает минуту, переданную с фронта"""

    str_with_min = request_body.split(b'name="min"')

    minute = findall(r"\d+", str(str_with_min[1]).split("-", maxsplit=1)[0])[0]

    return int(minute)
