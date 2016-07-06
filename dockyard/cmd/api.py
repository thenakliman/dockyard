import os
import sys

from oslo_config import cfg
from oslo_log import log as logging
from wsgiref import simple_server

from dockyard.api import app as api_app
from dockyard.common import utils


LOG = logging.getLogger(__name__)

def main():
    utils.prepare_logging(sys.argv)

    app = api_app.setup_app()

    # create the wsgi server and start it
    host, port = cfg.CONF.default.host, cfg.CONF.default.port
    srv = simple_server.make_server(host, port, app)

    LOG.info('Starting dockyard in PID %s', os.getpid())
    LOG.debug("Configuration:")
    cfg.CONF.log_opt_values(LOG, logging.DEBUG)

    LOG.info('serving at http://%s:%s' % (host, port))
    srv.serve_forever()


main()
