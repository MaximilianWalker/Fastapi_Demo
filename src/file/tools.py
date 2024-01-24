import sys
import os
import shutil
import subprocess
import json
from settings import settings
from .models import FileInfo, FileDetailedInfo

def get_file_size(path):
  return os.stat(path).st_size

def save_file(file):
  open()
  shutil.copyfileobj(uploaded_file.file, file_object) 

