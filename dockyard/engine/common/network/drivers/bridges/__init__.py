from oslo_config import cfg

HOST_SERVICE_OPT = [
    cfg.StrOpt('bridge',
                default='br100',
                help='Bridge for the external connectivity network'),
]

cfg.CONF.register_opts(HOST_SERVICE_OPT, 'network')
