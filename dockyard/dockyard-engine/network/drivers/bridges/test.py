from linux import LinuxBridgeManager

obj = LinuxBridgeManager()
names = obj.create_link_pair(id_=5456)
print names
obj.attach_if(obj.get_index(names['ext_if']), obj.get_index('br100'))
obj.move_to_namespace(net_ns_fd=5456)
obj.change_state(names['int_if'], 5456)
obj.addr(address='192.168.100.1', mask='255.255.255.0', broadcast='192.168.100.255', net_ns_fd='5456')
