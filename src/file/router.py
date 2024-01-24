from fastapi import WebSocket, APIRouter, Depends, Response, HTTPException, File, UploadFile, Header
from fastapi.responses import StreamingResponse
from typing import List, Optional

from settings import settings
from .tools import get_file_size

from .models import VideoInfo, VideoDetailedInfo
from .dependencies import get_db
from .exceptions import (
    UnallowedFileFormat
)

video_router = APIRouter(
    prefix="/file",
    tags=["file"]
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)

@video_router.get("/upload")
async def upload(file: UploadFile = File(...), db: str = Depends(get_db)):
    extension = file.filename.split(".")[-1]
    file_type = "VIDEO" if extension in settings.api_video_formats else None
    file_type = "IMAGE" if extension in settings.api_image_formats else None
    if file_type is not None:
        db.create_file()

    return {"success": True}
