from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class FileInfo(BaseModel):
    name: str
    file_type: str
    path: str

class FileDetailedInfo(BaseModel):
    upload_user_id: int
    upload_user_name: str
    upload_date: datetime
    status: str