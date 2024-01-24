from fastapi import Depends, Cookie, Header, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional
from functools import lru_cache
from settings import settings

from .models import User, AccessToken, RefreshToken
from exceptions import ServerDownException
from .exceptions import (
    IncorrectCredentialsException
)
from .procedures import UserProcedures
from .tools import (
    validate_password,
    get_token_claims,
    generate_access_token,
    gererate_refresh_token,
    validate_access_token, 
    validate_refresh_token
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="access_token")

def get_db():
    db = UserProcedures()
    try:
        db.connect()
        yield db
        db.close()
    except Exception as e:
        raise ServerDownException

def get_access_token(access_token: str = Depends(oauth2_scheme)):
    return validate_access_token(access_token)

def get_user_with_credentials(form_data: OAuth2PasswordRequestForm = Depends(), db: str = Depends(get_db)):
    if not db.username_exists(form_data.username):
        raise IncorrectCredentialsException
    user = User(**db.get_user(form_data.username))
    if not validate_password(form_data.password, user.password_hash):
        raise IncorrectCredentialsException
    user.permissions = db.get_role_permissions(user.role)
    return user

def get_user_with_token(access_token_claims: AccessToken = Depends(get_access_token), db: str = Depends(get_db)):
    user = {
        "username": access_token_claims.user,
        "email": access_token_claims.email,
        "role": access_token_claims.role,
        "permissions": access_token_claims.permissions
    }
    return User(**user)

def get_new_access_token_with_credentials(user: str = Depends(get_user_with_credentials), db: str = Depends(get_db)):
    return generate_access_token(user)

def get_new_refresh_token_with_credentials(
    request: Request, 
    user_agent: Optional[str] = Header(None), 
    user: str = Depends(get_user_with_credentials), 
):
    ip = str(request.client.host)
    return gererate_refresh_token(ip, user_agent, user)

def get_new_access_token_with_refresh(
    request: Request,
    refresh_token: Optional[str] = Cookie(None),
    user_agent: Optional[str] = Header(None), 
    db: str = Depends(get_db)
):
    ip = str(request.client.host)
    refresh_token_object = validate_refresh_token(refresh_token, ip, user_agent)
    user = User(**db.get_user(refresh_token_object.user))
    user.permissions = db.get_role_permissions(user.role)
    return generate_access_token(user)
