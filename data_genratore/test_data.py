import aiosqlite
from faker import Faker
import asyncio
import random

fake = Faker()

async def insert_test_data(db_path):
    async with aiosqlite.connect(db_path) as db:
        # Генерация тестовых данных для таблицы users
        for _ in range(20):
            await db.execute("INSERT INTO users (user_id) VALUES (?)", (fake.unique.random_int(min=1000, max=9999),))
        await db.commit()

        # Получаем все user_id из таблицы users
        cursor = await db.execute("SELECT id FROM users")
        user_ids = [row[0] for row in await cursor.fetchall()]

        # Генерация тестовых данных для таблицы apartment
        for _ in range(20):
            creator_id = random.choice(user_ids)
            apartment_number = fake.building_number()
            address = fake.address()
            status = random.choice(['active', 'inactive', 'pending'])
            await db.execute("""
                INSERT INTO apartment (creator_id, apartment_number, address, status)
                VALUES (?, ?, ?, ?)
            """, (creator_id, apartment_number, address, status))
        await db.commit()

        # Получаем все apartment_id из таблицы apartment
        cursor = await db.execute("SELECT id FROM apartment")
        apartment_ids = [row[0] for row in await cursor.fetchall()]

        # Генерация тестовых данных для таблицы rooms
        for _ in range(20):
            apartment_id = random.choice(apartment_ids)
            room_number = fake.random_int(min=1, max=10)
            creator_id = random.choice(user_ids)
            await db.execute("""
                INSERT INTO rooms (apartment_id, room_number, creator_id)
                VALUES (?, ?, ?)
            """, (apartment_id, room_number, creator_id))
        await db.commit()

        # Получаем все room_id из таблицы rooms
        cursor = await db.execute("SELECT id FROM rooms")
        room_ids = [row[0] for row in await cursor.fetchall()]

        # Генерация тестовых данных для таблицы question
        questions = [
            ("Качество уборки", "1-5", "cleanliness"),
            ("Качество обслуживания", "1-5", "service"),
            ("Удобство расположения", "1-5", "location"),
            ("Состояние мебели", "1-5", "furniture"),
            ("Шумоизоляция", "1-5", "noise"),
        ]
        for question_text, answers, tags in questions:
            await db.execute("""
                INSERT INTO question (question_text, answers, tags)
                VALUES (?, ?, ?)
            """, (question_text, answers, tags))
        await db.commit()

        # Получаем все question_id из таблицы question
        cursor = await db.execute("SELECT id FROM question")
        question_ids = [row[0] for row in await cursor.fetchall()]

        # Генерация тестовых данных для таблицы answers
        for _ in range(20):
            room_id = random.choice(room_ids)
            question_id = random.choice(question_ids)
            answer = fake.random_int(min=1, max=5)
            data = fake.sentence()
            await db.execute("""
                INSERT INTO answers (room_id, question_id, answer, data)
                VALUES (?, ?, ?, ?)
            """, (room_id, question_id, answer, data))
        await db.commit()


async def main():
    await insert_test_data()


if __name__ == "__main__":
    asyncio.run(main())