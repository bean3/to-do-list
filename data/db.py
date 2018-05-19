import sqlite3

class DB():
	def __init__(self):

		#Initial settings for sqlite
		self.conn = sqlite3.connect("potato.db")
		self.cur = self.conn.cursor()
		table_create_sql = """create table if not exists todo (
					id integer primary key autoincrement,
					what text not null,
					due text not null,
					category text not null,
					finished integer default 0);"""
		self.cur.execute(table_create_sql)
