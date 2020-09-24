from logging import getLogger, basicConfig, INFO
from os import getenv
from aiohttp import web
import aiohttp_cors
import aiomysql
from aiohttp_swagger import setup_swagger
import asyncio

from .views import (
    IndexView,
    TodoView,
)

IP = getenv('IP', '0.0.0.0')
PORT = getenv('PORT', '8000')

basicConfig(level=INFO)
logger = getLogger(__name__)


async def init(loop):
    app = web.Application(loop=loop)

    # Configure default CORS settings.
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
                allow_methods="*",
            )
    })

    # Routes
    cors.add(
        app.router.add_route('*', '/todos/', IndexView),
        webview=True)
    cors.add(
        app.router.add_route('*', '/todos/{uuid}', TodoView, name='todo'),
        webview=True)

    # Setup database
    db_loop = asyncio.get_event_loop()
    conn = await aiomysql.connect(host='0.0.0.0', port='3006',
                                   user='root', password='1324', db='db', loop=db_loop)

    cur = await conn.cursor()
    await cur.execute("SHOW DATABASES")
    print(cur.description)

    # Config
    setup_swagger(app, swagger_url="/api/v1/doc", swagger_from_file="swagger.yaml")
    logger.info("Starting server at %s:%s", IP, PORT)
    srv = await loop.create_server(app.make_handler(), IP, PORT)
    return srv
