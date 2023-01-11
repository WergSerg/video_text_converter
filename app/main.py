from fastapi import FastAPI, Request,  File, UploadFile

from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles


from .settings import TEMPLATES_PATH,STATIC_PATH
from .scripts import  VideoToTextConverter, get_minute_from_request_body

from app.scripts.converter_to_format import converter


app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")
TemplateResponse = Jinja2Templates(directory=TEMPLATES_PATH).TemplateResponse


@app.post('/download_file/')
async def download_text(file: UploadFile):
    file_name = file.filename
    binary_string = await file.read()
    convert = converter(file_name=file_name, binary_string=binary_string)
    global TEMP_FILE_NAME
    TEMP_FILE_NAME = convert.get_temporary_file_name()
    text='success'
    return JSONResponse(text)


@app.post('/create_file/')
async def create_file():
    global VIDEO_TO_TEXT_CONVERTER
    VIDEO_TO_TEXT_CONVERTER = VideoToTextConverter(TEMP_FILE_NAME)
    return JSONResponse(1)


@app.get('/get_total_min/')
async def get_total_min():

    total_minutes = VIDEO_TO_TEXT_CONVERTER.get_audio_total_minutes()
    return JSONResponse(total_minutes)

@app.post('/get_text/')
async def get_text(request: Request):
    request_body = await request.body()
    video_minute = await get_minute_from_request_body(request_body)
    text_from_video = VIDEO_TO_TEXT_CONVERTER.get_text_for_minute(video_minute)
    return JSONResponse({"text": text_from_video})

@app.get('/cancel/')
async def delete_file():
    VIDEO_TO_TEXT_CONVERTER.close()

@app.get("/")
async def root(request: Request) -> TemplateResponse:
    return  TemplateResponse("first.html", {"request": request})