import logging
import inspect
from typing import List

from aiohttp.http_exceptions import HttpBadRequest
from aiohttp.web_exceptions import HTTPMethodNotAllowed
from aiohttp.web_request import Request
from aiohttp.web_urldispatcher import UrlDispatcher

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
        for route in self.routes():
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