from setuptools import setup

setup(
	name='potatotodo',
	version='1.1.3',
	description='This is very usual todo-list',
	author = 'Team_potato',
	url = 'https://github.com/bean3/to-do-list',
	packages=['potatodata'],
	python_requires = '>=3.6',
	install_requires = ['click', 'colorama'],
	entry_points={
	    'console_scripts': [
	        'potato=potatodata.potato:run',
	        'potatofield=potatodata.potato:run'
	    ]
	},
	classifiers=['Programming Language :: Python :: 3.6']
)
