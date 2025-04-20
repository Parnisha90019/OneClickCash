import aiosqlite

class DataBase:
    con = None

    @classmethod
    async def on_startup(cls):
        cls.con = await aiosqlite.connect("database/user.db")
        await cls.con.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                user_id_1win INTEGER,
                verifed TEXT DEFAULT "0",
                deposited TEXT DEFAULT "0"
            )
        """)
        await cls.con.commit()

    @classmethod
    async def register(cls, user_id: int, verifed: str):
        await cls.con.execute("INSERT OR IGNORE INTO users (user_id, verifed) VALUES (?, ?)", (user_id, verifed))
        await cls.con.commit()

    @classmethod
    async def get_user(cls, user_id: int):
        cursor = await cls.con.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        return await cursor.fetchone()

    @classmethod
    async def update_user_id_1win(cls, user_id: int, user_id_1win: int):
        await cls.con.execute("UPDATE users SET user_id_1win = ? WHERE user_id = ?", (user_id_1win, user_id))
        await cls.con.commit()

    @classmethod
    async def update_verifed(cls, user_id: int):
        await cls.con.execute("UPDATE users SET verifed = ? WHERE user_id = ?", ("verifed", user_id))
        await cls.con.commit()

    @classmethod
    async def update_deposited(cls, user_id: int):
        await cls.con.execute("UPDATE users SET deposited = ? WHERE user_id = ?", ("deposited", user_id))
        await cls.con.commit()

    @classmethod
    async def has_deposited(cls, user_id: int):
        cursor = await cls.con.execute("SELECT deposited FROM users WHERE user_id = ?", (user_id,))
        result = await cursor.fetchone()
        return result[0] == "deposited" if result else False