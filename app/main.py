"""Главный файл приложения"""

from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import STATIC_PATH, TEMPLATES_PATH
from app.utils import get_recognized_text_in_html
from app.services import get_text_from_video_file


app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")

TemplateResponse = Jinja2Templates(directory=TEMPLATES_PATH).TemplateResponse


@app.post("/convert_video/")
async def convert_video_file(file: UploadFile) -> HTMLResponse:
    """Возвращает HTML с извлеченным из видео текстом"""

    recognized_text = await get_text_from_video_file(file)
    recognized_text_in_html = get_recognized_text_in_html(recognized_text)

    return HTMLResponse(recognized_text_in_html)


@app.get("/")
async def index(request: Request) -> TemplateResponse:
    """Index page"""

    return TemplateResponse("index.html", {"request": request})
