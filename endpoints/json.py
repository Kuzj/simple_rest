import logging
import json
from aiohttp.web_response import Response
from aiohttp.web import Request

import actions
from simple_rest import RestEndpoint

class JSONError(Exception):
    """Base class for exceptions in GrafanaEndpoint."""
    pass

class NoActionInMessage(JSONError):
    pass

class Endpoint(RestEndpoint):
    '''
    {"action":{
    "name":"http_request",
    "method":"post",
    "url":"http://127.0.0.1:8801",
    "data":"{'status': 'warning', 'host': 'host.alert.from', 'hostgroup': 'project', 'service': 'alert name or metric', 'text': 'text alert'}"
    }}
    '''
    def routes(self):
        return ['/json',]

    async def post(self, request: Request) -> Response:
        data = await request.json()
        logging.info(f'{self.__class__} {request.path} from {request.host} {request.method} request: {data}')
        if 'action' in data:
            await self.do_action(data['action'])
        else:
            #  HTTPBadRequest
            Response(status=400)
            raise NoActionInMessage
        return Response(status=200)
