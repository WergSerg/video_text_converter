"""Бизнес-логика"""

from os import remove

from app.config import TEMPORARY_FILE_NAME
from app.converter import VideoToTextConverter
from app.utils import get_recognized_text_in_html


async def get_text_from_video_file(file_body: bytes):
    """Создает файл, читает из него текст и удаляет"""

    with open(TEMPORARY_FILE_NAME, 'wb') as file:
        file.write(file_body)

    converter = VideoToTextConverter(TEMPORARY_FILE_NAME)
    recognized_text = converter.get_recognized_text()

    remove(TEMPORARY_FILE_NAME)

    return get_recognized_text_in_html(recognized_text)
