from typing import Optional, Set
from pydantic import BaseModel

class User (BaseModel):
    username: str
    email: str
    password_hash: Optional[str]
    role: str
    status: Optional[str]
    permissions: Optional[Set[str]]

class AccessToken (BaseModel):
    iss: str
    sub: str
    exp: float
    user: str
    email: str
    role: str
    permissions: Set[str]

class RefreshToken (BaseModel):
    iss: str
    sub: str
    exp: float
    user: str
    device: str
    os: str
    browser: str
    country: Optional[str]
    city: Optional[str]

#https://tools.ietf.org/html/rfc6749#section-5.1
class LoginResponse (BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class RefreshResponse (BaseModel):
    access_token: str
    token_type: str
    expires_in: int