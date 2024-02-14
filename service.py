from database import Database
from logger import logger


class User:

    def __init__(
        self, database: Database, user_id: int = None, username: str = None, balance: int = None
    ):
        self.database = database
        self.id = user_id
        self.username = username
        self.balance = balance

    def add_user(self):
        query = "INSERT INTO users (username, balance) VALUES (?, ?)"
        parameters = (self.username, self.balance)
        self.database.execute(query=query, parameters=parameters, commit=True)
        logger.info(f"Пользователь {self.username} добавлен.")

    def update_balance(self, new_balance: int):
        query = "UPDATE users SET balance = ? WHERE id = ?"
        parameters = (new_balance, self.id)
        self.database.execute(query=query, parameters=parameters, commit=True)
        logger.info(f"Баланс пользователя {self.username} обновлен.")

    def delete_user(self):
        query = "DELETE FROM users WHERE id = ?"
        parameters = (self.id,)
        self.database.execute(query=query, parameters=parameters, commit=True)
        logger.info(f"Пользователь {self.username} удален.")

    @classmethod
    def fetch_user(cls, database, user_id: int):
        query = "SELECT id, username, balance FROM users WHERE id = ?"
        parameters = (user_id,)
        data = database.execute(query=query, parameters=parameters, fetchone=True)
        if data:
            return cls(database, user_id=data[0], username=data[1], balance=data[2])
        else:
            logger.info("Пользователь не найден.")
            return None
