import sqlite3

class DataBase:
	def __init__(self) -> None:
		self.__conn = sqlite3.connect("data.db", check_same_thread=False) 
		self.__cursor = self.__conn.cursor()

		self.__initUsers()
		self.__initNews()

	def __initUsers(self) -> None:
		self.__cursor.execute("""
			CREATE TABLE IF NOT EXISTS users (
				IdName INTEGER
			)""")

	def __initNews(self) -> None:
		self.__cursor.execute("""
		CREATE TABLE IF NOT EXISTS news (
			AuthorID INTEGER, 			
			Content TEXT
		)""")

	def add_user(self, user: int) -> None:
		self.__cursor.execute(f"INSERT INTO users VALUES ({user})", )
		self.__conn.commit()

	def del_user(self, user: int) -> None:		
		self.__cursor.execute(f"DELETE FROM users WHERE IdName = {user}")
		self.__conn.commit()

	def add_news(self, news: list) -> None:
		self.__cursor.executemany("INSERT INTO news VALUES (?,?)", news)
		self.__conn.commit()
		
	def return_users(self) -> list:
		self.__cursor.execute("SELECT * FROM users")
		return self.__cursor.fetchall()

	def return_news(self) -> list:
		self.__cursor.execute("SELECT * FROM news")
		return self.__cursor.fetchall()

	def return_number_news(self) -> int:
		self.__cursor.execute("SELECT * FROM news")
		return len(self.__cursor.fetchall())
 
if __name__ == '__main__':
	db = DataBase()
	print(db.return_number_news())