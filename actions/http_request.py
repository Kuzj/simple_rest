import logging
from typing import Dict

from aiohttp import ClientSession

async def get(url: str) -> Dict[str,str]:
    async with ClientSession() as session:
        async with session.get(url) as resp:
            text = await resp.text()
            logging.info(f'Status: {resp.status}, data: {text}')
    return {'status': resp.status, 'text': text}

async def put(url: str, data: bytes ) -> Dict[str,str]:
    async with ClientSession() as session:
        async with session.put(url, data=data) as resp:
            text = await resp.text()
            logging.info(f'Status: {resp.status}, send: {data} to {url}')
    return {'status': resp.status, 'text': text}

async def post(url: str, data: bytes ) -> Dict[str,str]:
    async with ClientSession() as session:
        async with session.post(url, data=data) as resp:
            text = await resp.text()
            logging.info(f'Status: {resp.status}, send: {data} to {url}')
    return {'status': resp.status, 'text': text}