import pecan

from dockyard.api import config as api_config
from oslo_config import cfg
from pecan import make_app

from dockyard import model


API_SERVICE_OPT = [
    cfg.PortOpt('port',
                 default=5869,
                 help='Port for the dockyard service.'),
    cfg.IPOpt('host',
              default='127.0.0.1',
              help='Listening address for dockyard service'),
]

CONF = cfg.CONF
opt_group = cfg.OptGroup(name='default',
                         title='Group for the default values for dockyard api')
CONF.register_group(opt_group)
CONF.register_opts(API_SERVICE_OPT, opt_group)

def get_pecan_config():
    # Set up the pecan configuration
    filename = api_config.__file__.replace('.pyc', '.py')
    return pecan.configuration.conf_from_file(filename)

def setup_app(config=None):

    if not config:
        config = get_pecan_config() 

    model.init_model()
    app_conf = dict(config.app)

    return make_app(
        app_conf.pop('root'),
        logging=getattr(config, 'logging', {}),
        **app_conf
    )
