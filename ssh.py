#!/usr/bin/python

import base64
import getpass
import os
import socket
import sys
import getopt
import traceback
from paramiko.py3compat import input
import paramiko
import threading
import signal

PUPPET_INSTALL = '''''
					uptime
					sudo rpm -ivh https://yum.puppetlabs.com/puppetlabs-release-el-7.noarch.rpm
					sudo yum install puppet -y
					ls -lrt /etc/puppet
					cat /etc/puppet/puppet.conf
				'''''
MYSQL_CONFIG = '''''	
					 mysqladmin -u root create BooksDB
					 pwd
					 ls
     			                 mysql -u root BooksDB < '/tmp/foodmart_data.sql'
                                '''''

COPY_FILES = '''''
				sudo cp /tmp/puppet.conf /etc/puppet/puppet.conf
				sudo puppet agent --test
			'''''

hostname = ''
p_master = 'ip-172-31-27-31.us-west-2.compute.internal'
#p_master = 'ip-172-31-27-31.us-west-2.compute.internal'
p_username = 'ec2-user'
dirname = ''
filename = ''
site =''
username = ''
localpath = '/etc/puppet/puppet.conf'
remotepath = '/tmp/puppet.conf'
key = '/tmp/pravmal.pem'
debug = 1

sqllocalpath = '/home/ec2-user/foodmart_data.sql'
sqlremotepath = '/tmp/foodmart_data.sql'

def signal_cleanup(_signum, _frame):
	print '\nCLEANUP\n'
	sys.exit(0)


def connect_hostnexe(hostname, username):
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	hostname = socket.getfqdn(hostname)
	client.connect(hostname, username=username, key_filename=key)
	stdin, stdout, stderr = client.exec_command(PUPPET_INSTALL, get_pty=True)

	for line in stdout:
		if debug: print line.strip('\n')
		#if debug: print threading.current_thread().name, line,
	for line1 in stderr:
		print line1.strip('\n')
	client.close()


def configure_mysql(hostname, username):
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	hostname = socket.getfqdn(hostname)
	client.connect(hostname, username=username, key_filename=key)
	stdin, stdout, stderr = client.exec_command(MYSQL_CONFIG, get_pty=True)

	for line in stdout:
		if debug: print line.strip('\n')
		#if debug: print threading.current_thread().name, line,
	for line1 in stderr:
		print line1.strip('\n')
	client.close()

def connect_host_write_file(p_master,p_username,dirname,filename,site):
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	p_master = socket.getfqdn(p_master)
	client.connect(p_master, username=p_username, key_filename=key)
	sftp = client.open_sftp()
	f = sftp.open(dirname + '/' + filename, 'w')
	f.write(site)
	f.close()
	sftp.close()
	client.close()

def connect_hostncopy(hostname, username,localpath,remotepath):
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	hostname = socket.getfqdn(hostname)
	client.connect(hostname, username=username, key_filename=key)
	sftp = client.open_sftp()
	sftp.put(localpath, remotepath)
	stdin, stdout, stderr = client.exec_command(COPY_FILES, get_pty=True)

	for line in stdout:
		if debug: print line.strip('\n')
		#if debug: print threading.current_thread().name, line,
	for line1 in stderr:
		print line1.strip('\n')
	sftp.close()
	client.close()


def mysql_config(hostname, username,sqllocalpath,sqlremotepath):
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	hostname = socket.getfqdn(hostname)
	client.connect(hostname, username=username, key_filename=key)
	sftp = client.open_sftp()
	sftp.put(sqllocalpath, sqlremotepath)
	stdin, stdout, stderr = client.exec_command(MYSQL_CONFIG, get_pty=True)

	for line in stdout:
		if debug: print line.strip('\n')
		#if debug: print threading.current_thread().name, line,
	for line1 in stderr:
		print line1.strip('\n')
	sftp.close()
	client.close()



def main(argv):
	try:
		opts, args = getopt.getopt(argv,"s:e:u:p:k:",["Hserver=","EC2server=","suser","spass","pkgs"])
	except getopt.GetoptError:
		print 'USAGE: read_server.py -s <server_ip/name> or -e <ec2_serverIP/Name> -u <Server_user> -p <password> -pkg <package-name>'
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print 'USAGE: read_server.py -s <server_ip/name> or -e <ec2_serverIP/Name> -u <Server_user> -p <password> -pkg <package-name>'
			sys.exit(2)
		elif opt in ("-s", "--Hserver") :
			hostname = arg
		elif opt in ("-e", "--EC2server"):
			hostname = arg
		elif opt in ("-u","--suser"):
			username = arg
		elif opt in ("-k","--pkgs"):
			pkgs = arg

		elif opt in ("-p","--spass"):
			password = arg


	if debug:
		print "Server Name:%s"%hostname
		print "Server UserName:%s"%username
		print "Server Password:%s"%password
		print "Install packages:%s"%pkgs
	'''''
	Connecting Server with hostname and username
	Install puppet agent on the host
	'''''
	connect_hostnexe(hostname, username)

	'''''
	Updating Puppet master's site.pp with puppet agent file
	'''''
	dirname = '/etc/puppet/manifests'
	filename = 'site.pp'
	site = '''
node '%s'
{
	include %s
#	include '::mysql::server'
}
		'''%(hostname,pkgs)
	if debug:
                print "Dir Name:%s "%dirname
		print "fileName:%s "%filename
		print "p_master:%s"%p_master
		print "Site:%s"%site
	connect_host_write_file(p_master, p_username, dirname, filename, site)

	'''''
	Connecting puppet agent server and copy the puppet.conf which has puppet
	master server
	'''''
	connect_hostncopy(hostname, username,localpath,remotepath)
	if pkgs == '::mysql::server' :
		mysql_config(hostname, username,sqllocalpath,sqlremotepath)

if __name__ == "__main__":
	main(sys.argv[1:])
