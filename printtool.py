#!python
#==========================================================#
# title: printtool.py 
# decscription: smarter and more colorful printing
# author: sjdillon
# date: 20150307
# usage: 
# from printtool import print_message, 
# print_message ('script has been run, but source has changed','EXIT')
# python_version :2.7.7  
#==========================================================#
from colorama import Fore, Back, Style
import colorama
colorama.init()

def print_message(msg,status):
	if status in ('OK','PASS') :
		color=Fore.YELLOW
	elif status in ('RUNNING','FILE'):
		color=Fore.GREEN
	elif status in ('ERROR','QUIT'):	
		color=Fore.RED
	else:
		color=Fore.WHITE	
	color=color+Style.BRIGHT	
	msg='%s[%s]%s: %s'  % (color,status,Style.RESET_ALL,msg)
	print msg	

def print_table(rows, headers=None):
	"""print a table from rows"""
	"""if no headers passed, will use db column names"""
	table=[]
	for row in rows:
		if headers==None:
			headers=list(row._fields)
		table_row=[]
		for cell in xrange(len(row)):
			table_row.append(row[cell])
		table.append(table_row)	
	print tabulate(table, headers, tablefmt="grid")	

def test_messages():	
	print_message('testing yellow', 'OK')	
	print_message('testing red', 'ERROR')	
	print_message('testing green', 'RUNNING')
	print_message('testing white', 'NONE')
