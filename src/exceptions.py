from fastapi import HTTPException, status

ServerDownException = HTTPException(
    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    detail="Server Down",
    headers={"WWW-Authenticate": "Bearer"},
)