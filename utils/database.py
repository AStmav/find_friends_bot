import  sqlite3

class Database():
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_db()

    def create_db(self):
        try:
            query_users = ("CREATE TABLE IF NOT EXISTS users("
                           "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                           "user_name TEXT,"
                           "user_phone TEXT,"
                           "user_geo FLOAT,"
                           "telegram_id TEXT UNIQUE);")  # Добавил UNIQUE для telegram_id

            query_chats = ("CREATE TABLE IF NOT EXISTS chats("
                           "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                           "your_id INTEGER NOT NULL,"
                           "user_id INTEGER NOT NULL,"
                           "UNIQUE(your_id, user_id));")

            self.cursor.execute(query_users)
            self.cursor.execute(query_chats)
            self.connection.commit()
        except sqlite3.Error as error:
            print("Ошибка при создании таблицы:", error)



    def add_user (self, user_name, user_phone, user_geo, telegram_id):
        self.cursor.execute("INSERT INTO users (user_name, user_phone, user_geo, telegram_id) VALUES (?, ?, ?, ?)", (user_name, user_phone, user_geo, telegram_id))
        self.connection.commit()

    def select_users_id(self,telegram_id):
        users = self.cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
        return users.fetchone() #возвращаем данные о пользователе

    def select_place_user(self, telegram_id):
        user = self.cursor.execute("SELECT user_geo FROM users WHERE telegram_id = ?", (telegram_id,))
        return user.fetchone() #возвразаем координаты пользователя


    def select_places_all(self):
        try:
            self.cursor.execute("SELECT user_name, user_geo, telegram_id FROM users")
            result = self.cursor.fetchall() #тестово извлекаем все координаты всех пользователей
            return result
        except sqlite3.Error as Error:
            print("Ошибка при выполнении запроса:", Error)

    def update_user_geo(self, user_id, new_geo):
        try:
            query = "UPDATE users SET user_geo = ? WHERE telegram_id = ?"
            self.cursor.execute(query, (new_geo, user_id))#обновляем актульную геопозицию пользователя
            self.connection.commit()
        except sqlite3.Error as error:
            print("Ошибка при обновлении данных геопозиции:", error)


    def save_user_id_chat(self, your_id: int, user_id: int):
        try:
            # Удаление дублирующихся записей, если они существуют
            self.cursor.execute(
                "DELETE FROM chats WHERE (your_id = ? AND user_id = ?) OR (your_id = ? AND user_id = ?)",
                (your_id, user_id, user_id, your_id))
            # Добавление новой записи
            self.cursor.execute("INSERT INTO chats (your_id, user_id) VALUES (?, ?)",
                                (your_id, user_id))
            self.connection.commit()
        except sqlite3.Error as error:
            print("Ошибка при сохранении ID пользователей:", error)

    def get_chat_users(self, user_id: int):
        try:
            query = "SELECT your_id, user_id FROM chats WHERE your_id = ? OR user_id = ?"
            self.cursor.execute(query, (user_id, user_id))
            return self.cursor.fetchone()
        except sqlite3.Error as error:
            print("Ошибка при получении пользователей чата:", error)
            return None

    def end_chat(self, user_id: int):
        try:
            # Удаление записи чата, если она существует
            self.cursor.execute("DELETE FROM chats WHERE your_id = ? OR user_id = ?", (user_id, user_id))
            self.connection.commit()
        except sqlite3.Error as error:
            print("Ошибка при завершении чата:", error)


    def __del__(self): #закрытие соединения
        self.cursor.close()
        self.connection.close()



