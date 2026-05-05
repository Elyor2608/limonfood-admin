import psycopg2
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

async def create_pool():
    pass

async def get_staff(telegram_id):
    loop = asyncio.get_event_loop()
    def _get():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM staff WHERE telegram_id = %s", (telegram_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return row
    return await loop.run_in_executor(None, _get)

async def add_staff(telegram_id, ism, telefon, rol):
    loop = asyncio.get_event_loop()
    def _add():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS staff (
                id SERIAL PRIMARY KEY,
                telegram_id BIGINT UNIQUE NOT NULL,
                ism TEXT,
                telefon TEXT,
                rol TEXT,
                tasdiqlangan BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)
        cur.execute(
            "INSERT INTO staff (telegram_id, ism, telefon, rol) VALUES (%s, %s, %s, %s) ON CONFLICT (telegram_id) DO NOTHING",
            (telegram_id, ism, telefon, rol)
        )
        conn.commit()
        cur.close()
        conn.close()
    return await loop.run_in_executor(None, _add)
