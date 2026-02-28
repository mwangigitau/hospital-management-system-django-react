"""
JWT authentication middleware for Django Channels WebSocket connections.

Clients must pass the JWT access token via the `token` query-string parameter:
    ws://host/ws/hms/?token=<access_token>
"""
from urllib.parse import parse_qs

from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


@database_sync_to_async
def _get_user(user_id: str):
    from apps.accounts.models import User
    try:
        return User.objects.select_related('role').get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):
    """Resolve the JWT Bearer token from the query string and attach the user to scope."""

    async def __call__(self, scope, receive, send):
        query_string = scope.get('query_string', b'').decode()
        params = parse_qs(query_string)
        token_list = params.get('token', [])
        user = AnonymousUser()
        if token_list:
            try:
                access_token = AccessToken(token_list[0])
                user_id = access_token.get('user_id')
                if user_id:
                    user = await _get_user(str(user_id))
            except (InvalidToken, TokenError):
                pass
        scope['user'] = user
        return await super().__call__(scope, receive, send)


def JWTAuthMiddlewareStack(inner):
    """Convenience wrapper – mirrors Channels' AuthMiddlewareStack pattern."""
    return JWTAuthMiddleware(inner)
