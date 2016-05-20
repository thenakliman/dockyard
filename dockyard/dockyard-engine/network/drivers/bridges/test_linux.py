from linux import LinuxBridgeManager

obj = LinuxBridgeManager()
psid=4067
ifs = {'int_if': ('dockyard-i-%d' % psid),
       'ext_if': ('dockyard-x-%d' % psid)}
obj.create_link_pair(psid)
obj.move_to_namespace(ifname=ifs['int_if'], psid=psid)
obj.change_state(ifname=ifs['int_if'], state='up', psid=psid)
obj.addr(ifname=ifs['int_if'], address='192.168.100.4', mask=24, psid=psid)
obj.add_routes(dst='default', gateway='192.168.100.1', psid=psid, oif_name=ifs['int_if'])
