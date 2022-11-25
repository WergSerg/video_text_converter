"""Бизнес-логика"""

from os import remove

from fastapi import UploadFile

from app.converter import VideoToTextConverter
from app.utils import (
    get_temporary_file_name,
    write_content_from_file_to_temporary_file,
)


async def get_text_from_video_file(file: UploadFile):
    """Выдает текст из видео-файла"""

    temporary_file_name = get_temporary_file_name(file)

    await write_content_from_file_to_temporary_file(file, temporary_file_name)

    converter = VideoToTextConverter(temporary_file_name)
    recognized_text = converter.get_recognized_text()

    remove(temporary_file_name)

    return recognized_text
