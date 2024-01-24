from fastapi import HTTPException, status

InvalidTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid token",
    headers={"WWW-Authenticate": "Bearer"},
)

IncorrectCredentialsException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)

LocationMismatchException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Location mismatch",
    headers={"WWW-Authenticate": "Bearer"},
)

DeviceMismatchException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Device mismatch",
    headers={"WWW-Authenticate": "Bearer"},
)

UnavailableUsernameException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Username is already in use",
    headers={"WWW-Authenticate": "Bearer"},
)

UnavailableEmailException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Email is already in use",
    headers={"WWW-Authenticate": "Bearer"},
)

InvalidEmailException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid email.",
    headers={"WWW-Authenticate": "Bearer"},
)