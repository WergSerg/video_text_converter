"""Main app file"""

from fastapi import FastAPI, Request, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

TemplateResponse = Jinja2Templates(directory="app/templates").TemplateResponse


@app.post("/convert_video/")
async def convert_video_file(file: UploadFile):
    """Convert video file to text and return text"""

    return file.filename


@app.get("/")
async def index(request: Request) -> TemplateResponse:
    """Index page"""

    return TemplateResponse("index.html", {"request": request})
