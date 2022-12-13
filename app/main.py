"""Главный файл приложения"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import STATIC_PATH, TEMPLATES_PATH, TEMPORARY_FILE_NAME
from app.converter import VideoToTextConverter
from app.utils import get_minute_from_request_body


app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")

TemplateResponse = Jinja2Templates(directory=TEMPLATES_PATH).TemplateResponse


@app.post("/create_converter/")
async def create_converter(request: Request) -> JSONResponse:
    """Создает файл и конвертер"""

    with open(TEMPORARY_FILE_NAME, "wb") as file:
        file_body = await request.body()
        file.write(file_body)

    global VIDEO_TO_TEXT_CONVERTER
    VIDEO_TO_TEXT_CONVERTER = VideoToTextConverter(TEMPORARY_FILE_NAME)


@app.get("/get_video_minutes/")
async def get_video_total_minutes() -> JSONResponse:
    """Возвращает длительность видео-файла"""

    total_minutes = VIDEO_TO_TEXT_CONVERTER.get_audio_total_minutes()

    return JSONResponse({"total_minutes": total_minutes})


@app.post("/convert_video/")
async def convert_video_to_text(request: Request) -> JSONResponse:
    """Возвращает HTML с извлечённым из видео текстом"""

    request_body = await request.body()

    video_minute = await get_minute_from_request_body(request_body)
    text_from_video = VIDEO_TO_TEXT_CONVERTER.get_text_for_minute(video_minute)

    return JSONResponse({"text": text_from_video})


@app.get("/close_converter/")
async def close_converter() -> JSONResponse:
    """Закрывает конвертер"""

    VIDEO_TO_TEXT_CONVERTER.close()


@app.get("/")
async def index(request: Request) -> TemplateResponse:
    """Главная страница"""

    return TemplateResponse("index.html", {"request": request})
