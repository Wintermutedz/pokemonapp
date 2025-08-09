
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import pytesseract
from PIL import Image
import io
import sqlite3
import requests
import os

API_KEY = os.getenv("POKEMON_API_KEY", "")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conn = sqlite3.connect("collection.db")
conn.execute("""CREATE TABLE IF NOT EXISTS collection (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    tcgplayer_id TEXT,
    image_url TEXT,
    rarity TEXT,
    market_price REAL
)""")
conn.commit()

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    image = Image.open(io.BytesIO(await file.read()))
    text = pytesseract.image_to_string(image)
    return {"text": text}

@app.get("/search")
def search_card(name: str):
    if not API_KEY:
        return {"error": "API key not set"}
    response = requests.get(
        f"https://api.pokemontcg.io/v2/cards?q=name:{name}",
        headers={"X-Api-Key": API_KEY}
    )
    return response.json()

@app.post("/collection")
def add_to_collection(
    name: str = Form(...),
    tcgplayer_id: str = Form(...),
    image_url: str = Form(...),
    rarity: str = Form(...),
    market_price: float = Form(...),
):
    conn.execute(
        "INSERT INTO collection (name, tcgplayer_id, image_url, rarity, market_price) VALUES (?, ?, ?, ?, ?)",
        (name, tcgplayer_id, image_url, rarity, market_price)
    )
    conn.commit()
    return {"message": "Card added to collection."}

@app.get("/collection")
def get_collection():
    cur = conn.cursor()
    cur.execute("SELECT * FROM collection")
    rows = cur.fetchall()
    return {"cards": rows}
