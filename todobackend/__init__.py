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
    TagIndexView,
    TagView
)

IP = getenv('IP', '0.0.0.0')
PORT = getenv('PORT', '8000')

basicConfig(level=INFO)
logger = getLogger(__name__)

# connects to db, saves a connector the the app dict
async def init_db(app):
    connection = await aiomysql.connect(
        host='db',
        user='root',
        password='1324',
        db='db',
        loop=app.loop)
    if connection:
        print("got db connection:" + str(connection))
    app['db'] = connection

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
    # todos
    cors.add(
        app.router.add_route('*', '/todos/', IndexView),
        webview=True)
    cors.add(
        app.router.add_route('*', '/todos/{uuid}', TodoView, name='todo'),
        webview=True)
    # relations
    cors.add(
        app.router.add_route('*', '/todos/{uuid}/tags/', IndexView),
        webview=True)
    cors.add(
        app.router.add_route('*', '/todos/{uuid}/tags/{tag_id}', TagView),
        webview=True)

    # tags
    cors.add(
        app.router.add_route('*', '/tags/', TagIndexView),
        webview=True)
    cors.add(
        app.router.add_route('*', '/tags/{uuid}', TagView, name='tag'),
        webview=True)
    cors.add(
        app.router.add_route('*', '/tags/{tag_id}/todos/', TagIndexView),
        webview=True)

    #db setup
    await init_db(app)

    # Config
    setup_swagger(app, swagger_url="/api/v1/doc", swagger_from_file="swagger.yaml")
    logger.info("Starting server at %s:%s", IP, PORT)
    srv = await loop.create_server(app.make_handler(), IP, PORT)
    return srv
