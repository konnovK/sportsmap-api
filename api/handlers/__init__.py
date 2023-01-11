from .ping import ping_handler, auth_ping_handler
from .user import (
    register,
    login,
    update_self,
    delete_self,
    refresh_token,
    # confirmed_password_reset,
    # send_password_reset_link
)

from aiohttp import web


ROUTES = [
    web.get('/ping', ping_handler),
    web.get('/authping', auth_ping_handler),

    # admin
    web.post('/admin/login', login),
    web.post('/admin/token/refresh', refresh_token),

    web.post('/admin/users', register),
    web.delete('/admin/users', delete_self),
    web.put('/admin/users', update_self),
    #
    # web.post('/api/admin/password/reset/link', send_password_reset_link),
    # web.post('/api/admin/password/reset/confirmed', confirmed_password_reset),
]
