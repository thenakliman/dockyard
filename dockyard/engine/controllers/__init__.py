from oslo_config import cfg


NETWORK_DRIVER_OPT = [
    cfg.StrOpt('network_driver',
                default='bridges.linux.LinuxBridgeManager',
                help='Network driver for the changing settings for network.')
]

CONF = cfg.CONF
CONF.register_opts(NETWORK_DRIVER_OPT, group='default')
