from .ping import ping_handler, auth_ping_handler
from .user import (
    register,
    login,
    update_self,
    delete_self,
    refresh_token,
    get_user_by_id
    # confirmed_password_reset,
    # send_password_reset_link
)
from .facility import (
    create_facility,
    update_facility,
    delete_facility,
    get_facility_by_id,
    get_all_facilities,
    search_facilities,
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

    web.get('/admin/users/{id}', get_user_by_id),

    # web.post('/api/admin/password/reset/link', send_password_reset_link),
    # web.post('/api/admin/password/reset/confirmed', confirmed_password_reset),

    # facility
    web.post('/facility', create_facility),
    web.put('/facility/{id}', update_facility),
    web.delete('/facility/{id}', delete_facility),
    web.get('/facility/{id}', get_facility_by_id),
    web.get('/facility', get_all_facilities),

    web.post('/facility/search', search_facilities),
]
