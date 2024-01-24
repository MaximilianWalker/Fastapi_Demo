from fastapi import APIRouter, Depends, Form, Header, Request, Response, HTTPException
# from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional
from settings import settings
import re

from .models import (
    User,
    AccessToken,
    RefreshToken,
    LoginResponse,
    RefreshResponse
)
from .dependencies import (
    get_db,
    get_user_with_token,
    get_new_access_token_with_credentials,
    get_new_refresh_token_with_credentials,
    get_new_access_token_with_refresh
)
from .tools import (
    get_password_hash,
    validate_password,
    get_token_claims
)
from .exceptions import (
    InvalidTokenException,
    IncorrectCredentialsException,
    DeviceMismatchException,
    LocationMismatchException,
    UnavailableUsernameException,
    UnavailableEmailException,
    InvalidEmailException
)

user_router = APIRouter(
    prefix="/user",
    tags=["user"]
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)


@user_router.get("/me")
async def me(user: User = Depends(get_user_with_token)):
    return {
        "username": user.username,
        "email": user.email,
        "role": user.role
    }


@user_router.get("/refresh", response_model=RefreshResponse)
async def refresh(response: Response, access_token: dict = Depends(get_new_access_token_with_refresh)):
    content = {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": get_token_claims(access_token)["exp"]
    }

    response.set_cookie(
        key="access_token",
        value=access_token,
        # domain="localhost:3000",
        httponly=True
    )
    return content


@user_router.post("/register")
async def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: str = Depends(get_db)
):
    if not re.search("^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$", email):
        raise InvalidEmailException
    if db.username_exists(username):
        raise UnavailableUsernameException
    if db.email_exists(email):
        raise UnavailableEmailException

    password_hash = get_password_hash(password)
    db.create_user(username, email, password_hash)
    return {"success": True}


@user_router.post("/login", response_model=LoginResponse)
async def login(
    response: Response,
    access_token: str = Depends(get_new_access_token_with_credentials),
    refresh_token: str = Depends(get_new_refresh_token_with_credentials)
):
    content = {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": get_token_claims(access_token)["exp"]
    }

    response.set_cookie(
        key="access_token",
        value=access_token,
        # domain="localhost:3000",
        httponly=True
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        # domain="localhost:3000",
        httponly=True
    )
    return content


@user_router.get("/logout")
async def logout(response: Response):
    response.set_cookie(
        key="access_token",
        value=None,
        # domain="localhost:3000",
        httponly=True
    )
    response.set_cookie(
        key="refresh_token",
        value=None,
        # domain="localhost:3000",
        httponly=True
    )
    return {"success": True}


@user_router.get("/change-password")
async def change_password(
    old_password: str = Form(...),
    new_password: str = Form(...),
    user: User = Depends(get_user_with_token),
    db: str = Depends(get_db)
):
    if not validate_password(old_password, user.password_hash):
        raise IncorrectCredentialsException
    db.change_user_password(user, new_password)
    return {"success": True}


@user_router.post("/request-password-reset")
async def request_password_reset(
    username: str = Form(...),
    email: str = Form(...),
    db: str = Depends(get_db)
):
    if not re.search("^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$", email):
        raise InvalidEmailException
    if db.username_exists(username):
        raise UnavailableUsernameException
    if db.email_exists(email):
        raise UnavailableEmailException

    password_hash = get_password_hash(password)
    db.create_user(username, email, password_hash)
    return {"success": True}


@user_router.post("/submit-password-reset")
async def submit_password_reset(
    username: str = Form(...),
    email: str = Form(...),
    db: str = Depends(get_db)
):
    if not re.search("^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$", email):
        raise InvalidEmailException
    if not db.username_exists(username):
        raise UnavailableUsernameException
    if not db.email_exists(email):
        raise UnavailableEmailException

    password_hash = get_password_hash(password)
    db.create_user(username, email, password_hash)
    return {"success": True}
