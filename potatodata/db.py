import sqlite3
import re
from datetime import datetime

class DB():
	def __init__(self):
		self.inputFormat1 = r"(\d{4})[-](\d{2})[-](\d{2})[/](\d{2})[:](\d{2})"
		self.inputFormat2 = r"(\d{4})[-](\d{2})[-](\d{2})\s(\d{2})[:](\d{2})"
		self.invalidDue = list()

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

	def renew(self):
		regular = re.compile(self.inputFormat1)
		regular2 = re.compile(self.inputFormat2)

		self.cur.execute("select * from todo where 1")
		rows = self.cur.fetchall()

		if rows:
			for row in rows:
				due = row[2]
				match1 = regular.match(due)

				timeNow = datetime.now()
				match2 = regular2.match(str(timeNow))

				for i in range(1,6):
					if int(match1.group(i)) < int(match2.group(i)):
						self.invalidDue.append(row[0])
						break
					elif int(match1.group(i)) > int(match2.group(i)):
						break

		if self.invalidDue:
			for i in range(0,len(self.invalidDue)):
				sql = "delete from todo where id = ?"
				self.cur.execute(sql,(self.invalidDue[i],))
				self.conn.commit()
