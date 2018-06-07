class Remove():
	def __init__(self, db, num):
		self.cur = db.cur
		self.conn = db.conn
		self.planNumber = num

	def check(self):
		sql = "select id from todo where 1"
		self.cur.execute(sql)
		planNumbers = self.cur.fetchall()
		if (self.planNumber, ) in planNumbers:
			return True
		else:
			print("\nInvalid number :(\n")
			return False

	def execute(self):
		sql = "delete from todo where id=?"
		task = (self.planNumber,)
		self.cur.execute(sql, task)
		self.update()
		self.conn.commit()
		print("\nYour plan has been successfully removed!\n")

	def update(self):
		sql = "update todo set id=id-1 where id >" + str(self.planNumber)
		self.cur.execute(sql)