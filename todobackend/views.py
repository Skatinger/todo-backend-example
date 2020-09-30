from json import dumps
from logging import getLogger

from aiohttp.web import Response, View, json_response
from aiohttp_cors import CorsViewMixin

from .models import Task, Tag

logger = getLogger(__name__)


class IndexView(View, CorsViewMixin):
    def __init__(self, request):
        super().__init__(request)
        self.uuid = request.match_info.get('uuid')


    async def get(self):
        print("INDEX GET REQUEST ----")
        response = await Task.all_objects(self.request.app['db'])
        return json_response(response)

    async def post(self):
        print("INDEX POST REQUEST ----")
        content = await self.request.json()
        response = await Task.create_object(content, self.request.app.router['todo'].url_for,
            self.request.app['db'])
        return json_response(response)

    async def delete(self):
        print("DELETE ALL REQUEST ----")
        await Task.delete_all_objects(self.request.app['db'])
        return Response()

class TagIndexView(View, CorsViewMixin):
    def __init__(self, request):
        super().__init__(request)
        self.uuid = request.match_info.get('uuid')

    async def get(self):
        print("INDEX GET REQUEST ----")
        response = await Tag.all_objects(self.request.app['db'])
        return json_response(response)

    async def post(self):
        print("INDEX POST REQUEST ----")
        content = await self.request.json()
        if(self.uuid):
            print("nice, should associate the tag to the todo")
            response = await Task.add_tag(self.uuid, content["id"], self.request.app['db'])
        else:
            response = await Tag.create_object(content, self.request.app.router['todo'].url_for,
                self.request.app['db'])
        return json_response(response)

    async def delete(self):
        print("DELETE ALL REQUEST ----")
        print(self.uuid)
        if(self.uuid):
            await Tag.delete_all_by_task(self.request.app['db'], self.uuid)
        else:
            await Tag.delete_all_objects(self.request.app['db'])
        return Response()

class TodoView(View, CorsViewMixin):
    def __init__(self, request):
        super().__init__(request)
        self.uuid = request.match_info.get('uuid')

    async def get(self):
        print("TODO GET REQUEST")
        response = await Task.get_object(self.uuid, self.request.app['db'])
        return json_response(response)

    async def patch(self):
        print("TODO PATCH REQUEST")
        content = await self.request.json()
        print(content)
        response = await Task.update_object(self.uuid, content, self.request.app['db'])
        return json_response(response)

    async def delete(self):
        print("TODO DELETE REQUEST")
        await Task.delete_object(self.uuid, self.request.app['db'])
        return Response()

class TagView(View, CorsViewMixin):
    def __init__(self, request):
        super().__init__(request)
        print("GOT A REQUEEEEEEST")
        print(request)
        self.uuid = request.match_info.get('uuid')

    async def get(self):
        print("TODO GET REQUEST")
        response = await Tag.get_object(self.uuid, self.request.app['db'])
        return json_response(response)

    async def patch(self):
        print("TODO PATCH REQUEST")
        content = await self.request.json()
        print(content)
        response = await Tag.update_object(self.uuid, content, self.request.app['db'])
        return json_response(response)

    async def delete(self):
        print("TODO DELETE REQUEST")
        await Tag.delete_object(self.uuid, self.request.app['db'])
        return Response()
# curl -X DELETE --header 'Accept: application/json' 'http://localhost:8000/todos/1'
