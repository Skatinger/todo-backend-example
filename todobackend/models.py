from os import getenv
from uuid import uuid4
import aiomysql
from . import database


class Task:

    @classmethod
    async def get_related_tags(cls, uuid, conn):
        ids = await database.DBConnector(conn).relatedTags(uuid)
        # print("IDS before call are: ")
        # print(ids)
        print("all tags would be:")
        resp = await Tag.all_objects(conn)
        print(resp)
        print("ids are:")
        print(ids)
        if(len(ids)) == 0:
            print("got to lenid short 00000")
            return []
        else:
            return await database.DBConnector(conn).getMultiple(ids, "tags")

    @classmethod
    async def create_object(cls, content, url_for, conn):
        obj = {
            "title": "",
            "order": 1,
            "completed": False,
        }
        obj.update(content)
        res = await database.DBConnector(conn).create(obj, "tasks")
        res["url"] = 'http://localhost:8000/todos/' + str(res["id"])
        return res

    @classmethod
    async def all_objects(cls, conn):
        result = await database.DBConnector(conn).fetchall("tasks")
        HOST = getenv('HOST', 'localhost:8000')
        for obj in result:
            obj["tags"] = []
            obj["url"] = "http://{}/todos/{}".format(HOST, obj["id"])

        return result

    @classmethod
    async def delete_all_objects(cls, conn):
        res = await database.DBConnector(conn).delete_all("tasks")

    @classmethod
    async def add_tag(cls, task_id, tag_id, conn):
        res = await database.DBConnector(conn).addRelationTaskTag(task_id, tag_id)

    @classmethod
    async def get_object(cls, uuid, conn):
        res = await database.DBConnector(conn).get(uuid, "tasks")
        HOST = getenv('HOST', 'localhost:8000')
        res["url"] = "http://{}/todos/{}".format(HOST, res["id"])
        # add todos
        # first get all todo ids
        ids = await database.DBConnector(conn).relatedTags(uuid)
        # print("IDS before call are: ")
        # print(ids)
        if(len(ids)) == 0:
            res["tags"] = []
        else:
            tags = await database.DBConnector(conn).getMultiple(ids, "tags")
            res["tags"] = tags
        return res

    @classmethod
    async def delete_associated_tags(cls, task_id, tag_id, conn):
        await database.DBConnector(conn).deleteRelation(task_id, tag_id)

    @classmethod
    async def delete_object(cls, uuid, conn):
        await database.DBConnector(conn).delete(uuid, "tasks")
        await database.DBConnector(conn).deleteRelations(uuid, "tasks")

    @classmethod
    async def update_object(cls, uuid, value, conn):
        await database.DBConnector(conn).update(uuid, value, "tasks")
        obj = await cls.get_object(uuid, conn)
        return obj

class Tag:

    @classmethod
    async def create_object(cls, content, url_for, conn):
        obj = {
            "title" : ""
        }
        obj.update(content)
        res = await database.DBConnector(conn).create(obj, "tags")
        res["url"] = 'http://localhost:8000/tags/' + str(res["id"])
        res["todos"] = []
        return res

    @classmethod
    async def all_objects(cls, conn):
        result = await database.DBConnector(conn).fetchall("tags")
        HOST = getenv('HOST', 'localhost:8000')
        for obj in result:
            obj["todos"] = []
            obj["url"] = "http://{}/tags/{}".format(HOST, obj["id"])
        return result

    @classmethod
    async def delete_all_objects(cls, conn):
        res = await database.DBConnector(conn).delete_all("tags")

    @classmethod
    async def delete_all_by_task(cls, conn, uuid):
        todo = await Task.get_object(uuid, conn)
        # print("TODO IS")
        # print(todo)
        tagIds = await database.DBConnector(conn).relatedTags(todo["id"])
        res = await database.DBConnector(conn).deleteMultiple("tags", tagIds)

    @classmethod
    async def get_object(cls, uuid, conn):
        res = await database.DBConnector(conn).get(uuid, "tags")
        HOST = getenv('HOST', 'localhost:8000')
        res["url"] = "http://{}/tags/{}".format(HOST, res["id"])
        # get related tasks
        ids = await database.DBConnector(conn).relatedTasks(uuid)
        # print("IDS before call are: -------------------------------------------------------------")
        # print(ids)
        if(len(ids)) == 0:
            res["todos"] = []
        else:
            tasks = await database.DBConnector(conn).getMultiple(ids, "tasks")
            res["todos"] = tasks
        return res

    @classmethod
    async def get_related_tasks(cls, uuid, conn):
        ids = await database.DBConnector(conn).relatedTasks(uuid)
        # print("IDS before call are: ")
        # print(ids)
        if(len(ids)) == 0:
            return []
        else:
            return await database.DBConnector(conn).getMultiple(ids, "tasks")

    @classmethod
    async def delete_object(cls, uuid, conn):
        await database.DBConnector(conn).delete(uuid, "tags")
        await database.DBConnector(conn).deleteRelations(uuid, "tags")

    @classmethod
    async def update_object(cls, uuid, value, conn):
        await database.DBConnector(conn).update(uuid, value, "tags")
        obj = await cls.get_object(uuid, conn)
        print(obj)
        return obj
