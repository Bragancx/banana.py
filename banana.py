from __future__ import annotations
import sqlite3
from types import NoneType
import psycopg2

def tuple_to_string(data : tuple):
	return '", "'.join(data)


class Banana:

	__database_connection = None
	__database_cursor = None

	__table = ""

	def __gen_function(self,table):
		def BananaTable():
			self.__table = table
			return self.__BananaTableConnection(self.__database_cursor,self.__table)
		return BananaTable

	# Starts
	def __init__(self, connection = {}, configs = {}) -> None:

		# Check parameters
		if not ({'host', 'database', 'username', 'password'} <= connection.keys()):
			raise Exception ("Is missing parameters in the connection settings.")
		if ('port' not in connection): connection["port"] = 5432

		# Connect
		try:
			self.__database_connection = psycopg2.connect(host=connection["host"], dbname=connection["database"], user=connection["username"], password=connection["password"], port=connection["port"])
		except Exception as e:
			self.__database_connection = self.__database_connection.close()
			print("ERROR. Can't connect to the database!")
			print(e)
			return self
		
		# Generate table functions
		try:
			self.__database_cursor = self.__database_connection.cursor()
			self.__database_cursor.execute("SELECT DISTINCT table_name FROM information_schema.columns WHERE table_schema='public' ORDER BY table_name")

			for row in self.__database_cursor.fetchall():
				setattr(self,row[0].title().replace('_',''),self.__gen_function(row[0]))
		except Exception as e:
			print("ERROR. Can't generate schemas (can be ghosts?)")
			print(e)
		print("Banana started!")

	# Finish the connection
	def close(self) -> Banana:
		if self.__database_connection == None:
			print("Already disconnected! What do you want from me?!!")
		else:
			try:
				
				self.__database_cursor = self.__database_cursor.close()
				self.__database_connection = self.__database_connection.close()
				print("Connection closed!")
			except Exception as e:
				print("ERROR. Can't close connection!")
				print(e)
				return None
		return self

	def commit(self) -> Banana:
		self.__database_connection.commit()
		return self
	
	class __BananaTableConnection:

		__cursor = None
		__table = ""

		__data = {
			"method": "",
			"data": None,
			"where": None,
			"order": None
		}

		def __init__(self, cursor, table) -> None:
			self.__cursor = cursor
			self.__table = table

		#  Query methods
		def select(self, *columns) -> __BananaTableConnection:
			self.__data["method"] = "SELECT"
			self.__data["data"] = columns
			return self

		def insert(self, values : dict) -> __BananaTableConnection:
			self.__data["method"] = "INSERT"
			self.__data["data"] = values
			return self
		
		def update(self, values : dict) -> __BananaTableConnection:
			self.__data["method"] = "UPDATE"
			self.__data["data"] = values
			return self

		def delete(self, *ids : str) -> __BananaTableConnection:
			self.__data["method"] = "DELETE"
			self.__data["data"] = ids
			return self

		# Other methods

		def find(self, id : int) -> __BananaTableConnection:
			self.__data["method"] = "FIND"
			self.__data["data"] = id
			return self

		# Optional methods

		def where(self, *conditions : str) -> __BananaTableConnection:
			self.__data["where"] = conditions
			return self

		def order(self, *conditions : str) -> __BananaTableConnection:
			self._data["order"] = conditions

		def reset(self) -> None:
			self.__data = {
				"method": "",
				"data": None,
				"where": None,
				"order": None
			}

		def execute(self) -> list:
			_query = ""
			
			if self.__data["method"] == "": _query = self.__select()
			if self.__data["method"] == "SELECT": _query = self.__select()
			if self.__data["method"] == "INSERT": _query = self.__insert()
			if self.__data["method"] == "UPDATE": _query = self.__update()
			if self.__data["method"] == "DELETE": _query = self.__delete()
			if self.__data["method"] == "FIND": _query = "SELECT * FROM %s WHERE id = %s" % (self.__table, self.__data["data"])

			if _query == "":
				print("ERROR. Please check your query and try again!")
				print(_query)
				return []
			try:
				self.__cursor.execute(_query)
			except Exception as e:
				print("ERROR. Can't execute this query")
				print(e)
				return []

			self.reset()
			return self.__cursor.fetchall()


		def __select(self) -> str:
			query = "SELECT * FROM %s" % (self.__table)
			return self.__conditions(query)

		def __insert(self) -> str:
			_columns = []
			_values = []
			for key in self.__data["data"].keys():
				_columns.append(str(key))
				_values.append( self.__formatter(self.__data["data"][key]) )

			query = "INSERT INTO %s(\"%s\") VALUES (%s)" % (self.__table, '", "'.join(_columns), ", ".join(_values))
			return self.__conditions(query) + " RETURNING id"
		
		def __update(self) -> str:
			arr = []
			for key in self.__data["data"].keys():
				subdata = '"' + str(key) + '" = '
				subdata += self.__formatter(self.__data["data"][key])
				arr.append( subdata )

			query = "UPDATE %s SET %s" % ( self.__table, ", ".join(arr) )
			return self.__conditions(query) + " RETURNING id"
		
		def __delete(self) -> str:
			return "DELETE FROM %s WHERE id in (%s) RETURNING id" % (
				self.__table,
				", ".join(str(v) for v in self.__data["data"])
			)



		def __conditions(self,query) -> str:
			# WHERE
			if self.__data["where"] != None:
				query += " WHERE %s" % (" and ".join( self.__data["where"] )).replace("'","''")
			
			print("order:",type(self.__data["order"]) is None)
			# ORDER
			if self.__data["order"] != None:
				query += " ORDER BY %s" % (", ".join( self.__data["order"] )).replace("'","''")
			
			return query
		
		def __formatter(self,value) -> str:
			if (type(value) is str):
				return ("'%s'" % value)
			return str(value)