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
        self.cursor.execute(f"INSERT INTO users (user_name, user_phone, user_geo, telegram_id) VALUES (?, ?, ?, ?)", (user_name, user_phone, user_geo, telegram_id))
        self.connection.commit()

    def select_users_id(self,telegram_id):
        users = self.cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
        return  users.fetchone() #возвращаем данные о пользователе

    def __del__(self): #закрытие соединения
        self.cursor.close()
        self.connection.close()