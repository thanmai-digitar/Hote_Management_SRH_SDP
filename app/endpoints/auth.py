from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
import jwt
from ..crud.crud import MySQLCRUD
from passlib.context import CryptContext
from datetime import datetime, timedelta

router = APIRouter()
db = MySQLCRUD('host', 'user', 'password', 'database')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # Token expires in 15 minutes
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Use form_data.username as the email
    user = db.read('customers', conditions=f"WHERE email = '{form_data.username}'")
    print(user[0][4])
    if not user or not pwd_context.verify(form_data.password, user[0][5]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user[0][3]})
    customerid= user[0][4]  # Assuming user[0][3] 
    return {"customerid":customerid,"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        # You can add more user verification logic here (e.g., check if user exists in DB)
    except JWTError:
        raise credentials_exception
    return email

@router.get('/details')
async def get_user_details(current_user: str = Depends(get_current_user)):
    user = db.read('customers', conditions=f"WHERE email = '{current_user}'")
    if not user or len(user) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    # Ensure that the index used here matches the position of customer_id in your database schema
    return {"customer_id": user[0][0]}


@router.post("/admin/login")
async def admin_login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Authenticate against the admin table
    try:
        admin_user = db.read('admin', conditions=f"WHERE email = '{form_data.username}'")
        if not admin_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Admin not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not pwd_context.verify(form_data.password, admin_user[0][4]):  # Assuming password is the second element
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(data={"sub": admin_user[0][3]})  # Assuming email is the first element
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        # Log the exception for debugging
        print(f"Error during admin login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )