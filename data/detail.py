class Detail():
	def __init__(self, db, num):
		self.cur = db.cur
		self.conn = db.conn
		self.planNum = num

	def check(self):
		if self.planNum == None:
			self.planNum = input("Enter the number of plan you want to see details (0 : Exit) : ")
			while self.planNum.isdigit() != True:
				self.planNum = input("Enter the number of plan you want to see details (0 : Exit) : ")
			while int(self.planNum) < 0:
				self.planNum = input("Enter the number of plan you want to see details (0 : Exit) : ")
			if self.planNum == '0':
				print()
				exit()

		self.cur.execute("select * from todo where id=?", (self.planNum,))
		self.selectedRow = self.cur.fetchall()

		if self.selectedRow:
			return True
		else:
			print("\nInvaild number :(\n")
			return False

	def execute(self):
		num = self.selectedRow[0][0]
		descr = self.selectedRow[0][1]
		due = self.selectedRow[0][2]
		cat = self.selectedRow[0][3]
		fin = self.selectedRow[0][4]

		print(
			"\nNo. ", num,
			"\nDescription : ", descr,
			"\nDue : ", due,
			"\nCategory : ", cat,
			"\nStatus : ", "Done\n" if fin == 1 else "In progress\n", sep = "")




