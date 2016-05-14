from linux import LinuxBridgeManager
from base import InterfaceManager

obj = LinuxBridgeManager()
#names = obj.create_link_pair(id_=29966)
#print names
#obj.attach_if(obj.get_index(names['ext_if']), obj.get_index('br100'))
#obj.move_to_namespace(obj.get_index(names['int_if']), net_ns_fd=29966)
obj.addr(62, address='192.168.100.1', mask='255.255.255.0', broadcast='192.168.100.255', net_ns_fd='29966')
obj.change_state(names['int_if'], 'up', 29966)
