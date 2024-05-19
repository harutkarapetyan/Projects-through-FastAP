import datetime

from fastapi import Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordBearer

from passlib.context import CryptContext
from jose import jwt, JWTError

import main

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2schema = OAuth2PasswordBearer("auth/login")

ACCESS_TOKEN_MINUTES = 60
ACCESS_TOKEN_ALGORITHM = "HS256"
SECRET_KEY = "096533d29cd2502272a3a8a2c2405d1c670ee697fb85dea5268516271367eab3"


def hash_password(plain_password: str):
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_token(user_data: dict):
    user_data_copy = user_data.copy()
    user_data_copy.update({"exp": datetime.datetime.utcnow() + datetime.timedelta(ACCESS_TOKEN_MINUTES)})
    token = jwt.encode(user_data_copy, SECRET_KEY, ACCESS_TOKEN_ALGORITHM)
    return token


def verify_token(token):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ACCESS_TOKEN_ALGORITHM])

    if payload.get("user_id") is None:
        raise JWTError

    return payload


def get_current_user(token=Depends(oauth2schema)):
    payload = verify_token(token)
    user_id = payload.get("user_id")
    main.cursor.execute("""SELECT * FROM users WHERE user_id = %s""",
                        (user_id,))

    user_data = main.cursor.fetchone()

    if user_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"Message": "Your data not found"})

    return user_data
