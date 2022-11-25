"""Утилиты"""

from aiofiles import open as async_open
from fastapi import UploadFile

from app.config import APP_PATH


async def write_content_from_file_to_temporary_file(
        file: UploadFile, temporary_file_name: str
    ) -> None:
    """Записывает содержимое файла во временный файл"""

    async with async_open(temporary_file_name, "wb") as temporary_file:
        file_content = await file.read()

        await temporary_file.write(file_content)


def get_temporary_file_name(file: UploadFile) -> str:
    """Возвращает название временного файла"""

    file_extension = file.filename.split(".")[-1]

    return APP_PATH + "file." + file_extension


def get_recognized_text_in_html(recognized_text: dict) -> str:
    """Возвращает распознанный текст в формате HTML"""

    return "".join(
        f"<div style='width: 800px'><strong>{min}:</strong> {text}</div><br>"
        for min, text in recognized_text.items()
    )
