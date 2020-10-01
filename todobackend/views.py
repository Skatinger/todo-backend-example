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
        if(self.uuid):
            print("someone looking for tags list to this todo ?????????????????????????????????????????????????????????????????????????")
            print(self.request)
            print("tags currentyl are:")
            tgs = await Tag.all_objects(self.request.app['db'])
            print(tgs)
            response = await Task.get_related_tags(self.uuid, self.request.app['db'])
            print("alksfjöasjflsjfklsfjlsökfjsklfjslfajskdödddddd getting him:")
            print(response)
        else:
            print("just getting all ")
            response = await Task.all_objects(self.request.app['db'])
        return json_response(response)

    async def post(self):
        content = await self.request.json()
        if(self.uuid):
            print("GREAT, got a request to add assiciation")
            response = await Task.add_tag(self.uuid, content["id"], self.request.app['db'])
        else:
            response = await Task.create_object(content, self.request.app.router['todo'].url_for,
            self.request.app['db'])
        return json_response(response)

    async def delete(self):
        if(self.uuid):
            print("trying to delete all tags for a task")
            await Tag.delete_all_by_task(self.request.app['db'], self.uuid)
        else:
            await Task.delete_all_objects(self.request.app['db'])
        return Response()

class TagIndexView(View, CorsViewMixin):
    def __init__(self, request):
        super().__init__(request)
        self.uuid = request.match_info.get('tag_id')

    async def get(self):
        if(self.uuid):
            # received a specific tag, we want todos for it
            response = await Tag.get_related_tasks(self.uuid, self.request.app['db'])
        else:
            response = await Tag.all_objects(self.request.app['db'])
        return json_response(response)

    async def post(self):
        content = await self.request.json()
        # if(self.uuid):
        #     response = await Task.add_tag(self.uuid, content["id"], self.request.app['db'])
        # else:
        response = await Tag.create_object(content, self.request.app.router['todo'].url_for,
            self.request.app['db'])
        return json_response(response)

    async def delete(self):
        # todo not sure if this is correct
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
        response = await Task.get_object(self.uuid, self.request.app['db'])
        return json_response(response)

    async def patch(self):
        content = await self.request.json()
        print(content)
        response = await Task.update_object(self.uuid, content, self.request.app['db'])
        return json_response(response)

    async def delete(self):
        await Task.delete_object(self.uuid, self.request.app['db'])
        return Response()

class TagView(View, CorsViewMixin):
    def __init__(self, request):
        super().__init__(request)
        self.uuid = request.match_info.get('uuid')

    async def get(self):
        response = await Tag.get_object(self.uuid, self.request.app['db'])
        return json_response(response)

    async def patch(self):
        content = await self.request.json()
        print(content)
        response = await Tag.update_object(self.uuid, content, self.request.app['db'])
        return json_response(response)

    async def delete(self):
        await Tag.delete_object(self.uuid, self.request.app['db'])
        return Response()
