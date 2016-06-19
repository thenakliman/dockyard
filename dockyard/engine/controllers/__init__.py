from oslo_config import cfg

import dockyard.engine.common.containers.store.consul

NETWORK_DRIVER_OPT = [
    cfg.StrOpt('network_driver',
                default='bridges.linux.LinuxBridgeManager',
                help='Network driver for the changing settings for network.')
]

CONF = cfg.CONF
opt_group = cfg.OptGroup(name='network',
                         title='Group for the network values of dockyard api')
CONF.register_group(opt_group)
CONF.register_opts(NETWORK_DRIVER_OPT, opt_group)


CONF = cfg.CONF
CONF.register_opts(NETWORK_DRIVER_OPT, group='network')
