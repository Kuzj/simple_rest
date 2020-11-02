import logging
import json

from aiohttp.web_response import Response
from aiohttp.web import Request

import actions
from simple_rest import RestEndpoint
from helpers import dict2namedtuple

class GrafanaError(Exception):
    """Base class for exceptions in GrafanaEndpoint."""
    pass

class NoMessageInRequest(GrafanaError):
    """Erorr in message from grafana post data"""
    pass

class NoActionInMessage(GrafanaError):
    """Erorr in message from grafana post data"""
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
        return ['/grafana',]

    async def post(self, request: Request) -> Response:
        '''
        grafana_request_fields = ('dashboardId', 
                                  'evalMatches', 
                                  'message', 
                                  'orgId', 
                                  'panelId', 
                                  'ruleId', 
                                  'ruleName', 
                                  'ruleUrl', 
                                  'state', 
                                  'tags', 
                                  'title')
        '''
        data = await request.json()
        logging.info(f'{self.__class__} {request.path} from {request.host} {request.method} request: {data}')
        grafana_request = dict2namedtuple('grafana_request', data)
        #  TODO: Придумать что делать если message не json
        try:
            grafana_message = dict2namedtuple('grafana_message', json.loads(grafana_request.message))
        except json.decoder.JSONDecodeError:
            return Response(status=200)
        except AttributeError:
            Response(status=400)
            raise NoMessageInRequest()
        try:
            await self.do_action(grafana_message.action)
        except AttributeError:
            Response(status=400)
            raise NoActionInMessage
        return Response(status=200)
        