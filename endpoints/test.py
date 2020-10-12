import logging
from aiohttp.web_response import Response
from aiohttp.web import Request

from simple_rest import RestEndpoint

class TestEndpoint(RestEndpoint):

    def routes(self):
        return ['/test',]

    async def post(self, request: Request) -> Response:
        data = await request.text()
        logging.info(f'request data: {data}')
        return Response(status=200, body=data, content_type='text/plain')