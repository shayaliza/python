# from fastapi import FastAPI, Depends, HTTPException, status, Request, Response, Form, Body
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jose import JWTError, jwt
# from passlib.context import CryptContext
# from motor.motor_asyncio import AsyncIOMotorClient
# from pymongo.errors import DuplicateKeyError
# from pydantic import BaseModel, EmailStr, ValidationError
# from datetime import datetime, timedelta
# from bson import ObjectId
# from starlette.middleware.sessions import SessionMiddleware
# from fastapi.middleware.cors import CORSMiddleware
# import logging

# # Add CORS middleware

# # Configuration
# class Settings:
#     MONGO_URI: str = "mongodb+srv://chai:chaiforlife@cluster0.hn1kv1u.mongodb.net/?retryWrites=true&w=majority"
#     SECRET_KEY: str = "your_secret_key"
#     ALGORITHM: str = "HS256"
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

# settings = Settings()

# # Database
# client = AsyncIOMotorClient(settings.MONGO_URI)
# database = client['your_database_name']
# user_collection = database.get_collection('users')

# # Models
# class User(BaseModel):
#     id: str
#     username: str
#     email: EmailStr
#     hashed_password: str

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# class TokenData(BaseModel):
#     username: str

# class UserCreate(BaseModel):
#     username: str
#     email: EmailStr
#     password: str

# class UserLogin(BaseModel):
#     email: EmailStr
#     password: str

# # Utils
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def get_password_hash(password):
#     return pwd_context.hash(password)

# def create_access_token(data: dict, expires_delta: timedelta = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
#     return encoded_jwt

# # Authentication
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# async def get_user(email: str):
#     return await user_collection.find_one({"email": email})

# async def authenticate_user(email: str, password: str):
#     user = await get_user(email)
#     if user and verify_password(password, user["hashed_password"]):
#         return User(id=str(user["_id"]), username=user["username"], email=user["email"], hashed_password=user["hashed_password"])
#     return None

# def user_helper(user) -> dict:
#     return {
#         "id": str(user["_id"]),
#         "username": user["username"],
#         "email": user["email"],
#     }

# # FastAPI app
# app = FastAPI()

# # Add session middleware
# app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins="*",  # Replace with your frontend URL
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PUT", "DELETE"],
#     allow_headers=["*"],
# )

# # Setup logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

# @app.exception_handler(HTTPException)
# async def http_exception_handler(request: Request, exc: HTTPException):
#     logger.error(f"HTTP exception occurred: {exc.detail}")
#     return Response(content=str(exc.detail), status_code=exc.status_code)

# @app.exception_handler(ValidationError)
# async def validation_exception_handler(request: Request, exc: ValidationError):
#     logger.error(f"Validation error occurred: {exc.errors()}")
#     return Response(content=str(exc.errors()), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

# @app.exception_handler(Exception)
# async def general_exception_handler(request: Request, exc: Exception):
#     logger.error(f"An unexpected error occurred: {exc}")
#     return Response(content=str(exc), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @app.post("/auth/register", response_model=Token)
# async def register(user: UserCreate = Body(...)):
#     # logger.debug("Register endpoint called")
#     user_dict = user.dict()
#     # logger.debug(f"User data received: {user_dict}")
#     user_dict["hashed_password"] = get_password_hash(user.password)
#     del user_dict["password"]
#     # logger.debug(f"User data after hashing password: {user_dict}")
#     try:
#         result = await user_collection.insert_one(user_dict)
#         new_user = await user_collection.find_one({"_id": result.inserted_id})
#         access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#         access_token = create_access_token(data={"sub": new_user["email"]}, expires_delta=access_token_expires)
#         return {"access_token": access_token, "token_type": "bearer"}
#     except DuplicateKeyError:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

# @app.post("/auth/login", response_model=Token)
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = await authenticate_user(form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
#     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
#     return {"access_token": access_token, "token_type": "bearer"}

# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise credentials_exception
#         token_data = TokenData(username=email)
#     except JWTError:
#         raise credentials_exception
#     user = await get_user(email=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user

# @app.post("/session/login")
# async def session_login(response: Response, email: str = Form(...), password: str = Form(...)):
#     user = await authenticate_user(email, password)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
#     response.set_cookie(key="user_id", value=str(user.id))
#     response.set_cookie(key="email", value=user.email)
#     return {"message": "Logged in successfully"}

# @app.post("/session/logout")
# async def session_logout(response: Response):
#     response.delete_cookie(key="user_id")
#     response.delete_cookie(key="email")
#     return {"message": "Logged out successfully"}

# @app.get("/session/me")
# async def get_me(request: Request):
#     user_id = request.cookies.get("user_id")
#     email = request.cookies.get("email")
#     if not user_id or not email:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
#     user = await get_user(email=email)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
#     return user_helper(user)

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

# # Run the app
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True , cors = "*")


from fastapi import FastAPI, Depends, HTTPException, status, Request, Response, Form, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError
from pydantic import BaseModel, EmailStr, ValidationError
from datetime import datetime, timedelta
from bson import ObjectId
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configuration
class Settings:
    MONGO_URI: str = "mongodb+srv://chai:chaiforlife@cluster0.hn1kv1u.mongodb.net/?retryWrites=true&w=majority"
    SECRET_KEY: str = "your_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()

# Database
client = AsyncIOMotorClient(settings.MONGO_URI)
database = client['your_database_name']
user_collection = database.get_collection('users')

# Models
class User(BaseModel):
    id: str
    username: str
    email: EmailStr
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Utils
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_user(email: str):
    return await user_collection.find_one({"email": email})

async def authenticate_user(email: str, password: str):
    user = await get_user(email)
    if user and verify_password(password, user["hashed_password"]):
        return User(id=str(user["_id"]), username=user["username"], email=user["email"], hashed_password=user["hashed_password"])
    return None

def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
    }

# FastAPI app
app = FastAPI()

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",  # Replace with your frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP exception occurred: {exc.detail}")
    return Response(content=str(exc.detail), status_code=exc.status_code)

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    logger.error(f"Validation error occurred: {exc.errors()}")
    return Response(content=str(exc.errors()), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"An unexpected error occurred: {exc}")
    return Response(content=str(exc), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.post("/auth/register", response_model=Token)
async def register(user: UserCreate = Body(...)):
    user_dict = user.dict()
    user_dict["hashed_password"] = get_password_hash(user.password)
    del user_dict["password"]
    try:
        result = await user_collection.insert_one(user_dict)
        new_user = await user_collection.find_one({"_id": result.inserted_id})
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": new_user["email"]}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

@app.post("/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(username=email)
    except JWTError:
        raise credentials_exception
    user = await get_user(email=token_data.username)
    if user is None:
        raise credentials_exception
    return user

@app.post("/session/login")
async def session_login(response: Response, email: str = Form(...), password: str = Form(...)):
    user = await authenticate_user(email, password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    response.set_cookie(key="user_id", value=str(user.id))
    response.set_cookie(key="email", value=user.email)
    return {"message": "Logged in successfully"}

@app.post("/session/logout")
async def session_logout(response: Response):
    response.delete_cookie(key="user_id")
    response.delete_cookie(key="email")
    return {"message": "Logged out successfully"}

@app.get("/session/me")
async def get_me(request: Request):
    user_id = request.cookies.get("user_id")
    email = request.cookies.get("email")
    if not user_id or not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    user = await get_user(email=email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user_helper(user)

# @app.get("/auth/verify")
# async def verify_user(token: str = None, email: str = None, request: Request = None):
#     if token:
#         try:
#             payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#             email_from_token = payload.get("sub")
#             if email_from_token is None:
#                 raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
#             user = await get_user(email=email_from_token)
#             if user is None:
#                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
#             return {"message": "User verified successfully with token", "user": user_helper(user)}
#         except JWTError:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
#     elif email:
#         user_id = request.cookies.get("user_id")
#         email_from_cookie = request.cookies.get("email")
#         if user_id and email_from_cookie == email:
#             user = await get_user(email=email_from_cookie)
#             if user is None:
#                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
#             return {"message": "User verified successfully with session", "user": user_helper(user)}
#         else:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session or email")
#     else:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token or email must be provided")

@app.post("/auth/verify")
async def verify_user(data: dict = Body(...)):
    email = data.get("email")
    token = data.get("token")

    if token:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            email_from_token: str = payload.get("sub")
            if email_from_token != email:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
            user = await get_user(email=email)
            if user is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            return {"user": user_helper(user)}
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    else:
        user = await get_user(email=email)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return {"user": user_helper(user)}


@app.get("/")
async def root():
    return {"message": "Hello World"}

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
