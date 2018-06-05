from colorama import Fore, Back, Style
from sys import exit
from .category import Category
from .page import Page

def menu(name):
	return f"{Fore.RESET}{name}{Fore.LIGHTBLACK_EX}"

def bar():
	return f"{Fore.LIGHTBLACK_EX}|{Fore.RESET}"

class Plan():
	def __init__(self, db, pg, p_opt):

		#Default settings
		defaultPrintOption = "select * from todo where 1"
		self.selectedCat = "ALL"

		#Check the category if --cat option is given and there is at least 1 category
		if p_opt == 'category':
			category = Category(db)
			exit() if category.isEmpty() else None
			category.show()
			inputCat = input("\nWhich category do you want to see? : ")
			self.selectedCat = inputCat if category.check(inputCat) else exit()

		#Only options using 'p_opt' parameter will have the specific print option
		self.printOption = {
		'unfinished': "select * from todo where finished=0",
		'finished': "select * from todo where finished=1",
		'overdue': "select * from todo where finished=2",
		'category': f"select * from todo where category='{self.selectedCat}'" if p_opt == 'category' else None
		}.get(p_opt, defaultPrintOption)

		#Loading page methods
		db.cur.execute(self.printOption)
		self.rows = db.cur.fetchall()
		self.page = Page(self.rows, pg)

	def show(self):

		#Same with this : self.rows is not empty and given page number is in range(0, self.page.maxPageNum + 1)
		if self.rows and (self.page.isValid() or not self.page.isActivated()):

			print(
				f"{Back.BLACK}                         {Fore.LIGHTYELLOW_EX}P O T A T O {Fore.LIGHTGREEN_EX}F I E L D                         {Style.RESET_ALL}")
			
			for pageNum in range(1, self.page.maxPageNum + 1):

				#Pass the page which is not selected when --pg option is given
				if self.page.isActivated() and not self.page.isSelectedPage(pageNum):
					continue

				print(
					Fore.LIGHTBLACK_EX +
					"=======================================================================\n"
					"| "+menu("No.")+" |   "+menu("Description")+"   |       "+menu("Due")+"        |  "+menu("Category")+"  |   "+menu("Status")+"    |\n"
					"======================================================================="
					+ Fore.RESET)

				rowIndex = (pageNum - 1) * self.page.rowsinPage
				for row in self.rows[rowIndex:rowIndex + self.page.rowsinPage]:

					#Format of printing columns
					#1. Print the number of plan; Max : 3-digit number
					#2. Print description and if it is too long to print, append '...'; Max : 15 chars
					#3. Print the due as it is since the due has its own format; YYYY-MM-DD
					#4. Print the category in the similar way to the description
					#5. Print whether the plan is done or not
					num = str(row[0])
					descr = row[1] if len(row[1]) <= 15 else row[1][:12] + "..."
					due = row[2]
					cat = row[3] if len(row[3]) <= 10 else row[3][:7] + "..."

					# fin = "Done" if row[4] == 1 else "In Progress"
					if row[4] == 1:
						fin = "Done"
						finColor = Fore.GREEN
					elif row[4] == 2:
						fin = "Overdue"
						finColor = Fore.YELLOW
					else:
						fin = "In Progress"
						finColor = Fore.RED
						
					curCat = self.selectedCat if len(self.selectedCat) <= 10 else self.selectedCat[:7] + "..."

					print(bar()+f" {num:3} "+bar()+f" {descr:15} "+bar()+f" {due} "+bar()+f" {cat:10} "+bar()+f" {finColor}{fin:11}{Fore.RESET} "+bar())

				print(
					f"{Fore.LIGHTBLACK_EX}======================================================================={Fore.RESET}\n"
					f"{Back.BLACK}{Fore.LIGHTWHITE_EX} Category : {Fore.LIGHTMAGENTA_EX}{curCat:10}{Fore.LIGHTWHITE_EX}                                    Page {Fore.LIGHTMAGENTA_EX}{pageNum:03}{Fore.LIGHTWHITE_EX}/{self.page.maxPageNum:03} {Style.RESET_ALL}")

		else:

			#Same with this : self.rows is empty and given page number is 0
			if not self.rows and not self.page.isValid() and not self.page.isActivated():
				print("\nNothing to print :(\n")

			#Same with this : given page number is not valid
			else:
				print("\nInvalid page number :(\n")			