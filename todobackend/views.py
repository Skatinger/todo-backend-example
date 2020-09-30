from json import dumps
from logging import getLogger

from aiohttp.web import Response, View, json_response
from aiohttp_cors import CorsViewMixin

from .models import Task

logger = getLogger(__name__)


class IndexView(View, CorsViewMixin):
    async def get(self):
        response = await Task.all_objects(self.request.app['db'])
        return json_response(response)

    async def post(self):
        print("why is this a post")
        content = await self.request.json()
        response = await Task.create_object(content, self.request.app.router['todo'].url_for,
            self.request.app['db'])
        return json_response(response)

    async def delete(self):
        print("in dleete of index view")
        await Task.delete_all_objects(self.request.app['db'])
        return Response()


class TodoView(View, CorsViewMixin):
    def __init__(self, request):
        super().__init__(request)
        self.uuid = request.match_info.get('uuid')

    async def get(self):
        response = await Task.get_object(self.uuid, self.request.app['db'])
        return json_response(response)

    async def patch(self):
        content = await self.request.json()
        print("patch content: -------------")
        print(content)
        response = await Task.update_object(self.uuid, content, self.request.app['db'])
        return json_response(response)

    async def delete(self):
        print("in dleete of todoview")
        await Task.delete_object(self.uuid, self.request.app['db'])
        return Response()
