import re

class Modify():
	def __init__(self, db, num):
		self.cur = db.cur
		self.conn = db.conn
		self.rowNumber = num

		#Format settings
		self.inputFormat = r"(\d{4})[-](\d{2})[-](\d{2})[/](\d{2})[:](\d{2})"
		self.inputLength = 16

	def check(self):
		self.cur.execute("select * from todo where id=?", (self.rowNumber,))
		selectedRow = self.cur.fetchall()

		if selectedRow:

			#Nothing will change if input is empty
			print("\n(Nothing will change if you enter nothing.)")

			self.descr = str(input("\nWhat's your new plan? : "))
			self.descr = self.descr if self.descr else selectedRow[0][1]

			while True:
				self.due = str(input("\nWhen is the due date? : "))
				self.due = self.due if self.due else selectedRow[0][2]

				regular = re.compile(self.inputFormat)

				if len(self.due) != self.inputLength:
					print("Please type in the right format (YYYY-MM-DD/HH:MM).")
					continue
				match = regular.match(self.due)
				if match == None:
					print("Please type in the right format (YYYY-MM-DD/HH:MM).")
				else:
					break

			self.fin = str(input("\nIs it finished?(Y/N) : "))
			while (self.fin != 'Y' and self.fin != 'N' and self.fin != ''):
				self.fin = str(input("\nIs it finished?(Y/N) : "))
			if self.fin == 'Y':
				self.fin = 1
			elif self.fin == 'N':
				self.fin = 0

			self.fin = self.fin if self.fin else selectedRow[0][4]
				
			return True

		else:
			print("\nInvalid number :(\n")
			return False

	def execute(self):
			sql = "update todo set what=?, due=?, finished=? where id=?"
			task = (self.descr, self.due, self.fin, self.rowNumber)
			self.cur.execute(sql, task)
			self.conn.commit()

			print("\nYour plan has been successfully changed!\n")



