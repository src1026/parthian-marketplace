from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from auth import hash_password, verify_password, create_access_token
from mail_config import send_verification_email
from pydantic import BaseModel
import uuid
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

class RegisterRequest(BaseModel):
    email: str
    full_name: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/register")
async def register_user(user: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)
    verification_token = str(uuid.uuid4())

    new_user = User(
        email=user.email,
        full_name=user.full_name,
        provider="local",
        provider_id=user.email,
        password_hash=hashed_password,
        is_verified=False,
        verification_token=verification_token
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    await send_verification_email(user.email, verification_token)

    return {"message": "User registered successfully. Please verify your email."}


@router.get("/auth/verify")
def verify_email(token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.verification_token == token).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user.is_verified = True
    user.verification_token = None
    db.commit()

    return {"message": "Email verified successfully!"}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified. Please verify your email before logging in.")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/auth/google")
def google_login():
    return {"url": f"https://accounts.google.com/o/oauth2/auth?client_id={GOOGLE_CLIENT_ID}&response_type=code&scope=email profile&redirect_uri={GOOGLE_REDIRECT_URI}"}

@router.get("/auth/google/callback")
def google_callback(code: str, db: Session = Depends(get_db)):
    token_data = get_google_access_token(code)
    if "access_token" not in token_data:
        raise HTTPException(status_code=400, detail="Failed to get access token")

    user_info = get_google_user_info(token_data["access_token"])
    email = user_info["email"]
    provider_id = user_info["id"]

    user = db.query(User).filter(User.provider == "google", User.provider_id == provider_id).first()
    if not user:
        user = User(email=email, full_name=user_info.get("name"), provider="google", provider_id=provider_id)
        db.add(user)
        db.commit()

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

"""
class CartItemRequest(BaseModel):
    battery_id: str
    quantity: int = 1

@router.post("/cart", response_model=dict)
def add_to_cart(
    item: CartItemRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cart_item = db.query(CartItem).filter(
        CartItem.user_id == current_user.id,
        CartItem.battery_id == item.battery_id
    ).first()
    if cart_item:
        cart_item.quantity += item.quantity
    else:
        cart_item = CartItem(
            user_id=current_user.id,
            battery_id=item.battery_id,
            quantity=item.quantity
        )
        db.add(cart_item)
    db.commit()
    return {"success": True, "message": "Battery added to cart!"}

@router.get("/cart", response_model=list)
def get_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cart_items = db.query(CartItem).filter(CartItem.user_id == current_user.id).all()
    return cart_items
"""