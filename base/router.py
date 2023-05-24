from base64 import decode
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path
from .schema import MyGraphqlWsConsumer
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
import jwt
from .settings import SECRET_KEY
# from user.models import Token


@database_sync_to_async
def get_user(token_key):
    try:
        decodedPayload = jwt.decode(
            token_key, key=SECRET_KEY, algorithms=['HS256'])
        user_id = decodedPayload.get('sub')
        User = get_user_model()
        user = User.objects.get(pk=user_id)
        return user
    except Exception as e:
        return AnonymousUser()

# This is to enable authentication via websockets
# Source - https://stackoverflow.com/a/65437244/7981162


class TokenAuthMiddleware(BaseMiddleware):

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query = dict((x.split("=")
                     for x in scope["query_string"].decode().split("&")))
        token_key = query.get("token")
        scope["user"] = await get_user(token_key)
        scope["session"] = scope["user"] if scope["user"] else None
        return await super().__call__(scope, receive, send)


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(TokenAuthMiddleware(
            URLRouter(
                [path("ws/graphql/", MyGraphqlWsConsumer.as_asgi())]
            )
        )),
    }
)
