from netns import Namespace
from pyroute2 import IPRoute


ip = IPRoute()
with Namespace(29966, 'net'):
    ip.link.get_links()

print ip
