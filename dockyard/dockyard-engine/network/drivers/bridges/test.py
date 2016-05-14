from linux import LinuxBridgeManager
from base import Link, Addr

ifname='br1000'
peer = 'brx1000'
net_ns_fd='dockyard_6063'
obj = Link()
obj.create(ifname, peer)
#names = obj.create_link_pair(id_=6066)
#obj.attach_if(obj.get_index(names['ext_if']), obj.get_index('br100'))
print obj.get_ifs()
obj.move_to_namespace(ifname,net_ns_fd)
#for x in obj.lookup(net_ns_fd=net_ns_fd):
#    print x
obj.set_state(ifname, net_ns_fd, state='up')
Addr().add(ifname, address='192.168.100.1', mask=24, net_ns_fd='dockyard_6063')
#obj.change_state(names['int_if'], 'up', 6066)
