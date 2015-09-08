#!/usr/bin/python
from xml.dom.minidom import parse

doc = parse('servers.xml')
#print doc

elementNodes = doc.getElementsByTagName('packages')
print (elementNodes.firstChild.data)



#serverNodes =  doc.getElementsByTagName('node')
#for serverNode in serverNodes:
#		s_type = serverNode.getAttribute('id')
		

#for ele in elementNodes:
#	print ele.toxml()


#print elementNodes 
#print "Len : ", len(elementNodes)
