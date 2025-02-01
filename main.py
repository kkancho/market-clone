from fastapi import FastAPI, UploadFile, Form, Response, Depends, Cookie
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated, Optional
import sqlite3
import hashlib
import jwt
import datetime

# Initialize FastAPI
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins; customize in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
con = sqlite3.connect("db.db", check_same_thread=False)
cur = con.cursor()

# Create items table
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        image BLOB,
        price INTEGER NOT NULL,
        description TEXT,
        place TEXT NOT NULL,
        insertAt INTEGER NOT NULL
    ); 
"""
)

# Create users table
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL
    );
"""
)

con.commit()

# Secret keys for JWT
SECRET_ACCESS = "super-coding-access"
SECRET_REFRESH = "super-coding-refresh"
manager = LoginManager(SECRET_ACCESS, '/login')

# Helper function to hash passwords using SHA-256
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# User loader function for FastAPI Login
@manager.user_loader()
def query_user(user_id: str):
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    user = cur.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if user:
        return dict(user)  # Convert sqlite3.Row to dictionary
    return None

# Function to create Refresh Token
def create_refresh_token(user_id: str):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(days=7)
    payload = {
        "sub": user_id,
        "exp": expiration,
    }
    return jwt.encode(payload, SECRET_REFRESH, algorithm="HS256")

# Function to verify Refresh Token
def verify_refresh_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_REFRESH, algorithms=["HS256"])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Login API
@app.post('/login')
def login(id: Annotated[str, Form()], password: Annotated[str, Form()], response: Response):
    user = query_user(id)
    if not user:
        raise InvalidCredentialsException

    hashed_password = hash_password(password)  # Hash the provided password
    if hashed_password != user['password']:
        raise InvalidCredentialsException

    # Generate Access and Refresh Tokens
    access_token = manager.create_access_token(data={'sub': id})
    refresh_token = create_refresh_token(id)

    # Set Refresh Token as HttpOnly cookie
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
    print(f"Generated JWT Tokens: Access Token={access_token}, Refresh Token={refresh_token}")

    return {'access_token': access_token}

# Signup API
@app.post("/signup")
async def signup(
    id: Annotated[str, Form()],
    password: Annotated[str, Form()],
    name: Annotated[str, Form()],
    email: Annotated[str, Form()],
):
    try:
        # Check for duplicate user ID
        cur.execute("SELECT 1 FROM users WHERE id = ?", (id,))
        existing_user = cur.fetchone()

        if existing_user:
            return JSONResponse(
                content={"status": "error", "message": "이미 존재하는 아이디입니다."},
                status_code=400,
            )

        # Hash the password before storing it
        hashed_password = hash_password(password)
        print(f"Signup password (hashed): {hashed_password}")

        # Insert new user into the database
        cur.execute(
            """
            INSERT INTO users (id, name, email, password)
            VALUES (?, ?, ?, ?)
        """,
            (id, name, email, hashed_password),
        )
        con.commit()
        return JSONResponse(
            content={"status": "success", "message": "회원 가입에 성공했습니다."}, 
            status_code=201
        )
    except Exception as e:
        print(f"Signup Error: {str(e)}")
        return JSONResponse(
            content={"status": "error", "message": "회원 가입 중 문제가 발생했습니다."}, 
            status_code=500,
        )

# Refresh Token API
@app.post('/refresh')
def refresh_token(response: Response, refresh_token: Optional[str] = Cookie(None)):
    if not refresh_token:
        return JSONResponse(
            content={"status": "error", "message": "Refresh token이 없습니다."}, 
            status_code=401
        )

    user_id = verify_refresh_token(refresh_token)
    if not user_id:
        return JSONResponse(
            content={"status": "error", "message": "Refresh token이 유효하지 않습니다."}, 
            status_code=401
        )

    # Generate a new Access Token
    access_token = manager.create_access_token(data={'sub': user_id})
    print(f"New Access Token generated: {access_token}")

    return {'access_token': access_token}

# Helper function to get a new database connection
def get_db_connection():
    return sqlite3.connect("db.db", check_same_thread=False)

# API to create an item
@app.post("/items")
async def create_item(
    image: UploadFile,
    title: Annotated[str, Form()],
    price: Annotated[int, Form()],
    description: Annotated[str, Form()],
    place: Annotated[str, Form()],
    insertAt: Annotated[int, Form()],
    user=Depends(manager)
):
    try:
        image_bytes = await image.read()
        con = get_db_connection()
        cur = con.cursor()

        cur.execute(
            """
            INSERT INTO items(title, image, price, description, place, insertAt)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (title, image_bytes.hex(), price, description, place, insertAt),
        )

        con.commit()
        con.close()
        return JSONResponse(content={"status": "success"})
    except Exception as e:
        print(f"Error: {str(e)}")
        return JSONResponse(
            content={"status": "error", "message": str(e)}, status_code=500
        )

# API to retrieve all items
@app.get("/items")
async def get_items(user=Depends(manager)):
    try:
        if not user:
            return JSONResponse(
                content={"status": "error", "message": "User not authenticated"},
                status_code=401,
            )
        print(f"Authenticated user: {user}")
        con = get_db_connection()
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        rows = cur.execute("SELECT * FROM items;").fetchall()
        data = [dict(row) for row in rows]

        cur.close()
        con.close()

        return JSONResponse(content=jsonable_encoder(data))
    except Exception as e:
        print(f"Error during authentication: {str(e)}")
        return JSONResponse(
            content={"status": "error", "message": "Authentication failed"}, status_code=401
        )

# API to retrieve an image by item ID
@app.get("/images/{item_id}")
async def get_image(item_id: int):
    con = get_db_connection()
    cur = con.cursor()

    image_bytes = cur.execute(
        """
        SELECT image FROM items WHERE id = ?
        """,
        (item_id,),
    ).fetchone()
    con.close()

    if image_bytes:
        return Response(content=bytes.fromhex(image_bytes[0]), media_type="image/*")
    return JSONResponse(content={"error": "Image not found"}, status_code=404)

# Mount static files for frontend
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
