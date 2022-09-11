from __future__ import annotations
import sqlite3
import psycopg2

class Banana:

	__banana_connection = None

	# Show that started ok
	def __init__(self) -> None:
		print("Banana initialized")

	# Start the connection
	def connect(self, host : str, database : str, username : str, password : str) -> __BananaConnection:
		try:
			conn = psycopg2.connect(host=host, dbname=database, user=username, password=password)
			self.__banana_connection = self.__BananaConnection(self,conn)
			print("Connected successfully!")
			del conn
		except Exception as e:
			print("ERROR. Can't connect to the database")
			print(e)
		finally:
			return self.__banana_connection

	# Finish the connection
	def disconnect(self) -> Banana:
		if self.__banana_connection == None:
			print("Already disconnected")
		else:
			try:
				self.__banana_connection.close()
				print("Connection closed")
				__banana_connection = None
			except Exception as e:
				print("ERROR. Can't close connection")
				print(e)
				return None
		return self

	class __BananaConnection:

		__database_connection = None
		__database_cursor = None

		__operation_type = ""
		__select = []
		__where = []

		table = ""

		def __init__(self, parent : Banana, connection) -> None:
			self.__parent = parent
			self.__database_connection = connection
			self.__database_cursor = connection.cursor()
			print("BananaConnection initialized")

		def connect(self, *args) -> __BananaConnection:
			print("Already connected")

		# Finish the connection
		def disconnect(self) -> Banana:
			self.__database_cursor.close()
			return self.__parent.disconnect()

		# Table methods
		def set_table(self,table) -> __BananaConnection:
			self.table = table
			return self
			
		def get_table(self) -> str:
			return self.table


		# Essencial methods
		def select(self, *columns) -> __BananaConnection:
			self.__operation_type = "SELECT"
			self.__select.extend(columns)
			return self

		def insert(self, value : dict) -> __BananaConnection:
			self.__operation_type = "INSERT"
			return self
		
		def update(self, value : dict) -> __BananaConnection:
			self.__operation_type = "UPDATE"
			return self

		def delete(self, value) -> __BananaConnection:
			self.__operation_type = "DELETE"
			return self


		def where(self, *conditions : str or list) -> __BananaConnection:
			for con in conditions:
				self.__where.append(con)
			return self

		def execute(self) -> list:
			string_query = ""

			match self.__operation_type:
				case "SELECT":
					string_query = "SELECT $select$ FROM $table$"
					
					# REPLACES
					string_query = string_query.replace("$select$", '"' + '", "'.join(self.__select) + '"')
					string_query = string_query.replace("$table$",self.table)
					
					# WHERE CONDITION
					if self.__where != []: string_query += " WHERE $where$".replace("$where$"," and ".join(self.__where))
				
				case "INSERT":
					pass
			
			try:
				print(string_query)
				self.__database_cursor.execute(string_query)
				print("Query successfully executed")
			except Exception as e:
				print("ERROR. Can't execute this query")
				print(e)
			else:
				return self.__database_cursor.fetchall()