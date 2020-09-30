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
        cur = await self.connector.cursor()
        query = "INSERT INTO `db`.`tasks` (`title`, `completed`, `order`) VALUES ('{}','{}',{});".format(content["title"], 0, content["order"])
        await cur.execute(query)
        await self.connector.commit()
        content["uuid"] = cur.lastrowid
        await cur.close()
        return content

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
                if field_names[i] == 'completed':
                    # val = False if res[i] == 0 else True
                    dic[field_names[i]] = res[i] == 1
                else:
                    dic[field_names[i]] = res[i]
            ret.append(dic)

        print(ret)
        await cur.close()
        return ret

    async def update(self, uuid, obj):
        cur = await self.connector.cursor()
        cols = []
        for key in obj.keys():
            cols.append("`{}` = {}".format(key, obj[key]))
        cols = ", ".join(cols)
        query = "UPDATE tasks SET {} where `uuid` = {}".format(cols, uuid)
        print("query iis:")
        print(query)
        cur.execute(query)
        self.connector.commit()
        cur.close()
        return

    async def delete(self, uuid, db):
        print("deleting: " + str(uuid))
        cur = await self.connector.cursor()
        query = "DELETE FROM `db`.`tasks` WHERE `uuid` = {}".format(uuid)
        await cur.execute(query)
        await self.connector.commit()
        await cur.close()
