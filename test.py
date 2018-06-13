import os

def test_make():
	os.system('potato make --what icecream --due 2018-06-29/12:00 --cat chores')

def test_print():
	assert os.system('potato show') == "                         P O T A T O F I E L D                         \n"+
"=======================================================================\n"+
"| No. |   Description   |       Due        |  Category  |   Status    |\n"+
"=======================================================================\n"+
"| 1   | icecream        | 2018-06-29/12:00 | chores     | In Progress |\n"+
"=======================================================================\n"+
" Category : ALL                                           Page 001/001"

def main():
	test_make()
	test_print()

if __name__ == '__main__':
	main()