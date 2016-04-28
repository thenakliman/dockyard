from oslo_config import cfg

CONSUL_SERVICE_OPT = [
    cfg.StrOpt('service_name',
                default='dockyard',
                help='Name of this service used by the consul')
]

CONF = cfg.CONF
opt_group = cfg.OptGroup(name='consul',
                         title='Group for the consul parameters')
CONF.register_group(opt_group)
CONF.register_opts(CONSUL_SERVICE_OPT, opt_group)


DOCKER_SERVICE_OPT = [
    cfg.IPOpt('docker_host',
              default='0.0.0.0',
              help='IP address to which docker is binded'),
    cfg.IntOpt('docker_port',
              default='2375',
              help='PORT on which docker is listening'),
    cfg.StrOpt('docker_name',
              default='docker',
              help='Name of the service under which docker is registered')
]

CONF = cfg.CONF
opt_group = cfg.OptGroup(name='docker',
                         title='Group for the docker server parameters')
CONF.register_group(opt_group)
CONF.register_opts(DOCKER_SERVICE_OPT, opt_group)
