from fastapi import HTTPException, status

UnallowedFileFormat = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="This file format is invalid or not currently accepted by the server.",
    headers={"WWW-Authenticate": "Bearer"},
)