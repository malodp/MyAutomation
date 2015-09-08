#!/usr/bin/python
import sys, getopt



def main(argv):
	hostname = ''

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


	print 'Hostname is ', hostname



if __name__ == "__main__":
	main(sys.argv[1:])
