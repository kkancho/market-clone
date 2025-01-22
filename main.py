from fastapi import FastAPI, UploadFile, Form, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from typing import Annotated
import sqlite3

con = sqlite3.connect('db.db', check_same_thread=False)
cur = con.cursor()

cur.execute(f"""
            CREATE TABLE IF NOT EXISTS items (
	            id INTEGER PRIMARY KEY,
	            title TEXT NOT NULL,
	            image BLOB,
	            price INTEGER NOT NULL,
	            description TEXT,
	            place TEXT NOT NULL,
	            insertAt INTEGER NOT NULL
            ); 

            """)

# Database connection
# con = sqlite3.connect("./market-clone/db.db")
# cur = con.cursor()

# Initialize FastAPI
app = FastAPI()

def get_db_connection():
    return sqlite3.connect("./market-clone/db.db")

@app.post('/items')
async def create_item(
    image: UploadFile,
    title: Annotated[str, Form()],
    price: Annotated[int, Form()],
    description: Annotated[str, Form()],
    place: Annotated[str, Form()],
    insertAt: Annotated[int, Form()]
):
    
    image_bytes = await image.read()
    
    con = get_db_connection()
    cur = con.cursor()
    
    cur.execute("""
        INSERT INTO items(title, image, price, description, place, insertAt)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (title, image_bytes.hex(), price, description, place, insertAt))

    con.commit()
    con.close()
    
    return JSONResponse(content={"status": "success"})

@app.get('/items')
async def get_items():
    con = get_db_connection()
    cur.row_factory = sqlite3.Row
    cur = con.cursor()
    
    rows = cur.execute("SELECT * FROM items;").fetchall()
    con.close()
    
    data = [dict(row) for row in rows]
    return JSONResponse(content=jsonable_encoder(data))

@app.get('/images/{item_id}')
async def get_image(item_id: int):
    con = get_db_connection()
    cur = con.cursor()
    
    image_bytes = cur.execute("""
                            SELECT image from items WHERE id = ?
                            """, (item_id,)).fetchone()
    con.close()
        
    if image_bytes:
        return Response(content=bytes.fromhex(image_bytes[0]), media_type='image/*')
    return JSONResponse(content={"error": "Image not found"}, status_code=404)

# Mount static files for frontend
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")