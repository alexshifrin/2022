from datetime import datetime, timedelta

from jose import JWTError, jwt


# openssl rand -hex 32
SECRET_KEY = "9a3ec03db7789f636327c2af28f25adb1507c78db74e8b4f718ca4757b94416d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expiration = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expiration})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
