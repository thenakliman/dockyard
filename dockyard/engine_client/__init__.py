import importlib
from oslo_config import cfg

# Add default values for the database to be used for dockyard.
DATABASE_OPT = [
    cfg.StrOpt("driver",
                default="consul.consul_client.ConsulKV",
                help="Database driver for dockyard"),
    cfg.IntOpt('synchronization_time',
                default=20,
                help='Time after which data will be synced .')
]

CONF = cfg.CONF
opt_group = cfg.OptGroup(name='database',
                         title='Group for database')
CONF.register_group(opt_group)
CONF.register_opts(DATABASE_OPT, opt_group)
db_driver_loc = 'dockyard.common.stores'
db_driver_info = (('%s.%s') % (db_driver_loc, CONF.database.driver))
module_name, db = db_driver_info.rsplit(".", 1)
module = importlib.import_module(module_name)

#import synchronizer
