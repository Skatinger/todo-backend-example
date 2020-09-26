# import sqlalchemy
#
#
# tasks = sqlalchemy.Table(
#     "tasks",
#     sqlalchemy.MetaData(),
#     sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
#     sqlalchemy.Column("text", sqlalchemy.String)
# )


class DBConnector:

    def __init__(self, db):
        self.connector = db

    async def create(self, content):
        obj = {'completed': False}
        obj.update(content)

        cur = await self.connector.cursor()
        query = "INSERT INTO `db`.`tasks` (`title`, `completed`, `order`) VALUES ('{}','{}',{});".format(obj["title"], obj["completed"], obj["order"])
        await cur.execute(query)
        await self.connector.commit()
        obj["uuid"] = cur.lastrowid
        await cur.close()
        return obj

    async def read(self, query="*", id=None):

        # reading single record
        cur = await self.connector.cursor()
        await cur.execute("SELECT * FROM tasks")
        # print(cur.description)
        r = await cur.fetchall()
        print("result:")
        # print(cur.description)
        ret = []
        num_fields = len(cur.description)
        field_names = [i[0] for i in cur.description]
        print(field_names)
        # todo add column names from description
        for res in r:
            dic = {}
            for i in range(len(field_names)):
                dic[field_names[i]] = res[i]
            ret.append(dic)

        print(ret)
        await cur.close()
        return ret

    def update(obj, db):
        return 0

    def delete(obj, db):
        return 0
