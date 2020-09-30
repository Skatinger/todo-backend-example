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

    async def create(self, obj, model):
        cur = await self.connector.cursor()
        fields = []
        cols = []
        for key in obj.keys():
            fields.append("`{}`".format(key))
            if key == 'completed':
                val = 1 if obj[key] == 'false' else 0
                cols.append("'{}'".format(val))
            else:
                cols.append("'{}'".format(obj[key]))
        cols = ", ".join(cols)
        fields = ", ".join(fields)
        query = "INSERT INTO `db`.`{}` ({}) VALUES ({});".format(model, fields, cols)
        print(query)
        await cur.execute(query)
        await self.connector.commit()
        obj["id"] = cur.lastrowid
        await cur.close()
        return obj

    async def relatedTags(self, task_id):
        res = await self.getRelatedIds(task_id, 'tasks', 'tags')
        return res

    async def relatedTasks(self, tag_id):
        res = await self.getRelatedIds(tag_id, 'tags', 'tasks')
        return res

    # @param model1: the model on which the relation is
    # @param model2: the model to which the relation should lead
    async def getRelatedIds(self, uuid, model1, model2):
        query = '''SELECT `tasks_tags`.`{}_id` FROM `db`.`tasks_tags`
                   INNER JOIN `{}` ON `tasks_tags`.`{}_id` = `{}`.`id`
                   WHERE `{}`.`id` = {}
        '''.format(model2, model1, model1, model1, model1, uuid)
        print(query)
        cur = await self.connector.cursor()
        await cur.execute(query)
        r = await cur.fetchall()
        r = [res[0] for res in r]
        await self.connector.commit()
        await cur.close()
        return r

    async def deleteRelation(self, id, model):
        query = "DELETE FROM `db`.`tasks_tags` WHERE `{}_id` = {}".format(model, id)
        cur = await self.connector.cursor()
        await cur.execute(query)
        await self.connector.commit()
        await cur.close()

    async def get(self, id, model):
        query = "SELECT * FROM `db`.`{}` WHERE `{}`.`id` = {}".format(model, model, id)
        cur = await self.connector.cursor()
        await cur.execute(query)
        res = await cur.fetchone()

        # add field names
        num_fields = len(cur.description)
        field_names = [i[0] for i in cur.description]
        dic = {}
        for i in range(len(field_names)):
            # replace 1/0 from db to "True/False"
            if field_names[i] == 'completed':
                dic[field_names[i]] = True if res[i] == 1 else False
            else:
                dic[field_names[i]] = res[i]

        return dic

    async def addRelationTaskTag(self, task_id, tag_id):
        query = "INSERT INTO `db`.`tasks_tags` (tasks_id, tags_id) VALUES ({}, {});".format(task_id, tag_id)
        cur = await self.connector.cursor()
        print(query)
        await cur.execute(query)
        await self.connector.commit()
        await cur.close()


    async def getMultiple(self, ids, model):
        print(ids)
        if(len(ids)) > 1:
            return []
        print(", ".join([str(id) for id in ids]))
        query = "SELECT * FROM `db`.`{}` WHERE `{}`.`id` IN ({})".format(model, model, ", ".join([str(id) for id in ids]))
        print(query)
        cur = await self.connector.cursor()
        await cur.execute(query)
        r = await cur.fetchall()
        # build objects
        ret = []
        num_fields = len(cur.description)
        field_names = [i[0] for i in cur.description]
        print(field_names)
        for res in r:
            dic = {}
            for i in range(len(field_names)):
                # replace 1/0 from db to "True/False"
                if field_names[i] == 'completed':
                    dic[field_names[i]] = True if res[i] == 1 else False
                else:
                    dic[field_names[i]] = res[i]
            ret.append(dic)

        print("ret is:")
        print(ret)
        await cur.close()
        return ret



    async def fetchall(self, model):
        query = "SELECT * FROM `db`.`{}`".format(model)
        cur = await self.connector.cursor()
        await cur.execute(query)
        r = await cur.fetchall()
        print(r)

        # build objects
        ret = []
        num_fields = len(cur.description)
        field_names = [i[0] for i in cur.description]
        print(field_names)
        for res in r:
            dic = {}
            for i in range(len(field_names)):
                # replace 1/0 from db to "True/False"
                if field_names[i] == 'completed':
                    dic[field_names[i]] = True if res[i] == 1 else False
                else:
                    dic[field_names[i]] = res[i]
            ret.append(dic)

        print("ret is:")
        print(ret)
        await cur.close()
        return ret

    async def update(self, id, obj, model):
        cur = await self.connector.cursor()
        cols = []
        for key in obj.keys():
            if key == 'completed':
                val = 0 if obj[key] == 'false' else 1
                cols.append("`{}` = '{}'".format(key, val))
            else:
                cols.append("`{}` = '{}'".format(key, obj[key]))
        cols = ", ".join(cols)
        query = "UPDATE `db`.`{}` SET {} WHERE `{}`.`id` = {}".format(model, cols, model, id)
        await cur.execute(query)
        await self.connector.commit()
        await cur.close()
        return

    async def deleteMultiple(self, model, ids):
        ids = ", ".join([str(id) for id in ids])
        query = "DELETE FROM `db`.`{}` WHERE `{}`.`id` IN ({})".format(model, model, ids)
        cur = await self.connector.cursor()
        await cur.execute(query)
        await self.connector.commit()
        await cur.close()

    async def delete_all(self, model):
        query = "TRUNCATE TABLE `db`.`{}`".format(model)
        cur = await self.connector.cursor()
        await cur.execute(query)
        await self.connector.commit()
        await cur.close()

    async def delete(self, id, model):
        query = "DELETE FROM `db`.`{}` WHERE `{}`.`id` = {}".format(model, model, id)
        cur = await self.connector.cursor()
        await cur.execute(query)
        await self.connector.commit()
        await cur.close()
