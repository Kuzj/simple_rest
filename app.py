import logging
from aiohttp.web import Application, run_app

from simple_rest import RestEndpoint
from endpoints.test import TestEndpoint

logging.basicConfig(level=logging.DEBUG)

app = Application()
test = TestEndpoint()
test.register_routes(app.router)

if __name__ == "__main__":
    
    run_app(app, port=8800)