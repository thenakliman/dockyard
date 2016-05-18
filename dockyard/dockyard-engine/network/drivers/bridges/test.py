from linux import LinuxBridgeManager
from base import Link

#ifname='br1000'
#peer = 'brx1000'
#net_ns_fd='dockyard_4235'
#obj = LinuxBridgeManager()
#obj = Link()
#obj.create(ifname, peer)
#names = obj.create_link_pair(id_=4235)
#obj.attach_if(names['ext_if'], 'br100')
#print obj.get_ifs()
#obj.move_to_namespace(names['int_if'],net_ns_fd)
#for x in obj.lookup(net_ns_fd=net_ns_fd):
#    print x
#obj.set_state('veth-i-4235', net_ns_fd, state='up')
#obj.change_state(names['int_if'], 'up', 4235)
#obj.addr(names['int_if'], address='192.168.100.1', mask=24, net_ns_fd=4235)
