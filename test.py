import sqlite3
import os
import subprocess

def test_remove():
	os.system('')
	
def test_make():
	result = subprocess.check_output('potato make --what icecream --due 2018-06-29/12:00 --cat chores')
	assert result == b'\r\nYour plan has been successfully added!\r\n\r\n'

def test_print():
	result = subprocess.check_output('potato show')
	assert result == b'                         P O T A T O F I E L D                         \r\n=======================================================================\r\n| No. |   Description   |       Due        |  Category  |   Status    |\r\n=======================================================================\r\n| 1   | icecream        | 2018-06-29/12:00 | chores     | In Progress |\r\n| 2   | icecream        | 2018-06-29/12:00 | chores     | In Progress |\r\n| 3   | icecream        | 2018-06-29/12:00 | chores     | In Progress |\r\n=======================================================================\r\n Category : ALL                                           Page 001/001 \r\n'

def main():
	test_make()
	test_print()

if __name__ == '__main__':
	main()