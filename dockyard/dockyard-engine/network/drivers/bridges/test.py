from base import InterfaceManager

obj = InterfaceManager('1111', 'br-eth0')
obj.create_link_pair()
obj.attach_if()
