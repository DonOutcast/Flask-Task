import random
import sqlite3

from logger import logger


class Database:
    def __init__(self, database_file: str) -> None:
        self.database_file = database_file

    @property
    def connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.database_file)

    def execute(
            self,
            query: str,
            parameters: tuple = None,
            fetchone=False,
            fetchall=False,
            commit=False,
            many=False,
    ) -> tuple | None:
        data = None
        connection = None
        try:
            connection = self.connection
            parameters = parameters or ()
            cursor = connection.cursor()
            if many:
                cursor.executemany(query, parameters)
            else:
                cursor.execute(query, parameters)
            if commit:
                connection.commit()
            if fetchone:
                data = cursor.fetchone()
            if fetchall:
                data = cursor.fetchall()
        except sqlite3.Error as error:
            logger.error(f"Ошибка при подключении к Sqlite {error}")
        finally:
            connection.close()
            logger.info("Соединение с Sqlite закрыто")
        return data

    def _create_table_users(self):
        query = """
            CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY, username TEXT, balance INTEGER)
        """
        self.execute(query=query, commit=True)
        logger.info("Таблица users сделана")

    def _generate_random_users(self):

        for i in range(1, 6):
            username = f"user_{i}"
            balance = random.randint(5000, 15000)
            yield (username, balance)

    def init_db(self):
        self._create_table_users()
        query = """INSERT INTO users (username, balance) VALUES (?, ?)"""
        self.execute(query=query, parameters=self._generate_random_users(), commit=True, many=True)


database = Database("app.db")
database.init_db()
