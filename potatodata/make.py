import re
from datetime import datetime

class Make():
	def __init__(self, db, input_data):
		self.cur = db.cur
		self.conn = db.conn
		self.inputData = input_data

		#Needs
		self.need = []
		self.need += ['what'] if not self.inputData[0] else []
		self.need += ['due'] if not self.inputData[1] else []
		self.need += ['cat'] if not self.inputData[2] else []

		#Format settings
		self.inputFormat1 = r"(\d{4})[-](\d{2})[-](\d{2})[/](\d{2})[:](\d{2})"
		self.inputFormat2 = r"(\d{4})[-](\d{2})[-](\d{2})\s(\d{2})[:](\d{2})"
		self.inputLength = 16

	def interactive(self):
		if 'what' in self.need:
			descr = input("\nWhat is your plan? : ")
			while not descr:
				descr = input("\nWhat is your plan? : ")
			self.inputData[0] = descr

		if 'due' in self.need:
			due = input("\nWhen is the due date? : ")
			self.inputData[1] = due
			while not self.check():
				self.inputData[1] = input("\nWhen is the due date? : ")

		if 'cat' in self.need:
			cat = input("\nWhat is the category of this plan? : ")
			while not cat:
				cat = input("\nWhat is the category of this plan? : ")
			self.inputData[2] = cat

	#Check whether the input satisfies the format
	def check(self):
		inputDue = self.inputData[1]
		regular = re.compile(self.inputFormat1)
		regular2 = re.compile(self.inputFormat2)
		while True:
			if len(inputDue) != self.inputLength:
				print("Please type in the right format : YYYY-MM-DD/HH:MM")
				return False
			match = regular.match(inputDue)
			if match == None:
				print("Please type in the right format : YYYY-MM-DD/HH:MM")
				return False
			else:
				break
		timeNow = datetime.now()
		match2 = regular2.match(str(timeNow))
		inputDue = regular.match(self.inputData[1])
		if (int(inputDue.group(2)) not in range(1,13) or
			int(inputDue.group(3)) not in range(1,32) or
			int(inputDue.group(4)) not in range(0,24) or
			int(inputDue.group(5)) not in range(0,60)):
				print("This todo is not valid!")
				return False
		for i in range(1, 6):
			if int(inputDue.group(i)) < int(match2.group(i)):
				print("This todo is not valid!")
				return False
			elif int(int(inputDue.group(i)) > int(match2.group(i))):
				break
		self.validDue = inputDue.group(0)
		return True

	def execute(self):
		descr = self.inputData[0]
		cat = self.inputData[2]
		sql = "insert into todo (what, due, category) values (?, ?, ?)"

		self.cur.execute(sql, (descr, self.validDue, cat,))
		self.conn.commit()
		print("\nYour plan has been successfully added!\n")


