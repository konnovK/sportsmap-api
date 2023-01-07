from .ping import ping_handler, auth_ping_handler
from .user import (
    register,
    login,
    # change_user,
    # delete_self,
    refresh_token,
    # confirmed_password_reset,
    # send_password_reset_link
)

from aiohttp import web


ROUTES = [
    web.get('/ping', ping_handler),
    web.get('/authping', auth_ping_handler),

    # admin
    web.post('/api/admin/login', login),
    web.post('/api/admin/token/refresh', refresh_token),

    web.post('/api/admin/users', register),
    # web.delete('/api/admin/users', delete_self),
    # web.put('/api/admin/users', change_user),
    #
    # web.post('/api/admin/password/reset/link', send_password_reset_link),
    # web.post('/api/admin/password/reset/confirmed', confirmed_password_reset),
]
