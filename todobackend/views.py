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
        self.db = request.app['db']

    async def get(self):
        if(self.uuid):
            response = await Task.get_related_tags(self.uuid, self.db)
        else:
            response = await Task.all_objects(self.db)
        return json_response(response)

    async def post(self):
        content = await self.request.json()
        if(self.uuid):
            response = await Task.add_tag(self.uuid, content["id"], self.db)
        else:
            response = await Task.create_object(content, self.request.app.router['todo'].url_for,
            self.db)
        return json_response(response)

    async def delete(self):
        if(self.uuid):
            await Tag.delete_all_by_task(self.db, self.uuid)
        else:
            await Task.delete_all_objects(self.db)
        return Response()

class TagIndexView(View, CorsViewMixin):
    def __init__(self, request):
        super().__init__(request)
        self.uuid = request.match_info.get('tag_id')
        self.db = request.app['db']

    async def get(self):
        if(self.uuid):
            # received a specific tag, we want todos for it
            response = await Tag.get_related_tasks(self.uuid, self.db)
        else:
            # get all todos
            response = await Tag.all_objects(self.db)
        return json_response(response)

    async def post(self):
        content = await self.request.json()
        response = await Tag.create_object(content, self.request.app.router['todo'].url_for,
            self.db)
        return json_response(response)

    async def delete(self):
        # received todo id, delete all related tags
        if(self.uuid):
            await Tag.delete_all_by_task(self.db, self.uuid)
        else:
            await Tag.delete_all_objects(self.db)
        return Response()

class TodoView(View, CorsViewMixin):
    def __init__(self, request):
        super().__init__(request)
        self.uuid = request.match_info.get('uuid')
        self.db = request.app['db']

    async def get(self):
        response = await Task.get_object(self.uuid, self.db)
        return json_response(response)

    async def patch(self):
        content = await self.request.json()
        response = await Task.update_object(self.uuid, content, self.db)
        return json_response(response)

    async def delete(self):
        await Task.delete_object(self.uuid, self.db)
        return Response()

class TagView(View, CorsViewMixin):
    def __init__(self, request):
        super().__init__(request)
        self.uuid = request.match_info.get('uuid')
        self.db = request.app['db']

    async def get(self):
        response = await Tag.get_object(self.uuid, self.db)
        return json_response(response)

    async def patch(self):
        content = await self.request.json()
        response = await Tag.update_object(self.uuid, content, self.db)
        return json_response(response)

    async def delete(self):
        await Tag.delete_object(self.uuid, self.db)
        return Response()
