import sqlite3
import subprocess
	
def test_make():
	result = subprocess.check_output('potato make --what icecream --due 2018-06-29/12:00 --cat chores', shell=True)
	assert result == b'\nYour plan has been successfully added!\n\n'

def test_remove():
	result = subprocess.check_output('potato remove --all', shell=True)
	assert result == b'\nYour plans have been successfully removed!\n\n'

def test_print():
	result = subprocess.check_output('potato show', shell=True)
	assert result == b'\nNothing to print :(\n\n'

def main():
	test_make()
	test_remove()
	test_print()

if __name__ == '__main__':
	main()