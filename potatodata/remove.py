class Remove():
	def __init__(self, db, num, del_all=False):
		self.cur = db.cur
		self.conn = db.conn
		self.planNumber = num
		self.deleteAll = del_all

	def check(self):
		if self.deleteAll == True:
			return True
		else:
			sql = "select id from todo where 1"
			self.cur.execute(sql)
			planNumbers = self.cur.fetchall()
			if (self.planNumber, ) in planNumbers:
				return True
			else:
				print("\nInvalid number :(\n")
				return False

	def execute(self):
		if self.deleteAll == True:
			self.cur.execute("delete from todo")
		else:
			self.cur.execute("delete from todo where id=?", (self.planNumber,))
		self.conn.commit()
		print("\nYour plan" + ("s have" if self.deleteAll == True else " has") + " been successfully removed!\n")