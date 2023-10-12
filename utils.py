import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import  HTTPException, Depends
from models import (User,Company,Employee)
import secrets
import pytz 

ALGORITHM = "HS256"
#JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']   
#JWT_REFRESH_SECRET_KEY = os.environ['JWT_REFRESH_SECRET_KEY']   
JWT_SECRET_KEY = "43a14013532d31991d9fa29eefc9ec77b0699cf60dc3519bee55efe19e1237c8"
JWT_REFRESH_SECRET_KEY = "82b2102edfb4b0759d884f00163f9bee4a7c6fbb41f5377089bd8a74bc71158c"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context  = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return  pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=400, detail="Could not validate credentials")
        
        user = get_user(username)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        # Check if the token is expired
        expiration_timestamp = payload.get("exp")
        if expiration_timestamp is None:
            raise HTTPException(status_code=400, detail="Token has no expiration time")
        
        current_time = datetime.now(pytz.utc)
        if current_time > datetime.fromtimestamp(expiration_timestamp, tz=pytz.utc):
            raise HTTPException(status_code=400, detail="Token has expired")
        
        return user
    except JWTError:
        raise HTTPException(status_code=400, detail="Could not validate credentials")
    
async def get_user(username: str):
    user = await User.get(email=username)
    return user

def hash_password(password):
    return pwd_context.hash(password)

def generate_random_name():
    random_string = secrets.token_hex(10)
    return random_string