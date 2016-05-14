from pyroute2 import IPRoute
ip = IPRoute()
print ip.get_links()[0]
#print ip.get_links()
#for x in ip.get_links():
#    print x
