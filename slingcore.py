#!python
#==========================================================#
#title: slingcore.py
#description: applies a build to cassandra
#author: sjdillon
#date: 20150307
#usage: include slingcore
#python_version :2.7.7  
#rules:
#-validates: applied scripts match source control scripts
#-applies: new changes
#-stops: on failures and discrepencies
#-reruns: failures on next execution
#-note: source changes will need to be manually rectified
#==========================================================#
import md5
import os
import sys
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from printtool import print_message
import datetime

servers=''
uname=''
pw=''

def get_hash(instring):
	"""convert string to hash"""
	hash = md5.new(instring).hexdigest()
	return hash
	
def get_session(servers):
	"""get a session from cassandra"""
	auth_provider = PlainTextAuthProvider(username=uname, password=pw)    
	cluster = Cluster(servers,auth_provider=auth_provider)
	session = cluster.connect()
	session.default_timeout = 30
	return session

def run_cql(cmd):
	"""execute a command against cassandra"""
	try:
		session=get_session(servers)
		output=session.execute(cmd)
		return output
	except Exception, e:
		print_message('[STOPPING][CQL]:[%s] %s' % (type(e),str(e)),'ERROR')
		raise
		return False

def parse_file(filename):
	"""split multicommand files into individual commands"""
	r=get_raw_file(filename)
	data=r.split(';')
	return data[:-1]

def get_raw_file(filename):
	"""get the contents of a file"""
	with open (filename, "r") as file_name:
	    raw_file=file_name.read()
	    return raw_file	    

def logit(release,filename, cql, status=None):
	"""write a record of the script that has been executed"""
	dt=datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
	hash=get_hash(cql)
	insert="insert into sling.schema_version(release,filename, hash, status, create_dt) values('%s','%s', '%s', %i, '%s')"\
	 	% (release,filename, hash, status, dt)
	results=run_cql(insert)

def check_history(release,filename):
	query="select hash, filename, status from sling.schema_version where release='%s'" % (release)
	results=run_cql(query)
	for row in results:
		if row[1] == filename:
			if row[2] == 0:
				hash=str(row[0])
				return hash
				sys.exit(1)
	else:
		return False			

def fling(filename):
	"""run the script after checking the history"""
	base_filename=filename.split("\\")[-1]
	release=filename.split("\\")[-2]
	keyname='%s__%s' % (release,base_filename)
	history=check_history(release,keyname);
	print_message(base_filename, 'FILE') 
	cql=get_raw_file(filename)
	
	if history:
		hash=history
		if hash == get_hash(cql):
			print_message('confirmed previously run script matches current version under source control', 'PASS') 
			return True
		else:
			print_message ('script has been run, but source has changed','EXIT') 
		 	sys.exit(1)
	else:
		print_message('script has NOT been run already','RUNNING')	
		try:
			status=execute_file(filename)
			logit(release,keyname, cql,status)
			if status !=0:
				print '[QUIT]'
				print_message ('execute_file returned no status' , 'QUIT')
				sys.exit(1)
		except Exception, e:
			status=1
			print_message ('[fling]:[%s] %s' % (type(e),str(e)) , 'ERROR')
			logit(release,keyname, cql,1)	
			#print_message(str(e),'ERROR')
			sys.exit()		

def execute_file(filename):
	"""run the scripts in a file"""
	status=0
	try:
		commands=parse_file(filename)
		for command in commands:
			print command
 			output=run_cql(command)
 			if output:
 				print_message('[execute_file]:%s' % output, 'INFO')
 	except Exception, e:
 			print_message ('[execute_file]:[%s] %s' % (type(e),str(e)) , 'ERROR')
 			status = status+1
 			raise
 	return status


def execute_folder(cluster, dir, username, password):
	"""process all scripts in a folder"""
	global servers
	servers = cluster
	global uname
	uname = username
	global pw
	pw = password
	for f in os.listdir(dir):
		if ".cql" in f:
			f='%s\%s' % (dir,f)
	 		fling(f)


def get_build_info(cluster, dir, username, password):
	global servers
	servers = cluster
	global uname
	uname = username
	global pw
	pw = password

	release=str(dir)
	check_local=True
	if "\\" in release:
		release=release.split("\\")[-1]
	else:
		check_local=False

	"""get build history from db table and files in local folder"""
	headers=['Release','Filename','ApplyTime','Status']
	#get changes from db
	applied_cql="select release,filename, create_dt, status from sling.schema_version where release='%s' order by create_dt" % (release)
	rows=run_cql(applied_cql)
	#get local files
	if check_local:
		records=[]
		filenames=[]
		for f in rows:
			filenames.append(f[1])
		for file in os.listdir(dir):
			if ".cql" in file:
				record=[]
				record.append(release)
				filename=release+'__'+file
				record.append(release+'__'+file)
				record.append('')
				record.append('Pending')
				if filename not in filenames:
					rows.append(record)		
		#decode status: convert status number to string
	outer=[]
	for i in rows:
		inner=[]
		for idx, val in enumerate(i):
			if idx==3: 
				if val==0:
					val='Success'
				elif val==1:
					val='Failed'		
				inner.append(val)
			else:	
				inner.append(val)
		outer.append(inner)
	return outer, headers