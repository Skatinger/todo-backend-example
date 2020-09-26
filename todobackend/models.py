from os import getenv
from uuid import uuid4
import aiomysql
from . import database


class Task:

    db = {}

    @classmethod
    async def create_object(cls, content, url_for, conn):
        # old
        uuid = str(uuid4())
        HOST = getenv('HOST', 'localhost:8000')
        obj = {
            'uuid': uuid,
            'completed': False,
            'url': 'http://{HOST}{}'.format(
                url_for(uuid=uuid).path, **locals())
        }
        obj.update(content)
        cls.set_object(uuid, obj)
        # end old

        res = await database.DBConnector(conn).create(content)
        res["url"] = 'http://localhost:8000/todos/' + str(res["uuid"])
        return res

    @classmethod
    async def all_objects(cls, conn):
        result = await database.DBConnector(conn).read()
        print("REEEEEEEESULT:")
        print(list(result))
        print("VS")
        print(list(cls.db.values()))

        # return list(cls.db.values())
        return result

    @classmethod
    async def delete_all_objects(cls, conn):
        cls.db = {}

    @classmethod
    async def get_object(cls, uuid, conn):
        return cls.db[uuid]

    @classmethod
    async def delete_object(cls, uuid, conn):
        del cls.db[uuid]

    @classmethod
    def set_object(cls, uuid, value):
        cls.db[uuid] = value

    @classmethod
    def update_object(cls, uuid, value):
        obj = cls.db[uuid]
        obj.update(value)
        return obj
