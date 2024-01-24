from fastapi import WebSocket, APIRouter, Depends, Response, HTTPException, File, UploadFile, Header
from fastapi.responses import StreamingResponse
from typing import List, Optional

from settings import settings
from .tools import get_file_size

from .models import VideoInfo, VideoDetailedInfo
from .dependencies import get_db

video_router = APIRouter(
    prefix="/video",
    tags=["video"]
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)

@video_router.get("/info/{file_id}")
async def stream(file_id: int, db: str = Depends(get_db)):
    stream = ffmpeg.input("")
    stream = ffmpeg.run
    return StreamingResponse()

@video_router.get("/detailed-info/{file_id}")
async def stream(file_id: int, db: str = Depends(get_db)):
    stream = ffmpeg.input("")
    stream = ffmpeg.run
    return StreamingResponse()

@video_router.get("/original-stream/{file_id}")
async def original_stream(file_id: int, byte_range: Optional[str] = Header(None, alias="Range"), db: str = Depends(get_db)):
    # video = db.get_video(video_id)
    # video_stream = open(settings.storage_path + video.path + "/original")
    tmp_file = ""
    video_size = get_file_size(tmp_file)
    video_stream = open(tmp_file, "rb")
    if byte_range is not None:
        [start, end] = byte_range.replace("bytes=", "").split("-")
        start = int(start)
        chunk_size = min(settings.api_stream_chunk_size, video_size - start)
        end = int(end) if end is not "" else start + chunk_size - 1
        video_stream.seek(start)
        
        header = {
            "Content-Range": f"bytes {str(start)}-{str(end)}/{str(video_size)}",
            "Accept-Ranges": "bytes",
            'Content-Length': str(chunk_size),
            "Content-Type": "video/mp4"
        }
        return Response(content=video_stream.read(chunk_size), headers=header, status_code=206)
    else:
        header = {
            'Content-Length': str(video_size),
            "Content-Type": "video/mp4"
        }
        return Response(content=video_stream.read(), headers=header)