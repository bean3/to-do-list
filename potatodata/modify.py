import re
from datetime import datetime

class Modify():
	def __init__(self, db, num, input_data):
		self.cur = db.cur
		self.conn = db.conn
		self.rowNumber = num
		self.inputData = input_data

		#Rows
		self.cur.execute("select * from todo where id=?", (self.rowNumber,))
		self.selectedRow = self.cur.fetchall()

		#Items
		self.descr = self.inputData[0]
		self.due = self.inputData[1]
		self.cat = self.inputData[2]
		self.fin = self.inputData[3]

		#Needs
		self.need = []
		self.need += ['what'] if not self.descr else []
		self.need += ['due'] if not self.due else []
		self.need += ['cat'] if not self.cat else []
		self.need += ['fin'] if self.fin == None else []

		#Format settings
		self.inputFormat1 = r"(\d{4})[-](\d{2})[-](\d{2})[/](\d{2})[:](\d{2})"
		self.inputFormat2 = r"(\d{4})[-](\d{2})[-](\d{2})\s(\d{2})[:](\d{2})"
		self.inputLength = 16

	def isExist(self):
		return True if self.selectedRow else False

	def interactive(self):
		if self.need:
			#Nothing will change if input is empty
			print("\n(Nothing will change if you enter nothing.)")

			if 'what' in self.need:
				self.descr = input("\nWhat's your new plan? : ")
				self.descr = self.descr if self.descr else self.selectedRow[0][1]

			if 'due' in self.need:
				while True:
					self.due = input("\nWhen is the due date? : ")
					if self.due:
						self.due = self.due
						if not self.check():
							continue
						else:
							break
					else:
						self.due = self.selectedRow[0][2]
						break

			if 'cat' in self.need:
				self.cat = input("\nWhat is the category of this plan? : ")
				self.cat = self.cat if self.cat else self.selectedRow[0][3]

			if 'fin' in self.need:
				self.fin = input("\nIs it finished?(Y/N) : ")
				while (self.fin != 'Y' and self.fin != 'N' and self.fin != ''):
					self.fin = input("\nIs it finished?(Y/N) : ")
				if self.fin == 'Y':
					self.fin = 1
				elif self.fin == 'N':
					self.fin = 0
				else:
					self.fin = self.selectedRow[0][4]

	def check(self):
		regular = re.compile(self.inputFormat1)
		regular2 = re.compile(self.inputFormat2)

		if len(self.due) != self.inputLength:
			print("Please type in the right format (YYYY-MM-DD/HH:MM).")
			return False
		match = regular.match(self.due)
		if match == None:
			print("Please type in the right format (YYYY-MM-DD/HH:MM).")
			return False
		timeNow = datetime.now()
		match2 = regular2.match(str(timeNow))
		inputDue = regular.match(self.due)
		for i in range(1, 6):
			if int(inputDue.group(i)) < int(match2.group(i)):
				print("This todo is not valid!")
				return False
			elif int(int(inputDue.group(i)) > int(match2.group(i))):
				break
		self.due = inputDue.group(0)
		return True

	def execute(self):
			sql = "update todo set what=?, due=?, category=?, finished=? where id=?"
			task = (self.descr, self.due, self.cat, self.fin, self.rowNumber)
			self.cur.execute(sql, task)
			self.conn.commit()

			print("\nYour plan has been successfully changed!\n")



