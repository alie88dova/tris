import aiosqlite
import asyncio
from data_genratore.test_data import insert_test_data

#таблица для вайтлиста
async def create_users():
    async with aiosqlite.connect("database.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE
            )
        """)
        await db.commit()
#таблица данных по квартире
async def create_apartment():
    async with aiosqlite.connect("database.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS apartment (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                creator_id INTEGER, 
                apartment_number TEXT,
                address TEXT,
                time_create DATETIME DEFAULT current_timestamp,
                last_update DATETIME DEFAULT current_timestamp,
                status TEXT,
                FOREIGN KEY(creator_id) REFERENCES users(id)
            )
        """)
        await db.commit()
#таблица данных по комнатам
async def create_rooms():
    async with aiosqlite.connect("database.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                apartment_id INTEGER,
                room_number INTEGER,
                time_create DATETIME DEFAULT current_timestamp,
                creator_id INTEGER,
                FOREIGN KEY(apartment_id) REFERENCES apartment(id), 
                FOREIGN KEY(creator_id) REFERENCES users(id)
            )
        """)
        await db.commit()
#Таблица по вопросам
async def create_question():
    async with aiosqlite.connect("database.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS question (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_text TEXT,
                answers TEXT,
                tags TEXT
            )
        """)
        await db.commit()

#Связанная таблица
async def create_answers():
    async with aiosqlite.connect("database.db") as db:
        await db.execute("""
             CREATE TABLE IF NOT EXISTS answers (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 room_id INTEGER,
                 question_id INTEGER, 
                 answer INTEGER,
                 data TEXT NULL,
                 FOREIGN KEY(room_id) REFERENCES rooms(id),
                 FOREIGN KEY(question_id) REFERENCES question(id)
             )
         """)
        await db.commit()


if __name__ == '__main__':
    db_path = 'database.db'
    asyncio.run(insert_test_data(db_path))