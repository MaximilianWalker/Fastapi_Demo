from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from file.models import FileInfo, FileDetailedInfo

class EncodingProgress(BaseModel):
    frame: int
    fps: float
    stream_0_0_q: float
    total_size: int
    out_time_ms: int
    out_time: str
    dup_frames: int
    drop_frames: int
    progress: str

class VideoInfo(FileInfo):
    width: int
    height: int
    ratio: str
    video_codec: str
    audio_codec: str

class VideoDetailedInfo(VideoInfo, FileDetailedInfo):
    status: str
    fps: int
    video_bitrate: int
    audio_bitrate: int
    audio_channels: int
    data_rate: int
    bits_per_pixel: float