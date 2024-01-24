from fastapi import Depends
from functools import lru_cache
from .procedures import FileProcedures
from exceptions import ServerDownException

def get_db():
    db = FileProcedures()
    try:
        db.connect()
        yield db
        db.close()
    except Exception as e:
        raise ServerDownException