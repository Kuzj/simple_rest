import logging
import json
from aiohttp.web_response import Response
from aiohttp.web import Request

import actions
from simple_rest import RestEndpoint

class GrafanaError(Exception):
    """Base class for exceptions in GrafanaEndpoint."""
    pass

class NoMessageInRequest(GrafanaError):
    """Erorr in message from grafana post data"""
    pass

class NoActionInMessage(GrafanaError):
    """Erorr in message from grafana post data"""
    pass

class ActionFormatError(GrafanaError):
    """Erorr in action format"""
    pass

# TODO: Обработать сообщение когда проблема решается, например ничего не делать если 'state':'ok'
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

    #  TODO: Сделать access list например по хосту и методу (лучше на уровне actions??)
    async def do_action(self):
        if all([ _ in self.action for _ in ['name','method','url','data']]):
            if self.action['name'] in actions.actions_name_list:
                action = getattr(actions, self.action['name'])
                method = getattr(action, self.action['method'])
                await method(self.action['url'], self.action['data'])
            else:
                raise actions.ActionNotFound()
        else:
            raise ActionFormatError()

    async def post(self, request: Request) -> Response:
        data = await request.json()
        logging.info(f'{self.__class__} {request.path} from {request.host} {request.method} request: {data}')
        if 'message' in data:
            #  TODO: Придумать что делать если message не json
            try:
                grafana_message = json.loads(data["message"])
            except json.decoder.JSONDecodeError:
                return Response(status=200)
            if 'action' in grafana_message:
                self.action = grafana_message["action"]
                await self.do_action()
            else:
                #  HTTPBadRequest
                Response(status=400)
                raise NoActionInMessage
            return Response(status=200)
        else:
            #  HTTPBadRequest
            Response(status=400)
            raise NoMessageInRequest()
        