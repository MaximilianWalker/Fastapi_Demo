from fastapi import Depends
from functools import lru_cache

from .procedures import VideoProcedures

def get_db():
    db = VideoProcedures()
    try:
        db.connect()
        yield db
    finally:
        db.close()