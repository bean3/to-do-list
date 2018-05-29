from setuptools import setup

setup(
	name='potatotodo',
	version='1.0.0',
	description='This is very usual todo-list',
	author = 'Team_potato',
	url = 'https://github.com/bean3/to-do-list',
	packages=['potatodata'],
	python_requires = '>=3',
	entry_points={
	    'console_scripts': [
	        'potato=potatodata.potato:run',
	        'potatofield=potatodata.potato:run'
	    ]
	},
	classifiers      = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)
