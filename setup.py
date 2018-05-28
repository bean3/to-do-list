from setuptools import setup

setup(
	name='potatotodo',
	version='1.0.0',
	description='This is very usual todo-list',
	packages=['potatodata'],
	entry_points={
	    'console_scripts': [
	        'potato=potatodata.potato:run',
	        'potatofield=potatodata.potato:run'
	    ]
	}
)
