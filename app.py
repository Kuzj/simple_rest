#!/usr/bin/env python
import logging
from aiohttp.web import Application, run_app

from simple_rest import RestEndpoint
from endpoints.test import TestEndpoint
from endpoints.grafana import GrafanaEndpoint

logging.basicConfig(level=logging.DEBUG)

#  TODO: Загружать все endpoints из папки, например как actions
app = Application()
test = TestEndpoint()
test.register_routes(app.router)
grafana = GrafanaEndpoint()
grafana.register_routes(app.router)

if __name__ == "__main__":
    
    run_app(app, port=8800)