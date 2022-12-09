"""Главный файл приложения"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import STATIC_PATH, TEMPLATES_PATH
from app.services import get_text_from_video_file


app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")

TemplateResponse = Jinja2Templates(directory=TEMPLATES_PATH).TemplateResponse


@app.post("/convert_video/")
async def convert_video_to_text(request: Request) -> JSONResponse:
    """Возвращает HTML с извлечённым из видео текстом"""

    file_body = await request.body()

    recognized_text_in_html = await get_text_from_video_file(file_body)

    return JSONResponse({'text': recognized_text_in_html})


@app.get("/")
async def index(request: Request) -> TemplateResponse:
    """Главная страница"""

    return TemplateResponse("index.html", {"request": request})
