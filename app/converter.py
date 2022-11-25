"""Конвертер видео в текст"""

from contextlib import closing
from math import ceil
from os import remove
from wave import open as open_wav

from moviepy.editor import AudioFileClip
from speech_recognition import AudioFile, Recognizer

from app.config import FRAME_SIZE_IN_SECONDS, TEXT_LANGUAGE, WAV_FILE_NAME


class VideoToTextConverter:
    """Извлекает текст из видео.

    1. Создает .wav файл;
    2. Записывает в него аудио из видео-файла;
    3. Для каждой минуты аудио-дорожки считывает текст;
    4. Заносит текст в общий словарь;
    5. Удаляет .wav файл.

    """

    def __init__(self, file_path: str):
        self.__file_path = file_path

    def __write_audio_to_wav_file(self) -> None:
        """Записывает аудио с видео-файла в .wav файл"""

        audio = AudioFileClip(self.__file_path)
        audio.write_audiofile(WAV_FILE_NAME)

    def __get_audio_total_minutes(self) -> int:
        """Возвращает длительность аудио в минутах"""

        wav_file = open_wav(WAV_FILE_NAME, "r")

        with closing(wav_file) as file:
            frames_amount = file.getnframes()
            frame_rate = float(file.getframerate())

            frames_duration = frames_amount / frame_rate

        return ceil(frames_duration / FRAME_SIZE_IN_SECONDS)

    def __get_text_for_minute(self, minute: int) -> str:
        """Выдает текст из .wav файла для конкретной минуты"""

        recognizer = Recognizer()

        with AudioFile(WAV_FILE_NAME) as file:
            audio_from_file = recognizer.record(
                file,
                offset=minute * FRAME_SIZE_IN_SECONDS,
                duration=FRAME_SIZE_IN_SECONDS,
            )

            text = recognizer.recognize_google(
                audio_from_file,
                language=TEXT_LANGUAGE,
            )

        return text

    def __get_text_from_wav(self) -> dict:
        """Возвращает текст из .wav файла для каждой минуты"""

        total_minutes = self.__get_audio_total_minutes()
        minute_and_text = {}

        for minute in range(total_minutes):
            text = self.__get_text_for_minute(minute)

            minute_and_text[f"С {minute}-й по {minute + 1}-ю минуту"] = text

        return minute_and_text

    def get_recognized_text(self) -> dict:
        """Читает текст с .wav файла, после чего удаляет его"""

        self.__write_audio_to_wav_file()

        recognized_text = self.__get_text_from_wav()

        remove(f"{WAV_FILE_NAME}")

        return recognized_text
