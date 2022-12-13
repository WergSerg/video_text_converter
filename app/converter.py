"""Конвертер видео в текст"""

from contextlib import closing
from math import ceil
from os import remove
from wave import open as open_wav

from moviepy.editor import AudioFileClip
from speech_recognition import AudioFile, Recognizer, UnknownValueError

from app.config import (
    FRAME_SIZE_IN_SECONDS,
    TEMPORARY_FILE_NAME,
    TEXT_LANGUAGE,
    WAV_FILE_NAME,
)
from app.utils import get_recognized_text_in_html


class VideoToTextConverter:
    """Конвертер видео в текст"""

    def __init__(self, file_path: str):
        """Создает .wav файл и записывает в него аудио из видео-файла"""

        audio = AudioFileClip(file_path)
        audio.write_audiofile(WAV_FILE_NAME)

    def get_text_for_minute(self, minute: int) -> str:
        """Выдает текст из .wav файла для конкретной минуты"""

        recognizer = Recognizer()

        with AudioFile(WAV_FILE_NAME) as file:
            audio_from_file = recognizer.record(
                file,
                offset=minute * FRAME_SIZE_IN_SECONDS,
                duration=FRAME_SIZE_IN_SECONDS,
            )

            try:
                text = recognizer.recognize_google(
                    audio_from_file,
                    language=TEXT_LANGUAGE,
                )
            except UnknownValueError:
                text = ""

        return get_recognized_text_in_html(text)

    def get_audio_total_minutes(self) -> int:
        """Возвращает длительность .wav файла в минутах"""

        wav_file = open_wav(WAV_FILE_NAME, "r")

        with closing(wav_file) as file:
            frames_amount = file.getnframes()
            frame_rate = float(file.getframerate())

            frames_duration = frames_amount / frame_rate

        return ceil(frames_duration / FRAME_SIZE_IN_SECONDS)

    def close(self) -> None:
        """Закрывает конвертер - удаляет видео и .wav файлы"""

        remove(TEMPORARY_FILE_NAME)
        remove(WAV_FILE_NAME)
