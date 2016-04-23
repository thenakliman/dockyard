from oslo_config import cfg
from wsgiref import simple_server

from dockyard.api import app as api_app


def main():
    app = api_app.setup_app()

    # create the wsgi server and start it
    host, port = cfg.CONF.default.host, cfg.CONF.default.port
    srv = simple_server.make_server(host, port, app)
    srv.serve_forever()


main()
