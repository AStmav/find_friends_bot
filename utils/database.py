import  sqlite3

class Database():
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_db()
        self.create_chats_table()
        self.create_messages_table()
        self.create_active_chats_table()

    def create_db(self):
        try:
            query_users = ("CREATE TABLE IF NOT EXISTS users("
                           "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                           "user_name TEXT,"
                           "user_age INTEGER,"
                           "user_gender TEXT,"
                           "user_geo TEXT,"
                           "telegram_id TEXT,"
                           "UNIQUE(telegram_id));")
            self.cursor.execute(query_users)
            self.connection.commit()
        except sqlite3.Error as error:
            print("Ошибка при создании таблицы users:", error)

    def create_chats_table(self):
        try:
            query_chats = ("CREATE TABLE IF NOT EXISTS chats("
                           "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                           "your_id INTEGER NOT NULL,"
                           "user_id INTEGER NOT NULL,"
                           "is_active BOOLEAN DEFAULT 1,"
                           "UNIQUE(your_id, user_id),"
                           "FOREIGN KEY (your_id) REFERENCES users(id),"
                           "FOREIGN KEY (user_id) REFERENCES users(id));")
            self.cursor.execute(query_chats)
            self.connection.commit()
        except sqlite3.Error as error:
            print("Ошибка при создании таблицы chats:", error)


    def create_messages_table(self):
        try:
            query_messages = ("CREATE TABLE IF NOT EXISTS messages("
                              "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                              "chat_id INTEGER NOT NULL,"
                              "sender_id INTEGER NOT NULL,"
                              "text TEXT NOT NULL,"
                              "timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,"
                              "FOREIGN KEY (chat_id) REFERENCES chats(id),"
                              "FOREIGN KEY (sender_id) REFERENCES users(id));")
            self.cursor.execute(query_messages)
            self.connection.commit()
        except sqlite3.Error as error:
            print("Ошибка при создании таблицы messages:", error)

    def create_active_chats_table(self):
        try:
            query_active_chats = ("CREATE TABLE IF NOT EXISTS active_chats("
                                  "user_id INTEGER PRIMARY KEY,"
                                  "chat_id INTEGER NOT NULL,"
                                  "FOREIGN KEY (user_id) REFERENCES users(id),"
                                  "FOREIGN KEY (chat_id) REFERENCES chats(id));")
            self.cursor.execute(query_active_chats)
            self.connection.commit()
        except sqlite3.Error as error:
            print("Ошибка при создании таблицы active_chats:", error)

    def add_user(self, user_name, user_age, user_gender, user_geo, telegram_id):
        try:
            self.cursor.execute(
                "INSERT INTO users (user_name, user_age, user_gender, user_geo, telegram_id) VALUES (?, ?, ?, ?, ?)",
                (user_name, user_age, user_gender, user_geo, telegram_id)
            )
            self.connection.commit()
        except sqlite3.Error as error:
            print("Ошибка при добавлении пользователя:", error)

    def select_users_id(self,telegram_id):
        users = self.cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
        return users.fetchone() #возвращаем данные о пользователе

    def select_place_user(self, telegram_id):
        user = self.cursor.execute("SELECT user_geo FROM users WHERE telegram_id = ?", (telegram_id,))
        return user.fetchone() #возвразаем координаты пользователя


    def select_places_all(self):
        try:
            self.cursor.execute("SELECT user_name, user_geo, telegram_id, user_gender, user_age FROM users")
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

        with self.connection:
            self.cursor.execute(
                "INSERT INTO chats (your_id, user_id) VALUES (?, ?)",
                (your_id, user_id)
            )


    def get_chat_users(self, user_id:int):
        #получаем пользователей чата из бд
        with self.connection:
            self.cursor.execute(
                "SELECT your_id, user_id FROM chats WHERE your_id = ? OR user_id = ?",
                (user_id, user_id)
            )
            return self.cursor.fetchone()

    def check_existing_chat(self, your_id, user_id):
        #проверяем существует ли этот чат
        try:
            self.cursor.execute("SELECT 1 FROM chats WHERE your_id = ? AND user_id = ?", (your_id, user_id))
            return self.cursor.fetchone() is not None
        except sqlite3.Error as error:
            print("Ошибка при проверке существующего чата:", error)
            return False

    def get_user_name(self,user_id):
        try:
            with self.connection:
                self.cursor.execute(
                    "SELECT user_name FROM users WHERE telegram_id=?",
                    (user_id,)
                )
                result = self.cursor.fetchone()
                return result[0] if result else "Неизвестный пользователь"
        except sqlite3.Error as error:
            print("Ошибка при получении имени пользователя:", error)
            return "Неизвестный пользователь"

    def get_user_chats(self,user_id:int):
        #получаем все чаты пользователя
        with self.connection:
            self.cursor.execute(
                "SELECT user_id FROM chats WHERE your_id = ?",
                (user_id,)
            )
            chat_user_ids = self.cursor.fetchall()  # Возвращает список кортежей с user_id
            # Получаем имена пользователей для каждого user_id
            user_chats = []
            for chat in chat_user_ids:
                user_id = chat[0]
                user_name = self.get_user_name(user_id)
                user_chats.append((user_id, user_name))
            return user_chats

#########################################
    def set_active_chat(self, user_id, chat_id):
        try:
            self.cursor.execute("INSERT OR REPLACE INTO active_chats (user_id, chat_id) VALUES (?, ?)",
                                (user_id, chat_id))
            self.connection.commit()
        except sqlite3.Error as error:
            print("Ошибка при установке активного чата:", error)

    def get_active_chats(self, user_id):
        try:
            self.cursor.execute("""
                SELECT c.id, u.user_name
                FROM chats c
                JOIN users u ON c.user_id = u.telegram_id
                WHERE c.your_id = ? AND c.is_active = 1
            """, (user_id,))
            results = self.cursor.fetchall()
            #return [{'chat_id': row[0], 'user_name': row[1]} for row in results]
            return [{'chat_id': row[0], 'user_name': row[1]} for row in results]
        except sqlite3.Error as error:
            print("Ошибка при получении активных чатов:", error)
            return []

    def save_message(self, chat_id, sender_id, message):
        query = """
          INSERT INTO messages (chat_id, sender_id, text)
          VALUES (?, ?, ?);
          """
        self.cursor.execute(query, (chat_id, sender_id, message))
        self.connection.commit()

    def get_chat_id(self, your_id, user_id):
        query = """
        SELECT id FROM chats WHERE your_id = ? AND user_id = ?;
        """
        self.cursor.execute(query, (your_id, user_id))
        result = self.cursor.fetchone()
        return result[0] if result else None

    async def get_chat_messages(self, chat_id):
        try:
            query = """
            SELECT message FROM messages WHERE chat_id = ? ORDER BY timestamp ASC;
            """
            self.cursor.execute(query, (chat_id,))
            results = self.cursor.fetchall()
            return [{'text': row[0]} for row in results]
        except sqlite3.Error as error:
            print("Ошибка при получении сообщений чата:", error)
            return []

    def send_message_to_chat(self, from_user_id, chat_id, message):
        try:
            self.cursor.execute("""
                INSERT INTO messages (chat_id, sender_id, text)
                VALUES (?, ?, ?)
            """, (chat_id, from_user_id, message))
            self.connection.commit()
        except sqlite3.Error as error:
            print("Ошибка при отправке сообщения в чат:", error)

    def delete_chat_from_db(self, user1_id, user2_id):
        try:
            query = """
                       DELETE FROM chats
                       WHERE (your_id = ? AND user_id = ?)
                          OR (your_id = ? AND user_id = ?)
                   """
            self.cursor.execute(query, (user1_id, user2_id, user2_id, user1_id))
            self.connection.commit()
        except sqlite3.Error as error:
            print("Ошибка при удалении чата:", error)

    def get_chat_users(self, user_id):
        try:
            self.cursor.execute("""
                SELECT your_id, user_id
                FROM chats
                WHERE (your_id = ? OR user_id = ?) AND is_active = 1
            """, (user_id, user_id))
            return self.cursor.fetchone()
        except sqlite3.Error as error:
            print("Ошибка при получении пользователей чата:", error)
            return None

    def get_chat_users_by_chat_id(self, chat_id):
        try:
            query = "SELECT your_id, user_id FROM chats WHERE id = ?"
            self.cursor.execute(query, (chat_id,))
            result = self.cursor.fetchone()
            if result:
                return result
            return None
        except sqlite3.Error as error:
            print("Ошибка при получении пользователей чата:", error)
            return None

    def __del__(self): #закрытие соединения
        self.cursor.close()
        self.connection.close()



