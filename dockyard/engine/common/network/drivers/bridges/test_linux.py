from linux import LinuxBridgeManager
#from namespace import DockyardNamspace

obj = LinuxBridgeManager()
#ns = DockyardNamespace()
psid=8074
ifs = obj.create_link_pair()
obj.attach_port(ifname=ifs['ext_if'], br_name='br100')
obj.move_to_namespace(ifname=ifs['int_if'], psid=psid)
obj.change_state(ifname=ifs['int_if'], state='up', psid=psid)
obj.addr(ifname=ifs['int_if'], address='192.168.100.7', mask=24, psid=psid)
obj.add_routes(dst='default', gateway='192.168.100.1', psid=psid, oif_name=ifs['int_if'])
#ns.cleanup(psid)
