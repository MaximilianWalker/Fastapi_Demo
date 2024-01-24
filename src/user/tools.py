import json
from datetime import datetime, timedelta
from settings import settings
from jose import jwt
from passlib.hash import argon2
from urllib.request import urlopen
from user_agents import parse

from .models import AccessToken, RefreshToken
from .exceptions import (
    InvalidTokenException,
    LocationMismatchException,
    DeviceMismatchException
)

def get_password_hash(password):
    return argon2.hash(password)

def validate_password(password, password_hash):
    return argon2.verify(password, password_hash)

def get_device_info(user_agent):
    parsed_urser_agent = parse(user_agent)
    return parsed_urser_agent.device.family, parsed_urser_agent.os.family, parsed_urser_agent.browser.family

def get_location_info(ip):
    print('https://ipinfo.io/widget/' + ip)
    data = None
    try:
        data = json.load(urlopen('https://ipinfo.io/widget/' + ip))
        return data["country"], data["city"]
    except Exception as e:
        print(e)
        return None, None

def get_token_claims(token):
    return jwt.get_unverified_claims(token)

def get_access_token_expiration():
    return (datetime.now() + timedelta(minutes=settings.api_access_token_expiration_time)).timestamp()

def get_refresh_token_expiration():
    return (datetime.now() + timedelta(days=settings.api_refresh_token_expiration_time)).timestamp()

def generate_access_token(user):
    content = {
        "iss": settings.api_name,
        "sub": user.username,
        "exp": get_access_token_expiration(),
        "user": user.username,
        "email": user.email,
        "role": user.role,
        "permissions": user.permissions
    }
    return jwt.encode(content, settings.api_access_token_key, algorithm=settings.api_token_algorithm)

def gererate_refresh_token(ip, user_agent, user):
    device, os, browser = get_device_info(user_agent)
    country, city = get_location_info(ip)
    content = {
        "iss": settings.api_name,
        "sub": user.username,
        "exp": get_refresh_token_expiration(),
        "user": user.username,
        "device": device,
        "os": os,
        "browser": browser,
        "country": country,
        "city": city
    }
    return jwt.encode(content, settings.api_refresh_token_key, algorithm=settings.api_token_algorithm)

def validate_access_token(access_token):
    try:
        claims = jwt.decode(access_token, settings.api_access_token_key, algorithms=[settings.api_token_algorithm])
    except Exception as e:
        raise InvalidTokenException

    return AccessToken(**claims)

def validate_refresh_token(refresh_token, ip, user_agent):
    claims = None
    try:
        if refresh_token == None or refresh_token == "None":
            raise Exception("No token provided")
        claims = jwt.decode(refresh_token, settings.api_refresh_token_key, algorithms=[settings.api_token_algorithm])
    except Exception as e:
        print(e)
        raise InvalidTokenException

    refresh_token_object = RefreshToken(**claims)
    
    country, city = get_location_info(ip)
    if country != refresh_token_object.country or city != refresh_token_object.city:
        raise LocationMismatchException

    device, os, browser = get_device_info(user_agent)
    if device != refresh_token_object.device or os != refresh_token_object.os or browser != refresh_token_object.browser:
        raise DeviceMismatchException
    
    return RefreshToken(**claims)