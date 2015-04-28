#!python
#==========================================================#
#title: sling.py
#description: Command line utility to apply a build to cassandra
#author: sjdillon
#date: 20150307
#usage: python sling.py -U <uname> -P <pw> -S loadtest -D \Database\Cassandra\ReleaseScripts\4_2\
#python_version :2.7.7  
#rules:
#-validates: applied scripts match source control scripts
#-applies: new changes
#-stops: on failures and discrepencies
#-reruns: failures on next execution
#-note: source changes will need to be manually rectified
#==========================================================#
import argparse
import pickledb
from slingcore import execute_folder, get_build_info
from tabulate import tabulate

def get_config(key, dbfile):
	pdb=pickledb.load(dbfile, False)
	config=pdb.dgetall(key)
	return config

parser = argparse.ArgumentParser(description='apply schema changes to Cassandra')
parser.add_argument('-U','--username', help='login',required=True)
parser.add_argument('-P','--password', help='password',required=True)
parser.add_argument('-S','--servers', help='cluster key in config file',required=True)
parser.add_argument('-D','--directory', help='directory with files to apply',required=True)
parser.add_argument('-I','--info', help='get build info only',required=False, default=False)
parser.add_argument('-C','--config', help='pickledb config file with db connections',required=False,default='cassandra.db')
#parser.add_argument('-V','--verbose', help='output script content',required=False,default=True)
args = parser.parse_args()

uname=args.username
pw=args.password
servers=args.servers
fdir=args.directory.rstrip('\\')
config=args.config
info=args.info
#verbose=args.verbose

conns=get_config(servers,config)
if info:
	rows,headers=get_build_info(conns, fdir, uname, pw)
	print tabulate(rows,headers,tablefmt="grid")
else:
	execute_folder(conns, fdir, uname, pw)
	