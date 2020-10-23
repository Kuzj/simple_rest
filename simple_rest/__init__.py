import logging
import inspect
from typing import List

from aiohttp.http_exceptions import HttpBadRequest
from aiohttp.web_exceptions import HTTPMethodNotAllowed
from aiohttp.web_request import Request
from aiohttp.web_urldispatcher import UrlDispatcher

import actions

DEFAULT_METHODS = ('GET','POST', 'PUT')

class RestEndpoint:

    def __init__(self):
        self.methods = {}

        for method_name in DEFAULT_METHODS:
            method = getattr(self, method_name.lower(), None)
            if method:
                self.register_method(method_name, method)

    def register_method(self, method_name, method):
        self.methods[method_name.upper()] = method

    def routes(self) -> List[str]:
        return NotImplementedError
    
    def register_routes(self, router: UrlDispatcher):
        for route in self.routes(): # pylint: disable=not-an-iterable
            try:
                router.add_route('*', route, self.dispatch)
                logging.info(f'{self.__class__} register {route}')
            except RuntimeError as e:
                raise RuntimeError(f'{e}: {self.__class__} not register {route}')

    async def dispatch(self, request: Request):
        method = self.methods.get(request.method.upper())
        if not method:
            raise HTTPMethodNotAllowed('', DEFAULT_METHODS)

        wanted_args = list(inspect.signature(method).parameters.keys())
        available_args = request.match_info.copy()
        available_args.update({'request': request})

        unsatisfied_args = set(wanted_args) - set(available_args.keys())
        if unsatisfied_args:
            # Expected match info that doesn't exist
            raise HttpBadRequest('')

        return await method(**{arg_name: available_args[arg_name] for arg_name in wanted_args})

    #  TODO: Сделать access list например по хосту и методу
    async def do_action(self, action_request):
        if 'name' in action_request and 'method' in action_request:
            name = action_request['name']
            method = action_request['method']
            actions_list = list(actions.actions_dict.keys())
            if name in actions_list:
                methods_list = list(actions.actions_dict[name].keys())
                if method in methods_list:
                    args = actions.actions_dict[name][method]
                    if all([p in action_request for p in args]):
                        action = getattr(actions, name)
                        method = getattr(action, method)
                        await method(*[action_request[a] for a in args])
                    else:
                        raise actions.ArgumentMissing(f"Required arguments {args}")
                else:
                    raise actions.MethodNotFound(f"{method}")
            else:
                raise actions.ActionNotFound(f"{name}")
        else:
            raise actions.ActionFormatError("Action name or method is not specified")