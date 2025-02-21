from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

GOOGLE_CLIENT_ID = "google_client_id"
GOOGLE_CLIENT_SECRET = "google_client_secret"
GOOGLE_REDIRECT_URI = "http://localhost:8001/auth/google/callback"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_google_access_token(code: str):
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": GOOGLE_REDIRECT_URI
    }
    response = requests.post(token_url, data=data)
    return response.json()

def get_google_user_info(access_token: str):
    user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(user_info_url, headers=headers)
    return response.json()