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


UseGSSAPI = True             # enable GSS-API / SSPI authentication
DoGSSAPIKeyExchange = True
port = 22

def main(argv):

    try:
        opts, args = getopt.getopt(argv,"hs:e:",["iserver=","ec2server="])
    except getopt.GetoptError:
        print 'read_server.py -s <server_ip/name> -e <ec2_serverIP/Name>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'read_server.py -s <server_ip/name> -e <ec2_serverIP/Name>'
            sys.exit(2)
        elif opt in ("-s", "--iserver") :
            hostname = arg
        elif opt in ("-e", "--ec2server"):
            hostname = arg

    # get username
    #if username == '':
    default_username = getpass.getuser()
    username = input('Username [%s]: ' % default_username)
    if len(username) == 0:
        username = default_username
    if not UseGSSAPI or (not UseGSSAPI and not DoGSSAPIKeyExchange):
        password = getpass.getpass('Password for %s@%s: ' % (username, hostname))


    # now, connect and use paramiko Client to negotiate SSH2 across the connection
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print('*** Connecting...')
        
        if not UseGSSAPI or (not UseGSSAPI and not DoGSSAPIKeyExchange):
            if opt in ("-s", "--iserver") :
                print "Server_IP"
                client.connect(hostname, port, username, password)
            elif opt in ("-e", "--ec2server") :
                print "EC2-Server"
                client.connect(hostname, username=username, key_filename='C:/viewwork/prasanna-work/pravmal.pem')
        else:
            # SSPI works only with the FQDN of the target host
            hostname = socket.getfqdn(hostname)
            try:
                if opt in ("-s", "--iserver") :
                    client.connect(hostname, port, username, password)
                elif opt in ("-e", "--ec2server") :
                    client.connect(hostname, username=username, key_filename='C:/viewwork/prasanna-work/pravmal.pem')

            except Exception:
                password = getpass.getpass('Password for %s@%s: ' % (username, hostname))
                if opt in ("-s", "--iserver") :
                    client.connect(hostname, port, username, password)
                elif opt in ("-e", "--ec2server") :
                    client.connect(hostname, username=username, key_filename='C:/viewwork/prasanna-work/pravmal.pem')

        print('*** Here we go!\n')
        #client.connect(Host, 22, user)

        chan = client.get_transport().open_session()
        chan.get_pty()
        #stdin, stdout, stderr = client.exec_command('uptime;ls -l;touch puppet_module;ls -l;uptime')  ### Execute command on the client
        stdin, stdout, stderr = client.exec_command('''
            uptime
            touch winner
            rpm -ivh http://yum.puppetlabs.com/puppetlabs-release-el-7.noarch.rpm
            yum install puppet -y
            ls -lrt /etc/puppet
            ''')  ### Execute command on the client
        #print(chan.recv(4096))
 
        #for line1 in stderr:
        #    print line1.strip('\n') 
        print stderr.read()

        for line in stdout:
        	print line.strip('\n') 

        client.close()


    except Exception as e:
        print('*** Caught exception: %s: %s' % (e.__class__, e))
        traceback.print_exc()
        try:
            client.close()
        except:
            pass
        sys.exit(1)



if __name__ == "__main__":
    main(sys.argv[1:])
