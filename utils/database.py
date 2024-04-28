import  sqlite3

class Database():
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_db()


    def create_db(self):
        try:
            query = ("CREATE TABLE IF NOT EXISTS users("
                     "id INTEGER PRIMARY KEY,"
                     "user_name TEXT,"
                     "user_phone TEXT,"
                     "user_geo FLOAT,"
                     "telegram_id TEXT);")
            self.cursor.execute(query)
            self.connection.commit()
        except sqlite3.Error as Error:
            print("Ошибка при создании:", Error)

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
            self.cursor.execute("SELECT user_name, user_geo FROM users")
            result = self.cursor.fetchall() #тестово извлекаем все координаты всех пользователей
            return result
        except sqlite3.Error as Error:
            print("Ошибка при выполнении запроса:", Error)

    def update_user_geo(self, user_id, new_geo):
        try:
            query = "UPDATE users SET user_geo = ? WHERE telegram_id = ?"
            self.cursor.execute(query, (new_geo, user_id))
            self.connection.commit()
        except sqlite3.Error as error:
            print("Ошибка при обновлении данных геопозиции:", error)
    def __del__(self): #закрытие соединения
        self.cursor.close()
        self.connection.close()