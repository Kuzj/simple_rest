#!/usr/bin/env python
import logging
from aiohttp.web import Application, run_app

import endpoints
from simple_rest import RestEndpoint

format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=format, level=logging.DEBUG)
log_file_handler = logging.FileHandler(filename='app.log')
formatter = logging.Formatter(format)
log_file_handler.setFormatter(formatter)
logging.getLogger().addHandler(log_file_handler)

app = Application()
for module in endpoints.endpoints_list:
    module.Endpoint().register_routes(app.router)

if __name__ == "__main__":
    
    run_app(app, port=8800)